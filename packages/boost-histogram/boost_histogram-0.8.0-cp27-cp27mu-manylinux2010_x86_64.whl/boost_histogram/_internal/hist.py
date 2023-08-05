# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from .kwargs import KWArgs

from .. import _core
from .view import _to_view
from .axis import Axis
from .axistuple import AxesTuple
from .sig_tools import inject_signature
from .storage import Double, Storage
from .utils import cast, register, set_family, MAIN_FAMILY, CPP_FAMILY, set_module
from .six import string_types

import warnings
import copy
import numpy as np

import os
import threading

_histograms = (
    _core.hist.any_double,
    _core.hist.any_int64,
    _core.hist.any_atomic_int64,
    _core.hist.any_unlimited,
    _core.hist.any_weight,
    _core.hist.any_mean,
    _core.hist.any_weighted_mean,
)


def _fill_cast(value):
    """
    Convert to NumPy arrays. Some buffer objects do not get converted by forcecast.
    """
    if isinstance(value, string_types + (bytes,)) or not hasattr(value, "__iter__"):
        return value
    else:
        return np.ascontiguousarray(value)


def _hist_or_val(other):
    return other._hist if hasattr(other, "_hist") else other


def _arg_shortcut(item):
    msg = "Developer shortcut: will be removed in a future version"
    if isinstance(item, tuple) and len(item) == 3:
        warnings.warn(msg, FutureWarning)
        return _core.axis.regular_uoflow(item[0], item[1], item[2], None)
    elif isinstance(item, tuple) and len(item) == 4:
        warnings.warn(msg, FutureWarning)
        return _core.axis.regular_uoflow(*item)
    elif isinstance(item, Axis):
        return item._ax
    else:
        raise TypeError("Only axes supported in histogram constructor")
        # TODO: Currently segfaults if we pass in a non-axis to the C++ code
        # Using the public interface above, this should never be possible.


def _expand_ellipsis(indexes, rank):
    indexes = list(indexes)
    number_ellipses = indexes.count(Ellipsis)
    if number_ellipses == 0:
        return indexes
    elif number_ellipses == 1:
        index = indexes.index(Ellipsis)
        additional = rank + 1 - len(indexes)
        if additional < 0:
            raise IndexError("too many indices for histogram")

        # Fill out the ellipsis with empty slices
        return indexes[:index] + [slice(None)] * additional + indexes[index + 1 :]

    else:
        raise IndexError("an index can only have a single ellipsis ('...')")


# We currently do not cast *to* a histogram, but this is consistent
# and could be used later.
@register(_histograms)
class BaseHistogram(object):
    @inject_signature("self, *axes, storage=Double()", locals={"Double": Double})
    def __init__(self, *axes, **kwargs):
        """
        Construct a new histogram.

        If you pass in a single argument, this will be treated as a
        histogram and this will convert the histogram to this type of
        histogram (DensityHistogram, Histogram, BoostHistogram).

        Parameters
        ----------
        *args : Axis
            Provide 1 or more axis instances.
        storage : Storage = bh.storage.Double()
            Select a storage to use in the histogram
        """

        # Allow construction from a raw histogram object (internal)
        if not kwargs and len(axes) == 1 and isinstance(axes[0], _histograms):
            self._hist = axes[0]
            return

        if not kwargs and len(axes) == 1 and isinstance(axes[0], BaseHistogram):
            self._hist = copy.copy(axes[0]._hist)
            return

        # Keyword only trick (change when Python2 is dropped)
        with KWArgs(kwargs) as k:
            storage = k.optional("storage", Double())

        # Check for missed parenthesis or incorrect types
        if not isinstance(storage, Storage):
            if issubclass(storage, Storage):
                raise KeyError(
                    "Passing in an initialized storage has been removed. Please add ()."
                )
            else:
                raise KeyError("Only storages allowed in storage argument")

        # Allow a tuple to represent a regular axis
        axes = tuple(_arg_shortcut(arg) for arg in axes)

        if len(axes) > _core.hist._axes_limit:
            raise IndexError(
                "Too many axes, must be less than {}".format(_core.hist._axes_limit)
            )

        # Check all available histograms, and if the storage matches, return that one
        for h in _histograms:
            if isinstance(storage, h._storage_type):
                self._hist = h(axes, storage)
                return

        raise TypeError("Unsupported storage")

    def view(self, flow=False):
        """
        Return a view into the data, optionally with overflow turned on.
        """
        return _to_view(self._hist.view(flow))

    def __array__(self):
        return self.view(False)

    def __add__(self, other):
        return self.__class__(self._hist.__add__(other._hist))

    def __iadd__(self, other):
        self._hist.__iadd__(other._hist)
        self.axes = AxesTuple(self._axis(i) for i in range(self.ndim))
        return self

    def __eq__(self, other):
        return self._hist == other._hist

    def __ne__(self, other):
        return self._hist != other._hist

    # If these fail, the underlying object throws the correct error
    def __mul__(self, other):
        return self.__class__(self._hist.__mul__(other))

    def __rmul__(self, other):
        return self * other

    def __imul__(self, other):
        self._hist.__imul__(_hist_or_val(other))
        return self

    def __truediv__(self, other):
        if isinstance(other, BaseHistogram):
            result = self.copy()
            result.__itruediv__(other)
            return result
        else:
            return self.__class__(self._hist.__truediv__(_hist_or_val(other)))

    def __div__(self, other):
        if isinstance(other, BaseHistogram):
            result = self.copy()
            result.__idiv__(other)
            return result
        else:
            return self.__class__(self._hist.__div__(_hist_or_val(other)))

    def __itruediv__(self, other):
        if isinstance(other, BaseHistogram):
            view = self.view(flow=True)
            view.__itruediv__(other.view(flow=True))
        else:
            self._hist.__itruediv__(_hist_or_val(other))
        return self

    def __idiv__(self, other):
        if isinstance(other, BaseHistogram):
            view = self.view(flow=True)
            view.__idiv__(other.view(flow=True))
        else:
            self._hist.__idiv__(_hist_or_val(other))
        return self

    def __copy__(self):
        other = self.__class__.__new__(self.__class__)
        other._hist = copy.copy(self._hist)
        return other

    # TODO: Marked as too complex by flake8. Should be factored out a bit.
    @inject_signature("self, *args, weight=None, sample=None, threads=None")
    def fill(self, *args, **kwargs):  # noqa: C901
        """
        Insert data into the histogram.

        Parameters
        ----------
        *args : Union[Array[float], Array[int], Array[str], float, int, str]
            Provide one value or array per dimension.
        weight : List[Union[Array[float], Array[int], Array[str], float, int, str]]]
            Provide weights (only if the histogram storage supports it)
        sample : List[Union[Array[float], Array[int], Array[str], float, int, str]]]
            Provide samples (only if the histogram storage supports it)
        threads : Optional[int]
            Fill with threads. Defaults to None, which does not activate
            threaded filling.  Using 0 will automatically pick the number of
            available threads (usually two per core).
        """

        # Convert to NumPy arrays
        args = (_fill_cast(a) for a in args)

        threads = kwargs.pop("threads", None)

        if threads is None or threads == 1:
            self._hist.fill(*args, **kwargs)
        else:
            if threads == 0:
                threads = os.cpu_count()

            if (
                self._hist._storage_type is _core.storage.mean
                or self._hist._storage_type is _core.storage.weighted_mean
            ):
                raise RuntimeError("Mean histograms do not support threaded filling")

            weight = kwargs.pop("weight", None)
            sample = kwargs.pop("sample", None)

            data = [np.array_split(a, threads) for a in args]

            if weight is None or np.isscalar(weight):
                weights = [weight] * threads
            else:
                weights = np.array_split(weight, threads)

            if sample is None or np.isscalar(sample):
                samples = [sample] * threads
            else:
                samples = np.array_split(sample, threads)

            if self._hist._storage_type is _core.storage.atomic_int64:

                def fun(weight, sample, *args):
                    self._hist.fill(*args, weight=weight, sample=sample)

            else:
                sum_lock = threading.Lock()

                def fun(weight, sample, *args):
                    local_hist = self._hist.__copy__()
                    local_hist.reset()
                    kw = {}
                    if weight is not None:
                        kw["weight"] = weight
                    if sample is not None:
                        kw["sample"] = sample
                    local_hist.fill(*args, **kw)
                    with sum_lock:
                        self._hist += local_hist

            thread_list = [
                threading.Thread(target=fun, args=arrays)
                for arrays in zip(weights, samples, *data)
            ]

            for thread in thread_list:
                thread.start()

            for thread in thread_list:
                thread.join()

        return self

    def __repr__(self):
        ret = "{self.__class__.__name__}(\n  ".format(self=self)
        ret += ",\n  ".join(repr(self._axis(i)) for i in range(self._hist.rank()))
        ret += ",\n  storage={0}".format(self._storage_type())
        ret += ")"
        outer = self._hist.sum(flow=True)
        if outer:
            inner = self._hist.sum(flow=False)
            ret += " # Sum: {0}".format(inner)
            if inner != outer:
                ret += " ({0} with flow)".format(outer)
        return ret

    def __str__(self):
        """
        A rendering of the histogram is made using ASCII or unicode characters
        (whatever is supported by the terminal). What exactly is displayed is
        still experimental. Do not rely on any particular rendering.
        """
        # TODO check the terminal width and adjust the presentation
        # only use for 1D, fall back to repr for ND
        if self._hist.rank() == 1:
            s = str(self._hist)
            # get rid of first line and last character
            s = s[s.index("\n") + 1 : -1]
        else:
            s = repr(self)
        return s

    def _axis(self, i=0):
        """
        Get N-th axis.
        """
        return cast(self, self._hist.axis(i), Axis)

    @property
    def _storage_type(self):
        return cast(self, self._hist._storage_type, Storage)

    def _reduce(self, *args):
        return self.__class__(self._hist.reduce(*args))


# C++ version of histogram
@set_family(CPP_FAMILY)
@set_module("boost_histogram.cpp")
class histogram(BaseHistogram):
    axis = BaseHistogram._axis

    def rank(self):
        """
        Number of axes (dimensions) of histogram.
        """
        return self._hist.rank()

    def size(self):
        """
        Total number of bins in the histogram (including underflow/overflow).
        """
        return self._hist.size()

    def at(self, *indexes):
        """
        Select a contents given indices. -1 is the underflow bin, N is the overflow bin.
        """
        return self._hist.at(*indexes)

    # Call uses fill since it supports strings,
    # runtime argument list, etc.
    @inject_signature("self, *args, weight=None, sample=None")
    def __call__(self, *args, **kwargs):
        args_gen = (((a,) if isinstance(a, str) else a) for a in args)
        self._hist.fill(*args_gen, **kwargs)
        return self

    def _reset(self):
        self._hist.reset()
        return self

    def _empty(self, flow=False):
        return self._hist.empty(flow)

    def _sum(self, flow=False):
        return self._hist.sum(flow)

    def _project(self, *args):
        return self.__class__(self._hist.project(*args))


@set_family(MAIN_FAMILY)
@set_module("boost_histogram")
class Histogram(BaseHistogram):
    @inject_signature("self, *axes, storage=Double()", locals={"Double": Double})
    def __init__(self, *args, **kwargs):
        super(Histogram, self).__init__(*args, **kwargs)

        # If this is a property, tab completion in IPython does not work
        self.axes = AxesTuple(self._axis(i) for i in range(self.ndim))

    __init__.__doc__ = BaseHistogram.__init__.__doc__

    def __copy__(self):
        other = super(Histogram, self).__copy__()
        other.axes = AxesTuple(other._axis(i) for i in range(other.ndim))
        return other

    def __deepcopy__(self, memo):
        other = self.__class__.__new__(self.__class__)
        other._hist = copy.deepcopy(self._hist, memo)
        other.axes = AxesTuple(other._axis(i) for i in range(other.ndim))
        return other

    def __getstate__(self):
        state = self.__dict__.copy()
        del state["axes"]  # Don't save the cashe
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.axes = AxesTuple(self._axis(i) for i in range(self.ndim))

    def __repr__(self):
        newline = "\n  "
        sep = "," if len(self.axes) > 0 else ""
        ret = "{self.__class__.__name__}({newline}".format(
            self=self, newline=newline if len(self.axes) > 1 else ""
        )
        ret += ",{newline}".format(newline=newline).join(repr(ax) for ax in self.axes)
        ret += "{comma}{newline}storage={storage}".format(
            storage=self._storage_type(),
            newline=newline
            if len(self.axes) > 1
            else " "
            if len(self.axes) > 0
            else "",
            comma=sep,
        )
        ret += ")"
        outer = self.sum(flow=True)
        if outer:
            inner = self.sum(flow=False)
            ret += " # Sum: {0}".format(inner)
            if inner != outer:
                ret += " ({0} with flow)".format(outer)
        return ret

    def _compute_commonindex(self, index):
        """
        Takes indices and returns two iterables; one is a tuple or dict of the
        original, Ellipsis expanded index, and the other returns index,
        operation value pairs.
        """
        # Shorten the computations with direct access to raw object
        hist = self._hist

        # Support dict access
        if hasattr(index, "items"):
            indexes = [slice(None)] * hist.rank()
            for k, v in index.items():
                indexes[k] = v

        # Normalize -> h[i] == h[i,]
        else:
            if not isinstance(index, tuple):
                index = (index,)
            # Now a list
            indexes = _expand_ellipsis(index, hist.rank())

        if len(indexes) != hist.rank():
            raise IndexError("Wrong number of indices for histogram")

        # Allow [bh.loc(...)] to work
        for i in range(len(indexes)):
            if callable(indexes[i]):
                indexes[i] = indexes[i](self.axes[i])
            elif hasattr(indexes[i], "flow"):
                if indexes[i].flow == 1:
                    indexes[i] = hist.axis(i).size
                elif indexes[i].flow == -1:
                    indexes[i] = -1
            elif isinstance(indexes[i], int):
                if abs(indexes[i]) >= hist.axis(i).size:
                    raise IndexError("histogram index is out of range")
                indexes[i] %= hist.axis(i).size

        return indexes

    def to_numpy(self, flow=False):
        """
        Convert to a Numpy style tuple of return arrays.

        Return
        ------
        contents : Array[Any]
            The bin contents
        *edges : Array[float]
            The edges for each dimension
        """
        return self._hist.to_numpy(flow)

    @inject_signature("self, *, deep=True")
    def copy(self, **kwargs):
        """
        Make a copy of the histogram. Defaults to making a
        deep copy (axis metadata copied); use deep=False
        to avoid making a copy of axis metadata.
        """

        # Future versions may add new options here
        with KWArgs(kwargs) as k:
            deep = k.optional("deep", True)

        if deep:
            return copy.deepcopy(self)
        else:
            return copy.copy(self)

    def reset(self):
        """
        Reset bin counters to default values.
        """
        self._hist.reset()
        return self

    def empty(self, flow=False):
        """
        Check to see if the histogram has any non-default values.
        You can use flow=True to check flow bins too.
        """
        return self._hist.empty(flow)

    def sum(self, flow=False):
        """
        Compute the sum over the histogram bins (optionally including the flow bins).
        """
        return self._hist.sum(flow)

    @property
    def rank(self):
        """
        Number of axes (dimensions) of histogram. DEPRECATED, use ndim.
        """
        msg = "Use .ndim instead"
        warnings.warn(msg, FutureWarning)
        return self._hist.rank()

    @property
    def ndim(self):
        """
        Number of axes (dimensions) of histogram.
        """
        return self._hist.rank()

    @property
    def size(self):
        """
        Total number of bins in the histogram (including underflow/overflow).
        """
        return self._hist.size()

    @property
    def shape(self):
        """
        Tuple of axis sizes (not including underflow/overflow).
        """
        return self.axes.size

    # TODO: Marked as too complex by flake8. Should be factored out a bit.
    def __getitem__(self, index):  # noqa: C901

        indexes = self._compute_commonindex(index)

        # If this is (now) all integers, return the bin contents
        # But don't try *dict!
        if not hasattr(indexes, "items"):
            try:
                return self._hist.at(*indexes)
            except RuntimeError:
                pass

        integrations = set()
        slices = []

        # Compute needed slices and projections
        for i, ind in enumerate(indexes):
            if hasattr(ind, "__index__"):
                ind = slice(ind.__index__(), ind.__index__() + 1, sum)

            elif not isinstance(ind, slice):
                raise IndexError(
                    "Must be a slice, an integer, or follow the locator protocol."
                )
            start, stop = self.axes[i]._process_loc(ind.start, ind.stop)

            if ind != slice(None):
                merge = 1
                if ind.step is not None:
                    if hasattr(ind.step, "factor"):
                        merge = ind.step.factor
                    elif callable(ind.step):
                        if ind.step is sum:
                            integrations.add(i)
                        else:
                            raise RuntimeError("Full UHI not supported yet")

                        if ind.start is not None or ind.stop is not None:
                            slices.append(
                                _core.algorithm.slice(
                                    i, start, stop, _core.algorithm.slice_mode.crop
                                )
                            )
                        continue
                    else:
                        raise IndexError(
                            "The third argument to a slice must be rebin or projection"
                        )

                slices.append(_core.algorithm.slice_and_rebin(i, start, stop, merge))

        reduced = self._hist.reduce(*slices)

        if not integrations:
            return self.__class__(reduced)
        else:
            projections = [i for i in range(self.ndim) if i not in integrations]

            return (
                self.__class__(reduced.project(*projections))
                if projections
                else reduced.sum(flow=True)
            )

    def __setitem__(self, index, value):
        """
        There are several supported possibilities:

            h[slice] = array # same size

        If an array is given to a compatible slice, it is set.

            h[a:] = array # One larger

        If an array is given that does not match, if it does match the
        with-overflow size, it fills that.

        PLANNED (not yet supported):

            h[a:] = h2

        If another histogram is given, that must either match with or without
        overflow, where the overflow bins must be overflow bins (that is,
        you cannot set a histogram's flow bins from another histogram that
        is 2 larger). Bin edges must be a close match, as well. If you don't
        want this level of type safety, just use ``h[...] = h2.view()``.
        """
        indexes = self._compute_commonindex(index)

        if isinstance(value, BaseHistogram):
            raise TypeError("Not supported yet")

        value = np.asarray(value)
        view = self.view(flow=True)

        # Shortcut: allow raw arrays for WeightedSum
        weighted_dtype = np.dtype([("value", "<f8"), ("variance", "<f8")])
        if (
            view.dtype == weighted_dtype != value.dtype
            and len(value.dtype) != 2
            and value.ndim > 0
            and value.shape[-1] == 2
        ):
            value = value.astype(np.double).view(weighted_dtype)[..., 0]
        # Disallow mismatched data types
        elif len(value.dtype) != len(view.dtype):
            raise ValueError("Mismatched data types; matching types required")

        # Numpy does not broadcast partial slices, but we would need
        # to allow it (because we do allow broadcasting up dimensions)
        # Instead, we simply require matching dimensions.
        if value.ndim > 0 and value.ndim != sum(isinstance(i, slice) for i in indexes):
            raise ValueError(
                "Setting a {0}D histogram with a {1}D array must have a matching number of dimensions".format(
                    len(indexes), value.ndim
                )
            )

        # Here, value_n does not increment with n if this is not a slice
        value_n = 0
        for n, request in enumerate(indexes):
            has_underflow = self.axes[n].options.underflow
            has_overflow = self.axes[n].options.overflow

            if isinstance(request, slice):
                # Only consider underflow/overflow if the endpoints are not given
                use_underflow = has_underflow and request.start is None
                use_overflow = has_overflow and request.stop is None

                # Make the limits explicit since we may need to shift them
                start = 0 if request.start is None else request.start
                stop = len(self.axes[n]) if request.stop is None else request.stop
                request_len = stop - start

                # If set to a scalar, then treat it like broadcasting without flow bins
                if value.ndim == 0:
                    start = 0 + has_overflow
                    stop = len(self.axes[n]) + has_underflow

                # Normal setting
                elif request_len == value.shape[value_n]:
                    start += has_underflow
                    stop += has_underflow

                # Expanded setting
                elif request_len + use_underflow + use_overflow == value.shape[value_n]:
                    start += has_underflow and not use_underflow
                    stop += has_underflow + (has_overflow and use_overflow)

                # Single element broadcasting
                elif value.shape[value_n] == 1:
                    start += has_underflow
                    stop += has_underflow

                else:
                    msg = "Mismatched shapes in dimension {0}".format(n)
                    msg += ", {0} != {1}".format(value.shape[n], request_len)
                    if use_underflow or use_overflow:
                        msg += " or {0}".format(
                            request_len + use_underflow + use_overflow
                        )
                    raise ValueError(msg)
                indexes[n] = slice(start, stop, request.step)
                value_n += 1
            else:
                indexes[n] = request + has_underflow

        view[tuple(indexes)] = value

    def project(self, *args):
        """
        Project to a single axis or several axes on a multidiminsional histogram.
        Provided a list of axis numbers, this will produce the histogram over
        those axes only. Flow bins are used if available.
        """

        return self.__class__(self._hist.project(*args))
