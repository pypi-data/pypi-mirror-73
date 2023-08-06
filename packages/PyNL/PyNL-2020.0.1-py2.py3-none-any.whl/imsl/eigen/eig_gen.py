###########################################################################
# Copyright 2015-2019 Rogue Wave Software, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you
# may not use this file except in compliance with the License. You may
# obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied. See the License for the specific language governing
# permissions and limitations under the License.
###########################################################################
"""Eigenvalue analysis related functions."""
import ctypes as _ctypes
import numpy as _numpy

import imsl._constants as _constants
import imsl._imsllib as _imsllib
import collections as _collections


def _eig_gen_func(dtype):
    """Return the IMSL eig_gen function appropriate for dtype.

    Parameters
    ----------
    dtype : *numpy data type*
        The data type indicating which CNL function to choose.

    Returns
    -------
    *str or None*
        The underlying CNL function appropriate for `dtype` or None
        if a suitable function does not exist.

    """
    if _numpy.issubdtype(dtype, _numpy.float64):
        return _imsllib.imsl_d_eig_gen
    elif _numpy.issubdtype(dtype, _numpy.complex128):
        return _imsllib.imsl_z_eig_gen
    else:
        return None


def eig_gen(a, vectors=False):
    r"""Compute the eigenexpansion of a general real or complex matrix.

    Parameters
    ----------
    a : *(N,N) array_like*
        Array containing the input matrix.

    vectors : *bool, optional*
        Specifies if the eigenvectors should be returned.

        Default: `vectors = False`

    Returns
    -------
    A named tuple with the following fields:
    eigenvalues : *(N,) complex ndarray*
        The eigenvalues of the matrix, each repeated according to its
        algebraic multiplicity.

    eigenvectors : *(N,N) complex ndarray*
        The eigenvectors of the matrix. Returned only if `vectors = True`.

    Notes
    -----
    Function `eig_gen` computes the eigenvalues of a real or complex matrix
    by a two-phase process. In the real case, the matrix is reduced to upper
    Hessenberg form by elementary orthogonal or Gauss similarity
    transformations. Then, eigenvalues are computed using a *QR* or combined
    *LR-QR* algorithm ([1]_, pp. 373 - 382, and [2]_). The combined *LR-QR*
    algorithm is based on an implementation by Jeff Haag and David Watkins.
    Eigenvectors are then calculated as required. When eigenvectors are
    computed, the *QR* algorithm is used to compute the eigenexpansion. When
    only eigenvalues are required, the combined *LR-QR* algorithm is used.
    In the complex case, the matrix is reduced to upper Hessenberg form by
    elementary Gauss transformations. Then, the eigenvalues are computed
    using an explicitly shifted *LR* algorithm. Eigenvectors are calculated
    during the iterations for the eigenvalues ([3]_).

    References
    ----------
    .. [1] Golub, G.H., and C.F. Van Loan (1989), *Matrix Computations*,
           Second Edition, The Johns Hopkins University Press, Baltimore,
           Maryland.
    .. [2] Watkins, David S., and L. Elsner (1991), *Convergence of algorithm
           of decomposition type for the eigenvalue problem*, Linear Algebra
           Applications, 143, pp. 29-47.
    .. [3] Martin, R.S., and J.H. Wilkinson (1971), *The modified LR
           Algorithm for Complex Hessenberg Matrices*, Handbook, Volume II,
           Linear Algebra, Springer, New York.

    Examples
    --------
    *Example 1:*

    >>> import imsl.eigen as eig
    >>> import numpy as np
    >>> a = [[8.0, -1.0, -5.0], [-4.0, 4.0, -2.0], [18.0, -5.0, -7.0]]
    >>> result = eig.eig_gen(a, vectors=True)
    >>> print("Eigenvalues:\n"+str(result.eigenvalues))
    ... #doctest: +NORMALIZE_WHITESPACE
    Eigenvalues:
    [2.+4.j 2.-4.j 1.+0.j]
    >>> np.set_printoptions(precision=4, suppress=True)
    >>> print("Eigenvectors:\n"+str(result.eigenvectors)) #doctest: +SKIP
    Eigenvectors:
    [[ 0.3162-0.3162j  0.3162+0.3162j  0.4082+0.j    ]
     [ 0.6325+0.j      0.6325+0.j      0.8165+0.j    ]
     [ 0.0000-0.6325j  0.0000+0.6325j  0.4082+0.j    ]]
    >>> # Put back the default options
    >>> np.set_printoptions()

    *Example 2:*

    >>> import imsl.eigen as eig
    >>> import numpy as np
    >>> a = [[5.0+9.0j, 5.0+5.0j, -6.0-6.0j, -7.0-7.0j],
    ...      [3.0+3.0j, 6.0+10.0j, -5.0-5.0j, -6.0-6.0j],
    ...      [2.0+2.0j, 3.0+3.0j, -1.0+3.0j, -5.0-5.0j],
    ...      [1.0+1.0j, 2.0+2.0j, -3.0-3.0j, 4.0j]]
    >>> result = eig.eig_gen(a, vectors=True)
    >>> print("Eigenvalues:\n"+str(result.eigenvalues))
    ... #doctest: +NORMALIZE_WHITESPACE
    Eigenvalues:
    [4.+8.j 3.+7.j 2.+6.j 1.+5.j]
    >>> np.set_printoptions(precision=4, suppress=True)
    >>> print("Eigenvectors:\n"+str(result.eigenvectors)) #doctest: +SKIP
    Eigenvectors:
    [[ 0.5774+0.j  0.5774+0.j  0.3780+0.j  0.7559+0.j]
     [ 0.5774-0.j  0.5774-0.j  0.7559+0.j  0.3780+0.j]
     [ 0.5774-0.j  0.0000-0.j  0.3780+0.j  0.3780+0.j]
     [-0.0000+0.j  0.5774-0.j  0.3780+0.j  0.3780+0.j]]
    >>> # Put back the default options
    >>> np.set_printoptions()

    """
    if a is None:
        raise TypeError("None not supported")

    _a = _numpy.asarray(a, order='C')
    ref_type = _numpy.promote_types(_numpy.float64, _a.dtype)

    if (not _numpy.issubdtype(ref_type, _numpy.float64)
            and not _numpy.issubdtype(ref_type, _numpy.complex128)):
        raise ValueError("array type {} not supported".format(
            ref_type.name))

    # Convert the input data to the necessary data type (float or complex)
    _a = _numpy.asarray(_a, dtype=ref_type)

    if not (_a.ndim == 2):
        raise ValueError("a must be a two-dimensional square array")
    if _a.size == 0:
        raise ValueError("empty array not supported")
    if not (_a.shape[0] == _a.shape[1]):
        raise ValueError("a must be a two-dimensional square array")
    _n = _a.shape[0]

    #
    # Setup the parameters for the call to the system function.
    #
    args = []
    # Prepare required input argument list
    args.append(_ctypes.c_int(_n))
    args.append(_a.ctypes.data_as(_ctypes.c_void_p))

    # space for results
    if vectors:
        _vectors = _numpy.empty((_n, _n), dtype=_numpy.complex128)
        args.append(_constants.IMSL_VECTORS_USER)
        args.append(_vectors.ctypes.data_as(_ctypes.c_void_p))

    _result = _numpy.empty(_n, dtype=_numpy.complex128)
    args.append(_constants.IMSL_RETURN_USER)
    args.append(_result.ctypes.data_as(_ctypes.c_void_p))
    args.append(0)

    func = _eig_gen_func(ref_type)
    func(*args)

    # Package results in a named tuple
    result = _collections.namedtuple("eig_gen",
                                     ["eigenvalues",
                                      "eigenvectors"]
                                     )

    result.eigenvalues = _result
    if vectors is True:
        result.eigenvectors = _vectors
    else:
        result.eigenvectors = None

    return result
