import os.path

import numpy as np

from podpac.core.data.h5py_source import H5PY


class TestH5PY(object):
    source = os.path.join(os.path.dirname(__file__), "assets/h5raster.hdf5")

    def test_init(self):
        node = H5PY(source=self.source, data_key="/data/init", lat_key="/coords/lat", lon_key="/coords/lon")
        node.close_dataset()

    def test_dims(self):
        node = H5PY(source=self.source, data_key="/data/init", lat_key="/coords/lat", lon_key="/coords/lon")
        assert node.dims == ["lat", "lon"]
        node.close_dataset()

    def test_available_data_keys(self):
        node = H5PY(source=self.source, data_key="/data/init", lat_key="/coords/lat", lon_key="/coords/lon")
        assert node.available_data_keys == ["/data/init"]
        node.close_dataset()

    def test_coordinates(self):
        node = H5PY(source=self.source, data_key="/data/init", lat_key="/coords/lat", lon_key="/coords/lon")
        nc = node.coordinates
        assert node.coordinates.shape == (3, 4)
        np.testing.assert_array_equal(node.coordinates["lat"].coordinates, [45.1, 45.2, 45.3])
        np.testing.assert_array_equal(node.coordinates["lon"].coordinates, [-100.1, -100.2, -100.3, -100.4])
        node.close_dataset()

    def test_data(self):
        node = H5PY(source=self.source, data_key="/data/init", lat_key="/coords/lat", lon_key="/coords/lon")
        o = node.eval(node.coordinates)
        np.testing.assert_array_equal(o.data.ravel(), np.arange(12))
        node.close_dataset()

        # default
        node = H5PY(source=self.source, lat_key="/coords/lat", lon_key="/coords/lon")
        o = node.eval(node.coordinates)
        np.testing.assert_array_equal(o.data.ravel(), np.arange(12))
        node.close_dataset()

    def test_data_multiple(self):
        node = H5PY(
            source=self.source,
            data_key=["/data/init", "/data/init"],
            outputs=["a", "b"],
            lat_key="/coords/lat",
            lon_key="/coords/lon",
        )
        o = node.eval(node.coordinates)
        assert o.dims == ("lat", "lon", "output")
        np.testing.assert_array_equal(o["output"], ["a", "b"])
        np.testing.assert_array_equal(o.sel(output="a").data.ravel(), np.arange(12))
        np.testing.assert_array_equal(o.sel(output="b").data.ravel(), np.arange(12))
        node.close_dataset()

    def test_dataset_attrs(self):
        node = H5PY(source=self.source, data_key="/data/init", lat_key="/coords/lat", lon_key="/coords/lon")
        assert node.dataset_attrs() == {}
        assert node.dataset_attrs("data") == {"test": "test"}
        assert node.dataset_attrs("coords/lat") == {"unit": "degrees"}
        assert node.dataset_attrs("coords/lon") == {"unit": "degrees"}
        assert node.dataset_attrs("coords") == {"crs": "EPSG:4326s"}
        node.close_dataset()
