from dataflow.dataset_generators.intelinair.sampler import PolygonSampler
import dask
import numpy as np


def test_boxes_from_polygons():
    polygon = np.array(
        [
            [(2, 1), (5, 1), (5, 4), (3, 4), (3, 2), (2, 2), (2, 1)],
            [(2, 1), (5, 1), (5, 4), (3, 4), (3, 3), (4, 3), (4, 2), (2, 2), (2, 1)],
            [(2, 1), (5, 1), (5, 4), (2, 4), (2, 1)],
        ]
    )
    result = PolygonSampler._boxes_from_polygons(polygon)
    expected = np.array([[(2, 1), (5, 4)]] * 3)
    assert (result == expected).all()


def test_canvases_from_boxes_same_xy():
    shape = (4, 6, 6)
    ds = {"polygon_count": dask.array.from_array(np.array([2]))}
    samples = PolygonSampler(shape, ds)
    boxes = np.array([[(1, 1), (2, 2)], [(5, 6), (7, 8)]])
    result = samples._canvases_from_boxes(boxes, (9, 9))
    expected = np.array([[(0, 0), (6, 6)], [(3, 3), (9, 9)]])
    assert (result == expected).all()


def test_canvases_from_boxes_diff_xy():
    shape = (4, 4, 6)
    ds = {"polygon_count": dask.array.from_array(np.array([2]))}
    samples = PolygonSampler(shape, ds)
    boxes = np.array([[(5, 6), (7, 8)]])
    result = samples._canvases_from_boxes(boxes, (7, 9))
    expected = np.array([[(3, 3), (9, 7)]])
    assert (result == expected).all()


def test_intersect_boxes():
    canvas = np.array([(1, 1), (5, 5)])
    boxes = np.array([[(0, 0), (2, 2)], [(1, 2), (6, 6)], [(5, 5), (7, 7)]])
    indexes, result = PolygonSampler._intersect_boxes(canvas, boxes)
    expected = np.array([[(0, 0), (1, 1)], [(0, 1), (3, 3)]])
    assert (np.array(indexes) == np.array([0, 1])).all()
    assert (result == expected).all()
