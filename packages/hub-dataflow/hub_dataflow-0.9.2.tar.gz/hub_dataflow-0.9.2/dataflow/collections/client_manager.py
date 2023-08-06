from dataflow.hub_api import get_client as _get_client


_client = None


def get_client():
    # global _client
    # if _client is None:
    #     _client = Client(n_workers=4)
    # return _client
    return _get_client()
