"""
Tests for grdtrack
"""
import os

import numpy.testing as npt
import pandas as pd
import pytest

from .. import grdtrack
from .. import which
from ..datasets import load_earth_relief, load_ocean_ridge_points
from ..exceptions import GMTInvalidInput
from ..helpers import data_kind

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
TEMP_TRACK = os.path.join(TEST_DATA_DIR, "tmp_track.txt")


def test_grdtrack_input_dataframe_and_dataarray():
    """
    Run grdtrack by passing in a pandas.DataFrame and xarray.DataArray as
    inputs
    """
    dataframe = load_ocean_ridge_points()
    dataarray = load_earth_relief().sel(lat=slice(-49, -42), lon=slice(-118, -107))

    output = grdtrack(points=dataframe, grid=dataarray, newcolname="bathymetry")
    assert isinstance(output, pd.DataFrame)
    assert output.columns.to_list() == ["longitude", "latitude", "bathymetry"]
    npt.assert_allclose(output.iloc[0], [-110.9536, -42.2489, -2797.394987])

    return output


def test_grdtrack_input_csvfile_and_dataarray():
    """
    Run grdtrack by passing in a csvfile and xarray.DataArray as inputs
    """
    csvfile = which("@ridge.txt", download="c")
    dataarray = load_earth_relief().sel(lat=slice(-49, -42), lon=slice(-118, -107))

    try:
        output = grdtrack(points=csvfile, grid=dataarray, outfile=TEMP_TRACK)
        assert output is None  # check that output is None since outfile is set
        assert os.path.exists(path=TEMP_TRACK)  # check that outfile exists at path

        track = pd.read_csv(TEMP_TRACK, sep="\t", header=None, comment=">")
        npt.assert_allclose(track.iloc[0], [-110.9536, -42.2489, -2797.394987])
    finally:
        os.remove(path=TEMP_TRACK)

    return output


def test_grdtrack_input_dataframe_and_ncfile():
    """
    Run grdtrack by passing in a pandas.DataFrame and netcdf file as inputs
    """
    dataframe = load_ocean_ridge_points()
    ncfile = which("@earth_relief_01d", download="c")

    output = grdtrack(points=dataframe, grid=ncfile, newcolname="bathymetry")
    assert isinstance(output, pd.DataFrame)
    assert output.columns.to_list() == ["longitude", "latitude", "bathymetry"]
    npt.assert_allclose(output.iloc[0], [-32.2971, 37.4118, -1686.748899])

    return output


def test_grdtrack_input_csvfile_and_ncfile():
    """
    Run grdtrack by passing in a csvfile and netcdf file as inputs
    """
    csvfile = which("@ridge.txt", download="c")
    ncfile = which("@earth_relief_01d", download="c")

    try:
        output = grdtrack(points=csvfile, grid=ncfile, outfile=TEMP_TRACK)
        assert output is None  # check that output is None since outfile is set
        assert os.path.exists(path=TEMP_TRACK)  # check that outfile exists at path

        track = pd.read_csv(TEMP_TRACK, sep="\t", header=None, comment=">")
        npt.assert_allclose(track.iloc[0], [-32.2971, 37.4118, -1686.748899])
    finally:
        os.remove(path=TEMP_TRACK)

    return output


def test_grdtrack_wrong_kind_of_points_input():
    """
    Run grdtrack using points input that is not a pandas.DataFrame (matrix) or
    file
    """
    dataframe = load_ocean_ridge_points()
    invalid_points = dataframe.longitude.to_xarray()
    dataarray = load_earth_relief().sel(lat=slice(-49, -42), lon=slice(-118, -107))

    assert data_kind(invalid_points) == "grid"
    with pytest.raises(GMTInvalidInput):
        grdtrack(points=invalid_points, grid=dataarray, newcolname="bathymetry")


def test_grdtrack_wrong_kind_of_grid_input():
    """
    Run grdtrack using grid input that is not as xarray.DataArray (grid) or
    file
    """
    dataframe = load_ocean_ridge_points()
    dataarray = load_earth_relief().sel(lat=slice(-49, -42), lon=slice(-118, -107))
    invalid_grid = dataarray.to_dataset()

    assert data_kind(invalid_grid) == "matrix"
    with pytest.raises(GMTInvalidInput):
        grdtrack(points=dataframe, grid=invalid_grid, newcolname="bathymetry")


def test_grdtrack_without_newcolname_setting():
    """
    Run grdtrack by not passing in newcolname parameter setting
    """
    dataframe = load_ocean_ridge_points()
    dataarray = load_earth_relief().sel(lat=slice(-49, -42), lon=slice(-118, -107))

    with pytest.raises(GMTInvalidInput):
        grdtrack(points=dataframe, grid=dataarray)


def test_grdtrack_without_outfile_setting():
    """
    Run grdtrack by not passing in outfile parameter setting
    """
    csvfile = which("@ridge.txt", download="c")
    dataarray = load_earth_relief().sel(lat=slice(-49, -42), lon=slice(-118, -107))

    with pytest.raises(GMTInvalidInput):
        grdtrack(points=csvfile, grid=dataarray)
