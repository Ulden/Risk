#!/usr/bin/env python
# -*- coding:utf-8 -*-

import numpy as np
from numpy import linalg

def sum(arr, axis = None):
    colsum = np.sum(arr, axis = axis, keepdims = True)
    return np.divide(arr, colsum, dtype = np.float64)

def max(arr,axis = None):
    colmax = np.max(arr, axis = axis, keepdims = True)
    return np.divide(arr, colmax, dtype = np.float64)


def vector(arr, axis = None):
    frob = linalg.norm(arr, None, axis = axis)
    return np.divide(arr, frob, dtype = np.float64)


def push_negatives(arr, axis = None):
    mins = np.min(arr, axis = axis, keepdims = True)
    delta = (mins < 0) * mins
    return np.subtract(arr, delta)


def eps(arr, axis = None):
    eps = 0
    arr = np.asarray(arr)
    if np.any(arr == 0):
        if issubclass(arr.dtype.type, (np.inexact, float)):
            eps = np.finfo(arr.dtype.type).eps
        else:
            eps = np.finfo(np.float).eps
    return arr + eps