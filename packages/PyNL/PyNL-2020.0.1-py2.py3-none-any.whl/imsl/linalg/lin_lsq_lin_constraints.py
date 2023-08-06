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
"""lin_lsq_lin_constraints related functions."""
import ctypes as _ctypes
import numpy as _numpy

import imsl._constants as _constants
import imsl.constants as constants
import imsl._imsllib as _imsllib
import collections as _collections


def _lin_lsq_lin_constraints_func(dtype):
    """Return the IMSL _lin_lsq_lin_constraints function appropriate for dtype.

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
        return _imsllib.imsl_d_lin_lsq_lin_constraints
    else:
        return None


def lin_lsq_lin_constraints(a, b, c, bl, bu, con_type, xlb=None, xub=None,
                            abs_tol=None, rel_tol=None, max_iter=None):
    r"""Solve a linear least-squares problem with linear constraints.

    Parameters
    ----------
    a : *(M, N) array_like*
        Array containing the coefficients of the *M* least-squares equations.

    b : *(M,) array_like*
        Array containing the right-hand sides of the least-squares equations.

    c : *(K, N) array_like*
        Array containing the coefficients of the *K* general constraints. If
        the problem contains no general constraints, set ``c = None``.

    bl : *(K,) array_like*
        Array containing the lower limits of the general constraints. If
        there is no lower limit on the *i*-th constraint, then ``bl[i]``
        will not be referenced.

    bu : *(K,) array_like*
         Array containing the upper limits of the general constraints. If
         there is no upper limit on the *i*-th constraint, then ``bl[i]``
         will not be referenced.

    con_type : *(K,) array_like*
        Array indicating the type of the general constraints, where
        ``con_type[i] = 0, 1, 2, 3`` indicates =, <=, >= and range
        constraints, respectively.

    xlb : *(N,) array_like, optional*
        Array containing the lower bounds on the variables. If there is no
        lower bound on the *i*-th variable, then ``xlb[i]`` should be set to
        constant ``UNBOUNDED_ABOVE`` in module :py:mod:`imsl.constants`.

        Default: The variables have no lower bounds.

    xub : *(N,) array_like, optional*
        Array containing the upper bounds on the variables. If there is no
        upper bound on the *i*-th variable, then ``xlb[i]`` should be set to
        constant ``UNBOUNDED_BELOW`` in module :py:mod:`imsl.constants`.

        Default: The variables have no upper bounds.

    abs_tol : *float, optional*
        Absolute rank determination tolerance to be used.

        Default: `abs_tol` = math.sqrt(numpy.finfo(numpy.float64).eps).

    rel_tol : *float, optional*
        Relative rank determination tolerance to be used.

        Default: `rel_tol` = math.sqrt(numpy.finfo(numpy.float64).eps).

    max_iter : *int, optional*
        The maximum number of add/drop iterations.

        Default: `max_iter` = 5 * max(M,N).

    Returns
    -------
    A named tuple with the following fields:
    solution : *(N,) ndarray*
        The approximate solution of the least-squares problem.

    residual : *(M,) ndarray*
        The residuals `b-Ax` of the least-squares equations at the
        approximate solution.

    Notes
    -----
    Function `lin_lsq_lin_constraints` solves linear least-squares problems
    with linear constraints. These are systems of least-squares equations
    of the form

    .. math::
        Ax \cong b

    subject to

    .. math::
        b_l \le Cx \le b_u \\
        x_l \le x \le x_u


    Here *A* is the coefficient matrix of the least-squares equations, *b*
    is the right-hand side, and *C* is the coefficient matrix of the
    constraints. The vectors :math:`b_l, b_u, x_l` and :math:`x_u` are the
    lower and upper bounds on the constraints and the variables, respectively.
    The system is solved by defining dependent variables :math:`y \equiv Cx`
    and then solving the least-squares system with the lower and upper bounds
    on `x` and `y`. The equation :math:`Cx-y=0` is a set of equality
    constraints. These constraints are realized by heavy weighting, i.e., a
    penalty method ([1]_).

    References
    ----------
    .. [1] Hanson, Richard J. (1986), *Linear Least Squares with Bounds and
           Linear Constraints*, SIAM J. Sci. and Stat. Computing, 7(3),
           826-834.

    Examples
    --------
    The following problem is solved in the least-squares sense:

    .. math::
        3x_1+2x_2+x_3=3.3 \\
        4x_1+2x_2+x_3=2.3 \\
        2x_1+2x_2+x_3=1.3 \\
        x_1+x_2+x_3=1.0

    subject to

    .. math::
        x_1=x_2+x_3 \le 1 \\
        0 \le x_1 \le 0.5 \\
        0 \le x_2 \le 0.5 \\
        0 \le x_3 \le 0.5

    The approximate solution of the least-squares problem, the residuals of
    the least-squares equations at the solution and the norm of the residual
    vector are printed.

    >>> import imsl.linalg as la
    >>> import numpy as np
    >>> a = [[3.0, 2.0, 1.0], [4.0, 2.0, 1.0], [2.0, 2.0, 1.0],
    ...      [1.0, 1.0, 1.0]]
    >>> b = [3.3, 2.3, 1.3, 1.0]
    >>> c = [[1.0, 1.0, 1.0]]
    >>> xlb = [0.0, 0.0, 0.0]
    >>> xub = [0.5, 0.5, 0.5]
    >>> con_type = [1]
    >>> bc = [1.0]
    >>> x = la.lin_lsq_lin_constraints(a, b, c, bc, bc, con_type, xlb=xlb,
    ...                                xub=xub)
    >>> print(x.solution) # doctest: +NORMALIZE_WHITESPACE
    [0.5 0.3 0.2]
    >>> print(x.residual) # doctest: +NORMALIZE_WHITESPACE
    [-1.   0.5  0.5  0. ]
    >>> print("{0:8.6f}".format(np.linalg.norm(x.residual)))
    1.224745

    """
    if a is None:
        raise TypeError("None not supported")
    if b is None:
        raise TypeError("None not supported")

    _a = _numpy.asarray(a, order='C')
    ref_type = _numpy.promote_types(_numpy.float64, _a.dtype)

    if (not _numpy.issubdtype(ref_type, _numpy.float64)):
        raise ValueError("array type {} not supported".format(
            ref_type.name))

    # Convert the input data to double precision
    _a = _numpy.asarray(a, dtype=ref_type)

    if _a.ndim != 2:
        raise ValueError("a must be a two-dimensional array")
    if _a.size == 0:
        raise ValueError("empty array not supported")
    _nra = _a.shape[0]
    _nca = _a.shape[1]

    _b = _numpy.asarray(b, order='C', dtype=ref_type)
    if _b.ndim != 1:
        raise ValueError("b must be a one-dimensional array")
    if _b.shape[0] != _nra:
        raise ValueError("shapes of a and b not compatible: "
                         "a.shape[0] ({}) does not equal b.shape[0] "
                         "({})".format(_nra, _b.shape[0]))

    if c is None:
        _ncon = 0
    else:
        _c = _numpy.asarray(c, order='C', dtype=ref_type)
        if _c.ndim != 2:
            raise ValueError("c must be a two-dimensional array")
        if _c.size == 0:
            raise ValueError("empty array not supported")
        if _c.shape[1] != _nca:
            raise ValueError("shapes of a and c not compatible: "
                             "a.shape[1] ({}) does not equal c.shape[1] "
                             "({})".format(_nca, _c.shape[1]))
        _ncon = _c.shape[0]

    if _ncon > 0:
        if bl is None:
            raise TypeError("None not supported")
        _bl = _numpy.asarray(bl, order='C', dtype=ref_type)
        if _bl.ndim != 1:
            raise ValueError("bl must be a one-dimensional array")
        if _bl.shape[0] != _ncon:
            raise ValueError("shapes of bl and c not compatible: "
                             "bl.shape[0] ({}) does not equal c.shape[0] "
                             "({})".format(_bl.shape[0], _ncon))

        if bu is None:
            raise TypeError("None not supported")
        _bu = _numpy.asarray(bu, order='C', dtype=ref_type)
        if _bu.ndim != 1:
            raise ValueError("bu must be a one-dimensional array")
        if _bu.shape[0] != _ncon:
            raise ValueError("shapes of bu and c not compatible: "
                             "bu.shape[0] ({}) does not equal c.shape[0] "
                             "({})".format(_bu.shape[0], _ncon))

        if con_type is None:
            raise TypeError("None not supported")
        _con_type = _numpy.asarray(con_type, order='C', dtype=_numpy.int32)
        if _con_type.ndim != 1:
            raise ValueError("con_type must be a one-dimensional array")
        if _con_type.shape[0] != _ncon:
            raise ValueError("shapes of con_type and c not compatible: "
                             "con_type.shape[0] ({}) does not equal "
                             "c.shape[0] ({})".format(_con_type.shape[0],
                                                      _ncon))

    if xlb is not None:
        _xlb = _numpy.asarray(xlb, order='C', dtype=ref_type)
        if _xlb.ndim != 1:
            raise ValueError("xlb must be a one-dimensional array")
        if _xlb.shape[0] != _nca:
            raise ValueError("shapes of xlb and a not compatible: "
                             "xlb.shape[0] ({}) does not equal a.shape[1] "
                             "({})".format(_xlb.shape[0], _nca))
    else:
        _xlb = _numpy.empty((_nca,), order='C', dtype=ref_type)
        _xlb[:] = constants.UNBOUNDED_ABOVE

    if xub is not None:
        _xub = _numpy.asarray(xub, order='C', dtype=ref_type)
        if _xub.ndim != 1:
            raise ValueError("xub must be a one-dimensional array")
        if _xub.shape[0] != _nca:
            raise ValueError("shapes of xub and a not compatible: "
                             "xub.shape[0] ({}) does not equal a.shape[1] "
                             "({})".format(_xub.shape[0], _nca))
    else:
        _xub = _numpy.empty((_nca,), order='C', dtype=ref_type)
        _xub[:] = constants.UNBOUNDED_BELOW

    #
    # Setup the parameters for the call to the CNL function.
    #
    args = []

    # Prepare required input argument list
    args.append(_ctypes.c_int(_nra))
    args.append(_ctypes.c_int(_nca))
    args.append(_ctypes.c_int(_ncon))
    args.append(_a.ctypes.data_as(_ctypes.c_void_p))
    args.append(_b.ctypes.data_as(_ctypes.c_void_p))
    if _ncon == 0:
        # Add NULL pointers for c, bl, bu and con_type
        # to the argument list if no constraints exist
        args.append(_ctypes.POINTER(_ctypes.c_void_p)())
        args.append(_ctypes.POINTER(_ctypes.c_void_p)())
        args.append(_ctypes.POINTER(_ctypes.c_void_p)())
        args.append(_ctypes.POINTER(_ctypes.c_void_p)())
    else:
        args.append(_c.ctypes.data_as(_ctypes.c_void_p))
        args.append(_bl.ctypes.data_as(_ctypes.c_void_p))
        args.append(_bu.ctypes.data_as(_ctypes.c_void_p))
        args.append(_con_type.ctypes.data_as(_ctypes.c_void_p))

    args.append(_xlb.ctypes.data_as(_ctypes.c_void_p))
    args.append(_xub.ctypes.data_as(_ctypes.c_void_p))

    if abs_tol is not None:
        args.append(_constants.IMSL_ABS_FCN_TOL)
        args.append(_ctypes.c_double(abs_tol))

    if rel_tol is not None:
        args.append(_constants.IMSL_REL_FCN_TOL)
        args.append(_ctypes.c_double(rel_tol))

    if max_iter is not None:
        args.append(_constants.IMSL_ITMAX)
        args.append(_ctypes.c_int(max_iter))

    # space for results
    _result = _numpy.empty(_nca, dtype=ref_type)
    args.append(_constants.IMSL_RETURN_USER)
    args.append(_result.ctypes.data_as(_ctypes.c_void_p))

    _residual = _numpy.empty(_nra, dtype=ref_type)
    args.append(_constants.IMSL_RESIDUAL_USER)
    args.append(_residual.ctypes.data_as(_ctypes.c_void_p))

    # terminate the CNL arg list with a zero.
    args.append(0)

    func = _lin_lsq_lin_constraints_func(ref_type)
    func(*args)

    # Package results in a named tuple
    result = _collections.namedtuple("lin_lsq_lin_constraints",
                                     ["solution",
                                      "residual"]
                                     )

    result.solution = _result
    result.residual = _residual

    return result
