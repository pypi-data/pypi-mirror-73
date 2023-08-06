import dask
import numpy as np

from .core import Tensor


def from_array(array, dtag=None, dcompress=None, chunksize=-1) -> Tensor:
    """ Generates tensor from arraylike object
    """
    meta = {
        "dtype": array.dtype,
        "dtag": dtag,
        "dcompress": dcompress,
        "chunksize": chunksize,
    }
    if str(array.dtype) == "object":
        array = dask.array.from_array(array, chunks=1)
    else:
        array = dask.array.from_array(array)
    return Tensor(meta, array)


def concat(tensors, axis=0, chunksize=-1):
    """ Concats multiple tensors on axis into one tensor
    All input tensors should have same dtag, dtype, dcompress
    """
    raise NotImplementedError()


def stack(tensors, axis=0, chunksize=-1):
    """ Stack multiple tesnors into new axis
    All input tensors should have same dtag, dtype, dcompress
    """
    raise NotImplementedError()


def from_zeros(shape, dtype, dtag=None, dcompress=None, chunksize=-1) -> Tensor:
    """ Generates tensor from 0 filled array
    """
    meta = {
        "dtype": dtype,
        "dtag": dtag,
        "dcompress": dcompress,
        "chunksize": chunksize,
    }
    array = dask.array.from_array(np.zeros(shape, dtype))
    return Tensor(meta, array)
