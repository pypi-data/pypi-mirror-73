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
"""Sparse LP module."""
import ctypes as _ctypes
import numpy as _numpy
from scipy.sparse import coo_matrix, csc_matrix

import imsl._constants as _constants
import imsl.constants as constants
import imsl._imsllib as _imsllib
import collections as _collections


def _sparse_lp_func(dtype):
    """Return the IMSL sparse_lp function appropriate for dtype.

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
        return _imsllib.imsl_d_sparse_lin_prog
    else:
        return None


def sparse_lp(a, b, c, xb=None, obj_constant=0.0, preorder=0,
              presolve=0, max_iter=200, opt_tol=1.0e-10,
              primal_infeas_tol=1.0e-8, dual_infeas_tol=1.0e-8):
    r"""Solve a sparse linear programming problem.

    The linear programming problem is of the form

    Minimize c^T * x

    Subject to:

                b_l <= A * x <= b_u,

                x_l <= x <= x_u

    Parameters
    ----------
    a : *sparse matrix*
        The constraint matrix of shape *(M,N)* in SciPy's `COO`_ or
        `CSC`_ format. If no constraint matrix is required, either
        set `a` to None or to a matrix of shape *(0,N)*.

    b : *tuple*
        A three-element tuple `(bl, bu, constr_type)` containing the
        constraint bounds and information about the constraint type. If a
        constraint is two-sided then `bl` contains the lower bound and `bu`
        the upper bound of the constraint. If a constraint is one-sided,
        then `bl` must contain the bound and the corresponding entry in `bu`
        is ignored.

        `bl` can be defined in one of two forms:

            - A scalar : The same bound `bl` will be applied to all
              constraints.
            - *(M,) array_like* : Bound `bl[i]` will be applied to the
              `i` -th constraint.

        `bu` can be defined in one of two forms:

            - A scalar : The same upper bound `bu` will be applied to all
              constraints.
            - *(M,) array_like* : Upper bound `bu[i]` will be applied to the
              `i` -th constraint.

        `constr_type` can be defined in one of two forms:

            - A scalar : All constraints are of type `constr_type`.
            - *(M,) array_like* : The `i` -th constraint is of type
              `constr_type[i]`.

        Let :math:`r_i = a_{i1}x_1+\ldots+a_{in}x_n` be the `i` -th
        constraint, with lower bound :math:`bl_i` and upper bound
        :math:`bu_i`.
        Then, the value of `constr_type[i]` signifies the following:

          +-------------------+------------------------------+
          |  `constr_type[i]` | Constraint                   |
          +===================+==============================+
          |      0            | :math:`r_i = bl_i`           |
          +-------------------+------------------------------+
          |      1            | :math:`r_i \le bl_i`         |
          +-------------------+------------------------------+
          |      2            | :math:`r_i \ge bl_i`         |
          +-------------------+------------------------------+
          |      3            | :math:`bl_i \le r_i \le bu_i`|
          +-------------------+------------------------------+
          |      4            | Ignore this constraint       |
          +-------------------+------------------------------+

        Note that `constr_type[i]` = 3 should only be used for constraints `i`
        with both finite lower and finite upper bound. For one-sided
        constraints, use `constr_type[i]` = 1 or `constr_type[i]` = 2. For
        free constraints, use `constr_type[i]` = 4.

        If no constraint matrix `a` is available, then `b` is ignored.

    c : *(N,) array_like*
        Array containing the coefficients of the objective function.

    xb : *tuple, optional*
        A two-element tuple `(xlb, xub)` containing the lower and upper
        bounds on the variables.

        `xlb` can be defined in one of two forms:

            - A scalar : The same lower bound `xlb` will be applied to all
              variables.
            - *(N,) array_like* : Each variable :math:`x_i` will be lower
              bounded by `xlb[i]`.

        Use constant ``UNBOUNDED_BELOW`` from the :py:mod:`~imsl.constants`
        module to specify negative infinite bounds.

        `xub` can be defined in one of two forms:
            - A scalar : The same upper bound `xub` will be applied to all
              variables.
            - *(N,) array_like* : Each variable :math:`x_i` will be upper
              bounded by `xub[i]`.

        Use constant ``UNBOUNDED_ABOVE`` from the :py:mod:`~imsl.constants`
        module to specify positive infinite bounds.

        Default: All variables are non-negative.

    obj_constant : *float, optional*
        Value of the constant term in the objective function.

    preorder : *int, optional*
        The variant of the Minimum Degree Ordering (MDO) algorithm used
        in the preordering of the normal equations or augmented system
        matrix:

        .. rst-class:: nowrap

            +--------------+-------------------------------------+
            |  `preorder`  |   Method                            |
            +==============+=====================================+
            |      0       | A variant of the MDO algorithm      |
            |              | using pivotal cliques.              |
            +--------------+-------------------------------------+
            |      1       | A variant of George and Liu's       |
            |              | Quotient Minimum Degree algorithm.  |
            +--------------+-------------------------------------+

    presolve : *int, optional*
        Presolve the LP problem in order to reduce the problem size or
        to detect infeasibility or unboundedness of the problem.
        Depending on the number of presolve techniques used, different
        presolve levels can be chosen:

        .. rst-class:: nowrap

            +--------------+----------------------------------------+
            |  `presolve`  |   Description                          |
            +==============+========================================+
            |      0       |  No presolving                         |
            +--------------+----------------------------------------+
            |      1       | Eliminate singleton rows               |
            +--------------+----------------------------------------+
            |      2       | Additionally to 1, eliminate redundant |
            |              | (and forcing) rows                     |
            +--------------+----------------------------------------+
            |      3       | Additionally to 2, eliminate dominated |
            |              | variables.                             |
            +--------------+----------------------------------------+
            |      4       | Additionally to 3, eliminate singleton |
            |              | columns.                               |
            +--------------+----------------------------------------+
            |      5       | Additionally to 4, eliminate doubleton |
            |              | rows.                                  |
            +--------------+----------------------------------------+
            |      6       | Additionally to 5, eliminate aggregate |
            |              | columns.                               |
            +--------------+----------------------------------------+

    max_iter :  *int, optional*
        The maximum number of iterations allowed for the primal-dual
        solver.

    opt_tol :  *float, optional*
        The relative optimality tolerance.

    primal_infeas_tol : *float, optional*
        The primal infeasibility tolerance.

    dual_infeas_tol : *float, optional*
        The dual infeasibility tolerance.

    Returns
    -------
    A named tuple with the following fields:

    sol : *(N,) ndarry*
        Array containing the primal solution of the LP problem.

    obj : *float*
        Optimal value of the objective function.

    dual : *(M,) ndarray*
        Array containing the dual solution.

    n_iter : *int*
        The number of iterations required by the primal-dual solver.

    infeas : *tuple*
        A 3-element tuple containing the primal and dual infeasibilities.
        Element `infeas[0]` contains the primal infeasibility of the solution,
        `infeas[1]` the violation of the variable bounds, and `infeas[2]` the
        dual infeasibility of the solution.

    cp_ratios : *tuple*
        A 2-element tuple containing the ratios of the smallest
        (in `cp_ratios[0]`) and largest (in `cp_ratios[1]`) complementarity
        product to the average.

    Notes
    -----
    The function `sparse_lp`  uses an infeasible primal-dual interior-point
    method to solve linear programming problems, i.e., problems of the form

    .. math::
        \min_{x \in {R}^n} c^Tx \quad \text{subject to} \quad
            b_l \le Ax \le b_u\\
            x_l \le x \le x_u

    where *c* is the objective coefficient vector, *A* is the coefficient
    matrix, and the vectors :math:`b_l, b_u, x_l` and :math:`x_u` are the
    lower and upper bounds on the constraints and the variables, respectively.

    Internally, `sparse_lp` transforms the problem given by the user into a
    simpler form that is computationally more tractable. After redefining the
    notation, the new form reads

    .. math::
        \begin{array}{lrll}
        \min{c^Tx}&&&\\
        \text{subject to} & Ax&= b&\\
        & x_i+s_i&=u_i, \quad x_i, s_i \ge 0, &i \in I_u\\
        & x_j&\ge 0, &j \in I_s
        \end{array}

    Here, :math:`I_u \cup I_s = \{1,\ldots,n\}` is a partition of the index set
    :math:`\{1,\ldots,n\}` into upper bounded and standard variables.

    To simplify the description, the following assumes that the problem above
    contains only variables with upper bounds, i.e. is of the form

    .. math::
        \begin{array}{clrl}
        &\min{c^Tx}&&\\
        (P)&\text{subject to} & Ax&= b\\
        && x+s&=u,\\
        && x,s&\ge 0
        \end{array}

    The corresponding dual problem is

    .. math::
        \begin{array}{clrl}
        &\max{b^Ty-u^Tw}&&\\
        (D)&\text{subject to} & A^Ty+z-w&=c,\\
        && z,w&\ge 0
        \end{array}

    The Karush-Kuhn-Tucker (KKT) optimality conditions for *(P)* and *(D)* are

    .. math::
        \begin{array}{rlr}
        Ax&=b,&\quad (1.1)\\
        x+s&=u,&\quad (1.2)\\
        A^Ty+z-w&=c,&\quad (1.3)\\
        XZe&=0,&\quad (1.4)\\
        SWe&=0,&\quad (1.5)\\
        x,z,s,w&\ge 0,&\quad (1.6)
        \end{array}

    where :math:`X=diag(x)`, :math:`Z=diag(z)`, :math:`S=diag(s)` and
    :math:`W=diag(w)` are diagonal matrices, and :math:`e=(1,\ldots,1)^T`
    is a vector of ones.

    Function `sparse_lp`, like all infeasible interior point methods, generates
    a sequence

    .. math::
        (x_k,s_k,y_k,z_k,w_k), \quad k=0,1,\ldots

    of iterates that satisfy :math:`(x_k,s_k,y_k,z_k,w_k)>0` for all *k*, but
    are in general not feasible, i.e. the linear constraints (1.1)-(1.3) are
    only satisfied in the limiting case :math:`k \to \infty`.

    The barrier parameter :math:`\mu`, defined by

    .. math::
        \mu = \frac{x^Tz+s^Tw}{2n}

    measures how well the complementarity conditions (1.4), (1.5) are
    satisfied.

    Mehrotra's predictor-corrector algorithm is a variant of Newton's method
    applied to the KKT conditions (1.1)-(1.5). Function `sparse_lp` uses a
    modified version of this algorithm to compute the iterates
    :math:`(x_k,s_k,y_k,z_k,w_k)`. In every step of the algorithm, the search
    direction vector

    .. math::
        \Delta := (\Delta x, \Delta s, \Delta y, \Delta z, \Delta w)

    is decomposed into two parts,
    :math:`\Delta = \Delta_a + \Delta_c^{\omega}`,
    where :math:`\Delta_a` and :math:`\Delta_c^{\omega}` denote the
    affine-scaling and a weighted centering component, respectively. Here,

    .. math::
        \Delta_c^{\omega}:=(\omega_P\Delta x_c, \omega_P\Delta s_c,
        \omega_D \Delta y_c, \omega_D \Delta z_c, \omega_D \Delta w_c)

    where :math:`\omega_P` and :math:`\omega_D` denote the primal and dual
    corrector weights, respectively.

    The vectors :math:`\Delta_a` and
    :math:`\Delta_c := (\Delta x_c, \Delta s_c, \Delta y_c,
    \Delta z_c, \Delta w_c)` are determined by solving the linear system

    .. math::
        \begin{bmatrix}
            A & 0 & 0 & 0 & 0\\
            I & 0 & I & 0 & 0\\
            0 & A^T & 0 & I & -I\\
            Z & 0 & 0 & X & 0\\
            0 & 0 & W & 0 & S
        \end{bmatrix}
        \begin{bmatrix}
          \Delta x\\
          \Delta y\\
          \Delta s\\
          \Delta z\\
          \Delta w
        \end{bmatrix}
        =
        \begin{bmatrix}
          r_b\\
          r_u\\
          r_c\\
          r_{xz}\\
          r_{ws}
        \end{bmatrix}
        \quad (2)

    for two different right-hand sides.

    For :math:`\Delta_a`, the right-hand side is defined as

    .. math::
        (r_b,r_u,r_c,r_{xz},r_{ws})=(b-Ax,u-x-s,c-A^Ty-z+w,-XZe,-WSe).

    Here, :math:`r_b` and :math:`r_u` are the violations of the primal
    constraints and :math:`r_c` defines the violations of the dual
    constraints.

    The resulting direction :math:`\Delta_a` is the pure Newton step applied
    to the system (1.1)-(1.5).

    In order to obtain the corrector direction :math:`\Delta_c`, the maximum
    stepsizes :math:`\alpha_{Pa}` in the primal and :math:`\alpha_{Da}` in
    the dual space preserving nonnegativity of :math:`(x,s)` and
    :math:`(z,w)` respectively, are determined, and the predicted
    complementarity gap

    .. math::
        g_a = (x+\alpha_{Pa}\Delta x_a)^T(z+\alpha_{Da}\Delta z_a)+
              (s+\alpha_{Pa}\Delta s_a)^T(w+\alpha_{Da}\Delta w_a)


    is computed. It is then used to determine the barrier parameter

    .. math::
        \hat{\mu} = \left( \frac{g_a}{g} \right)^2 \frac{g_a}{2n},

    where :math:`g=x^Tz+s^Tw` denotes the current complementarity gap.

    The direction :math:`\Delta_c` is then computed by choosing

    .. math::
        (r_b,r_u,r_c,r_{xz},r_{ws})=(0,0,0,\hat{\mu}e-
        \Delta X_a \Delta Z_a e,\hat{\mu} e-\Delta W_a \Delta S_ae)

    as the right-hand side in the linear system (2).

    Function `sparse_lp` now uses a linesearch to find the optimal weight
    :math:`\hat{\omega}=\left( \hat{\omega_P}, \hat{\omega_D} \right)` that
    maximizes the stepsizes :math:`\left( \alpha_P, \alpha_D \right)` in the
    primal and dual directions of :math:`\Delta = \Delta_a +
    \Delta_c^{\omega}`, respectively.

    A new iterate is then computed using a step reduction factor
    :math:`\alpha_0 = 0.99995`:

    .. math::
        \begin{array}{cl}
        (x_{k+1},s_{k+1},y_{k+1},z_{k+1},w_{k+1}) \quad = &
        (x_k,s_k,y_k,z_k,w_k)+\\
        & \quad \alpha_0 \left( \alpha_P \Delta x, \alpha_P \Delta s,
        \alpha_D \Delta y, \alpha_D \Delta z, \alpha_D \Delta w \right)
        \end{array}


    In addition to the weighted Mehrotra predictor-corrector, `sparse_lp`
    also uses multiple centrality correctors to enlarge the primal-dual
    stepsizes per iteration step and to reduce the overall number of
    iterations required to solve an LP problem. The maximum number of
    centrality corrections depends on the ratio of the factorization and
    solve efforts for system (2) and is therefore problem dependent. For a
    detailed description of multiple centrality correctors, refer to [1]_.

    The linear system (2) can be reduced to more compact forms, the
    augmented system (AS)

    .. math::
        \begin{bmatrix}
            -\Theta^{-1} & A^T\\
                       A & 0
        \end{bmatrix}
        \begin{bmatrix}
            \Delta x\\
            \Delta y
        \end{bmatrix}
        =
        \begin{bmatrix}
            r\\
            h
        \end{bmatrix}
        \quad (3)

    or further by elimination of  :math:`\Delta x` to the normal equations
    (NE) system

    .. math::
        A \Theta A^T \Delta y = A \Theta r + h, \quad (4)

    where

    .. math::
        \Theta = \left( X^{-1}Z+S^{-1}W \right)^{-1}, r = r_c-X^{-1}r_{xz}
        +S^{-1}r_{ws}-S^{-1}Wr_u, h=r_b.

    The matrix on the left-hand side of (3), which is symmetric indefinite,
    can be transformed into a symmetric quasidefinite matrix by regularization.
    Since these types of matrices allow for a Cholesky-like factorization, the
    resulting linear system can be solved easily for
    :math:`(\Delta x, \Delta y)` by triangular substitutions. For more
    information on the regularization technique, see [3]_.
    For the NE system, matrix :math:`A \Theta A^T` is positive definite, and
    therefore a sparse Cholesky algorithm can be used to factor
    :math:`A \Theta A^T` and solve the system for :math:`\Delta y` by
    triangular substitutions with the Cholesky factor *L*.

    In function `sparse_lp`, both approaches are implemented. The AS approach
    is chosen if *A* contains dense columns, if there is a considerable number
    of columns in *A* that are much denser than the remaining ones or if there
    are many more rows than columns in the structural part of *A*. Otherwise,
    the NE approach is selected.

    Function `sparse_lp` stops with optimal termination status if the current
    iterate satisfies the following three conditions:

    .. math::
        \begin{array}{rl}
        \frac{\mu}{1+0.5(|c^Tx|+|b^Ty-u^Tw|)} & \le \texttt{opt_tol},\\[1ex]
        \frac{\|(b-Ax,x+s-u)\|}{1+\|(b,u)\|} &
            \le \texttt{primal_infeas_tol}, \\[1ex]
        \frac{\|c-A^Ty-z+w\|}{1+\|c\|} & \le \texttt{dual_infeas_tol},
        \end{array}

    where `primal_infeas_tol`, `dual_infeas_tol` and `opt_tol` are primal
    infeasibility, dual infeasibility and optimality tolerances, respectively.
    The default value is 1.0e-10 for opt_tol and 1.0e-8 for the other two
    tolerances.

    Function `sparse_lp` is based on the code HOPDM developed by Jacek Gondzio
    et al., see [2]_.

    References
    ----------
    .. [1] Gondzio, Jacek (1994), *Multiple Centrality Corrections in a
           Primal-Dual Method for Linear Programming*, Logilab Technical
           Report 1994.20, Logilab, HEC Geneva, Section of Management
           Studies, Geneva.

    .. [2] Gondzio, Jacek (1995), *HOPDM - Modular Solver for LP Problems*,
           User's Guide to version 2.12, WP-95-50, International Institute
           for Applied Systems Analysis, Laxenburg, Austria.

    .. [3] Altman, Anna, and Jacek Gondzio (1998), *Regularized Symmetric
           Indefinite Systems in Interior Point Methods for Linear and
           Quadratic Optimization*, Logilab Technical Report 1998.6,
           Logilab, HEC Geneva, Section of Management Studies, Geneva.

    Examples
    --------
    The linear programming problem

    .. math::
        \min f(x) =  2x_1-8x_2+3x_3 \\
        \text{subject to} \quad  x_1 + 3x_2 \le 3 \\
                    2x_2+3x_3 \le 6 \\
                    x_1+x_2+x_3 \ge 2 \\
                    -1 \le x_1 \le 5\\
                    0 \le x_2 \le 7\\
                    0 \le x_3 \le 9

    is solved.

    >>> import numpy as np
    >>> from scipy.sparse import coo_matrix
    >>> from imsl.optimize import sparse_lp
    >>> row = np.array([0, 0, 1, 1, 2, 2, 2])
    >>> col = np.array([0, 1, 1, 2, 0, 1, 2])
    >>> val = np.array([1.0, 3.0, 2.0, 3.0, 1.0, 1.0, 1.0])
    >>> bl = np.array([3.0, 6.0, 2.0])
    >>> bu = None
    >>> constr_type = np.array([1, 1, 2])
    >>> b = (bl, bu, constr_type)
    >>> c = np.array([2.0, -8.0, 3.0])
    >>> xlb = np.array([-1.0, 0.0, 0.0])
    >>> xub = np.array([5.0, 7.0, 9.0])
    >>> xb = (xlb, xub)
    >>> # Create matrix in SCS (COO) format
    >>> a = coo_matrix((val, (row, col)))
    >>> lp_result = sparse_lp(a, b, c, xb)
    >>> np.set_printoptions(precision=3)
    >>> print("Solution vector:\n")
    ... #doctest: +NORMALIZE_WHITESPACE
    Solution vector:
    >>> print(str(lp_result.sol)) #doctest: +NORMALIZE_WHITESPACE
    [-0.375  1.125  1.25 ]
    >>> print("\nOptimal objective value: {0:10.4f}".format
    ...       (lp_result.obj)) #doctest: +NORMALIZE_WHITESPACE
    Optimal objective value:    -6.0000

    .. _COO: http://docs.scipy.org/doc/scipy/reference/generated/
             scipy.sparse.coo_matrix.html#scipy.sparse.coo_matrix

    .. _CSC: http://docs.scipy.org/doc/scipy/reference/generated/
             scipy.sparse.csc_matrix.html#scipy.sparse.csc_matrix

    """
    if c is None:
        raise TypeError("None not supported")

    _c = _numpy.asarray(c, dtype=_numpy.float64, order='C')

    if _c.ndim != 1:
        raise ValueError("array of dimension {} not"
                         " supported".format(_c.ndim))

    if _c.size == 0:
        raise ValueError("empty array not supported")

    ncol = _c.size

    if a is None:
        # No constraint matrix exists
        _m_a = 0
        _n_a = ncol
    else:
        if not (isinstance(a, coo_matrix) or isinstance(a, csc_matrix)):
            raise TypeError("Type of constraint matrix not supported")

        if isinstance(a, coo_matrix):
            if (a.data is None) or (a.row is None) or (a.col is None):
                raise TypeError("None not supported")

        if isinstance(a, csc_matrix):
            if (a.data is None) or (a.indices is None) or (a.indptr is None):
                raise TypeError("None not supported")

        # Transform constraint matrix into CSC format; transforming
        # into triplet format is more memory consuming
        if isinstance(a, coo_matrix):
            _a = a.tocsc()
        else:
            _a = a

        _nnz_a = _a.nnz
        _m_a = _a.shape[0]
        _n_a = _a.shape[1]
        _a_rows = _a.indices
        _a_indptr = _a.indptr
        _a_data = _a.data

        # Check validity of constraint matrix
        if _m_a != 0 and _n_a != ncol:
            raise ValueError("Constraint matrix has wrong column dimension")

    # Treat case of non-existing constraint matrix separately
    if _m_a == 0:
        _a_rows = None
        _a_indptr = None
        _a_data = None
        _nnz_a = 0
    else:
        # Transform constraint matrix into correct type required by CNL
        # Note: _a_data/_a_rows can contain millions of entries
        # Therefore, error checks of the entries in _a_rows and _a_indptr
        # are only done inside the CNL function
        _a_rows = _numpy.asarray(_a_rows, dtype=_numpy.int32, order='C')
        _a_indptr = _numpy.asarray(_a_indptr, dtype=_numpy.int32, order='C')
        _a_data = _numpy.asarray(_a_data, dtype=_numpy.float64, order='C')

        if _a_rows.ndim != 1:
            raise ValueError("array of dimension {} not"
                             " supported".format(_a_rows.ndim))

        if _a_rows.size < _nnz_a:
            raise ValueError("array of row subscripts of the constraint "
                             "matrix must be at least as large as the number "
                             "of nonzeros in the constraint matrix")

        # Correct dimension of _a_ind_ptr is already checked by the line
        # _nnz_a = _a.nnz
        # above.

        if _a_indptr.size < _n_a + 1:
            raise ValueError("the index vector of the constraint matrix"
                             " must be larger than the number of columns in"
                             " the constraint matrix")

        if _a_data.ndim != 1:
            raise ValueError("array of dimension {} not"
                             " supported".format(_a_data.ndim))

        if _a_data.size < _nnz_a:
            raise ValueError("the array of numerical values of the constraint"
                             " matrix must be at least as large as the number"
                             " of nonzeros in the constraint matrix")

    # Constraint bounds
    if _m_a == 0:
        _bl = None
        _bu = None
        _constr_type = None
    else:
        if b is None:
            raise TypeError("None not supported")

        if len(b) != 3:
            raise TypeError("variable b has incorrect size")

        bl = b[0]
        bu = b[1]
        constr_type = b[2]

        if (bl is None) or (constr_type is None):
            raise TypeError("None not supported")

        if _numpy.isscalar(bl):
            _bl_val = _numpy.float64(bl)
            _bl = _numpy.empty((_m_a,), dtype=_numpy.float64)
            _bl[0:] = _bl_val
        else:
            # Prepare array of lower bounds
            _bl = _numpy.asarray(bl, dtype=_numpy.float64, order='C')

            if _bl.ndim != 1:
                raise ValueError("array of dimension {} not"
                                 " supported".format(_bl.ndim))
            if _bl.size < _m_a:
                raise ValueError("array of lower constraint bounds too short")

        # Prepare array of constraint types
        is_two_sided = False
        if _numpy.isscalar(constr_type):
            _constr_type_val = int(constr_type)
            if _constr_type_val not in range(5):
                raise ValueError("constraint type value not feasible")
            if _constr_type_val == 0:
                _constr_type = None
            else:
                _constr_type = _numpy.empty((_m_a,), dtype=_numpy.int32)
                _constr_type[0:] = _constr_type_val
                if _constr_type_val == 3:
                    is_two_sided = True
        else:
            _constr_type = _numpy.asarray(constr_type, dtype=_numpy.int32,
                                          order='C')

            if _constr_type.ndim != 1:
                raise ValueError("array of dimension {} not"
                                 " supported".format(_constr_type.ndim))

            if _constr_type.size < _m_a:
                raise ValueError("array of constraint types too short")

        # Check entries in array _constr_type
            for i in range(_m_a):
                if _constr_type[i] not in range(5):
                    raise ValueError("constraint type value not feasible")
                elif _constr_type[i] == 3:
                    # assumes that two-sided bounds are always finite
                    is_two_sided = True

        # Prepare array of upper bounds
        if not is_two_sided:
            _bu = None
        else:
            if (bu is None):
                raise TypeError("None not supported")

            if _numpy.isscalar(bu):
                _bu_val = _numpy.float64(bu)
                _bu = _numpy.empty((_m_a,), dtype=_numpy.float64)
                _bu[0:] = _bu_val
            else:
                _bu = _numpy.asarray(bu, dtype=_numpy.float64, order='C')

                if _bu.ndim != 1:
                    raise ValueError("array of dimension {} not"
                                     " supported".format(_bu.ndim))
                if _bu.size < _m_a:
                    raise ValueError("array of upper constraint bounds too"
                                     " short")

        # Check for Nan, inf and inconsistencies
        if is_two_sided:
            for i in range(_m_a):
                if _numpy.isnan(_bl[i]):
                    raise ValueError("array of lower constraint bounds "
                                     "contains NaNs")
                elif _numpy.isinf(_bl[i]):
                    raise ValueError("array of lower constraint bounds "
                                     "contains infinite values")
                if _constr_type[i] == 3:
                    if _numpy.isnan(_bu[i]):
                        raise ValueError("array of upper constraint bounds "
                                         "contains NaNs")
                    elif _numpy.isinf(_bu[i]):
                        raise ValueError("array of upper constraint bounds "
                                         "contains infinite values")
                    if _bl[i] > _bu[i]:
                        raise ValueError("the constraint bounds are "
                                         "inconsistent.")
        else:
            for i in range(_m_a):
                if _numpy.isnan(_bl[i]):
                    raise ValueError("array of lower constraint bounds "
                                     "contains NaNs")
                elif _numpy.isinf(_bl[i]):
                    raise ValueError("array of lower constraint bounds "
                                     "contains infinite values")

    # Prepare variable bounds
    if xb is None:
        _xl = None
        _xu = None
    else:
        if len(xb) != 2:
            raise TypeError("argument xb has incorrect length")

        xl = xb[0]
        xu = xb[1]

        if (xl is None) or (xu is None):
            raise TypeError("None not supported")

        if _numpy.isscalar(xl):
            _xl_val = _numpy.float64(xl)

            # Check for Nan, inf and inconsistencies
            if _numpy.isnan(_xl_val):
                raise ValueError("lower variable bound is NaN")
            elif _numpy.isinf(_xl_val):
                raise ValueError("lower variable bound is infinite")

            if _xl_val == 0.0:
                _xl = None
            else:
                _xl = _numpy.empty((ncol,), dtype=_numpy.float64)
                _xl[0:] = _xl_val
        else:
            _xl = _numpy.asarray(xl, dtype=_numpy.float64, order='C')

            if _xl.ndim != 1:
                raise ValueError("array of dimension {} not"
                                 " supported".format(_xl.ndim))
            if _xl.size < ncol:
                raise ValueError("array of lower variable bounds too short")

            # Check for Nan, inf and inconsistencies
            for i in range(ncol):
                if _numpy.isnan(_xl[i]):
                    raise ValueError("array of lower variable bounds contains"
                                     " NaNs")
                elif _numpy.isinf(_xl[i]):
                    raise ValueError("array of lower variable bounds contains"
                                     " infinite values")

        if _numpy.isscalar(xu):
            _xu_val = _numpy.float64(xu)

            # Check for Nan, inf and inconsistencies
            if _numpy.isnan(_xu_val):
                raise ValueError("upper variable bound is NaN")
            elif _numpy.isinf(_xu_val):
                raise ValueError("upper variable bound is infinite")

            if _xu_val == constants.UNBOUNDED_ABOVE:
                _xu = None
            else:
                _xu = _numpy.empty((ncol,), dtype=_numpy.float64)
                _xu[0:] = _xu_val
        else:
            _xu = _numpy.asarray(xu, dtype=_numpy.float64, order='C')

            if _xu.ndim != 1:
                raise ValueError("array of dimension {} not"
                                 " supported".format(_xu.ndim))
            if _xu.size < ncol:
                raise ValueError("array of upper variable bounds too short")

            # Check for Nan, inf and inconsistencies
            for i in range(ncol):
                if _numpy.isnan(_xu[i]):
                    raise ValueError("array of upper variable bounds contains"
                                     " NaNs")
                elif _numpy.isinf(_xu[i]):
                    raise ValueError("array of upper variable bounds contains"
                                     " infinite values")

        # Check for inconsistent variable bounds
        if (_xl is not None) and (_xu is not None):
            for i in range(ncol):
                if (_xl[i] > _xu[i]):
                    raise ValueError("the bounds on the variable constraints"
                                     " are inconsistent")
        elif _xl is not None:
            for i in range(ncol):
                if (_xl[i] > constants.UNBOUNDED_ABOVE):
                    raise ValueError("the bounds on the variable constraints"
                                     " are inconsistent")
        elif _xu is not None:
            for i in range(ncol):
                if (_xu[i] < 0.0):
                    raise ValueError("the bounds on the variable constraints"
                                     " are inconsistent")

    _obj_constant = float(obj_constant)

    _preorder = int(preorder)

    if _preorder not in (0, 1):
        raise ValueError("preorder must be 0 or 1")

    _presolve = int(presolve)

    if _presolve not in range(7):
        raise ValueError("presolve must be an int in the interval [0,...,6]")

    _max_iter = int(max_iter)
    if _max_iter <= 0:
        raise ValueError("max_iter must be greater than zero")

    _opt_tol = float(opt_tol)

    if (_opt_tol <= 0.0):
        raise ValueError("opt_tol must be greater than zero")

    _primal_infeas_tol = float(primal_infeas_tol)

    if (_primal_infeas_tol <= 0.0):
        raise ValueError("primal_infeas_tol must be greater than zero")

    _dual_infeas_tol = float(dual_infeas_tol)

    if (_dual_infeas_tol <= 0.0):
        raise ValueError("dual_infeas_tol must be greater than zero")

    # Generate output arrays/scalars
    _sol = _numpy.empty(ncol, dtype=_numpy.float64)
    _obj = _ctypes.c_double()
    _dual = _numpy.empty(max(1, _m_a), dtype=_numpy.float64)
    _n_iter = _ctypes.c_int32()
    _err_b = _ctypes.c_double()
    _err_u = _ctypes.c_double()
    _err_c = _ctypes.c_double()
    _cp_smallest = _ctypes.c_double()
    _cp_largest = _ctypes.c_double()

    args = []
    # Prepare required input argument list
    args.append(_ctypes.c_int32(_m_a))
    args.append(_ctypes.c_int32(ncol))
    args.append(_ctypes.c_int32(_nnz_a))
    args.append(_ctypes.POINTER(_ctypes.c_void_p)())
    if _bl is None:
        args.append(_ctypes.POINTER(_ctypes.c_void_p)())
    else:
        args.append(_bl.ctypes.data_as(_ctypes.c_void_p))
    args.append(_c.ctypes.data_as(_ctypes.c_void_p))

    # Add the optional input arguments
    if _constr_type is not None:
        args.append(_constants.IMSL_CONSTR_TYPE)
        args.append(_constr_type.ctypes.data_as(_ctypes.c_void_p))

    if _bu is not None:
        args.append(_constants.IMSL_UPPER_LIMIT)
        args.append(_bu.ctypes.data_as(_ctypes.c_void_p))

    if _xl is not None:
        args.append(_constants.IMSL_LOWER_BOUND)
        args.append(_xl.ctypes.data_as(_ctypes.c_void_p))

    if _xu is not None:
        args.append(_constants.IMSL_UPPER_BOUND)
        args.append(_xu.ctypes.data_as(_ctypes.c_void_p))

    args.append(_constants.IMSL_OBJ_CONSTANT)
    args.append(_ctypes.c_double(_obj_constant))
    args.append(_constants.IMSL_PREORDERING)
    args.append(_ctypes.c_int32(_preorder))
    args.append(_constants.IMSL_MAX_ITERATIONS)
    args.append(_ctypes.c_int32(_max_iter))
    args.append(_constants.IMSL_OPT_TOL)
    args.append(_ctypes.c_double(_opt_tol))
    args.append(_constants.IMSL_PRINF_TOL)
    args.append(_ctypes.c_double(_primal_infeas_tol))
    args.append(_constants.IMSL_DLINF_TOL)
    args.append(_ctypes.c_double(_dual_infeas_tol))
    args.append(_constants.IMSL_PRESOLVE)
    args.append(_ctypes.c_int32(_presolve))
    args.append(_constants.IMSL_CSC_FORMAT)
    if _m_a == 0:
        args.append(_ctypes.POINTER(_ctypes.c_void_p)())
        args.append(_ctypes.POINTER(_ctypes.c_void_p)())
        args.append(_ctypes.POINTER(_ctypes.c_void_p)())
    else:
        args.append(_a_indptr.ctypes.data_as(_ctypes.c_void_p))
        args.append(_a_rows.ctypes.data_as(_ctypes.c_void_p))
        args.append(_a_data.ctypes.data_as(_ctypes.c_void_p))

    # Add the output arguments
    args.append(_constants.IMSL_OBJ)
    args.append(_ctypes.byref(_obj))
    args.append(_constants.IMSL_ITERATION_COUNT)
    args.append(_ctypes.byref(_n_iter))
    args.append(_constants.IMSL_DUAL_USER)
    args.append(_dual.ctypes.data_as(_ctypes.c_void_p))
    args.append(_constants.IMSL_PRIMAL_INFEAS)
    args.append(_ctypes.byref(_err_b))
    args.append(_ctypes.byref(_err_u))
    args.append(_constants.IMSL_DUAL_INFEAS)
    args.append(_ctypes.byref(_err_c))
    args.append(_constants.IMSL_CP_RATIO_SMALLEST)
    args.append(_ctypes.byref(_cp_smallest))
    args.append(_constants.IMSL_CP_RATIO_LARGEST)
    args.append(_ctypes.byref(_cp_largest))
    args.append(_constants.IMSL_RETURN_USER)
    args.append(_sol.ctypes.data_as(_ctypes.c_void_p))

    args.append(0)

    func = _sparse_lp_func(_c.dtype)
    func(*args)

    result = _collections.namedtuple("SparseLPResults",
                                     ["sol",
                                      "obj",
                                      "dual",
                                      "n_iter",
                                      "infeas",
                                      "cp_ratios"]
                                     )

    result.sol = _sol
    result.obj = _obj.value
    if _m_a == 0:
        result.dual = None
    else:
        result.dual = _dual
    result.n_iter = _n_iter.value
    result.infeas = (_err_b.value, _err_u.value, _err_c.value)
    result.cp_ratios = (_cp_smallest.value, _cp_largest.value)

    return result
