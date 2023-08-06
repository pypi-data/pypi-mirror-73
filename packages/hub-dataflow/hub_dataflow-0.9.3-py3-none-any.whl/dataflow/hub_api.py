import math
import time
from threading import RLock

from dataflow.logger import logger
from dask.cache import Cache
from dask.distributed import Client
from dataflow.cloud.cluster import Cluster
from dataflow.cloud.iam_blocked_check import check_arns

local_dir = "data/preprocess_nova"
bucket2obj = {}
botolock = RLock()
_client = None


def get_client():
    global _client
    if _client is None:
        _client = init()
    return _client


def init(
    token: str = "",
    cache=2e9,
    cloud=False,
    n_workers=4,
    image="snarkai/hub:dataflow-prod",
):
    """Initializes cluster either local or on the cloud
        
        Parameters
        ----------
        token: str
            token provided by snark
        cache: float
            Amount on local memory to cache locally, default 2e9 (2GB)
        cloud: bool
            Should be run locally or on the cloud
        n_workers: int
            number of concurrent workers, default 5
        image: str
            default (snarkai/hub:dataflow-prod)
            change to snarkai/hub:dataflow-prod

    """
    if cloud:
        check_arns()
        logger.info("Starting Cloud Cluster, it will take 5 mins")

        # TODO simplify container login
        t1 = time.time()
        cluster = Cluster(n_workers=n_workers, image=image,)
        client = Client(cluster)
        t2 = time.time()
        logger.info(f"Cluster started in {t2-t1}s: {cluster.dashboard_link}")
    else:
        client = Client(n_workers=n_workers, processes=True, memory_limit=50e9,)
    cache = Cache(cache)
    cache.register()
    global _client
    _client = client
    return client


def slice_ds(ds: dict, start: int, stop: int, step: int = 1):
    """Slicing dataset according to the given range. This function must be used
    to slice sampler dataset as it takes care of some special keys.

    Parameters
    ----------
    ds: Dict
        Representing dataset as dictionary.
    start: int
        Starting integer where the slicing of the object starts. 
    stop: int
        Integer until which the slicing takes place. The slicing stops at index stop -1 (last element).
    step (optional) : int
        Integer value which determines the increment between each index for slicing. Defaults to 1.

    Returns
    -------
    dict
        Dictionary dataset where each key is sliced by given range

    Examples
    --------
    >>> train = hub_api.slice_ds(ds, 0, 10)
    >>> val = hub_api.slice_ds(ds, 10, -1)
    """
    key = sorted(ds.keys())[-1]
    dslen = ds[key].shape[0]
    if stop == -1:
        stop = dslen
    if stop > dslen:
        raise Exception(
            f"stop is larger than dataset size, stop: {stop}, dataset len: {dslen}"
        )
    if start >= stop:
        raise Exception(f"start >= stop start: {start}, stop: {stop}")
    interval = slice(start, stop, step)
    new_ds = {k: v[interval] for k, v in ds.items() if k != "__special__"}
    if "__special__" in ds:
        new_ds["__special__"] = ds["__special__"]
    return new_ds


def slicep_ds(ds: dict, start: float, end: float):
    """Slicing dataset according to the given range. This function must be used
    to slice sampler dataset as it takes care of some special keys
    Parameters
    ----------
    ds: Dict
        Representing dataset as dictionary.
    start: float
        Starting percentile where the slicing of the object starts
    end: int
        Ending percentile until which the slicing takes place. The slicing stops at index stop 100 (last element)

    Returns
    ----------
    Dictionary dataset where each key is sliced by given range

    Examples
    --------
    >>> train = hub_api.slice_ds(ds, 0, 40)
    >>> val = hub_api.slice_ds(ds, 40, 100)
    """
    key = sorted(list(ds.keys()))[-1]
    cnt = ds[key].shape[0]
    start = int(math.floor(start * cnt / 100.0))
    end = int(math.ceil(end * cnt / 100.0))
    return slice_ds(ds, start, end, 1)