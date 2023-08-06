"""
One-Dimensional Coordinates
"""


from __future__ import division, unicode_literals, print_function, absolute_import

import copy

import numpy as np
import traitlets as tl

from podpac.core.utils import ArrayTrait
from podpac.core.coordinates.utils import make_coord_value, make_coord_delta, make_coord_delta_array
from podpac.core.coordinates.utils import add_coord, divide_delta, lower_precision_time_bounds
from podpac.core.coordinates.utils import Dimension
from podpac.core.coordinates.base_coordinates import BaseCoordinates


class Coordinates1d(BaseCoordinates):
    """
    Base class for 1-dimensional coordinates.

    Coordinates1d objects contain values and metadata for a single dimension of coordinates. :class:`podpac.Coordinates` and
    :class:`StackedCoordinates` use Coordinate1d objects.
    
    Parameters
    ----------
    name : str
        Dimension name, one of 'lat', 'lon', 'time', or 'alt'.
    coordinates : array, read-only
        Full array of coordinate values.
    
    See Also
    --------
    :class:`ArrayCoordinates1d`, :class:`UniformCoordinates1d`
    """

    name = Dimension(allow_none=True)
    _properties = tl.Set()

    @tl.observe("name")
    def _set_property(self, d):
        if d["name"] is not None:
            self._properties.add(d["name"])

    def _set_name(self, value):
        # set name if it is not set already, otherwise check that it matches
        if "name" not in self._properties:
            self.name = value
        elif self.name != value:
            raise ValueError("Dimension mismatch, %s != %s" % (value, self.name))

    # ------------------------------------------------------------------------------------------------------------------
    # standard methods
    # ------------------------------------------------------------------------------------------------------------------

    def __repr__(self):
        return "%s(%s): Bounds[%s, %s], N[%d]" % (
            self.__class__.__name__,
            self.name or "?",
            self.bounds[0],
            self.bounds[1],
            self.size,
        )

    def __eq__(self, other):
        if not isinstance(other, Coordinates1d):
            return False

        # defined coordinate properties should match
        for name in self._properties.union(other._properties):
            if getattr(self, name) != getattr(other, name):
                return False

        # shortcuts (not strictly necessary)
        for name in ["size", "is_monotonic", "is_descending", "is_uniform"]:
            if getattr(self, name) != getattr(other, name):
                return False

        return True

    # ------------------------------------------------------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def dims(self):
        if self.name is None:
            raise TypeError("cannot access dims property of unnamed Coordinates1d")
        return (self.name,)

    @property
    def udims(self):
        return self.dims

    @property
    def idims(self):
        return self.dims

    @property
    def shape(self):
        return (self.size,)

    @property
    def coords(self):
        """:dict-like: xarray coordinates (container of coordinate arrays)"""

        return {self.name: self.coordinates}

    @property
    def dtype(self):
        """:type: Coordinates dtype.

        ``float`` for numerical coordinates and numpy ``datetime64`` for datetime coordinates.
        """

        raise NotImplementedError

    @property
    def deltatype(self):
        if self.dtype is np.datetime64:
            return np.timedelta64
        else:
            return self.dtype

    @property
    def is_monotonic(self):
        raise NotImplementedError

    @property
    def is_descending(self):
        raise NotImplementedError

    @property
    def is_uniform(self):
        raise NotImplementedError

    @property
    def start(self):
        raise NotImplementedError

    @property
    def stop(self):
        raise NotImplementedError

    @property
    def step(self):
        raise NotImplementedError

    @property
    def bounds(self):
        """ Low and high coordinate bounds. """

        raise NotImplementedError

    @property
    def properties(self):
        """:dict: Dictionary of the coordinate properties. """

        return {key: getattr(self, key) for key in self._properties}

    @property
    def definition(self):
        """:dict: Serializable 1d coordinates definition."""
        return self._get_definition(full=False)

    @property
    def full_definition(self):
        """:dict: Serializable 1d coordinates definition, containing all properties. For internal use."""
        return self._get_definition(full=True)

    def _get_definition(self, full=True):
        raise NotImplementedError

    @property
    def _full_properties(self):
        return {"name": self.name}

    # ------------------------------------------------------------------------------------------------------------------
    # Methods
    # ------------------------------------------------------------------------------------------------------------------

    def copy(self):
        """
        Make a deep copy of the 1d Coordinates.

        Returns
        -------
        :class:`Coordinates1d`
            Copy of the coordinates.
        """

        raise NotImplementedError

    def simplify(self):
        """ Get the simplified/optimized representation of these coordinates.

        Returns
        -------
        simplified : Coordinates1d
            simplified version of the coordinates
        """

        raise NotImplementedError

    def get_area_bounds(self, boundary):
        """
        Get low and high coordinate area bounds.

        Arguments
        ---------
        boundary : float, timedelta, array, None
            Boundary offsets in this dimension.
            
            * For a centered uniform boundary (same for every coordinate), use a single positive float or timedelta 
                offset. This represents the "total segment length" / 2.
            * For a uniform boundary (segment or polygon same for every coordinate), use an array of float or 
                timedelta offsets
            * For a fully specified boundary, use an array of boundary arrays (2-D array, N_coords x boundary spec), 
                 one per coordinate. The boundary_spec can be a single number, two numbers, or an array of numbers.
            * For point coordinates, use None.

        Returns
        -------
        low: float, np.datetime64
            low area bound
        high: float, np.datetime64
            high area bound
        """

        # point coordinates
        if boundary is None:
            return self.bounds

        # empty coordinates
        if self.size == 0:
            return self.bounds

        if np.array(boundary).ndim == 0:
            # shortcut for uniform centered boundary
            boundary = make_coord_delta(boundary)
            lo_offset = -boundary
            hi_offset = boundary
        elif np.array(boundary).ndim == 1:
            # uniform boundary polygon
            boundary = make_coord_delta_array(boundary)
            lo_offset = min(boundary)
            hi_offset = max(boundary)
        else:
            L, H = self.argbounds
            lo_offset = min(make_coord_delta_array(boundary[L]))
            hi_offset = max(make_coord_delta_array(boundary[H]))

        lo, hi = self.bounds
        lo = add_coord(lo, lo_offset)
        hi = add_coord(hi, hi_offset)

        return lo, hi

    def _select_empty(self, return_indices):
        I = []
        if return_indices:
            return self[I], I
        else:
            return self[I]

    def _select_full(self, return_indices):
        I = slice(None)
        if return_indices:
            return self[I], I
        else:
            return self[I]

    def select(self, bounds, return_indices=False, outer=False):
        """
        Get the coordinate values that are within the given bounds.

        The default selection returns coordinates that are within the bounds::

            In [1]: c = ArrayCoordinates1d([0, 1, 2, 3], name='lat')

            In [2]: c.select([1.5, 2.5]).coordinates
            Out[2]: array([2.])

        The *outer* selection returns the minimal set of coordinates that contain the bounds::
        
            In [3]: c.select([1.5, 2.5], outer=True).coordinates
            Out[3]: array([1., 2., 3.])

        The *outer* selection also returns a boundary coordinate if a bound is outside this coordinates bounds but
        *inside* its area bounds::
        
            In [4]: c.select([3.25, 3.35], outer=True).coordinates
            Out[4]: array([3.0], dtype=float64)

            In [5]: c.select([10.0, 11.0], outer=True).coordinates
            Out[5]: array([], dtype=float64)
        
        Parameters
        ----------
        bounds : (low, high) or dict
            Selection bounds. If a dictionary of dim -> (low, high) bounds is supplied, the bounds matching these
            coordinates will be selected if available, otherwise the full coordinates will be returned.
        outer : bool, optional
            If True, do an *outer* selection. Default False.
        return_indices : bool, optional
            If True, return slice or indices for the selection in addition to coordinates. Default False.

        Returns
        -------
        selection : :class:`Coordinates1d`
            Coordinates1d object with coordinates within the bounds.
        I : slice or list
            index or slice for the selected coordinates (only if return_indices=True)
        """

        # empty case
        if self.dtype is None:
            return self._select_empty(return_indices)

        if isinstance(bounds, dict):
            bounds = bounds.get(self.name)
            if bounds is None:
                return self._select_full(return_indices)

        bounds = make_coord_value(bounds[0]), make_coord_value(bounds[1])

        # check type
        if not isinstance(bounds[0], self.dtype):
            raise TypeError(
                "Input bounds do match the coordinates dtype (%s != %s)" % (type(self.bounds[0]), self.dtype)
            )
        if not isinstance(bounds[1], self.dtype):
            raise TypeError(
                "Input bounds do match the coordinates dtype (%s != %s)" % (type(self.bounds[1]), self.dtype)
            )

        my_bounds = self.bounds

        # If the bounds are of instance datetime64, then the comparison should happen at the lowest precision
        if self.dtype == np.datetime64:
            my_bounds, bounds = lower_precision_time_bounds(my_bounds, bounds, outer)

        # full
        if my_bounds[0] >= bounds[0] and my_bounds[1] <= bounds[1]:
            return self._select_full(return_indices)

        # none
        if my_bounds[0] > bounds[1] or my_bounds[1] < bounds[0]:
            return self._select_empty(return_indices)

        # partial, implemented in child classes
        return self._select(bounds, return_indices, outer)

    def _select(self, bounds, return_indices, outer):
        raise NotImplementedError

    def _transform(self, transformer):
        if self.name != "alt":
            # this assumes that the transformer does not have a spatial transform
            return self.copy()

        # transform "alt" coordinates
        from podpac.core.coordinates.array_coordinates1d import ArrayCoordinates1d

        _, _, tcoordinates = transformer.transform(np.zeros(self.size), np.zeros(self.size), self.coordinates)
        return ArrayCoordinates1d(tcoordinates, **self.properties)

    def issubset(self, other):
        """ Report whether other coordinates contains these coordinates.

        Arguments
        ---------
        other : Coordinates, Coordinates1d
            Other coordinates to check

        Returns
        -------
        issubset : bool
            True if these coordinates are a subset of the other coordinates.
        """

        from podpac.core.coordinates import Coordinates

        if isinstance(other, Coordinates):
            if self.name not in other.dims:
                return False
            other = other[self.name]

        # short-cuts that don't require checking coordinates
        if self.size == 0:
            return True

        if other.size == 0:
            return False

        if self.dtype != other.dtype:
            return False

        if self.bounds[0] < other.bounds[0] or self.bounds[1] > other.bounds[1]:
            return False

        # check actual coordinates using built-in set method issubset
        # for datetimes, convert to the higher resolution
        my_coordinates = self.coordinates
        other_coordinates = other.coordinates

        if self.dtype == np.datetime64:
            if my_coordinates[0].dtype < other_coordinates[0].dtype:
                my_coordinates = my_coordinates.astype(other_coordinates.dtype)
            elif other_coordinates[0].dtype < my_coordinates[0].dtype:
                other_coordinates = other_coordinates.astype(my_coordinates.dtype)

        return set(my_coordinates).issubset(other_coordinates.ravel())
