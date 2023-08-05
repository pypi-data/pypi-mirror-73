# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from .._core.algorithm import (
    shrink_and_rebin,
    crop_and_rebin,
    slice_and_rebin,
    rebin,
    shrink,
    crop,
    slice,
    slice_mode,
)

del absolute_import, division, print_function

__all__ = (
    "shrink_and_rebin",
    "crop_and_rebin",
    "slice_and_rebin",
    "rebin",
    "shrink",
    "crop",
    "slice",
    "slice_mode",
    "sum",
    "reduce",
    "empty",
    "reduce",
    "project",
)


shrink_and_rebin.__module__ = "boost_histogram.cpp"
crop_and_rebin.__module__ = "boost_histogram.cpp"
slice_and_rebin.__module__ = "boost_histogram.cpp"
rebin.__module__ = "boost_histogram.cpp"
shrink.__module__ = "boost_histogram.cpp"
crop.__module__ = "boost_histogram.cpp"
slice.__module__ = "boost_histogram.cpp"


def sum(histogram, flow=True):
    """\
    Sum a histogram, optionally without flow bins. The default matches the C++
    default of all bins included in the sum.
    """
    return histogram._sum(flow)


def reduce(histogram, *args):
    "Reduce a histogram with 1 or more reduce options"
    return histogram._reduce(*args)


def empty(histogram, flow=False):
    """Check to see if a histogram is empty, optionally with flow bins"""
    return histogram._empty(flow)


def project(histogram, *args):
    """
    Project to a single axis or several axes on a multidiminsional histogram.
    Provided a list of axis numbers, this will produce the histogram over those
    axes only. Flow bins are used if available.
    """
    return histogram._project(*args)
