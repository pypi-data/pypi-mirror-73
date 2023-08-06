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
"""LU factorization related class, methods and functions."""
import ctypes as _ctypes
import numpy as _numpy

import imsl._constants as _constants
import imsl._imsllib as _imsllib

_in = ('C', 'A')
_out = ('C', 'A', 'W', 'O')
_inout = ('C', 'A', 'W', 'O')


def _lin_sol_gen_func(dtype):
    """Return the IMSL lin_sol_gen function appropriate for dtype.

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
    if (_numpy.issubdtype(dtype, _numpy.float64)):
        return _imsllib.imsl_d_lin_sol_gen
    elif (_numpy.issubdtype(dtype, _numpy.complex128)):
        return _imsllib.imsl_z_lin_sol_gen
    else:
        return None


class LU():
    r"""Solve a real general system of linear equations.

    Solve a real general system of linear equations :math:`Ax = b`. Using
    specific methods, any of several related computations can be performed.
    These extra tasks include computing the *LU* factorization of *A* using
    partial pivoting, computing the inverse matrix :math:`A^{-1}`, solving
    :math:`A^T x = b` or :math:`A^H x = b`, or computing the solution of
    :math:`Ax = b` given the *LU* factorization of *A*.

    Parameters
    ----------
    a : *(N,N) array_like*
        Array containing the input matrix.

    """

    def __init__(self, a):
        """Instantiate LU class."""
        self._a = a
        self._factor_pvt = None
        self._factor_factor = None
        self._cond = None
        self._inverse = None

        if self._a is None:
            raise TypeError("None not supported")

        self._a = _numpy.array(a, order='C')

        # attempt to promote matrix a to a compatible type.
        common_type = _numpy.promote_types(_numpy.float64, self._a.dtype)
        self._a = _numpy.asarray(self._a, dtype=common_type)

        if (not _numpy.issubdtype(self._a.dtype, _numpy.float64)
                and not _numpy.issubdtype(self._a.dtype, _numpy.complex128)):
            raise ValueError("array type {} not supported".format(
                             self._a.dtype.name))

        if self._a.ndim != 2:
            raise ValueError("array of dimension {} not"
                             " supported".format(self._a.ndim))

        if self._a.size == 0:
            raise ValueError("empty array not supported")

        if (self._a.shape[0] != self._a.shape[1]):
            raise ValueError("input matrix must be square")

    def solve(self, b, transpose=False):
        r"""
        Solve a system of linear equations using right-hand side `b`.

        See Also
        --------
        lu_solve : equivalent function containing full documentation.

        Notes
        -----
        This method caches the *LU* factorization the first time it is
        calculated, and re-uses it on subsequent calls. This is especially
        useful if linear systems with the same coefficient matrix but
        different right-hand sides have to be solved.

        Examples
        --------
        >>> import imsl.linalg as la
        >>> a = [[1.0, 3.0, 3.0], [1.0, 3.0, 4.0], [1.0, 4.0, 3.0]]
        >>> b = [1.0, 4.0, -1.0]
        >>> lu = la.LU(a)
        >>> x = lu.solve(b)
        >>> print(x) # doctest: +NORMALIZE_WHITESPACE
        [-2. -2. 3.]

        """
        if b is None:
            raise TypeError("None not supported")

        b = _numpy.asarray(b, dtype=self._a.dtype, order='C')

        if b.ndim != 1:
            raise ValueError("array of dimension {} not"
                             " supported".format(b.ndim))

        if b.size != self._a.shape[0]:
            raise ValueError("dependent variable values length ({}) does not"
                             " match coefficient matrix row count"
                             " ({})".format(b.size, self._a.shape[0]))

        args = []

        row_dim = self._a.shape[0]

        args.append(row_dim)
        args.append(self._a.ctypes.data_as(_ctypes.c_void_p))
        args.append(b.ctypes.data_as(_ctypes.c_void_p))

        solution = _numpy.empty_like(b)
        args.append(_constants.IMSL_RETURN_USER)
        args.append(solution.ctypes.data_as(_ctypes.c_void_p))

        _transpose = int(transpose)
        if _transpose:
            args.append(_constants.IMSL_TRANSPOSE)

        if self._factor_factor is None:
            self._factor_pvt = _numpy.empty(row_dim, dtype=_numpy.int32)
            self._factor_factor = _numpy.empty([row_dim, row_dim],
                                               dtype=self._a.dtype)
        else:
            args.append(_constants.IMSL_SOLVE_ONLY)

        args.append(_constants.IMSL_FACTOR_USER)
        args.append(self._factor_pvt.ctypes.data_as(_ctypes.c_void_p))
        args.append(self._factor_factor.ctypes.data_as(_ctypes.c_void_p))

        if self._cond is None:
            args.append(_constants.IMSL_CONDITION)
            cond = _ctypes.c_double()
            args.append(_ctypes.byref(cond))

        args.append(0)

        func = _lin_sol_gen_func(self._a.dtype)
        func(*args)

        if self._cond is None:
            self._cond = cond.value

        return solution

    def factor(self):
        r"""Compute the pivoted *LU* factorization of the matrix.

        See Also
        --------
        lu_factor : equivalent function containing full documentation.

        Notes
        -----
        This method caches the *LU* factorization the first time it is
        calculated, and re-uses it on subsequent calls to methods from
        class :py:class:`LU()`.

        """
        if (self._factor_factor is None or self._factor_pvt is None
                or self._cond is None):
            args = []

            row_dim = self._a.shape[0]

            args.append(row_dim)
            args.append(self._a.ctypes.data_as(_ctypes.c_void_p))
            args.append(0)  # b is ignored

            self._factor_pvt = _numpy.empty(row_dim, dtype=_numpy.int32)
            self._factor_factor = _numpy.empty([row_dim, row_dim],
                                               dtype=self._a.dtype)

            args.append(_constants.IMSL_FACTOR_ONLY)
            args.append(_constants.IMSL_FACTOR_USER)
            args.append(self._factor_pvt.ctypes.data_as(_ctypes.c_void_p))
            args.append(self._factor_factor.ctypes.data_as(_ctypes.c_void_p))

            args.append(_constants.IMSL_CONDITION)
            cond = _ctypes.c_double()
            args.append(_ctypes.byref(cond))

            args.append(0)

            func = _lin_sol_gen_func(self._a.dtype)
            func(*args)

            self._cond = cond.value

        return (_numpy.copy(self._factor_pvt),
                _numpy.copy(self._factor_factor))

    def factor_full(self):
        r"""Compute the pivoted *LU* factorization of the matrix.

        See Also
        --------
        lu_factor_full : equivalent function containing full documentation.

        """
        n = self._a.shape[0]
        if (self._factor_factor is None or self._factor_pvt is None):
            ipvt, LU_matrix = self.factor()
        else:
            ipvt = self._factor_pvt
            LU_matrix = self._factor_factor

        L_factor = _numpy.eye(n, dtype=self._a.dtype)
        U_factor = _numpy.zeros((n, n), dtype=self._a.dtype)
        L_column = _numpy.empty(n, dtype=self._a.dtype)

        # Populate the strictly lower triangular part of the L_factor
        for i in range(1, n):
            L_column[i:n] = -LU_matrix[i:n, i - 1]
            # Permute L_column[i:n]
            # For the mathematical aspects, see Golub/Van Loan,
            # "Matrix Computations", Third Edition, pp. 113-114
            for j in range(i, n - 1):
                row = ipvt[j] - 1
                if row != j:
                    temp = L_column[row]  # ipvt is 1-based
                    L_column[row] = L_column[j]
                    L_column[j] = temp
            L_factor[i:n, i - 1] = L_column[i:n]

        # Copy U factor into U_factor
        for i in range(n):
            U_factor[i, i:n] = LU_matrix[i, i:n]

        # Construct permutation matrix P
        P = _numpy.zeros((n, n), dtype=self._a.dtype)

        # Generate permutation vector permu:
        #  _                                                _
        # |    1          2          3      ...     n        |
        # |                                                  |
        # |  permu[0]   permu[1]   permu[2]  ...  permu[n-1] |
        # |_                                                _|
        #

        permu = [i for i in range(1, n + 1)]

        for i in range(1, n + 1):
            temp = ipvt[i - 1]
            val1 = permu[i - 1]
            val2 = permu[temp - 1]
            permu[temp - 1] = val1
            permu[i - 1] = val2

        # Use permu to compute permutation matrix P
        for i in range(0, n):
            P[i, permu[i] - 1] = 1.0  # implicit type conversion

        return P, L_factor, U_factor

    def inv(self):
        r"""Compute the inverse of the matrix.

        See Also
        --------
        lu_inv : equivalent function containing full documentation.

        """
        if self._inverse is None:
            args = []

            row_dim = self._a.shape[0]

            args.append(row_dim)
            args.append(self._a.ctypes.data_as(_ctypes.c_void_p))
            args.append(0)  # b is ignored

            self._inverse = _numpy.empty([row_dim, row_dim],
                                         dtype=self._a.dtype)

            args.append(_constants.IMSL_INVERSE_ONLY)
            args.append(_constants.IMSL_INVERSE_USER)
            args.append(self._inverse.ctypes.data_as(_ctypes.c_void_p))

            args.append(0)

            func = _lin_sol_gen_func(self._a.dtype)
            func(*args)

        return _numpy.copy(self._inverse)

    def cond(self):
        r"""Compute the :math:`L_1` norm condition number of the matrix.

        See Also
        --------
        lu_cond : equivalent function containing full documentation.

        """
        if self._cond is None:
            self.factor()

        return self._cond


def lu_solve(a, b, transpose=False):
    r"""Solve a general system *Ax = b* of linear equations.

    Parameters
    ----------
    a : *(N,N) array_like*
        Array containing the matrix *A*.
    b : *(N,) array_like*
        Array containing the right-hand side.
        Elements of this array must be convertible to the same
        type as array `a`.
    transpose : *bool, optional*
        If True, solve :math:`A^Tx = b` (if `a` contains entries of
        type *float*) or :math:`A^Hx = b` (if `a` contains entries of
        type *complex*). Default is False.

    Returns
    -------
    *(N,) ndarray*
        The solution `x` of the linear system *Ax=b*.

    Notes
    -----
    In a first step, this function computes the *LU* factorization of
    matrix *A*. Then, it finds the solution of the linear system `Ax = b`
    by solving two simpler systems, :math:`y=L^{-1}b` and
    :math:`x=U^{-1}y`.

    This function creates a temporary :py:class:`LU()` instance
    and calls method :py:meth:`LU.solve` on that instance.

    Examples
    --------
    >>> import imsl.linalg as la
    >>> a = [[1.0, 3.0, 3.0], [1.0, 3.0, 4.0], [1.0, 4.0, 3.0]]
    >>> b = [1.0, 4.0, -1.0]
    >>> x = la.lu_solve(a, b)
    >>> print(x) # doctest: +NORMALIZE_WHITESPACE
    [-2. -2. 3.]

    """
    solver = LU(a)
    return solver.solve(b, transpose=transpose)


def lu_cond(a):
    r"""Compute the :math:`L_1` norm condition number of a matrix.

    Parameters
    ----------
    a : *(N,N) array_like*
        Array containing the matrix.

    Returns
    -------
    *float*
        The :math:`L_1` condition number of `a`.

    Notes
    -----
    The :math:`L_1` condition number of a matrix *A* is defined as
    :math:`\kappa(A)=||A||_1||A^{-1}||_1`. Its computation uses
    the same algorithm as in [1]_. If the estimated condition
    number is greater than :math:`1/\epsilon` (where :math:`\epsilon`
    is the machine precision), a warning message is issued. This
    indicates that very small changes in *A* may produce large
    changes in the solution *x* of a linear system *Ax = b*.

    This function creates a temporary :py:class:`LU()` instance
    and calls method :py:meth:`LU.cond` on that instance.

    References
    ----------
    .. [1] Dongarra, J.J., J.R. Bunch, C.B. Moler, and G.W. Stewart (1979),
           *LINPACK User's Guide*, SIAM, Philadelphia.

    """
    solver = LU(a)
    return solver.cond()


def lu_factor(a):
    r"""Compute the pivoted *LU* factorization of a matrix.

    Parameters
    ----------
    a : *(N,N) array_like*
        Square matrix to be factorized.

    Returns
    -------
    pvt : *(N,) ndarray*
        The pivot sequence determined during the factorization.
    fac : *(N,N) ndarray*
        The *LU* factorization of the matrix.

    Notes
    -----
    The computed *LU* factorization of matrix *A* satisfies
    :math:`L^{-1}A = U`. Let :math:`F` denote the matrix stored in `fac`.
    The triangular matrix :math:`U` is then stored in the upper triangle
    of :math:`F`. The strict lower triangle of :math:`F` contains
    the information needed to reconstruct :math:`L^{-1}`
    using

        :math:`L^{-1} = L_{n-1}P_{n-1} \ldots L_1P_1.`

    The factors :math:`P_i` and :math:`L_i` are defined by partial
    pivoting. :math:`P_i` is the identity matrix with rows *i*
    and ``pvt[i-1]`` interchanged. :math:`L_i` is the identity
    matrix with :math:`F_{ji}`, for :math:`j = i+1,\ldots n`,
    inserted below the diagonal in column *i*.

    The factorization efficiency is based on a technique of
    "loop unrolling and jamming" by Dr. Leonard J. Harding of the
    University of Michigan, Ann Arbor, Michigan.

    This function creates a temporary :py:class:`LU()` instance
    and calls method :py:meth:`LU.factor` on that instance.

    An exception is raised if :math:`U`, the upper triangular part
    of the factorization, has a zero diagonal element.

    """
    solver = LU(a)
    return solver.factor()


def lu_inv(a):
    r"""Compute the inverse of a matrix.

    Parameters
    ----------
    a : *(N,N) array_like*
        Square matrix to be inverted.

    Returns
    -------
    *(N,N) ndarray*
        The inverse of the matrix `a`.

    Notes
    -----
    This function creates a temporary :py:class:`LU()` instance
    and calls method :py:meth:`LU.inv` on that instance.

    """
    solver = LU(a)
    return solver.inv()


def lu_factor_full(a):
    r"""Compute the *LU* decomposition of matrix *A*, *PA=LU*.

    Parameters
    ----------
    a : *(N,N) array_like*
        Square matrix to be factorized.

    Returns
    -------
    P : *(N,N) ndarray*
        A permutation matrix, matrix *P* in the factorization *PA=LU*.
    L : *(N,N) ndarray*
        A unit lower triangular matrix, the *L* factor in the factorization
        *PA=LU*.
    U : *(N,N) ndarray*
        An upper triangular matrix, the *U* factor in the factorization
        *PA=LU*.

    Notes
    -----
    Function `lu_factor_full` returns full matrices *P*, *L* and *U* that
    describe the *LU* factorization *PA=LU*. This is in contrast to
    function `lu_factor` which returns only a compressed form of the
    factorization.

    Examples
    --------
    >>> import numpy as np
    >>> import imsl.linalg as la
    >>> A = [[1.0, 3.0, 3.0], [1.0, 3.0, 4.0], [1.0, 4.0, 3.0]]
    >>> P, L, U = la.lu_factor_full(A)
    >>> print("P*A:\n"+str(np.dot(P,A))) # doctest: +NORMALIZE_WHITESPACE
    P*A:
    [[1. 3. 3.]
     [1. 4. 3.]
     [1. 3. 4.]]
    >>> print("L*U:\n"+str(np.dot(L,U))) # doctest: +NORMALIZE_WHITESPACE
    L*U:
    [[1. 3. 3.]
     [1. 4. 3.]
     [1. 3. 4.]]

    """
    solver = LU(a)
    return solver.factor_full()
