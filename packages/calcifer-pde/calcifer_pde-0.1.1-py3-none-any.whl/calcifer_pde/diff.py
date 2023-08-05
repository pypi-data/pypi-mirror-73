""" diferentiation routines """

import numpy as np

__all__ = ["diff_first_dim", "diff_scnd_dim"]


def diff_first_dim(array_):
    """ compute differentiation on the first dimension
    FIRST ORDER"""
    out = np.zeros_like(array_)
    # pylint: disable=unsubscriptable-object
    size_i = out.shape[0]

    out[range(1, size_i), :] = (
        array_[range(1, size_i), :]
        - array_[range(0, size_i - 1), :])

    out[0, :] = (array_[1, :] - array_[0, :])
    return out


def diff_scnd_dim(array_):
    """ compute differentiation on the second dimension.
    FIRST ORDER"""
    out = np.zeros_like(array_)
    # pylint: disable=unsubscriptable-object
    size_j = out.shape[1]

    out[:, range(1, size_j)] = (
        array_[:, range(1, size_j)]
        - array_[:, range(0, size_j - 1)])
    out[:, 0] = (array_[:, 1] - array_[:, 0])
    return out

