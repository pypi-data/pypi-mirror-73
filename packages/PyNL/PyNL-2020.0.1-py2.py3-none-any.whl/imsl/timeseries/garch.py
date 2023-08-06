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
"""Garch related functions."""
import ctypes as _ctypes
import numpy as _numpy

import imsl._constants as _constants
import imsl._imsllib as _imsllib
import collections as _collections


def _garch_func(dtype):
    """Return the IMSL garch function appropriate for dtype.

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
        return _imsllib.imsls_d_garch
    else:
        return None


def garch(p, q, series, guess, max_sigma=10.0):
    r"""Compute parameter estimates of a GARCH model.

    Parameters
    ----------
    p : *int*
        Number of GARCH parameters.

    q : *int*
        Number of ARCH parameters.

    series : *(N,) array_like*
        Array containing the observed time series data.

    guess : *(p+q+1,) array_like*
        Array containing the initial values for the parameter array `x`.

    max_sigma : *float, optional*
        Value of the upper bound on the first element (sigma) of the array
        `x` of returned estimated coefficients.

        Default: `max_sigma` = 10.

    Returns
    -------
    A named tuple with the following fields:

    x : *(p+q+1,) ndarray*
        Array containing the estimated values of sigma squared, followed
        by the `q` ARCH parameters and the `p` GARCH parameters.

    log_likeli : *float*
        Value of the log-likelihood function evaluated at the estimated
        parameter array `x`.

    aic : *float*
        Value of the Akaike Information Criterion (AIC) evaluated at the
        estimated parameter array `x`.

    var : *(p+q+1, p+q+1) ndarray*
        Array of size `(p+q+1)` :math:`\times` `(p+q+1)` containing the
        variance-covariance matrix.

    Notes
    -----
    The Generalized Autoregressive Conditional Heteroskedastic (GARCH) model
    for a time series :math:`{w_t}` is defined as

    .. math::
        w_t = z_t \sigma_t

    .. math::
        \sigma_t^2 = \sigma^2 + \sum_{i=1}^p \beta_i \sigma_{t-i}^2+
        \sum_{i=1}^q \alpha_i w_{t-i}^2 ,

    where :math:`z_t` is a sequence of independent and identically
    distributed standard normal random variables,

    .. math::
        0<\sigma^2< \text{max_sigma}, \beta_i \ge 0, \alpha_i \ge 0, \;
        \text{and} \\
        \sum_{i=2}^{p+q+1} x_i = \sum_{i=1}^p \beta_i +
        \sum_{i=1}^q \alpha_i < 1.

    The above model is denoted as GARCH(`p`, `q`). The :math:`\beta_i` and
    :math:`\alpha_i` coefficients are referred to as GARCH and ARCH
    coefficients, respectively. When :math:`\beta_i=0, i=1,2,\ldots,p`,
    the above model reduces to ARCH(`q`) which was proposed by Engle ([1]_).
    The nonnegativity conditions on the parameters imply a nonnegative variance
    and, the condition on the sum of the :math:`\beta_i`'s and
    :math:`\alpha_i`'s is required for wide sense stationarity.

    In the empirical analysis of observed data, GARCH(1,1) or GARCH(1,2) models
    have often found to appropriately account for conditional
    heteroskedasticity ([2]_). This finding is similar to linear time series
    analysis based on ARMA models.

    Note that for the above models, positive and negative past values have a
    symmetric impact on the conditional variance. In practice, many series may
    have a strong asymmetric influence on the conditional variance. To take
    into account this phenomena, Nelson ([3]_) put forward exponential
    GARCH (EGARCH).
    Lai ([4]_, [5]_, [6]_) proposed and studied some properties of a general
    class of models that extended the linear relationship of the conditional
    variance in ARCH and GARCH into a nonlinear relationship.

    The maximum likelihood method is used in estimating the parameters in
    GARCH(`p`, `q`). The log-likelihood of the model for the observed series
    :math:`{w_t}` with length *m* is

    .. math::
        \log(L) = -\frac{m}{2}\log(2\pi)-\frac{1}{2}\sum_{t=1}^my_t^2/
        \sigma_t^2 -\frac{1}{2}\sum_{t=1}^m \log(\sigma_t^2), \\
        \text{where}\quad \sigma_t^2 = \sigma^2+\sum_{i=1}^p\beta_i
        \sigma_{t-i}^2+\sum_{i=1}^q\alpha_iw_{t-i}^2

    Thus, :math:`\log(L)` is maximized subject to the constraints on the
    :math:`\alpha_i, \beta_i`, and :math:`\sigma`.

    In this model, if `q` = 0, the GARCH model is singular since the estimated
    Hessian matrix is singular.

    The initial values of the parameter vector `x` entered in vector `guess`
    must satisfy certain constraints. The first element of `guess` refers to
    :math:`\sigma^2` and must be greater than zero and less than `max_sigma`.
    The remaining `p+q` initial values must each be greater than or equal
    to zero and sum to a value less than one.

    To guarantee stationarity in model fitting,

    .. math::
        \sum_{i=2}^{p+q+1}x_i = \sum_{i=1}^p \beta_i +
        \sum_{i=1}^q \alpha_i < 1

    is checked internally. The initial values should be selected from values
    between zero and one.

    AIC is computed by

    .. math::
        -2 \log(L) + 2 (p+q+1),

    where :math:`\log(L)` is the value of the log-likelihood function.

    Statistical inferences can be performed outside the function GARCH
    based on the output of the log-likelihood function (`log_likeli`),
    the Akaike Information Criterion (`aic`), and the
    variance-covariance matrix (`var`).

    References
    ----------
    .. [1] Engle, C. (1982), *Autoregressive conditional heteroskedasticity
           with estimates of the variance of U.K. inflation*, Econometrica,
           50, 987-1008.

    .. [2] Palm, F. C. (1996), *GARCH models of volatility*. In Handbook of
           Statistics, Vol. 14, 209-240. Eds: Maddala and Rao. Elsevier,
           New York.

    .. [3] Nelson, Peter (1989), *Multiple Comparisons of Means Using
           Simultaneous Confidence Intervals*, Journal of Quality Technology,
           21, 232-241.

    .. [4] Lai, D. (1998), *Local Asymptotic Normality for Location-Scale
           Type Processes*, Far East Journal of Theorectical Statistics,
           Vol. 2, 171-186.

    .. [5] Lai, D. (1999), *Asymptotic distributions of the correlation
           integral based statistics*, Journal of Nonparametric Statistics,
           10(2), 127-135.

    .. [6] Lai, D. (2000), *Asymptotic distribution of the estimated BDS
           statistic and residual analysis of AR Models on the Canadian lynx
           data*, Journal of Biological Systems, Vol. 8, 95-114.

    Examples
    --------
    The data for this example are generated to follow a GARCH(`p,q`) process
    by using a random number generation function `sgarch`. The data set is
    analyzed and estimates of sigma, the ARCH and GARCH parameters, the
    log-likelihood and the AIC are returned.

    >>> import numpy as np
    >>> from imsl.timeseries.garch import garch
    >>> def sgarch(p, q, m, x, y, z, y0, sigma):
    ...     k = max(1, p, q)
    ...     for i in range(0, k):
    ...         y0[i] = z[i] * x[0]
    ...     # Compute the initial value of sigma
    ...     s3 = 0.0
    ...     if max(p, q) >= 1:
    ...         for i in range(1, p+q+1):
    ...             s3 += x[i]
    ...     for i in range(k):
    ...         sigma[i] = x[0] / (1.0 - s3)
    ...     for i in range(k, m+1000):
    ...         s1 = 0.0
    ...         s2 = 0.0
    ...         if q >= 1:
    ...             for j in range(q):
    ...                 s1 += x[j + 1] * y0[i - j - 1] * y0[i - j - 1]
    ...         if p >= 1:
    ...             for j in range(p):
    ...                 s2 += x[q + 1 + j] * sigma[i - j - 1]
    ...         sigma[i] = x[0] + s1 + s2
    ...         y0[i] = z[i] * np.sqrt(sigma[i])
    ...     # Discard the first 1000 simulated observations
    ...     y[0:m] = y0[1000:1000+m]
    >>>
    >>> np.random.seed(182198625)
    >>> m = 1000
    >>> p = 2
    >>> q = 1
    >>> wk1 = np.random.normal(size=m + 1000)
    >>> wk2 = np.empty(m+1000, dtype=np.float64)
    >>> wk3 = np.empty(m+1000, dtype=np.float64)
    >>> y = np.empty(m, dtype=np.float64)
    >>> x = np.array([1.3, 0.2, 0.3, 0.4], dtype=np.float64)
    >>> guess = np.array([1.0, 0.1, 0.2, 0.3], dtype=np.float64)
    >>>
    >>> sgarch(p, q, m, x, y, wk1, wk2, wk3)
    >>>
    >>> result = garch(p, q, y, guess)
    >>>
    >>> print("Sigma estimate is {0:11.4f}".format(result.x[0]))
    ... # doctest: +NORMALIZE_WHITESPACE
    Sigma estimate is      1.3083
    >>> print("ARCH(1) estimate is {0:11.4f}".format(result.x[1]))
    ... # doctest: +NORMALIZE_WHITESPACE
    ARCH(1) estimate is      0.1754
    >>> print("GARCH(1) estimate is {0:11.4f}".format(result.x[2]))
    ... # doctest: +NORMALIZE_WHITESPACE
    GARCH(1) estimate is      0.3519
    >>> print("GARCH(2) estimate is {0:11.4f}".format(result.x[3]))
    ... # doctest: +NORMALIZE_WHITESPACE
    GARCH(2) estimate is      0.3477
    >>> print("\nLog-likelihood function value is {0:11.4f}".format
    ...       (result.log_likeli)) # doctest: +NORMALIZE_WHITESPACE
    Log-likelihood function value is  -2558.5405
    >>> print("Akaike Information Criterion value is {0:11.4f}".format
    ...       (result.aic)) # doctest: +NORMALIZE_WHITESPACE
    Akaike Information Criterion value is   5125.0810
    >>> print("\n    Variance-covariance matrix")
    ... # doctest: +NORMALIZE_WHITESPACE
        Variance-covariance matrix
    >>> np.set_printoptions(precision=2)
    >>> print(str(result.var)) # doctest: +SKIP
    [[   73.91   481.41   657.06   663.43]
     [  481.55  4823.93  5019.15  5040.94]
     [  657.06  5018.17  6448.31  6523.42]
     [  663.44  5039.96  6523.44  6645.81]]

    """
    _p = int(p)

    if _p < 0:
        raise ValueError("number p of GARCH parameters must be nonnegative,"
                         " but p = {} is given".format(_p))

    _q = int(q)

    if _q < 0:
        raise ValueError("number q of ARCH parameters must be nonnegative,"
                         " but q = {} is given".format(_q))

    if series is None:
        raise TypeError("None not supported")

    _series = _numpy.asarray(series, order='C')
    ref_type = _numpy.promote_types(_numpy.float64, _series.dtype)
    _series = _numpy.asarray(_series, dtype=ref_type)

    if (not _numpy.issubdtype(_series.dtype, _numpy.float64)):
        raise TypeError("array type {} not supported".format(
            _series.dtype.name))

    if _series.ndim != 1:
        raise ValueError("array of dimension {} not"
                         " supported".format(_series.ndim))

    if _series.size == 0:
        raise ValueError("empty array not supported")

    if _series.size < _p + _q + 1:
        raise ValueError("time series too short")

    _m = _series.size

    if guess is None:
        raise TypeError("None not supported")

    _guess = _numpy.asarray(guess, dtype=ref_type, order='C')

    if _guess.ndim != 1:
        raise ValueError("array of dimension {} not"
                         " supported".format(_guess.ndim))

    if _guess.size < _p + _q + 1:
        raise ValueError("array guess too short")

    # First convert max_sigma using float() in order to catch max_sigma=None.
    _max_sigma = float(max_sigma)
    _max_sigma = _numpy.float64(max_sigma)
    if (_max_sigma <= 0.0):
        raise ValueError("max_sigma must be greater than zero, but "
                         "max_sigma = {} is given".format(_max_sigma))

    # Generate output arrays/scalars
    _x = _numpy.empty(p + q + 1, dtype=ref_type)
    _var = _numpy.empty((p + q + 1, p + q + 1), dtype=ref_type)
    c_log_likeli = _ctypes.c_double()
    c_aic = _ctypes.c_double()

    args = []
    # Prepare required input argument list
    args.append(_ctypes.c_int(_p))
    args.append(_ctypes.c_int(_q))
    args.append(_ctypes.c_int(_m))
    args.append(_series.ctypes.data_as(_ctypes.c_void_p))
    args.append(_guess.ctypes.data_as(_ctypes.c_void_p))

    # Add the optional input arguments
    args.append(_constants.IMSLS_MAX_SIGMA)
    args.append(_ctypes.c_double(_max_sigma))

    # Add the output arguments
    args.append(_constants.IMSLS_A)
    args.append(_ctypes.byref(c_log_likeli))
    args.append(_constants.IMSLS_AIC)
    args.append(_ctypes.byref(c_aic))
    args.append(_constants.IMSLS_VAR_USER)
    args.append(_var.ctypes.data_as(_ctypes.c_void_p))
    args.append(_constants.IMSLS_RETURN_USER)
    args.append(_x.ctypes.data_as(_ctypes.c_void_p))

    args.append(0)

    func = _garch_func(_series.dtype)
    func(*args)

    result = _collections.namedtuple("GarchResults",
                                     ["x",
                                      "log_likeli",
                                      "aic",
                                      "var"]
                                     )

    result.x = _x
    result.log_likeli = c_log_likeli.value
    result.aic = c_aic.value
    result.var = _var

    return result
