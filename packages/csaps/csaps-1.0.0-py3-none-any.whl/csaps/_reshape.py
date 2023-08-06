# -*- coding: utf-8 -*-

import typing as ty
import numpy as np


def to_2d(arr: np.ndarray, axis: int) -> np.ndarray:
    """Transforms the shape of N-D array to 2-D NxM array

    The function transforms N-D array to 2-D NxM array along given axis,
    where N is dimension and M is the nember of elements.

    The function does not create a copy.

    Parameters
    ----------
    arr : np.array
        N-D array

    axis : int
        Axis that will be used for transform array shape

    Returns
    -------
    arr2d : np.ndarray
        2-D NxM array view

    Raises
    ------
    ValueError : axis is out of array axes

    See Also
    --------
    from_2d

    Examples
    --------

    .. code-block:: python

        >>> shape = (2, 3, 4)
        >>> arr = np.arange(1, np.prod(shape)+1).reshape(shape)
        >>> arr_2d = to_2d(arr, axis=1)
        >>> print(arr)
        [[[ 1  2  3  4]
          [ 5  6  7  8]
          [ 9 10 11 12]]

         [[13 14 15 16]
          [17 18 19 20]
          [21 22 23 24]]]
        >>> print(arr_2d)
        [[ 1  5  9]
         [ 2  6 10]
         [ 3  7 11]
         [ 4  8 12]
         [13 17 21]
         [14 18 22]
         [15 19 23]
         [16 20 24]]

    """

    arr = np.asarray(arr)
    axis = arr.ndim + axis if axis < 0 else axis

    if axis >= arr.ndim:  # pragma: no cover
        raise ValueError(f'axis {axis} is out of array axes {arr.ndim}')

    tr_axes = list(range(arr.ndim))
    tr_axes.pop(axis)
    tr_axes.append(axis)

    new_shape = (np.prod(arr.shape) // arr.shape[axis], arr.shape[axis])

    return arr.transpose(tr_axes).reshape(new_shape)


def block_view(arr: np.ndarray, block: ty.Tuple[int]) -> np.ndarray:
    """Returns array block view for given n-d array

    Creates n-d array block view with shape (k0, ..., kn, b0, ..., bn) for given
    array with shape (m0, ..., mn) and block (b0, ..., bn).

    Parameters
    ----------
    arr : array-like
        The input array with shape (m0, ..., mn)
    block : tuple
        The block tuple (b0, ..., bn)

    Returns
    -------
    a_view : array-like
        The block view for given array (k0, ..., kn, b0, ..., bn)

    """
    shape = tuple(size // blk for size, blk in zip(arr.shape, block)) + block
    strides = tuple(stride * blk for stride, blk in zip(arr.strides, block)) + arr.strides

    return np.lib.stride_tricks.as_strided(arr, shape=shape, strides=strides)
