import os
import time
from operator import mul
from functools import reduce

import fsspec
import numpy as np
from PIL import Image
from dataflow.creds import Creds
from dataflow.logger import logger
from subprocess import Popen, PIPE


def save(img: np.ndarray, name: str = "outfile", full_path=None):
    img = img.astype("float")
    img -= img.min(axis=(0, 1))
    img = img / img.max(axis=(0, 1))
    img *= 255
    img = img.astype("uint8")

    if img.shape[-1] == 4:
        img = Image.fromarray(img[:, :, 1:4])
    else:
        img = Image.fromarray(img)
    if full_path:
        img.save(full_path)
    else:
        img.save(f"data/{name}.png")


def connect_fs(url: str, creds: Creds = None) -> fsspec.AbstractFileSystem:
    if url.startswith("s3://"):
        if creds is None:
            return fsspec.filesystem("s3")
        else:
            return fsspec.filesystem(
                "s3",
                key=creds.get("aws_access_key_id"),
                secret=creds.get("aws_secret_access_key"),
                # token=creds.get("aws_secret_access_token"),
            )
    else:
        if not os.path.exists(url):
            raise Exception(f"Folder not found for: {url}")
        return fsspec.filesystem("file")


def execute(cmd):
    env = os.environ.copy()
    cmd = " ".join([ele for ele in cmd])
    logger.debug("Executing " + cmd)
    t1 = time.time()

    if cmd[-2:] == " &":  # Run in background
        os.system(cmd)
        logger.debug("running in background mode {}".format(time.time() - t1))
        return "running background"
    p = Popen(cmd, shell=True, stdout=PIPE, env=env)
    logger.debug("running in forward mode {}".format(time.time() - t1))
    out = p.stdout.read()
    return out


def compute_chunk_size(dtype: str, shape: list):
    """  Compute effective chunk size for arrays >12MB
    Parameters
    ----------
    dtype: str
        e.g. "uint8", "int8", "int32", "float32" 
    shape: list
        e.g. [1,2024,2024]
    """
    shape = list(map(lambda x: x if x > 0 else 1, shape))
    bsize = np.dtype(dtype).itemsize

    csize = (12 * 1024 * 1024) // (bsize * reduce(mul, shape[1:])) + 1
    csize = min(csize, shape[0])
    return csize
