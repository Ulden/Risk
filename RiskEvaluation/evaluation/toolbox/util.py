#!/usr/bin/env python
# -*- coding:utf-8 -*-

import numpy as np

MIN = -1
MAX = 1


def criteriarr(criteria):
    criteria = np.asarray(criteria)
    if np.setdiff1d(criteria, [MIN, MAX]):
        msg = "Criteria Array only accept '{}' or '{}' Values. Found {}"
        raise ValueError(msg.format(MAX, MIN, criteria))
    return criteria


def is_mtx(mtx, size = None):
    try:
        a, b = mtx.shape
        if size and (a, b) != size:
            return False
    except:
        return False
    return True


def nearest(array, value, side = None):
    if side not in (None, "gt", "lt"):
        msg = "'side' must be None, 'gt' or 'lt'. Found {}".format(side)
        raise ValueError(msg)

    raveled = np.ravel(array)
    cleaned = raveled[~np.isnan(raveled)]

    if side is None:
        idx = np.argmin(np.abs(cleaned - value))

    else:
        masker, decisor = ((np.ma.less_equal, np.argmin) if side == "gt" else
        (np.ma.greater_equal, np.argmax))

        diff = cleaned - value
        mask = masker(diff, 0)
        if np.all(mask):
            return None

        masked_diff = np.ma.masked_array(diff, mask)
        idx = decisor(masked_diff)

    return cleaned[idx]
