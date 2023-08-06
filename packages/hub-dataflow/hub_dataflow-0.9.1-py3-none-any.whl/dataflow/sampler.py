"""Sampler module containing different sampling methods"""
from typing import Tuple

import numpy as np
import cv2

from .base_module import BaseModule
from dataflow.logger import logger


class PolygonSampler(BaseModule):
    """Sampling method based on polygons.

    Parameters
    ----------
    sampleshape: tuple of 3 len
        Shape of each image in the sample. First item is the channel and other two are the image size

        Example
        -------
        (4, 512, 512), (3, 1024, 1024)
        
    dataset: dict
        The dataset for which sampling will be done. It contains the following required keys:
            | field: list of images from which to crop the samples
            | polygons: polygon objects for each image. Sampling will be done per each polygon putting it into the center
            | boundary_bolygons: polygons for each image describing the areas of interest in the image
            | polygon_count: This is a metadata containing the number of polgons for each image
    Examples
    --------
    >>> shape = (4, 512, 512)
    >>> dataset = Intelinair(....)()
    >>> samples = PolygonSampler(shape, dataset)
    """

    def __init__(self, sampleshape, dataset: dict, box_mask: bool = False):
        """Constructs samples of given shape."""
        sampleshape = tuple(sampleshape)
        assert (
            len(sampleshape) == 3
        ), "sampleshape must be in 3 length like (4, 512, 512)"
        assert isinstance(dataset, dict)
        assert (
            sampleshape[0] < 5
        ), "First item in the sampleshape is the channel and must be less than 5"
        self._sampleshape = sampleshape[1:]
        self._channels = sampleshape[0]
        # TODO no need to keep the information
        self._polygons = dataset["polygon_count"].compute()
        self._dataset = dataset
        self._box_mask_compute = box_mask

    def meta(self, id, metainput: dict):
        """Metadata of the samples.

        Parameters
        ----------
        id: int
            index of the image for which polygons the samples will be created.
        metainput: dict
            dictionary containing information about ingested data. Required field here is "field"
        Returns
        -------
        dict: dictionary of metadata with keys ["image", "label", "mask", "box"]
            | image: image from which to crop the samples
            | label: polygon objects. Sampling will be done per each polygon putting it into the center
            | mask: polygons describing the areas of interest in the image
            | box: bounding boxes for the lables in each sample
        """
        cnt = self._polygons[id]
        ds = {
            "image": {
                "shape": (cnt, self._channels) + self._sampleshape,
                "dtype": metainput["field"]["dtype"],
            },
            "label": {"shape": (cnt,) + self._sampleshape, "dtype": "uint8"},
            "mask": {"shape": (cnt,) + self._sampleshape, "dtype": "bool"},
            "box": {"shape": (cnt,), "dtype": "object"},
            "box_type": {"shape": (cnt,), "dtype": "object"},
            "box_mask": {"shape": (cnt,), "dtype": "object"},
        }
        if not self._box_mask_compute:
            del ds["box_mask"]
        return ds

    def forward(self, id: int, input_data: dict, metainput: dict) -> dict:
        field = input_data["field"]
        if field.shape[0] != self._channels:
            raise Exception(
                f"Field has {field.shape[0]} channels, while {self._channels} channels were requested"
            )
        polygons = input_data["polygons"]
        polygon_labels = input_data["polygon_labels"]
        boundary_polygons = input_data["boundary_polygons"]
        ds = super().from_meta(metainput)
        image = ds["image"]
        mask = ds["label"]
        boundary = ds["mask"]
        boxes = ds["box"]
        box_type = ds["box_type"]
        if self._box_mask_compute:
            box_mask = ds["box_mask"]
        # TODO fix shape and remove [0]
        max_size = input_data["field"].shape[1:3]
        _box_type = np.array(polygon_labels)
        _mask, _ = self._load_mask(polygons, max_size, polygon_labels=_box_type)
        _boundary, _ = self._load_mask(boundary_polygons, max_size)
        _boundary = _boundary.astype("uint8")
        _boxes = self._boxes_from_polygons(polygons)
        _canvases = self._canvases_from_boxes(_boxes, max_size)
        for j, canvas in enumerate(_canvases):
            slice_x, slice_y = [slice(canvas[0][k], canvas[1][k], 1) for k in range(2)]
            try:
                mask[j] = _mask[slice_y, slice_x]
                boundary[j] = _boundary[slice_y, slice_x]
                indexes, boxes[j] = self._intersect_boxes(canvas, _boxes)
                boxes[j] = self._reshape_boxes(boxes[j])
                image[j] = field[:, slice_y, slice_x]
                box_type[j] = _box_type[indexes]
                if self._box_mask_compute:
                    box_mask[j] = np.array(
                        [
                            self._load_mask([polygons[index]], max_size)[0][
                                slice_y, slice_x
                            ]
                            for index in indexes
                        ]
                    )
            except Exception as e:
                logger.error(e)
        ds = {
            "image": image,
            "label": mask,
            "mask": boundary,
            "box": boxes,
            "box_type": box_type,
        }
        if self._box_mask_compute:
            ds["box_mask"] = box_mask
        return ds

    def __call__(self):
        result = super().__call__(input_data=self._dataset)
        result["__special__"] = {
            "box": ["int32", (1000, 4)],
            "box_type": ["int32", (1000,)],
            "box_mask": ["bool", (1000, self._sampleshape[0], self._sampleshape[1])],
        }
        if not self._box_mask_compute:
            del result["__special__"]["box_mask"]

        return result

    @staticmethod
    def _load_mask(
        polygons: np.ndarray,
        size: Tuple[int, int],
        seperate_masks: bool = False,
        polygon_labels: np.ndarray = None,
    ) -> np.ndarray:
        """Creating mask array of given <size> filled with 0s and 1s.
        The areas of polygons are filled with 1, other areas are 0
        """
        total_mask = np.zeros(size, dtype="uint8")
        zero_mask = total_mask.copy()
        masks = []
        for idx, p in enumerate(polygons):
            try:
                m = cv2.fillPoly(zero_mask.copy(), [p], color=(1, 1, 1))
                if polygon_labels is None:
                    total_mask |= m
                else:
                    np.maximum(total_mask, m * polygon_labels[idx], out=total_mask)
                if seperate_masks:
                    masks += [m]

            except Exception as e:
                print(e)
        if seperate_masks:
            return total_mask, np.array(masks)
        else:
            return total_mask, None

    @staticmethod
    def _intersect_boxes(canvas: np.ndarray, boxes: np.ndarray) -> np.ndarray:
        """Returns the intersections of all boxes with the given canvas"""
        intersect = [
            np.clip(boxes[:, :, k], canvas[0, k], canvas[1, k] - 1) for k in range(2)
        ]
        boxes_ = np.stack(intersect, axis=-1)
        bool_ = boxes_[:, 0] < boxes_[:, 1]
        bool_ = np.all(bool_, axis=1)
        indexes = [i for i, b in enumerate(bool_) if b]
        boxes_ = boxes_[bool_]
        boxes_ -= canvas[0]
        # boxes_[:, 1] -= 1
        return indexes, boxes_

    @staticmethod
    def _reshape_boxes(boxes: np.ndarray) -> np.ndarray:
        """Reshaping (2, 2) boxes into (4,) shape which is required by training some models"""
        return boxes.reshape(boxes.shape[:-2] + (4,))

    @staticmethod
    def _boxes_from_polygons(polygons: np.ndarray) -> np.ndarray:
        """Creates the bounding boxes of given polygons."""
        boxes = np.zeros([len(polygons), 2, 2], dtype="int32")
        for i, polygon in enumerate(polygons):
            max_ = np.amax(polygon, axis=0)
            min_ = np.amin(polygon, axis=0)
            boxes[i] = np.array([min_, max_])
        return boxes

    def _canvases_from_boxes(
        self, boxes: np.ndarray, max_size: Tuple[int, int]
    ) -> np.ndarray:
        """Creates canvaces for the given boxes by self._sampleshape sizes and limited from the <max_size>.
        Both self._sampleshape and max_size are reverted as in pictures shape first is y and then x
        """
        edge = np.array(self._sampleshape[::-1])
        max_size = max_size[::-1]
        canvases = np.zeros([len(boxes), 2, 2], dtype="int32")
        for i, box in enumerate(boxes):
            center = (box[0] + box[1]) // 2
            loc = center - edge // 2
            loc = [min(max_size[j], loc[j] + edge[j]) - edge[j] for j in range(2)]
            loc = [max(0, loc[j]) for j in range(2)]
            loc = np.array(loc)
            canvases[i] = np.array([loc, loc + edge])
        return canvases
