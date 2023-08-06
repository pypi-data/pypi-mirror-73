from typing import Tuple

import dask
import numpy as np

from dataflow.collections._store_version import CURRENT_STORE_VERSION


def _dask_shape_backward(shape: Tuple[int]):
    if len(shape) == 0:
        return shape
    else:
        return (-1,) + (shape[1:]) if np.isnan(shape[0]) else shape


class Tensor:
    def __init__(self, meta: dict, daskarray, delayed_objs: tuple = None):
        if not meta.get("preprocessed"):
            meta = Tensor._preprocess_meta(meta, daskarray)
        self._meta = meta
        self._array = daskarray
        self._delayed_objs = delayed_objs
        self._shape = _dask_shape_backward(daskarray.shape)
        self._dtype = meta["dtype"]
        self._dtag = meta.get("dtag")
        self._dcompress = meta.get("dcompress")
        self._dcompress_algo = meta.get("dcompress_algo")
        self._dcompress_lvl = meta.get("dcompress_lvl")

    @staticmethod
    def _preprocess_meta(meta, daskarray):
        meta = dict(meta)
        meta["preprocessed"] = True
        meta["dtype"] = meta.get("dtype") or daskarray.dtype
        meta["shape"] = daskarray.shape
        meta["STORE_VERSION"] = CURRENT_STORE_VERSION
        if "dcompress" in meta:
            dcompress_comp = str(meta["dcompress"]).split(sep=":")
            assert len(dcompress_comp) in [
                1,
                2,
            ], "Invalid dcompress format, should be {algo:compress_lvl} or {algo}"
            meta["dcompress_algo"] = dcompress_comp[0]
            meta["dcompress_lvl"] = (
                dcompress_comp[1] if len(dcompress_comp) == 2 else None
            )
        else:
            meta["dcompress"] = None
            meta["dcompress_algo"] = None
            meta["dcompress_lvl"] = None
        return meta

    @property
    def shape(self):
        return self._shape

    @property
    def ndim(self):
        return len(self._shape)

    @property
    def count(self):
        return self._shape[0]

    def __len__(self) -> int:
        return self._shape[0]

    @property
    def dtype(self):
        return self._dtype

    @property
    def dtag(self):
        return self._dtag

    @property
    def dcompress(self):
        return self._dcompress

    def __getitem__(self, slices) -> "Tensor":
        arr = self._array[slices]
        if isinstance(arr, dask.delayed.__class__):
            assert False
            return arr
        else:
            return Tensor(self._meta, arr)

    def __iter__(self):
        for i in range(len(self)):
            yield self._array[i]

    def compute(self):
        return self._array.compute()
