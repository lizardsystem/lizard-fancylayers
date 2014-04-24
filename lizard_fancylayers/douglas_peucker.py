#------------------------------------------------------------------------------
# Copyright (c) 2005, Enthought, Inc.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
#
# Author: Enthought, Inc.
# Description: <Enthought util package component>
#
# Changed by ejnens: added decimate_until, fixed decimate recusion causing a
# stack overflow, properly use numpy bool arrays
#------------------------------------------------------------------------------

from collections import deque
import logging

import numpy as np
from numpy import sqrt, argmax, zeros, absolute

MAX_FLOT_POINTS = 1000

logger = logging.getLogger(__name__)


def decimate_until(x, y, tolerance, max_values=1200, max_steps=35,
                   step_factor=8.0):
    if len(x) <= max_values:
        # nothing to do
        return x, y
    for step in range(max_steps):
        logger.debug('decimate_until: step %s', step)
        # operate on a copy, so the errors don't accumulate
        x2 = x.copy()
        y2 = y.copy()
        x2, y2 = decimate(x2, y2)
        if len(x2) > max_values:
            tolerance *= step_factor
        else:
            break
    return x2, y2


def decimate(datetimes, values):
    """ Returns decimated x and y arrays.

    This is Douglas and Peucker's algorithm rewritten to use Numeric arrays.
    Tolerance is usually determined by determining the size that a single pixel
    represents in the units of x and y.

    Compression ratios for large seismic and well data sets can be significant.

    """

    # Todo - we could improve the aesthetics by scaling (normalizing) the x and
    # y arrays. eg in a well the curve varies by +/- 1 and the depths by
    # 0,10000. This affects the accuracy of the representation in sloping
    # regions.
    #import pdb;pdb.set_trace()
    x = datetimes.astype(np.int64)
    lowest_time = x.min()
    np.subtract(x, lowest_time, x)
    hres = (x.max() - x.min()) / float(MAX_FLOT_POINTS)
    vres = (values.max() - values.min()) / float(MAX_FLOT_POINTS)
    tolerance = vres
    logger.debug("Hres: %s   vres: %s", hres, vres)
    np.multiply(x, hres/vres, x)
    y = values
    logger.debug("Horizontal min/max: %s   %s", x.min(), x.max())
    logger.debug("Vertical min/max: %s   %s", y.min(), y.max())
    logger.debug("Tolerance: %s", tolerance)

    keep = zeros(len(x), dtype=np.bool)
    segments = deque([(0, len(x) - 1)])
    while segments:
        si, ei = segments.pop()
        keep[si] = True
        keep[ei] = True

        # check if the two data points are adjacent
        if ei < (si + 2):
            continue

        # now find the perpendicular distance to each point
        x0 = x[si+1:ei]
        y0 = y[si+1:ei]

        xei_minux_xsi = x[ei] - x[si]
        yei_minux_ysi = y[ei] - y[si]

        top = absolute(xei_minux_xsi * (y[si] - y0) - (x[si] - x0) *
                       yei_minux_ysi)

        # The algorithm currently does an expensive sqrt operation which is not
        # strictly necessary except that it makes the tolerance correspond to
        # a real world quantity.
        bot = sqrt(xei_minux_xsi*xei_minux_xsi + yei_minux_ysi*yei_minux_ysi)
        dist = top / bot

        # find the point that is furthest from line between points si and ei
        index = argmax(dist)

        if dist[index] > tolerance:
            abs_index = index + (si + 1)
            segments.append((si, abs_index))
            segments.append((abs_index, ei))

    return datetimes[keep], y[keep]


def simplify(timeseries):
    """Simplify a timeseries (i.e. reduce the number of events).

    Apply the Ramer-Douglas-Peucker algorithm to reduce the number of events,
    without loosing the main characteristics of the timeseries.

    Rationale: most JavaScript libraries cannot swallow huge timeseries.

    Return a tuple of dates and values lists.
    """

    timestamps = timeseries.keys()
    values = timeseries.values

    if values.size <= MAX_FLOT_POINTS:
        logger.debug("Max %s points, found %s. That's OK.",
                     MAX_FLOT_POINTS, values.size)
        return list(timestamps), list(values)

    # Filter out NaN values until the algorithm can handle them.
    an = np.invert(np.isnan(values))
    timestamps = timestamps[an]
    values = values[an]

    logger.debug("Before line simplification: %s points", timestamps.size)
    timestamps, values = decimate(timestamps, values)
    logger.debug("After line simplification: %s points", timestamps.size)

    timestamps = timestamps.tolist()
    values = values.tolist()
    return timestamps, values
