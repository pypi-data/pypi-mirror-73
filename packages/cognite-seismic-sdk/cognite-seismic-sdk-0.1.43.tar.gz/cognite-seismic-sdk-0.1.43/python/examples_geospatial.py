# Copyright 2020 Cognite AS

"""Cognite Geospatial API Example

"""
from os import getenv
from random import randint

import numpy as np
from cognite.geospatial import CogniteGeospatialClient


def main():
    api_key = getenv("API_KEY")
    base_url = getenv("API_HOST")
    api_port = getenv("API_PORT")
    project = getenv("PROJECT")
    client = CogniteGeospatialClient(
        base_url=base_url or "localhost", port=api_port or 8080, api_key=api_key or "TESTKEY", project=project or "test"
    )
    random_suff = str(randint(0, 4000000000))
    point = client.create_geometry(
        name="Test_Point_" + random_suff,
        layer="point",
        crs="epsg:23031",
        asset_ids=[1, 2, 3],
        external_id="test_point_" + random_suff,
        geometry="POINT(100 120)",
        source="test",
    )
    print(point)
    deleted_point = client.delete_spatial(id=point.id)
    print(deleted_point)

    image = client.save_spatial(
        name="Test_Raster_" + random_suff,
        external_id="test_raster_" + random_suff,
        description="test data",
        source="test",
        crs="epsg:23031",
        layer="seismic",
        attributes={
            "iline": np.array([1, 1, 2, 2], dtype=np.int32),
            "xline": np.array([1, 2, 1, 2], dtype=np.int32),
            "active": np.array([True, True, True, True]),
            "x": np.array([420838.328165, 420838.328165, 420938.328165, 420938.328165]),
            "y": np.array([6539805.411659, 6539905.411659, 6539805.411659, 6539905.411659]),
        },
        asset_ids=[4, 5],
    )
    print("image", image)
    id = image.id
    external_id = image.external_id
    crs = image.crs

    # List Items
    items = client.find_spatial(limit=10)  # source="horizon", limit=10)
    print("List:", items)

    # Get Spatial Item Info
    item = client.get_spatial_info(id=id)
    print("Item by id:", item)

    item = client.get_spatial_info(external_id=external_id)
    print("Item by external_id:", item)

    # Get Spatial Item Data
    item = client.get_spatial(id=id)
    print("Item by id:", item is not None)
    value = item.get()
    print("Image points", value.shape)
    value = item.grid()
    print("Image grid", value)

    item = client.get_spatial(external_id=external_id)
    print("Item by external_id:", item is not None)

    # Get Spatial Coverage
    coverage = client.get_coverage(id=id)
    print("Coverage by id:", coverage is not None)
    coverage = client.get_coverage(external_id=external_id)
    print("Coverage by external_id:", coverage is not None)

    # coverage = client.get_coverage(id=id, projection="3d")
    # print("Coverage by external_id:", coverage)

    # Find Within
    items = client.find_within(id=id, crs=crs)
    print("Within by geometry:", items)

    # Find Within
    # items = client.find_within(id=id, crs=crs, projection="3d")
    # print("Within by geometry:", items)

    items = client.find_within(external_id=external_id, crs=crs)
    print("Within by geometry:", items)

    items = client.find_within(geography="POINT(1 1)", crs=crs)
    print("Within by geometry:", items)

    # Find Within Distance
    items = client.find_within(id=id, distance=1, crs=crs)
    print("Within by geometry distance:", items)

    items = client.find_within(external_id=external_id, distance=1, crs=crs)
    print("Within by geometry distance:", items)

    items = client.find_within(geography="POINT(1 1)", distance=1, crs=crs)
    print("Within distance by geometry distance:", items)

    # Find Within Distance
    items = client.find_within_completely(id=id, crs=crs)
    print("Completely within by geometry distance:", items)

    items = client.find_within_completely(external_id=external_id, crs=crs)
    print("Completely within by geometry distance:", items)

    items = client.find_within_completely(geography="POINT(1 1)", crs=crs)
    print("Completely within distance by geometry distance:", items)


if __name__ == "__main__":
    main()
