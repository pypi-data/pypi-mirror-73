from dataflow.dataset_generators.intelinair import ingestor
from dataflow.collections import dataset

_intelinair_bucket_path = "s3://intelinair-processing-agmri"
_intelinair_creds_path = "~/.snark/intelinair"


def test_tif_file_not_found():
    # "9GPAK8U7WA" - no tif file, "GYUJAVCEY" - awesome flight_code
    flight_codes = ["9GPAK8U7WA"]
    my_ingestor = ingestor.Ingestor(
        alert_types=[ingestor.UIUC_ENDROW],
        url=_intelinair_bucket_path,
        channels=["red"],
    )

    ds = dataset.generate(my_ingestor, flight_codes)
    # first field should should be empty, because no tif file exists.
    assert ds["field"][0].compute().shape == (0,)


def test_no_polygon_found():
    # "WE83UTP9K" - no polygons, "GYUJAVCEY" - awesome flight_code
    flight_codes = ["WE83UTP9K"]
    my_ingestor = ingestor.Ingestor(
        alert_types=[ingestor.UIUC_ENDROW],
        url=_intelinair_bucket_path,
        channels=["red"],
    )
    ds = dataset.generate(my_ingestor, flight_codes)
    assert ds["polygons"][0].compute().shape == (0,)
