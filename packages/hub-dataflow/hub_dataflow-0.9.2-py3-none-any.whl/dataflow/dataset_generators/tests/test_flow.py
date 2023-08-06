import os
import glob
import inspect

import dask
import numpy as np

from dataflow.dataset_generators.intelinair import ingestor
from dataflow.dataset_generators.intelinair import sampler
from dataflow.collections import dataset
from dataflow.utils import save

TEST_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    os.path.basename(__file__).rstrip(".py"),
)

_intelinair_bucket_path = "s3://intelinair-processing-agmri"
_intelinair_creds_path = "~/.snark/intelinair"


# TODO
def test_multilabel():
    fname = inspect.stack()[0][3].split("test_")[1]
    flight_codes = ["L4XRHNUBC"]

    ingest = ingestor.Ingestor(
        alert_types=[
            ingestor.UIUC_SBIR_COFFEE_TREE,
            ingestor.UIUC_SBIR_COFFEE_WEEDS,
            ingestor.UIUC_SBIR_COFFEE_GAPS,
        ],
        url="s3://intelinair-prod-private/prod/flights/",
        channels=["red", "green", "blue"],
    )

    ds = dataset.generate(ingest, flight_codes)
    my_sampler = sampler.PolygonSampler((3, 128, 128))

    ds = dataset.generate(my_sampler, ds)
    sample_dict = ds.store("./data/temp/v2")
    for el in sample_dict.keys():
        for i in range(2):
            arr = sample_dict[el][i].compute()
            gt_arr = np.load(f"{TEST_DIR}/{fname}_{i}_{el}.npy", allow_pickle=True)
            assert (arr == gt_arr).all()


# def flow_input_df():
#     intelin = Intelinair(intelinair.UIUC_ENDROW, max=5)
#     polys = dask.compute(
#         intelin._get_polygons_boundary_polygons_per_field(
#             "TVH8NLZU7", intelinair.UIUC_ENDROW
#         )
#     )
#     with open(f"{TEST_DIR}/input_dict.json", "w") as fout:
#         fout.write(json.dumps(polys[0]))


# def flow_expected():
#     fname = inspect.stack()[0][3].split("_expected")[0]
#     # with open(f"{TEST_DIR}/input_dict.json", "r") as finput:
#     # input_dict = json.load(finput)
#     flight_codes = intelinair.flight_codes_query(
#         [intelinair.UIUC_ENDROW], range_=(13, 15)
#     )
#     print(flight_codes)
#     return
#     ingestor = Intelinair(
#         flight_codes=flight_codes,
#         alert_types=[intelinair.UIUC_ENDROW],
#         url=_intelinair_bucket_path,
#         channels=["red", "green", "blue"],
#     )()
#     samples = PolygonSampler((3, 512, 1024), ingestor)()
#     el = 20
#     samples_dict = {key: samples[key][:el] for key in samples}
#     samples_dict = hub.zoom(samples_dict, zoom=[1, 2])
#     samples_dict = dask.compute(samples_dict)[0]
#     # for i in range(el):
#     #    save(samples_dict["image"][i].transpose(1, 2, 0), f"temp/{i}_image")
#     #    save(samples_dict["mask"][i], f"temp/{i}_mask")
#     #    save(samples_dict["labels"][i], f"temp/{i}_labels")
#     # return
#     for el in samples_dict:
#         for i in range(len(samples_dict[el])):
#             np.save(f"{TEST_DIR}/{fname}_{i}_{el}.npy", samples_dict[el][i])


def save_bbox(boxes, npy, out):
    label = npy.replace("box", "label")
    lnpy = np.load(label)
    for x in boxes:
        lnpy[x[1] : (x[3]), (x[0], (x[2]))] = 1
        lnpy[(x[1], (x[3])), x[0] : (x[2])] = 1
    save(np.array(lnpy, dtype=bool), full_path=out)


def flow_save_png(path):
    npy_files = glob.glob(f"{path}/*.npy")
    os.makedirs(path, exist_ok=True)
    for npy in npy_files:
        npy_dir, npy_name = os.path.split(npy)
        new_path = path.replace("test_flow", "test_flow_images")
        os.makedirs(new_path, exist_ok=True)
        out = os.path.join(new_path, npy_name.replace(".npy", ".png"))
        x = np.load(npy, allow_pickle=True)
        if "box_type" in npy:
            continue
        elif "box" in npy:
            save_bbox(x, npy, out)
        else:
            if "image" in npy:
                x = x.transpose(1, 2, 0)
            save(x, full_path=out)


def test_0_flight_codes():
    flight_codes = []
    ingest = ingestor.Ingestor(
        alert_types=[ingestor.UIUC_SBIR_COFFEE_TREE],
        url="s3://intelinair-prod-private/prod/flights/",
    )
    ds = dataset.generate(ingest, flight_codes)
    ds = ds.store("./data/temp/v3")
    assert len(ds) == 0
    assert "polygon_labels" in ds.keys()
    assert ds["polygon_labels"].shape == (0,)


def test_no_specefic_alert_type_for_flight_code():
    # "K6TINMCM7 fligth code generated with alert_type UIUC_ENDROW and doesn't have COFFEE_TREEs
    flight_codes = ["K6TINMCM7"]
    ingest = ingestor.Ingestor(
        alert_types=[ingestor.UIUC_SBIR_COFFEE_TREE],
        url=_intelinair_bucket_path,
        channels=["red"],
    )
    ds = dataset.generate(ingest, flight_codes)
    my_sampler = sampler.PolygonSampler((1, 512, 1024))
    ds = dataset.generate(my_sampler, ds)
    assert len(ds["image"].compute()) == 0


def test_skip_large_field():
    # "P9THUZUQ3" field larger than 10GB
    flight_codes = ["P9THUZUQ3"]
    ingest = ingestor.Ingestor(
        alert_types=[ingestor.UIUC_ENDROW],
        url=_intelinair_bucket_path,
        channels=["red", "green", "blue"],
    )
    ds = dataset.generate(ingest, flight_codes)
    my_sampler = sampler.PolygonSampler((3, 512, 1024))
    ds = dataset.generate(my_sampler, ds)
    assert len(ds["image"].compute()) == 0


# def bad_flight():
#     pass
#     # got some problem for the below flight_codes for red channel, however can't repreduce
#     # flight_codes = ["CD2F26XHE", "XYE3T7MKL"]
#     # ingest_obj = Intelinair(
#     #    flight_codes=flight_codes1,
#     #    alert_types=[intelinair.UIUC_SBIR_COFFEE_TREE],
#     #    url="s3://intelinair-prod-private/prod/flights/",
#     #    creds=_intelinair_creds_path,
#     #    channels=["red", "green", "blue"],
#     # )


# test_0_flight_codes()
# test_multilabel()
# test_multilabel()
# flow_expected()
# flow_save_png("./data/flow")
# test_flow()
# test_usecase4_pipeline()

# test_usecase4_pipeline()
# test_intelinair_flight_codes_query()
# P9THUZUQ3 --- large field

# if __name__ == "__main__":
#     # print(TEST_DIR)
#     # test_multilabel()
#     # flow_save_png("./dataflow/dataset_generators/tests/test_flow")
#     test_flow()

