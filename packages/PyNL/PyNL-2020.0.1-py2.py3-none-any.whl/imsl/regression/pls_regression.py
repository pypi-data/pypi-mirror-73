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
"""pls_regression related functions."""
import ctypes as _ctypes
import numpy as _numpy

import imsl._constants as _constants
import imsl._imsllib as _imsllib
import collections as _collections


def _pls_regression_func(dtype):
    """Return the IMSL pls_regression function appropriate for dtype.

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
        return _imsllib.imsls_d_pls_regression
    else:
        return None


def pls_regression(y, x, n_components=None, cross_validation=True, n_fold=5,
                   scale=False):
    r"""Perform partial least squares (PLS) regression.

    Parameters
    ----------
    y : *(ny,h) array_like*
        Array of size *ny* :math:`\times` *h* containing the response
        variables.
    x : *(nx,p) array_like*
        Array of size *nx* :math:`\times` *p* containing the predictor
        variables.
    n_components : *int, optional*
        The number of PLS components to fit.

        Default: `n_components` = `p`.
    cross_validation : *boolean, optional*
        If *True*, the function performs *K*-fold cross validation to select
        the number of components. If *False*, the function fits only the model
        specified by `n_components`.

    n_fold : *int, optional*
        The number of folds to use in the cross validation.

    scale : *boolean, optional*
        If *False*, `y` and `x` are centered to have mean 0 but are not scaled.
        If *True*, `y` and `x` are scaled to have mean 0 and standard
        deviation 1.

    Returns
    -------
    A named tuple with the following fields:

    coef : *(p, h) ndarray*
        Array containing the final PLS regression coefficient estimates.

    residuals : *(min(ny, nx), h) ndarray*
        Array containing residuals of the final fit for each response variable.

    std_errors : *(p, h) ndarray*
        Array containing the standard errors of the PLS coefficients.

    press : *(n_components, h) ndarray*
        Array containing the predicted residual error sum of squares obtained
        by cross-validation for each model of size `j=1,...,n_components`
        components. This argument is set to *None*, if `cross_validation` =
        *False*.

    x_scores : *(min(ny, nx), n_components) ndarray*
        Array containing `X`- scores.

    y_scores : *(min(ny, nx), n_components) ndarray*
        Array containing `Y`- scores.

    x_loadings : *(p, n_components) ndarray*
        Array containing `X`- loadings.

    y_loadings : *(h, n_components) ndarray*
        Array containing `Y`- loadings.

    weights : *(p, n_components) ndarray*
        Array containing the weight vectors.

    Notes
    -----
    Function `pls_regression` performs partial least squares regression for a
    response matrix :math:`Y(n_y \times h)` and a set of `p` explanatory
    variables, :math:`X(n_x \times p)`. `pls_regression` finds linear
    combinations of the predictor variables that have highest covariance with
    `Y`. In so doing, `pls_regression` produces a predictive model for `Y`
    using components (linear combinations) of the individual predictors. Other
    names for these linear combinations are scores, factors, or latent
    variables. Partial least squares regression is an alternative method to
    ordinary least squares for problems with many, highly collinear predictor
    variables. For further discussion see, for example, [1]_ and [3]_.

    In Partial Least Squares (PLS), a score, or component matrix, `T`, is
    selected to represent both `X` and `Y`, as in

    .. math::
        X = TP^T + E_x

    and

    .. math::
       Y = TQ^T + E_y .

    The matrices `P` and `Q` are the least squares solutions of `X` and
    `Y` regressed on `T`.

    That is,

    .. math::
        P^T = \left( T^T T \right)^{-1}T^TX

    and

    .. math::
        Q^T = \left( T^T T \right)^{-1}T^TY .

    The columns of `T` in the above relations are often called `X`-scores,
    while the columns of `P` are the `X`-loadings. The columns of the
    matrix `U` in :math:`Y = UQ^T + G` are the corresponding `Y` scores, where
    `G` is a residual matrix and `Q`, as defined above, contains the
    `Y`-loadings.

    Restricting `T` to be linear in `X`, the problem is to find a set of
    weight vectors (columns of `W`) such that `T = XW` predicts both
    `X` and `Y` reasonably well.

    Formally, :math:`w=[w_1,\ldots,w_{m-1},w_m,\ldots,w_M],` where each
    :math:`w_j` is a column vector of length :math:`p`, :math:`M \le p`
    is the number of components, and where the `m`-th partial least
    squares (PLS) component :math:`w_m` solves:

    .. math::
        \left\{ \begin{array}{c}
        \max_\alpha \text{Corr}^2(Y,X\alpha)\text{Var}(X \alpha)\\
        s.t.\\
        \|\alpha\| = 1\\
        \alpha^T S w_l = 0, l=1,\ldots,m-1
        \end{array} \right.

    where :math:`S=X^TX` and
    :math:`\| \alpha \|=\sqrt{\alpha^T \alpha}` is
    the Euclidean norm. For further details, see [4]_, pages 80-82.

    That is, :math:`w_m` is the vector that maximizes the product of the
    squared correlation between `Y` and :math:`X \alpha` and the variance
    of :math:`X\alpha`, subject to being orthogonal to each previous weight
    vector left multiplied by `S`. The PLS regression coefficients
    :math:`\hat{\beta}_{PLS}` arise from

    .. math::
        Y = X \hat{\beta}_{PLS}+E_y = TQ^T + E_y = XWQ^T + E_y, \quad
        \text{or} \quad \hat{\beta}_{PLS} = WQ^T.

    Algorithms to solve the above optimization problem include NIPALS
    (nonlinear iterative partial least squares) developed by Herman Wold
    (1966, 1985) and numerous variations, including the SIMPLS algorithm
    of de Jong ([2]_). `pls_regression` implements the SIMPLS method.
    SIMPLS is appealing because it finds a solution in terms of the original
    predictor variables, whereas NIPALS reduces the matrices at each step.
    For univariate `Y` it has been shown that SIMPLS and NIPALS are equivalent
    (the score, loading, and weights matrices will be proportional between
    the two methods).

    By default, `pls_regression` searches for the best number of PLS components
    using `K`-fold cross-validation. That is, for each
    :math:`M = 1, 2, \ldots, p,` `pls_regression` estimates a PLS model with
    `M` components using all of the data except a hold-out set of size roughly
    equal to `nobs`/`k`, where `nobs` = min(*nx*, *ny*). Using the resulting
    model estimates, `pls_regression` predicts the outcomes in the hold-out set
    and calculates the predicted residual sum of squares (PRESS). The procedure
    then selects the next hold-out sample and repeats for a total of `K` times
    (i.e., folds). For further details see [4]_, pages 241-245.

    For each response variable, `pls_regression` returns results for the model
    with lowest PRESS. The best model (the number of components giving lowest
    PRESS), generally will be different for different response variables.

    References
    ----------
    .. [1] Abdi, Herve (2010), *Partial least squares regression and
           projection on latent structure regression (PLS regression)*,
           Wiley Interdisciplinary Reviews: Computational Statistics, 2,
           97-106.

    .. [2] de Jong, Sijmen (1993), *SIMPLS: An alternative approach to partial
           least squares regression*, Chemometrics and Intelligent Laboratory
           Systems, 18, 251-263.

    .. [3] Frank, Ildiko E., and Jerome J. Friedman (1993), *A Statistical
           View of Some Chemometrics Regression Tools*, Technometrics,
           Volume 35, Issue 2, pp. 109-135.

    .. [4] Hastie, Trevor, Tibshirani, Robert, and Friedman, Jerome (2009),
           *The Elements of Statistical Learning: Data Mining, Inference,
           and Prediction*, 2nd ed., Springer, New York.

    .. [5] Wold, Svante, Michael Sjostrom, and Lennart Eriksson (2001),
           *PLS-regression: a basic tool of chemometrics*, Chemometrics and
           Intelligent Laboratory Systems, Volume 58, 109-130.

    Examples
    --------
    *Example 1:*

    The following artificial data set is provided in [2]_:

    .. math::
        X = \begin{bmatrix}
            -4 & 2 & 1\\
            -4 & -2 & -1\\
             4 &  2 & -1\\
             4 & -2 & 1
            \end{bmatrix} \; , \quad
        Y = \begin{bmatrix}
             430 & -94\\
            -436 & 12\\
            -361 & -22\\
             367 & 104
            \end{bmatrix}

    The first call to `pls_regression` fixes the number of components to 3 for
    both response variables, and the second call performs *K*-fold cross
    validation. Note that because the number of folds is equal to `nobs`
    = min(*nx*, *ny*), `pls_regression` performs leave-one-out (LOO)
    cross-validation.

    >>> import numpy as np
    >>> import warnings
    >>> from imsl.regression import pls_regression
    >>> x = np.array([[-4.0,  2.0,  1.0],
    ...              [-4.0, -2.0, -1.0],
    ...              [4.0,   2.0, -1.0],
    ...              [4.0,  -2.0,  1.0]])
    >>> y = np.array([[430.0, -94.0],
    ...              [-436.0, 12.0],
    ...              [-361.0, -22.0],
    ...              [367.0, 104.0]])
    >>> with warnings.catch_warnings(record=True):
    ...    result = pls_regression(y, x, n_components=3,
    ...                            cross_validation=False)
    >>> np.set_printoptions(precision=1)
    >>> print("Example 1a: no cross-validation")
    ... # doctest: +NORMALIZE_WHITESPACE
    Example 1a: no cross-validation
    >>> print("\nPLS Coefficients:") # doctest: +NORMALIZE_WHITESPACE
    <BLANKLINE>
    PLS Coefficients:
    >>> print(result.coef) # doctest: +SKIP
    >>> print("\nPredicted Y:")
    <BLANKLINE>
    Predicted Y:
    >>> print(y-result.residuals) # doctest: +SKIP
    >>> print("\nStd. Errors:")
    <BLANKLINE>
    Std. Errors:
    >>> print(result.std_errors) # doctest: +SKIP
    >>> with warnings.catch_warnings(record=True):
    ...    result2 = pls_regression(y, x, n_components=3,
    ...                             cross_validation=True,
    ...                             n_fold=y.shape[0])
    >>> print("\n\nExample 1b: cross-validation")
    ... # doctest: +NORMALIZE_WHITESPACE
    <BLANKLINE>
    <BLANKLINE>
    Example 1b: cross-validation
    >>> print("\nPLS Coefficients:") # doctest: +NORMALIZE_WHITESPACE
    <BLANKLINE>
    PLS Coefficients:
    >>> print(result2.coef) # doctest: +NORMALIZE_WHITESPACE
    [[ 15.9  12.7]
     [ 49.2 -23.9]
     [371.1   0.6]]
    >>> print("\nPredicted Y:") # doctest: +NORMALIZE_WHITESPACE
    <BLANKLINE>
    Predicted Y:
    >>> print(y-result2.residuals) # doctest: +NORMALIZE_WHITESPACE
    [[ 405.8 -97.8]
     [-533.3  -3.5]
     [-208.8   2.2]
     [ 336.4  99.1]]
    >>> print("\nStd. Errors:") # doctest: +NORMALIZE_WHITESPACE
    <BLANKLINE>
    Std. Errors:
    >>> print(result2.std_errors) # doctest: +NORMALIZE_WHITESPACE
    [[134.1  7.1]
     [269.9  3.8]
     [478.5 19.5]]

    *Example 2:*

    The data, as appears in [5]_, is a single response variable, the "free
    energy of the unfolding of a protein", while the predictor variables are 7
    different, highly correlated measurements taken on 19 amino acids.

    >>> import numpy as np
    >>> from imsl.regression import pls_regression
    >>> x = np.array([[0.23,  0.31,  -0.55,  254.2,  2.126,  -0.02,   82.2],
    ...              [-0.48,  -0.6,   0.51,  303.6,  2.994,  -1.24,  112.3],
    ...              [-0.61, -0.77,    1.2,  287.9,  2.994,  -1.08,  103.7],
    ...              [ 0.45,  1.54,   -1.4,  282.9,  2.933,  -0.11,   99.1],
    ...              [-0.11, -0.22,   0.29,  335.0,  3.458,  -1.19,  127.5],
    ...              [-0.51, -0.64,   0.76,  311.6,  3.243,  -1.43,  120.5],
    ...              [  0.0,   0.0,    0.0,  224.9,  1.662,   0.03,   65.0],
    ...              [ 0.15,  0.13,  -0.25,  337.2,  3.856,  -1.06,  140.6],
    ...              [  1.2,   1.8,   -2.1,  322.6,   3.35,   0.04,  131.7],
    ...              [ 1.28,   1.7,   -2.0,  324.0,  3.518,   0.12,  131.5],
    ...              [-0.77, -0.99,   0.78,  336.6,  2.933,  -2.26,  144.3],
    ...              [  0.9,  1.23,   -1.6,  336.3,   3.86,  -0.33,  132.3],
    ...              [ 1.56,  1.79,   -2.6,  366.1,  4.638,  -0.05,  155.8],
    ...              [ 0.38,  0.49,   -1.5,  288.5,  2.876,  -0.31,  106.7],
    ...              [  0.0, -0.04,   0.09,  266.7,  2.279,   -0.4,   88.5],
    ...              [ 0.17,  0.26,  -0.58,  283.9,  2.743,  -0.53,  105.3],
    ...              [ 1.85,  2.25,   -2.7,  401.8,  5.755,  -0.31,  185.9],
    ...              [ 0.89,  0.96,   -1.7,  377.8,  4.791,  -0.84,  162.7],
    ...              [ 0.71,  1.22,   -1.6,  295.1,  3.054,  -0.13,  115.6]])
    >>> y = np.array([8.5, 8.2, 8.5, 11.0, 6.3, 8.8, 7.1,
    ...               10.1, 16.8, 15.0, 7.9, 13.3, 11.2,
    ...               8.2, 7.4, 8.8, 9.9, 8.8, 12.0])
    >>> result = pls_regression(y, x, n_components=7, cross_validation=False,
    ...                         scale=True)
    >>> np.set_printoptions(precision=2)
    >>> print("Example 2a: no cross-validation")
    ... # doctest: +NORMALIZE_WHITESPACE
    Example 2a: no cross-validation
    >>> print("\nPLS Coefficients:") # doctest: +NORMALIZE_WHITESPACE
    <BLANKLINE>
    PLS Coefficients:
    >>> print(result.coef) # doctest: +SKIP
    >>> print("\nPredicted Y:")
    <BLANKLINE>
    Predicted Y:
    >>> print(y-result.residuals) # doctest: +SKIP
    >>> np.set_printoptions(precision=4)
    >>> print("\nStd. Errors:")
    <BLANKLINE>
    Std. Errors:
    >>> print(result.std_errors) # doctest: +SKIP
    >>> np.set_printoptions(precision=2)
    >>> result2 = pls_regression(y, x, n_components=7, scale=True)
    >>> print("\n\nExample 2b: cross-validation")
    ... # doctest: +NORMALIZE_WHITESPACE
    <BLANKLINE>
    <BLANKLINE>
    Example 2b: cross-validation
    >>> print("\nPLS Coefficients:") # doctest: +NORMALIZE_WHITESPACE
    <BLANKLINE>
    PLS Coefficients:
    >>> print(result2.coef) # doctest: +SKIP
    [[ 5.87e-01]
     [ 6.00e-01]
     [-3.80e-01]
     [ 6.03e-04]
     [-3.88e-02]
     [ 7.09e-01]
     [ 2.77e-03]]
    >>> print("\nPredicted Y:") # doctest: +NORMALIZE_WHITESPACE
    <BLANKLINE>
    Predicted Y:
    >>> print(y-result2.residuals[:,0]) # doctest: +SKIP
    [  9.86   7.71   7.35  11.02   8.32   7.46   9.32   9.    12.09  12.09
       6.59  11.11  12.46  10.27   9.02   9.51  12.82  10.69  11.09]
    >>> np.set_printoptions(precision=4)
    >>> print("\nStd. Errors:") # doctest: +NORMALIZE_WHITESPACE
    <BLANKLINE>
    Std. Errors:
    >>> print(result2.std_errors) # doctest: +SKIP
    [[0.2212]
     [0.4183]
     [0.1292]
     [0.0036]
     [0.214 ]
     [0.3021]
     [0.0087]]


    """
    if y is None:
        raise TypeError("None not supported")

    if x is None:
        raise TypeError("None not supported")

    _y = _numpy.asarray(y, order='C')
    # attempt to promote y to a compatible type.
    ref_type = _numpy.promote_types(_numpy.float64, _y.dtype)
    _y = _numpy.asarray(_y, dtype=ref_type)

    if (not _numpy.issubdtype(_y.dtype, _numpy.float64)):
        raise ValueError("array type {} not supported".format(
                         _y.dtype.name))

    _x = _numpy.asarray(x, dtype=ref_type, order='C')

    # Check dimensions of _y and _x
    if _y.ndim not in (1, 2):
        raise ValueError("array of dimension {} not"
                         " supported".format(_y.ndim))

    if _y.size == 0:
        raise ValueError("empty array not supported")

    if _x.ndim not in (1, 2):
        raise ValueError("array of dimension {} not"
                         " supported".format(_y.ndim))

    if _x.size == 0:
        raise ValueError("empty array not supported")

    ny = _y.shape[0]
    if _y.ndim == 1:
        h = 1
    else:
        h = _y.shape[1]

    nx = _x.shape[0]
    if _x.ndim == 1:
        p = 1
    else:
        p = _x.shape[1]

    if n_components is None:
        _n_components = p
    else:
        _n_components = int(n_components)
        if _n_components < 1 or _n_components > p:
            raise ValueError("n_components must be greater than 0 and less "
                             "than or equal to the number of columns of x")

    _cross_validation = int(cross_validation)
    if _cross_validation not in (0, 1):
        raise ValueError("cross_validation must be True or False")

    _n_fold = int(n_fold)

    if _cross_validation == 1:
        if _n_fold < 2 or _n_fold > min(ny, nx):
            raise ValueError("n_fold must be between 2 and min(ny, nx)")

    _scale = int(scale)
    if _scale not in (0, 1):
        raise ValueError("scale must be True or False")

    args = []
    # Prepare required input argument list
    args.append(_ctypes.c_int(ny))
    args.append(_ctypes.c_int(h))
    args.append(_y.ctypes.data_as(_ctypes.c_void_p))
    args.append(_ctypes.c_int(nx))
    args.append(_ctypes.c_int(p))
    args.append(_x.ctypes.data_as(_ctypes.c_void_p))

    # Now add the optional input arguments
    if n_components is not None:
        args.append(_constants.IMSLS_N_COMPONENTS)
        args.append(_ctypes.c_int(_n_components))

    args.append(_constants.IMSLS_CROSS_VALIDATION)
    args.append(_ctypes.c_int(_cross_validation))

    if _cross_validation == 1:
        args.append(_constants.IMSLS_N_FOLD)
        args.append(_ctypes.c_int(_n_fold))

    if _scale == 1:
        args.append(_constants.IMSLS_SCALE)
        args.append(_ctypes.c_int(_scale))

    nobs = min(nx, ny)
    iy = h
    ix = p
    # Generate output arrays and add them to the argument list
    coef = _numpy.empty((p, h), dtype=ref_type)
    args.append(_constants.IMSLS_RETURN_USER)
    args.append(coef.ctypes.data_as(_ctypes.c_void_p))

    residuals = _numpy.empty((nobs, iy), dtype=ref_type)
    args.append(_constants.IMSLS_RESIDUALS_USER)
    args.append(residuals.ctypes.data_as(_ctypes.c_void_p))

    std_errors = _numpy.empty((ix, iy), dtype=ref_type)
    args.append(_constants.IMSLS_STD_ERRORS_USER)
    args.append(std_errors.ctypes.data_as(_ctypes.c_void_p))

    if _cross_validation == 1:
        press = _numpy.empty((_n_components, iy), dtype=ref_type)
        args.append(_constants.IMSLS_PRESS_USER)
        args.append(press.ctypes.data_as(_ctypes.c_void_p))
    else:
        press = None

    x_scores = _numpy.empty((nobs, _n_components), dtype=ref_type)
    args.append(_constants.IMSLS_X_SCORES_USER)
    args.append(x_scores.ctypes.data_as(_ctypes.c_void_p))

    y_scores = _numpy.empty((nobs, _n_components), dtype=ref_type)
    args.append(_constants.IMSLS_Y_SCORES_USER)
    args.append(y_scores.ctypes.data_as(_ctypes.c_void_p))

    x_loadings = _numpy.empty((ix, _n_components), dtype=ref_type)
    args.append(_constants.IMSLS_X_LOADINGS_USER)
    args.append(x_loadings.ctypes.data_as(_ctypes.c_void_p))

    y_loadings = _numpy.empty((iy, _n_components), dtype=ref_type)
    args.append(_constants.IMSLS_Y_LOADINGS_USER)
    args.append(y_loadings.ctypes.data_as(_ctypes.c_void_p))

    weights = _numpy.empty((ix, _n_components), dtype=ref_type)
    args.append(_constants.IMSLS_WEIGHTS_USER)
    args.append(weights.ctypes.data_as(_ctypes.c_void_p))

    args.append(0)
    func = _pls_regression_func(ref_type)
    func(*args)

    result = _collections.namedtuple("PLS",
                                     ["coef",
                                      "residuals",
                                      "std_errors",
                                      "press",
                                      "x_scores",
                                      "y_scores",
                                      "x_loadings",
                                      "y_loadings",
                                      "weights"]
                                     )
    result.coef = coef
    result.residuals = residuals
    result.std_errors = std_errors
    result.press = press
    result.x_scores = x_scores
    result.y_scores = y_scores
    result.x_loadings = x_loadings
    result.y_loadings = y_loadings
    result.weights = weights
    return result
