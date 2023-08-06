from collections import abc
from configparser import ConfigParser
import json
import multiprocessing
import os
from typing import Dict, Tuple

import dask
import fsspec
import numpy as np

try:
    import torch
except ImportError:
    pass

from dataflow.collections.tensor.core import Tensor
from dataflow.collections.client_manager import get_client
from dataflow.ingestor.intelinair.logger import logger


class DatasetGenerator:
    def __init__(self):
        pass

    def __call__(self, input):
        raise NotImplementedError()

    def meta(self):
        raise NotImplementedError()


def _numpy_to_tuple(arr: np.ndarray):
    return [np.array([t]) for t in arr]


def _numpy_saver(fs: fsspec.AbstractFileSystem, filepath: str, array: np.ndarray):
    with fs.open(filepath, "wb") as f:
        np.save(f, array, allow_pickle=True)


def _numpy_saver_multi(
    fs: fsspec.AbstractFileSystem, filepath: str, arrays: np.ndarray, offset: int
):
    for i in range(len(arrays)):
        _numpy_saver(fs, os.path.join(filepath, f"{offset+i}.npy"), arrays[i : i + 1])
    return len(arrays)


def _preprocess_meta_before_save(meta: dict):
    meta = dict(meta)
    meta["dtype"] = str(meta["dtype"])
    return meta


def _dask_shape(input_shape: Tuple[int]):
    return (np.nan,) + input_shape[1:] if input_shape[0] == -1 else input_shape


def _dict_to_tuple(d: dict):
    keys = sorted(d.keys())
    lens = {len(d[key]) for key in keys}
    assert len(lens) == 1
    cnt = next(iter(lens))
    return [d[key][i] for i in range(cnt) for key in keys], keys


def _tuple_to_dict(t: tuple, keys: tuple):
    cnt = len(keys)
    assert len(t) % cnt == 0
    return {key: [t[i] for i in range(j, len(t), cnt)] for j, key in enumerate(keys)}


def _load_creds(creds):
    if creds is None:
        return None
    elif isinstance(creds, str) and os.path.exists(creds):
        parser = ConfigParser()
        parser.read(creds)
        return {section: dict(parser.items(section)) for section in parser.sections()}
    else:
        return creds


def _load_fs_and_path(path, creds):
    creds = _load_creds(creds)
    if path.startswith("s3://"):
        path = path[5:]
        if creds is not None:
            return (
                fsspec.filesystem(
                    "s3",
                    key=creds.get("aws_access_key_id"),
                    secret=creds.get("aws_secret_access_key"),
                    # token=creds.get("aws_secret_access_token"),
                ),
                path,
            )
        else:
            return fsspec.filesystem("s3"), path
    else:
        return fsspec.filesystem("file"), os.path.expanduser(path)


class Dataset:
    def __init__(self, tensors: Dict[str, Tensor]):
        self._tensors = tensors
        shape = None
        for name, tensor in tensors.items():
            if shape is None or tensor.ndim > len(shape):
                shape = tensor.shape
            self._len = tensor.count

    def __len__(self) -> int:
        return self._len

    @property
    def count(self) -> int:
        return self._len

    def __iter__(self):
        for i in range(len(self)):
            yield {key: t._array[i] for key, t in self._tensors.items()}

    def keys(self):
        yield from self._tensors.keys()

    def items(self):
        yield from self._tensors.items()

    def __getitem__(self, slices) -> "Dataset":
        if isinstance(slices, tuple):
            if all([isinstance(s, str) for s in slices]):
                return Dataset({key: self._tensors[key] for key in slices})
            elif isinstance(slices[0], abc.Iterable) and all(
                [isinstance(s, str) for s in slices[0]]
            ):
                return Dataset({key: self._tensors[key] for key in slices[0]})[
                    slices[1:]
                ]
            else:
                assert all(
                    [isinstance(s, slice) or isinstance(s, int) for s in slices]
                ), "invalid indexing, either wrong order or wrong type"
                ndim = len(slices)
                if all(isinstance(s, int) for s in slices):
                    return {
                        name: tensor[slices]
                        for name, tensor in self._tensors.items()
                        if tensor.ndim >= ndim
                    }
                else:
                    return Dataset(
                        {
                            name: tensor[slices]
                            for name, tensor in self._tensors.items()
                            if tensor.ndim >= ndim
                        }
                    )

        elif isinstance(slices, str):
            return self._tensors[slices]
        elif isinstance(slices, slice):
            return Dataset({key: value[slices] for key, value in self._tensors.items()})
        elif isinstance(slices, int):
            return {key: value[slices] for key, value in self._tensors.items()}

    def cache(self) -> "Dataset":
        raise NotImplementedError()

    def _store_unknown_sized_ds(self, fs: fsspec.AbstractFileSystem, path: str) -> int:
        client = get_client()
        worker_count = multiprocessing.cpu_count()
        # worker_count = 4
        chunks = {key: t._delayed_objs for key, t in self._tensors.items()}
        chunk_count = [len(items) for _, items in chunks.items()]
        assert (
            len(set(chunk_count)) == 1
        ), "Number of chunks in each tensor should be the same to be able to store dataset"
        chunk_count = chunk_count[0]
        count = 0
        for i in range(0, chunk_count, worker_count):
            batch_count = min(i + worker_count, chunk_count) - i
            tasks = {
                key: delayed_objs[i : i + batch_count]
                for key, delayed_objs in chunks.items()
            }
            # logger.info(tasks)
            tasks, keys = _dict_to_tuple(tasks)

            # dask.visualize(
            #     tasks, filename=f"./data/tasks/{i}", optimize_graph=True,
            # )
            persisted = client.persist(tasks)
            persisted = _tuple_to_dict(persisted, keys)
            # for j in range(batch_count):
            #     assert (
            #         len(
            #             {
            #                 # len(objs[j])
            #                 # client.submit()
            #                 dask.delayed(len)(objs[j]).compute()
            #                 for objs in persisted.values()
            #             }
            #         )
            #         == 1
            #     ), "All numpy arrays returned from call should have same len"
            lens = [
                # len(next(iter(persisted.values()))[j])
                dask.delayed(len)(next(iter(persisted.values()))[j]).compute()
                for j in range(batch_count)
            ]
            tasks = [
                dask.delayed(_numpy_saver)(
                    fs, os.path.join(path, key, f"{sum(lens[:j], count) + i}.npy"), d,
                )
                # dask.delayed(_numpy_saver)(fs, os.path.join(path, key), objs[j])
                for key, objs in persisted.items()
                for j in range(batch_count)
                for i, d in enumerate(
                    dask.delayed(_numpy_to_tuple, nout=lens[j])(objs[j])
                )
            ]
            client.gather(client.compute(tasks))
            # wait(dask.persist(*tasks))
            # wait(client.persist(*tasks))
            count = sum(lens, count)
            logger.info(f"Samples done: {count}")
        return count

    def _store_known_sized_ds(self, fs: fsspec.AbstractFileSystem, path: str) -> int:
        tasks = {
            name: [
                dask.delayed(_numpy_saver)(
                    fs, os.path.join(path, name, str(i) + ".npy"), t._array[i : i + 1]
                )
                for i in range(len(self))
            ]
            for name, t in self._tensors.items()
        }

        for i in range(len(self)):
            dask.compute([tasks[name][i] for name in self._tensors])

    @property
    def meta(self) -> dict:
        tensor_meta = {
            name: _preprocess_meta_before_save(t._meta)
            for name, t in self._tensors.items()
        }
        ds_meta = {"tensors": tensor_meta, "len": self.count}
        return ds_meta

    def delete(self, tag, creds=None) -> bool:
        fs, path = _load_fs_and_path(tag, creds)
        fs: fsspec.AbstractFileSystem = fs
        if fs.exists(path):
            fs.delete(path, recursive=True)
            return True
        return False

    def store(self, tag, creds=None) -> "Dataset":
        fs, path = _load_fs_and_path(tag, creds)
        fs: fsspec.AbstractFileSystem = fs
        self.delete(path, creds)
        fs.makedirs(path)
        tensor_paths = [os.path.join(path, t) for t in self._tensors]
        for tensor_path in tensor_paths:
            fs.makedir(tensor_path)
        tensor_meta = {
            name: _preprocess_meta_before_save(t._meta)
            for name, t in self._tensors.items()
        }
        count = self.count
        if count == -1:
            count = self._store_unknown_sized_ds(fs, path)
        else:
            self._store_known_sized_ds(fs, path)

        for _, el in tensor_meta.items():
            el["shape"] = (count,) + el["shape"][1:]
        ds_meta = {"tensors": tensor_meta, "len": count}
        with fs.open(os.path.join(path, "meta.json"), "w") as f:
            f.write(json.dumps(ds_meta, indent=2, sort_keys=True))

        return load(tag, creds)

    def to_pytorch(self, transform=None):
        return TorchDataset(self, transform)


def _numpy_load(fs: fsspec.AbstractFileSystem, filepath: str) -> np.ndarray:
    assert fs.exists(filepath)
    with fs.open(filepath, "rb") as f:
        return np.load(f, allow_pickle=True)


def load(tag, creds=None) -> Dataset:
    """ Load a dataset from repository using given url
    """
    fs, path = _load_fs_and_path(tag, creds)
    fs: fsspec.AbstractFileSystem = fs
    assert fs.exists(path)
    with fs.open(os.path.join(path, "meta.json"), "r") as f:
        ds_meta = json.loads(f.read())

    for name in ds_meta["tensors"]:
        assert fs.exists(os.path.join(path, name))
    if ds_meta["len"] == 0:
        logger.warning("The dataset is empty (has 0 samples)")
        return Dataset(
            {
                name: Tensor(
                    tmeta,
                    dask.array.from_array(
                        np.empty(shape=(0,) + tuple(tmeta["shape"][1:]), dtype="uint8"),
                    ),
                )
                for name, tmeta in ds_meta["tensors"].items()
            }
        )

    return Dataset(
        {
            name: Tensor(
                tmeta,
                dask.array.concatenate(
                    [
                        dask.array.from_delayed(
                            dask.delayed(_numpy_load)(
                                fs, os.path.join(path, name, str(i) + ".npy")
                            ),
                            shape=(1,) + tuple(tmeta["shape"][1:]),
                            dtype=tmeta["dtype"],
                        )
                        for i in range(ds_meta["len"])
                    ]
                ),
            )
            for name, tmeta in ds_meta["tensors"].items()
        }
    )


def _is_arraylike(arr):
    return (
        isinstance(arr, np.ndarray) or isinstance(arr, list) or isinstance(arr, tuple)
    )


def _is_tensor_dynamic(tensor):
    # print(type(tensor._array.to_delayed().flatten()[0]))
    arr = tensor._array.to_delayed().flatten()[0].compute()
    return str(tensor.dtype) == "object" and _is_arraylike(arr.flatten()[0])


class TorchDataset:
    def __init__(self, ds, transform=None):
        self._ds = ds
        self._transform = transform
        self._dynkeys = {
            key for key in self._ds.keys() if _is_tensor_dynamic(self._ds[key])
        }

    def _do_transform(self, data):
        return self._transform(data) if self._transform else data

    def __len__(self):
        return len(self._ds)

    def __getitem__(self, index):
        return self._do_transform(
            {key: value.compute() for key, value in self._ds[index].items()}
        )

    def __iter__(self):
        for i in range(len(self)):
            yield self[i]

    def collate_fn(self, batch):
        batch = tuple(batch)
        keys = tuple(batch[0].keys())
        ans = {key: [item[key] for item in batch] for key in keys}
        for key in keys:
            if key not in self._dynkeys:
                ans[key] = torch.tensor(ans[key])
            else:
                ans[key] = [torch.tensor(item) for item in ans[key]]
        return ans
