#!/usr/bin/env python
# -*- coding:utf-8 -*-

import numpy as np
from scipy import stats


def rankdata(arr, reverse = False):
    if reverse:
        arr = np.multiply(arr, -1)
    return stats.rankdata(arr, "ordinal").astype(int)


def dominance(r0, r1):
    N = len(r0)
    r0_lt_r1 = np.count_nonzero(np.less(r0, r1))
    if r0_lt_r1 > N - r0_lt_r1:
        return r0_lt_r1

    r1_lt_r0 = np.count_nonzero(np.less(r1, r0))
    if r1_lt_r0 > N - r1_lt_r0:
        return -r1_lt_r0

    return 0


def equality(r0, r1):
    return np.count_nonzero(np.equal(r0, r1))


def kendall_dominance(r0, r1):
    r0sum, r1sum = np.sum(r0), np.sum(r1)
    if r0sum < r1sum:
        return 0, (r0sum, r1sum)
    if r0sum > r1sum:
        return 1, (r0sum, r1sum)
    return None, (r0sum, r1sum)


def spearmanr(r0, r1):
    N = len(r0)
    num = 6.0 * np.sum(np.subtract(r0, r1) ** 2)
    denom = N * ((N ** 2) - 1)
    return 1 - (num / denom)
