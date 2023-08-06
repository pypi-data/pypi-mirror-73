from __future__ import division, unicode_literals, print_function, absolute_import

import sys
import traitlets as tl


class BaseCoordinates(tl.HasTraits):
    """Base class for single or stacked one-dimensional coordinates."""

    def _set_name(self, value):
        raise NotImplementedError

    @property
    def name(self):
        """:str: Dimension name."""
        raise NotImplementedError

    @property
    def dims(self):
        """:tuple: Dimensions."""
        raise NotImplementedError

    @property
    def udims(self):
        """:tuple: Dimensions."""
        raise NotImplementedError

    @property
    def idims(self):
        """:tuple: Dimensions."""
        raise NotImplementedError

    @property
    def size(self):
        """Number of coordinates."""
        raise NotImplementedError

    @property
    def shape(self):
        """coordinates shape."""
        raise NotImplementedError

    @property
    def coordinates(self):
        """Coordinate values."""
        raise NotImplementedError

    @property
    def coords(self):
        """xarray coords value"""
        raise NotImplementedError

    @property
    def definition(self):
        """Coordinates definition."""
        raise NotImplementedError

    @property
    def full_definition(self):
        """Coordinates definition, containing all properties. For internal use."""
        raise NotImplementedError

    @classmethod
    def from_definition(cls, d):
        """Get Coordinates from a coordinates definition."""
        raise NotImplementedError

    def copy(self):
        """Deep copy of the coordinates and their properties."""
        raise NotImplementedError

    def get_area_bounds(self, boundary):
        """Get coordinate area bounds, including boundary information, for each unstacked dimension. """
        raise NotImplementedError

    def select(self, bounds, outer=False, return_indices=False):
        """Get coordinate values that are with the given bounds."""
        raise NotImplementedError

    def simplify(self):
        """ Get the simplified/optimized representation of these coordinates. """
        raise NotImplementedError

    def issubset(self, other):
        """Report if these coordinates are a subset of other coordinates."""
        raise NotImplementedError

    def __getitem__(self, index):
        raise NotImplementedError

    def __repr__(self):
        raise NotImplementedError

    def __eq__(self, other):
        raise NotImplementedError

    # python 2 compatibility
    if sys.version < "3":

        def __ne__(self, other):
            return not self.__eq__(other)
