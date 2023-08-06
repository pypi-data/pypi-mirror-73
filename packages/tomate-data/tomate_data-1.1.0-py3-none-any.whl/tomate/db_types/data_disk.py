"""Manage on-disk data."""

# This file is part of the 'tomate' project
# (http://github.com/Descanonge/tomate) and subject
# to the MIT License as defined in the file 'LICENSE',
# at the root of this project. © 2020 Clément HAËCK


import logging
import itertools
from typing import Any, Dict, List, Union, Tuple, Type

import numpy as np

from tomate.coordinates.coord import Coord
from tomate.custom_types import KeyLike, KeyLikeValue
from tomate.data_base import DataBase
from tomate.filegroup.filegroup_load import FilegroupLoad, do_post_loading
from tomate.filegroup.filegroup_scan import make_filegroup
from tomate.keys.keyring import Keyring
from tomate.scope import Scope
from tomate.variables_info import VariablesInfo


log = logging.getLogger(__name__)


class DataDisk(DataBase):
    """Added functionalities for on-disk data management.

    Scan metadata.
    Load data from disk.

    :param root: Root data directory containing all files.

    :attr root: str: Root data directory containing all files.
    :attr filegroups: List[FilegroupLoad]:
    :attr allow_advanced: bool: If allows advanced data arrangement.
    :attr post_loading_funcs: List[Tuple[Callable[DataBase]],
                                   KeyVar, bool, Dict[str, Any]]:
        Functions applied after loading data.
        Each element is a tuple of the function, the variable that triggers
        the call, a boolean True if all said variables must present to trigger,
        False if any variable must be loaded, and kwargs to pass.
    """
    def __init__(self, dims: List[Coord],
                 root: str, filegroups: List[FilegroupLoad],
                 vi: VariablesInfo = None):
        super().__init__(dims, vi)
        self.root = root

        self.filegroups = filegroups
        for fg in self.filegroups:
            fg.db = self

        self.allow_advanced = False

        self.post_loading_funcs = []

    def __repr__(self):
        s = [super().__repr__()]
        s.append("{} Filegroups:".format(len(self.filegroups)))
        s += ['\t{}'.format(', '.join(fg.variables)) for fg in self.filegroups]
        return '\n'.join(s)

    def add_filegroup(self, fg_type: Type,
                      coords_fg: List[Tuple[Union[str, Coord], Union[str, bool], str]],
                      name: str = '', root: str = None,
                      variables_shared: bool = False,
                      **kwargs: Any):
        """Add filegroup to database.

        See :func:`Constructor.add_filegroup
        <tomate.constructor.Contructor.add_filegroup>` for details.
        """
        fg = make_filegroup(fg_type, self.root, self.avail.dims,
                            coords_fg, self.vi, root, name,
                            variables_shared, **kwargs)
        fg.db = self
        self.filegroups.append(fg)

    def load(self, *keys: KeyLike, **kw_keys: KeyLike):
        """Load part of data from disk into memory.

        What variables, and what coordinates indices to load can be specified.
        Keys specified to subset data act on the available scope.
        If a dimensions is omitted or None, all available values are loaded.

        :param keys: [opt] What part of each dimension to load, in the
            order dimensions are stored. Can be integers, list of integers,
            slices, or None.
        :param kw_keys: [opt] What part of each dimension to load. Takes precedence
            over positional `keys`. Key for variables should be named 'var'.

        Examples
        --------
        Load everything available

        >>> db.load(None)

        Load first index of the first coordinate for the SST variable

        >>> db.load("SST", 0)

        Load everything for SST and Chla variables.

        >>> db.load(["SST", "Chla"], slice(None, None), None)

        Load time steps 0, 10, and 12 of all variables.

        >>> db.load(None, time=[0, 10, 12])

        Load first index of the first coordinate, and a slice of lat
        for the SST variable.

        >>> db.load("SST", 0, lat=slice(200, 400))
        """
        self.unload_data()

        kw_keys = self.get_kw_keys(*keys, **kw_keys)
        keyring = Keyring(**kw_keys)
        keyring.make_full(self.dims)
        keyring.make_total()
        keyring.make_int_list()
        keyring.make_var_idx(self.avail.var)
        keyring.sort_by(self.dims)

        self.loaded = self.get_subscope('avail', keyring)
        self.loaded.name = 'loaded'

        self.self_allocate(self.loaded.shape)

        loaded = any([fg.load_from_available(keyring)
                      for fg in self.filegroups])
        if not loaded:
            log.warning("Nothing loaded.")
        else:
            self.do_post_loading(keyring)

    def load_by_value(self, *keys: KeyLikeValue, by_day=False,
                      **kw_keys: KeyLikeValue):
        """Load part of data from disk into memory.

        Part of the data to load is specified by values or index.

        :param keys: [opt] Values to load for each dimension,
            in the order dimensions are stored.
            If is slice, use start and stop as boundaries.
            Step has no effect. If is float, int, or a list of,
            closest index for each value is taken. Act on loaded scope.
        :param by_day: If True, find indices prioritising dates.
            See :ref:`Some examples of coordinates subclasses` for details.
        :param kw_keys: [opt] Values to load for each dimension.
            Argument name is dimension name, argument value is similar to `keys`.
            Take precedence over `keys`. Argument name can also be a dimension
            name appended with `_idx`, in which case the selection is made by
            index instead. Value selection has priority.

        Examples
        --------
        Load latitudes from 10N to 30N.

        >>> db.load_by_value('SST', lat=slice(10., 30.))

        Load latitudes from 5N to maximum available.

        >>> db.load_by_value('SST', lat=slice(5, None))

        Load depth closest to 500 and first time index.

        >>> db.load_by_value(depth=500., time_idx=0)

        Load depths closest to 0, 10, 50

        >>> db.load_by_value(depth=[0, 10, 50])

        See also
        --------
        load
        """
        kw_keys = self.get_kw_keys(*keys, **kw_keys)
        scope = self.get_subscope_by_value('avail', int2list=True, by_day=by_day, **kw_keys)
        self.load_selected(scope=scope)

    def load_selected(self, keyring: Keyring = None,
                      scope: Union[str, Scope] = 'selected',
                      **keys: KeyLike):
        """Load data from a child scope of available.

        Subset is specified by a scope.
        The selection scope is expected to be created from
        the available one.

        :param keyring: [opt]
        :param scope: [opt] Selected scope created from available scope.
            Defaults to `self.selected`.
        :param keys: [opt]

        :raises KeyError: Selection scope is empty.
        :raises ValueError: Selection scope was not created from available.
        """
        scope = self.get_scope(scope)
        if scope.is_empty():
            raise KeyError(f"Selection scope is empty ('{scope.name}').")
        if scope.parent_scope != self.avail:
            raise ValueError("The parent scope is not the available data scope."
                             " (is '{}')".format(scope.parent_scope.name))

        scope_ = scope.copy()
        scope_.slice(int2list=False, keyring=keyring, **keys)
        self.load(**scope_.parent_keyring.kw)

    def do_post_loading(self, keyring: Keyring):
        """Apply post loading functions."""
        do_post_loading(keyring['var'], self, self.avail.var,
                        self.post_loading_funcs)

    def write(self, filename: str, wd: str = None,
              file_kw: Dict = None, var_kw: Dict[str, Dict] = None,
              **keys: KeyLike):
        """Write data and metadata to disk.

        If a variable to write is contained in multiple filegroups,
        only the first filegroup will be used to write this variable.

        Filegroups variables CoordScan should contain the variables to write,
        otherwise one can use filegroup.write() directly.

        :param filename: File to write in. Relative to each filegroup root
            directory, or from `wd` if specified.
        :param wd: [opt] Force to write `filename` in this directory instead
            of each filegroups root.
        :param file_kw: Keywords argument to pass to `open_file`.
        :param var_kw: Variables specific arguments.
        """
        keyring = Keyring(**keys)
        keyring.make_full(self.dims)
        keyring.make_total()
        variables = self.loaded.var.get_var_names(keyring['var'].value)
        if isinstance(variables, str):
            variables = [variables]

        for fg in self.filegroups:
            variables_fg = [v for v in variables
                            if v in fg.variables]
            for v in variables_fg:
                variables.remove(v)
            if variables_fg:
                keyring_fg = keyring.copy()
                keyring_fg['var'] = variables_fg
                fg.write(filename, wd, keyring=keyring_fg,
                         file_kw=file_kw, var_kw=var_kw)

    def write_add_variable(self, var: str, sibling: str,
                           kwargs: Dict = None, **keys: KeyLike):
        """Add variables to files.

        :param var: Variable to add. Must be in loaded scope.
        :param sibling: Variable along which to add the data.
            New variable will be added to the same files
            and in same order.
        :param keys: [opt] If a subpart of data is to be written.
            The selected data must match in shape that of the
            sibling data on disk.
        """
        scope = self.loaded.copy()
        scope.slice(var=sibling, **keys, int2list=False)
        for fg in self.filegroups:
            fg.write_add_variable(var, sibling, scope.parent_keyring,
                                  kwargs=kwargs)

    def scan_variables_attributes(self):
        """Scan variables specific attributes.

        Filegroups should be functionnal for this.
        """
        for fg in self.filegroups:
            if 'var' in fg.scan_attr:
                fg.scan_variables_attributes()

    def scan_files(self):
        """Scan files for metadata.

        :raises RuntimeError: If no filegroups in database.
        """
        if not self.filegroups:
            raise RuntimeError("No filegroups in database.")
        self.check_regex()
        self.check_scanning_functions()
        for fg in self.filegroups:
            fg.scan_files()

    def compile_scanned(self):
        """Compile metadata scanned.

        -Apply CoordScan selections.
        -Aggregate coordinate values from all filegroups.
        -If advanced data organization is not allowed, only keep
        intersection.
        -Apply coordinates values to available scope.
        """
        if len(self.filegroups) == 1:
            fg = self.filegroups[0]
            fg.apply_coord_selection()
            values = {d: fg.cs[d][:] for d in self.dims}
            self._apply_coord_values(values)
            for d in self.dims:
                fg.cs[d].contains = np.arange(fg.cs[d].size)
        else:
            for fg in self.filegroups:
                fg.apply_coord_selection()
            values = self._get_coord_values()
            self._find_contained(values)

            if not self.allow_advanced:
                self._get_intersection(values)
                self._find_contained(values)

            self.check_duplicates()
            self._apply_coord_values(values)

    def _find_contained(self, values):
        for fg in self.filegroups:
            for dim, value in values.items():
                fg.cs[dim].find_contained(value)

    def _get_coord_values(self) -> Dict[str, np.ndarray]:
        """Aggregate all available coordinate values.

        :returns: Values for each dimension.
        :raises ValueError: No values found for a variable.
        """
        values_c = {}
        for c in self.dims:
            values = []
            for fg in self.filegroups:
                if fg.cs[c].size is not None:
                    values += list(fg.cs[c][:])

            values = np.array(values)

            if values.size == 0:
                raise ValueError(f"No values found for {c} in any filegroup.")

            if c != 'var':
                values.sort()
                threshold = max([fg.cs[c].float_comparison
                                 for fg in self.filegroups])
                duplicates = np.abs(np.diff(values)) < threshold
                if np.any(duplicates):
                    log.debug("Removing duplicates in available '%s' values"
                              " using float threshold %s", c, threshold)
                values = np.delete(values, np.where(duplicates))

            values_c[c] = values
        return values_c

    def _get_intersection(self, values: Dict[str, np.ndarray]):
        """Get intersection of coordinate values.

        Only keep coordinates values common to all filegroups.
        The variables dimensions is excluded from this.
        Slice CoordScan and `contains` accordingly.

        :param values: All values available for each dimension.
            Modified in place to only values common
            accross filegroups.
        """
        for dim in self.coords:
            none = np.zeros(values[dim].size, bool)
            for fg in self.filegroups:
                none ^= np.equal(fg.contains[dim], None)
            if np.any(none):
                values[dim] = np.delete(values[dim], np.where(none))
                sel = np.where(~none)[0]
                for fg in self.filegroups:
                    cs = fg.cs[dim]
                    size, extent = cs.size, cs.get_extent_str()
                    if cs.slice_from_avail(sel):
                        log.warning("'%s' in '%s' will be cut: found %d values ranging %s",
                                    dim, fg.name, size, extent)
                        if cs.size == 0:
                            raise IndexError(f"No common values for '{dim}'")

                cs = self.filegroups[0].cs[dim]
                log.warning("Common values taken for '%s', %d values ranging %s.",
                            dim, cs.size, cs.get_extent_str())

    def _apply_coord_values(self, values: Dict[str, np.ndarray]):
        """Set found values to master coordinates."""
        for dim, val in values.items():
            self.avail.dims[dim].update_values(val)

    def check_duplicates(self):
        """Check for duplicate data points.

        ie if a same data point (according to coordinate values)
        can be found in two filegroups.

        :raises ValueError: If there is a duplicate.
        """
        for fg1, fg2 in itertools.combinations(self.filegroups, 2):
            intersect = []
            for c1, c2 in zip(fg1.contains.values(), fg2.contains.values()):
                w1 = np.where(~np.equal(c1, None))[0]
                w2 = np.where(~np.equal(c2, None))[0]
                intersect.append(np.intersect1d(w1, w2).size)
            if all(s > 0 for s in intersect):
                raise ValueError("Duplicate values in filegroups {} and {}"
                                 .format(fg1.name, fg2.name))

    def check_regex(self):
        """Check if a pregex has been added where needed.

        :raises RuntimeError: If regex is empty and there is at
            least one shared coordinate.
        """
        for fg in self.filegroups:
            coords = list(fg.iter_shared(True))
            if len(coords) > 0 and fg.regex == '':
                raise RuntimeError(f"Filegroup '{fg.name}' is missing a regex.")

    def check_scanning_functions(self):
        """Check if CoordScan have scanning functions set."""
        for fg in self.filegroups:
            for name, cs in fg.cs.items():
                if cs.shared and not cs.is_to_scan():
                    raise KeyError(f"'{name}' (in filegroup '{fg.name}') is shared"
                                   " but has not scanning function set.")
                if not cs.shared and not cs.scan:
                    log.warning("'%s' (in filegroup '%s') has no scanning function set"
                                " and was not given values manually",
                                name, fg.name)
