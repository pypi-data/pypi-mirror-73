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
"""Auto_arima related functions."""
import ctypes as _ctypes
import numpy as _numpy

import imsl._constants as _constants
import imsl._imsllib as _imsllib
import collections as _collections
from imsl.constants import AIC, AICC, BIC


def _auto_arima_func(dtype):
    """Return the IMSL auto_arima function appropriate for dtype.

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
        return _imsllib.imsls_d_auto_arima
    else:
        return None


def auto_arima(tpoints, series, orders, max_lag=10, delta=0.7, critical=3.0,
               epsilon=0.001, information_criterion=AIC, n_predict=0,
               confidence=95.0):
    r"""Identify outliers in a multiplicative seasonal ARIMA model.

    This function automatically identifies time series outliers, determines
    parameters of a multiplicative seasonal
    :math:`\text{ARIMA}(p,0,q) \times (0,d,0)_s` model and produces forecasts
    that incorporate the effects of outliers whose effects persist beyond the
    end of the series.

    Parameters
    ----------
    tpoints : *(n_obs,) array_like*
        Array containing the integer time points
        :math:`t_1, t_2, \ldots,t_{\text{n_obs}}` the time series was
        observed. It is required that :math:`t_1, t_2, \ldots,t_{\text{n_obs}}`
        are in strictly ascending order.

    series : *(n_obs,) array_like*
        Array containing the observed time series values
        :math:`Y_1^{\ast},Y_2^{\ast},\ldots,Y_{\text{n_obs}}^{\ast}`.
        This series can contain outliers and missing values. Outliers are
        identified by this function and missing values are identified by the
        time values in array `tpoints`. If the time interval between two
        consecutive time points is greater than one, i.e.
        :math:`t_{i+1}-t_i=m>1`, then *m-1* missing values are assumed to exist
        between :math:`t_i` and :math:`t_{i+1}` at times
        :math:`t_i+1,t_i+2,\ldots,t_{i+1}-1`. Therefore, the gap free series is
        assumed to be defined for equidistant time points. Missing values are
        automatically estimated prior to identifying outliers and producing
        forecasts. Forecasts are generated for both missing and observed
        values.

    orders : *tuple of array_like*
        A four-tuple *(p0, q0, s0, d0)* of arrays containing the AR orders
        *p*, the MA orders *q*, the periods *s* and differences *d*, over which
        the search for the optimum model is conducted. All possible
        combinations of values in *p0*, *q0*, *s0* and *d0* are investigated.
        Entries in *p0*, *q0* and *d0* must be non-negative, whereas all
        periods in *s0* must be strictly positive.

    max_lag : *int, optional*
        The maximum lag allowed when fitting an AR(*p*) model.
        If `orders` [0] = range(*m*) and `orders` [1] = [0], i.e. if an optimum
        AR model is searched, then `max_lag` is set internally to *m-1*, the
        maximum order of the AR models under consideration.

    delta : *float, optional*
        The dampening effect parameter used in the detection of a Temporary
        Change Outlier (TC), `0 < delta < 1`.

    critical : *float, optional*
        Critical value used as a threshold for outlier detection,
        `critical > 0`.

    epsilon : *float, optional*
        Positive tolerance value controlling the accuracy of parameter
        estimates during outlier detection.

    information_criterion : *{AIC, AICC, BIC}, optional*
        The information criterion used for optimum model selection.
        Values `AIC`, `AICC` and `BIC` are named constants defined
        in module :py:mod:`imsl.constants`.

        .. rst-class:: nowrap

            +---------------+------------------------------------------+
            |  Criterion    | Selected Information Criterion           |
            +===============+==========================================+
            |    AIC        | Akaike's Information Criterion           |
            +---------------+------------------------------------------+
            |    AICC       | Akaike's Corrected Information Criterion |
            +---------------+------------------------------------------+
            |    BIC        | Bayesian Information Criterion           |
            +---------------+------------------------------------------+

        Default: `information_criterion = imsl.constants.AIC`

    n_predict : *int, optional*
        The number of forecasts requested. Forecasts are made from the last
        observed value of the series.

    confidence : *float, optional*
        The confidence level for computing forecast confidence limits, taken
        from the exclusive interval (0, 100).

    Returns
    -------
    A named tuple with the following fields:
    residual : *(n,) ndarray*
        An array of length
        `n` = :math:`t_{\text{n_obs}}-t_1+1 \ge \text{n_obs}`,
        containing :math:`\hat{e}_t`, the estimates of the white noise in the
        outlier free original series.

    residual_sigma : *float*
        Residual standard error (RSE) of the outlier free original series.

    outlier_statistics : *tuple*
        A two-tuple of arrays containing the outlier statistics. The first
        array, of type `int`, contains the time points at which the outliers
        were observed. The second array, of type `object`, contains identifiers
        indicating the types of outliers observed. Outlier types fall into
        one of five categories:

        .. rst-class:: nowrap

            +---------------+------------------------------+
            |  Identifier   | Outlier Type                 |
            +===============+==============================+
            |    IO         | Innovational Outlier         |
            +---------------+------------------------------+
            |    AO         | Additive Outlier             |
            +---------------+------------------------------+
            |    LS         | Level Shift Outlier          |
            +---------------+------------------------------+
            |    TC         | Temporary Change Outlier     |
            +---------------+------------------------------+
            |    UI         | Unable to Identify           |
            +---------------+------------------------------+

    info_criteria_vals : *tuple of float*
         A three-tuple, `(aic, aicc, bic)`, containing the AIC (Akaike's
         information criterion), AICC (corrected AIC) and BIC (Bayesian
         Information Criterion) value for the optimum model.

    outfree_series : *(n, 2) ndarray*
        An array of dimension `n` by 2, where
        `n` = :math:`t_{\text{n_obs}}-t_1+1`.
        The first column contains the observations from the original series,
        plus estimated values for any time gap. The second column contains
        the same values as the first column, adjusted by removing any outlier
        effects. In effect, the second column contains estimates of the
        underlying outlier-free series. If no outliers are detected, then
        both columns will contain identical values.

    outfree_forecast : *tuple*
        A three-tuple of arrays of length `n_predict`. The first array
        contains the forecasted values for the original outlier free series,
        the second the standard errors for these forecasts, and the third the
        psi weights of the infinite order moving average form of the model.

    outlier_forecast : *tuple*
        A three-tuple of arrays of length `n_predict`. The first array
        contains the forecasted values for the original series, the second
        the standard errors for these forecasts, and the third the psi weights
        of the infinite order moving average form of the model.

    opt_model : *named tuple*
         A named tuple describing the optimum model fitted to the outlier-free
         series. The fields are described in the following table:

         .. rst-class:: nowrap

             +---------------+-----------------------------------------------+
             |  Field name   | Content                                       |
             +===============+===============================================+
             |  const        | model constant                                |
             +---------------+-----------------------------------------------+
             |  ar           | ndarray of autoregressive (AR) coefficients   |
             +---------------+-----------------------------------------------+
             |  ma           | ndarray of moving average (MA) coefficients   |
             +---------------+-----------------------------------------------+
             |  s            | period (seasonality) of the model             |
             +---------------+-----------------------------------------------+
             |  d            | difference used in the model                  |
             +---------------+-----------------------------------------------+

         If `d = 0`, then an ARMA(*p*, *q*) or AR(*p*) model is fitted to the
         outlier-free version :math:`Y_t` of the observed series
         :math:`Y_t^\ast`. If `d>0`, these parameters are computed for an
         ARMA(*p*, *q*) representation of the outlier-free, seasonally adjusted
         series
         :math:`Z_t=\Delta_s^d \cdot Y_t=(1-B_s)^d\cdot Y_t`,
         where
         :math:`B_sY_t=Y_{t-s}` and :math:`s \ge 1`.

    Notes
    -----
    Function `auto_arima` determines the parameters of a multiplicative
    seasonal :math:`\text{ARIMA}(p,0,q) \times (0,d,0)_s` model, and then uses
    the fitted model to identify outliers and prepare forecasts. The order of
    this model can be specified or automatically determined.

    The :math:`\text{ARIMA}(p,0,q) \times (0,d,0)_s` model handled by
    `auto_arima` has the following form:

    .. math::
        \phi(B) \Delta_s^d(Y_t-\mu) = \theta(B)a_t, \; t=1,2,\ldots,n,

    where

    .. math::
        \phi(B)=1-\phi_1B-\phi_2B^2-\cdots-\phi_pB^p,
        \theta(B)=1-\theta_1B-\theta_2B^2-\cdots-\theta_qB^q,

    .. math::
        \Delta_s^d=(1-B^s)^d

    and

    .. math::
        B^kY_t=Y_{t-k}\,.

    It is assumed that all roots of :math:`\phi(B)` and :math:`\theta(B)` lie
    outside the unit circle. Clearly, if *s = 1*, the model reduces to the
    traditional ARIMA(*p*, *d*, *q*) model, and if *d = 0*, the model reduces
    to the traditional ARMA(*p*, *q*) model.

    :math:`Y_t` is the unobserved, outlier-free time series with mean
    :math:`\mu` and white noise :math:`a_t`. This model is referred to as the
    underlying, outlier-free model. Function `auto_arima` does not assume that
    this series is observable. It assumes that the observed values might be
    contaminated by one or more outliers, whose effects are added to the
    underlying outlier-free series:

    .. math::
        Y_t^{\ast} = Y_t + \text{outlier_effect}_{\;\,t}

    Outliers are classified into one of five categories (see "Outliers" below
    for details). Once outliers are identified, `auto_arima` estimates
    :math:`Y_t`, the outlier-free series representation of the data, by
    removing the estimated outlier effects.

    Using the information about the adjusted
    :math:`\text{ARIMA}(p,0,q) \times (0,d,0)_s` model and the removed
    outliers, forecasts are then prepared for the outlier-free series. Outlier
    effects are added to these forecasts to produce a forecast for the observed
    series, :math:`Y_t^{\ast}`. If there are no outliers, then the forecasts
    for the outlier-free series and the observed series will be identical.

    *Outliers*

    The algorithm of Chen and Liu ([1]_) is used to identify outliers. Both the
    time and classification for these outliers are returned in
    `outlier_statistics`. Outliers are classified into one of five categories
    based upon the standardized statistic for each outlier type. The time at
    which the outlier occurred is given in the first array of the two-tuple
    `outlier_statistics`. The outlier identifier returned in the second array
    is according to the descriptions in the following table:

    +-------------+--------------+--------------------------------------------+
    | Outlier     |              |                                            |
    | Identifier  |  Name        |   General Description                      |
    +=============+==============+============================================+
    |  'IO'       | Innovational | Innovational outliers persist. That is,    |
    |             | Outlier      | there is an initial impact at the time the |
    |             |              | outlier occurs. This effect continues in a |
    |             |              | lagged fashion with all future             |
    |             |              | observations. The lag coefficients are     |
    |             |              | determined by the coefficients of the      |
    |             |              | underlying                                 |
    |             |              | :math:`\text{ARIMA}(p,0,q)\times (0,d,0)_s`|
    |             |              | model.                                     |
    +-------------+--------------+--------------------------------------------+
    |  'AO'       | Additive     | Additive outliers do not persist. As the   |
    |             | Outlier      | name implies, an additive outlier affects  |
    |             |              | only the observation at the time the       |
    |             |              | outlier occurs. Hence additive outliers    |
    |             |              | have no effect on future forecasts.        |
    +-------------+--------------+--------------------------------------------+
    |  'LS'       | Level Shift  | Level shift outliers persist. They have    |
    |             |              | the effect of either raising or lowering   |
    |             |              | the mean of the series starting at the     |
    |             |              | time the outlier occurs. This shift in the |
    |             |              | mean is abrupt and permanent.              |
    +-------------+--------------+--------------------------------------------+
    |  'TC'       | Temporary    | Temporary change outliers persist and are  |
    |             | Change       | similar to level shift outliers with one   |
    |             |              | major exception. Like level shift outliers,|
    |             |              | there is an abrupt change in the mean of   |
    |             |              | the series at the time this outlier occurs.|
    |             |              | However, unlike level shift outliers, this |
    |             |              | shift is not permanent. The TC outlier     |
    |             |              | gradually decays, eventually bringing the  |
    |             |              | mean of the series back to its original    |
    |             |              | value. The rate of this decay is modeled   |
    |             |              | using the parameter `delta`. The default   |
    |             |              | of `delta=0.7` is the value recommended    |
    |             |              | for general use by Chen and Liu.           |
    +-------------+--------------+--------------------------------------------+
    |  'UI'       | Unable to    | If an outlier is identified as the last    |
    |             | Identify     | observation, then the algorithm is unable  |
    |             |              | to determine the outlier's classification. |
    |             |              | For forecasting, a UI outlier is treated as|
    |             |              | an IO outlier. That is, its effect is      |
    |             |              | lagged into the forecasts.                 |
    +-------------+--------------+--------------------------------------------+

    Examples
    --------
    *Example 1:*

    This example uses time series D from [2]_, the hourly viscosity readings
    of a chemical process. A group of AR(*p*) models is fit to the first 304
    observations of this series, measured at time points *t* = 1 to *t* = 304.
    The optimum model is determined and a forecast is done at origin *t* = 304
    for lead times 1 to 6. The forecasts are compared with the actual time
    series values which are stored in array `actual`.

    >>> import numpy as np
    >>> import imsl.timeseries.auto_arima as auto_arima
    >>> # Values of series D at time points t=1,...,t=304
    >>> x = [8.0, 8.0, 7.4, 8.0, 8.0, 8.0, 8.0, 8.8, 8.4, 8.4, 8.0, 8.2, 8.2,
    ...      8.2, 8.4, 8.4, 8.4, 8.6, 8.8, 8.6, 8.6, 8.6, 8.6, 8.6, 8.8, 8.9,
    ...      9.1, 9.5, 8.5, 8.4, 8.3, 8.2, 8.1, 8.3, 8.4, 8.7, 8.8, 8.8, 9.2,
    ...      9.6, 9.0, 8.8, 8.6, 8.6, 8.8, 8.8, 8.6, 8.6, 8.4, 8.3, 8.4, 8.3,
    ...      8.3, 8.1, 8.2, 8.3, 8.5, 8.1, 8.1, 7.9, 8.3, 8.1, 8.1, 8.1, 8.4,
    ...      8.7, 9.0, 9.3, 9.3, 9.5, 9.3, 9.5, 9.5, 9.5, 9.5, 9.5, 9.5, 9.9,
    ...      9.5, 9.7, 9.1, 9.1, 8.9, 9.3, 9.1, 9.1, 9.3, 9.5, 9.3, 9.3, 9.3,
    ...      9.9, 9.7, 9.1, 9.3, 9.5, 9.4, 9.0, 9.0, 8.8, 9.0, 8.8, 8.6, 8.6,
    ...      8.0, 8.0, 8.0, 8.0, 8.6, 8.0, 8.0, 8.0, 7.6, 8.6, 9.6, 9.6, 10.0,
    ...      9.4, 9.3, 9.2, 9.5, 9.5, 9.5, 9.9, 9.9, 9.5, 9.3, 9.5, 9.5, 9.1,
    ...      9.3, 9.5, 9.3, 9.1, 9.3, 9.1, 9.5, 9.4, 9.5, 9.6, 10.2, 9.8, 9.6,
    ...      9.6, 9.4, 9.4, 9.4, 9.4, 9.6, 9.6, 9.4, 9.4, 9.0, 9.4, 9.4, 9.6,
    ...      9.4, 9.2, 8.8, 8.8, 9.2, 9.2, 9.6, 9.6, 9.8, 9.8, 10.0, 10.0, 9.4,
    ...      9.8, 8.8, 8.8, 8.8, 8.8, 9.6, 9.6, 9.6, 9.2, 9.2, 9.0, 9.0, 9.0,
    ...      9.4, 9.0, 9.0, 9.4, 9.4, 9.6, 9.4, 9.6, 9.6, 9.6, 10.0, 10.0, 9.6,
    ...      9.2, 9.2, 9.2, 9.0, 9.0, 9.6, 9.8, 10.2, 10.0, 10.0, 10.0, 9.4,
    ...      9.2, 9.6, 9.7, 9.7, 9.8, 9.8, 9.8, 10.0, 10.0, 8.6, 9.0, 9.4, 9.4,
    ...      9.4, 9.4, 9.4, 9.6, 10.0, 10.0, 9.8, 9.8, 9.7, 9.6, 9.4, 9.2, 9.0,
    ...      9.4, 9.6, 9.6, 9.6, 9.6, 9.6, 9.6, 9.0, 9.4, 9.4, 9.4, 9.6, 9.4,
    ...      9.6, 9.6, 9.8, 9.8, 9.8, 9.6, 9.2, 9.6, 9.2, 9.2, 9.6, 9.6, 9.6,
    ...      9.6, 9.6, 9.6, 10.0, 10.0, 10.4, 10.4, 9.8, 9.0, 9.6, 9.8, 9.6,
    ...      8.6, 8.0, 8.0, 8.0, 8.0, 8.4, 8.8, 8.4, 8.4, 9.0, 9.0, 9.4, 10.0,
    ...      10.0, 10.0, 10.2, 10.0, 10.0, 9.6, 9.0, 9.0, 8.6, 9.0, 9.6, 9.6,
    ...      9.0, 9.0, 8.9, 8.8, 8.7, 8.6, 8.3, 7.9]
    >>> # Actual values of series D at time points t=305,...,t=310
    >>> actual = [8.5, 8.7, 8.9, 9.1, 9.1, 9.1]
    >>> col_labels = ("Lead Time", "Orig. Series", "Forecast", "Deviation",
    ...               "Psi")
    >>> n_predict = 6
    >>> # Define times from t=1 to t=304
    >>> n_obs = len(x)
    >>> times = np.empty((n_obs,), dtype=np.int32)
    >>> for i in range(n_obs):
    ...     times[i] = i+1
    >>> # Candidate models (autoregressive models, AR[0],..., AR[5])
    >>> cand_models = (range(6), [0], [1], [0])
    >>> result = auto_arima(times, x, cand_models, critical=3.8,
    ...                     n_predict=n_predict)
    >>> print("\nAutomatic AR model selection\n")
    <BLANKLINE>
    Automatic AR model selection
    <BLANKLINE>
    >>> opt_model = result.opt_model
    >>> print("Optimum Model : p={0:d}, q={1:d}, s={2:d}, d={3:d}\n".format(
    ...       opt_model.ar.size, opt_model.ma.size, opt_model.s, opt_model.d))
    ... #doctest: +NORMALIZE_WHITESPACE
    Optimum Model : p=1, q=0, s=1, d=0
    <BLANKLINE>
    >>> num_outliers = result.outlier_statistics[0].size
    >>> print("Number of outliers: {0:d}\n".format(num_outliers))
    ... #doctest: +NORMALIZE_WHITESPACE
    Number of outliers: 1
    <BLANKLINE>
    >>> print("Outlier statistics:\n")
    Outlier statistics:
    <BLANKLINE>
    >>> print("Time point  Outlier type\n")
    Time point  Outlier type
    <BLANKLINE>
    >>> stat = result.outlier_statistics
    >>> for i in range(num_outliers):
    ...     print("{0:d}{1:>11s}".format(stat[0][i], stat[1][i]))
    ... #doctest: +NORMALIZE_WHITESPACE
    217         TC
    >>> print("\nAIC = {0:0.3f}".format(result.info_criteria_vals[0]))
    <BLANKLINE>
    AIC = 678.225
    >>> print("RSE = {0:0.3f}".format(result.residual_sigma))
    RSE = 0.291
    >>> np.set_printoptions(precision=3)
    >>> print("\nParameters:")
    <BLANKLINE>
    Parameters:
    >>> print("Model constant : {0:0.3f}\n".format(opt_model.const))
    ... #doctest: +NORMALIZE_WHITESPACE
    Model constant : 1.044
    >>> if (opt_model.ar.size > 0):
    ...     print("AR parameters : " + str(opt_model.ar))
    ... #doctest: +NORMALIZE_WHITESPACE
    AR parameters : [0.888]
    >>> if (opt_model.ma.size > 0):
    ...     print("MA parameters : " + str(opt_model.ma))
    >>> print("")
    <BLANKLINE>
    >>> fcast = result.outlier_forecast
    >>> # Print Forecast Table
    >>> print("                   * * * Forecast Table * * *")
    ... #doctest: +NORMALIZE_WHITESPACE
                       * * * Forecast Table * * *
    >>> print("{0:9s} {1:>15s} {2:>10s} {3:>12s} {4:>9s}".format(col_labels[0],
    ...     col_labels[1], col_labels[2], col_labels[3], col_labels[4]))
    ... #doctest: +NORMALIZE_WHITESPACE
    Lead Time    Orig. Series   Forecast    Deviation       Psi
    >>> for i in range(n_predict):
    ...     j = i+1
    ...     print("{0:9d} {1:15.4f} {2:10.4f} {3:12.4f} {4:9.4f}".format(j,
    ...         actual[i], fcast[0][i], fcast[1][i], fcast[2][i]))
    ... #doctest: +NORMALIZE_WHITESPACE
            1          8.5000     8.0572       0.5697    0.8877
            2          8.7000     8.1967       0.7618    0.7881
            3          8.9000     8.3206       0.8843    0.6996
            4          9.1000     8.4306       0.9699    0.6210
            5          9.1000     8.5282       1.0325    0.5513
            6          9.1000     8.6148       1.0792    0.4894
    >>> # Put back the default options
    >>> np.set_printoptions()

    *Example 2:*

    This example uses the same data as Example 1, but now `auto_arima` seeks
    the optimum model under a set of ARIMA models with a possible seasonal
    adjustment. As a result, the unadjusted model with `p = 3`, `q = 1`,
    `s = 1`, `d = 0` is chosen as optimum.

    >>> import numpy as np
    >>> import imsl.timeseries.auto_arima as auto_arima
    >>> # Values of series D at time points t=1,...,t=304
    >>> x = [8.0, 8.0, 7.4, 8.0, 8.0, 8.0, 8.0, 8.8, 8.4, 8.4, 8.0, 8.2, 8.2,
    ...      8.2, 8.4, 8.4, 8.4, 8.6, 8.8, 8.6, 8.6, 8.6, 8.6, 8.6, 8.8, 8.9,
    ...      9.1, 9.5, 8.5, 8.4, 8.3, 8.2, 8.1, 8.3, 8.4, 8.7, 8.8, 8.8, 9.2,
    ...      9.6, 9.0, 8.8, 8.6, 8.6, 8.8, 8.8, 8.6, 8.6, 8.4, 8.3, 8.4, 8.3,
    ...      8.3, 8.1, 8.2, 8.3, 8.5, 8.1, 8.1, 7.9, 8.3, 8.1, 8.1, 8.1, 8.4,
    ...      8.7, 9.0, 9.3, 9.3, 9.5, 9.3, 9.5, 9.5, 9.5, 9.5, 9.5, 9.5, 9.9,
    ...      9.5, 9.7, 9.1, 9.1, 8.9, 9.3, 9.1, 9.1, 9.3, 9.5, 9.3, 9.3, 9.3,
    ...      9.9, 9.7, 9.1, 9.3, 9.5, 9.4, 9.0, 9.0, 8.8, 9.0, 8.8, 8.6, 8.6,
    ...      8.0, 8.0, 8.0, 8.0, 8.6, 8.0, 8.0, 8.0, 7.6, 8.6, 9.6, 9.6, 10.0,
    ...      9.4, 9.3, 9.2, 9.5, 9.5, 9.5, 9.9, 9.9, 9.5, 9.3, 9.5, 9.5, 9.1,
    ...      9.3, 9.5, 9.3, 9.1, 9.3, 9.1, 9.5, 9.4, 9.5, 9.6, 10.2, 9.8, 9.6,
    ...      9.6, 9.4, 9.4, 9.4, 9.4, 9.6, 9.6, 9.4, 9.4, 9.0, 9.4, 9.4, 9.6,
    ...      9.4, 9.2, 8.8, 8.8, 9.2, 9.2, 9.6, 9.6, 9.8, 9.8, 10.0, 10.0, 9.4,
    ...      9.8, 8.8, 8.8, 8.8, 8.8, 9.6, 9.6, 9.6, 9.2, 9.2, 9.0, 9.0, 9.0,
    ...      9.4, 9.0, 9.0, 9.4, 9.4, 9.6, 9.4, 9.6, 9.6, 9.6, 10.0, 10.0, 9.6,
    ...      9.2, 9.2, 9.2, 9.0, 9.0, 9.6, 9.8, 10.2, 10.0, 10.0, 10.0, 9.4,
    ...      9.2, 9.6, 9.7, 9.7, 9.8, 9.8, 9.8, 10.0, 10.0, 8.6, 9.0, 9.4, 9.4,
    ...      9.4, 9.4, 9.4, 9.6, 10.0, 10.0, 9.8, 9.8, 9.7, 9.6, 9.4, 9.2, 9.0,
    ...      9.4, 9.6, 9.6, 9.6, 9.6, 9.6, 9.6, 9.0, 9.4, 9.4, 9.4, 9.6, 9.4,
    ...      9.6, 9.6, 9.8, 9.8, 9.8, 9.6, 9.2, 9.6, 9.2, 9.2, 9.6, 9.6, 9.6,
    ...      9.6, 9.6, 9.6, 10.0, 10.0, 10.4, 10.4, 9.8, 9.0, 9.6, 9.8, 9.6,
    ...      8.6, 8.0, 8.0, 8.0, 8.0, 8.4, 8.8, 8.4, 8.4, 9.0, 9.0, 9.4, 10.0,
    ...      10.0, 10.0, 10.2, 10.0, 10.0, 9.6, 9.0, 9.0, 8.6, 9.0, 9.6, 9.6,
    ...      9.0, 9.0, 8.9, 8.8, 8.7, 8.6, 8.3, 7.9]
    >>> # Actual values of series D at time points t=305,...,t=310
    >>> actual = [8.5, 8.7, 8.9, 9.1, 9.1, 9.1]
    >>> col_labels = ("Lead Time", "Orig. Series", "Forecast", "Deviation",
    ...               "Psi")
    >>> n_predict = 6
    >>> # Define times from t=1 to t=304
    >>> n_obs = len(x)
    >>> times = np.empty((n_obs,), dtype=np.int32)
    >>> for i in range(n_obs):
    ...     times[i] = i+1
    >>> # Candidate models (multiplicative seasonal ARIMA models, with
    >>> # p0 = (0, 1, 2 ,3), q0 = (0, 1, 2, 3), s0 = (1, 2), d0 = (0, 1, 2))
    >>> cand_models = (range(4), range(4), [1, 2], range(3))
    >>> result = auto_arima(times, x, cand_models, critical=3.8,
    ...                     n_predict=n_predict)
    >>> print("\nAutomatic ARIMA model selection, differencing allowed\n")
    <BLANKLINE>
    Automatic ARIMA model selection, differencing allowed
    <BLANKLINE>
    >>> opt_model = result.opt_model
    >>> print("Optimum Model: p={0:d}, q={1:d}, s={2:d}, d={3:d}\n".format(
    ...        opt_model.ar.size, opt_model.ma.size, opt_model.s, opt_model.d))
    Optimum Model: p=3, q=1, s=1, d=0
    <BLANKLINE>
    >>> num_outliers = result.outlier_statistics[0].size
    >>> print("Number of outliers: {0:d}\n".format(num_outliers))
    Number of outliers: 1
    <BLANKLINE>
    >>> print("Outlier statistics:")
    Outlier statistics:
    >>> print("Time point  Outlier type")
    Time point  Outlier type
    >>> stat = result.outlier_statistics
    >>> for i in range(num_outliers):
    ...     print("{0:d}{1:>11s}".format(stat[0][i], stat[1][i]))
    ... #doctest: +NORMALIZE_WHITESPACE
    217         TC
    >>> print("\nAIC = {0:0.3f}".format(result.info_criteria_vals[0]))
    <BLANKLINE>
    AIC = 675.886
    >>> print("RSE = {0:0.3f}".format(result.residual_sigma))
    RSE = 0.287
    >>> np.set_printoptions(precision=3)
    >>> print("\nParameters:")
    <BLANKLINE>
    Parameters:
    >>> print("Model constant : {0:0.3f}".format(opt_model.const))
    Model constant : 1.893
    >>> if (opt_model.ar.size > 0):
    ...     print("AR parameters : " + str(opt_model.ar))
    ... #doctest: +NORMALIZE_WHITESPACE
    AR parameters : [ 0.184  0.641 -0.029]
    >>> if (opt_model.ma.size > 0):
    ...     print("MA parameters : " + str(opt_model.ma))
    ... #doctest: +NORMALIZE_WHITESPACE
    MA parameters : [-0.743]
    >>> print("")
    <BLANKLINE>
    >>> fcast = result.outlier_forecast
    >>> # Print Forecast Table
    >>> print("                   * * * Forecast Table * * *")
    ... #doctest: +NORMALIZE_WHITESPACE
                       * * * Forecast Table * * *
    >>> print("{0:9s} {1:>15s} {2:>10s} {3:>12s} {4:>9s}".format(col_labels[0],
    ...         col_labels[1], col_labels[2], col_labels[3], col_labels[4]))
    ... #doctest: +NORMALIZE_WHITESPACE
    Lead Time    Orig. Series   Forecast    Deviation       Psi
    >>> for i in range(n_predict):
    ...     j = i+1
    ...     print("{0:9d} {1:15.4f} {2:10.4f} {3:12.4f} {4:9.4f}".format(j,
    ...         actual[i], fcast[0][i], fcast[1][i], fcast[2][i]))
    ... #doctest: +NORMALIZE_WHITESPACE
            1          8.5000     8.0471       0.5620    0.9274
            2          8.7000     8.2004       0.7664    0.8123
            3          8.9000     8.3347       0.8921    0.7153
            4          9.1000     8.4534       0.9784    0.6257
            5          9.1000     8.5570       1.0397    0.5504
            6          9.1000     8.6483       1.0847    0.4819
    >>> # Put back the default options
    >>> np.set_printoptions()

    *Example 3:*

    This example uses the same data as Example 2, but now the specific optimum
    model `p` = 3, `q` = 1, `s` = 1, `d` = 0 found in Example 2 is chosen for
    outlier detection and forecasting.

    >>> import numpy as np
    >>> import imsl.timeseries.auto_arima as auto_arima
    >>> # Values of series D at time points t=1,...,t=304
    >>> x = [8.0, 8.0, 7.4, 8.0, 8.0, 8.0, 8.0, 8.8, 8.4, 8.4, 8.0, 8.2, 8.2,
    ...      8.2, 8.4, 8.4, 8.4, 8.6, 8.8, 8.6, 8.6, 8.6, 8.6, 8.6, 8.8, 8.9,
    ...      9.1, 9.5, 8.5, 8.4, 8.3, 8.2, 8.1, 8.3, 8.4, 8.7, 8.8, 8.8, 9.2,
    ...      9.6, 9.0, 8.8, 8.6, 8.6, 8.8, 8.8, 8.6, 8.6, 8.4, 8.3, 8.4, 8.3,
    ...      8.3, 8.1, 8.2, 8.3, 8.5, 8.1, 8.1, 7.9, 8.3, 8.1, 8.1, 8.1, 8.4,
    ...      8.7, 9.0, 9.3, 9.3, 9.5, 9.3, 9.5, 9.5, 9.5, 9.5, 9.5, 9.5, 9.9,
    ...      9.5, 9.7, 9.1, 9.1, 8.9, 9.3, 9.1, 9.1, 9.3, 9.5, 9.3, 9.3, 9.3,
    ...      9.9, 9.7, 9.1, 9.3, 9.5, 9.4, 9.0, 9.0, 8.8, 9.0, 8.8, 8.6, 8.6,
    ...      8.0, 8.0, 8.0, 8.0, 8.6, 8.0, 8.0, 8.0, 7.6, 8.6, 9.6, 9.6, 10.0,
    ...      9.4, 9.3, 9.2, 9.5, 9.5, 9.5, 9.9, 9.9, 9.5, 9.3, 9.5, 9.5, 9.1,
    ...      9.3, 9.5, 9.3, 9.1, 9.3, 9.1, 9.5, 9.4, 9.5, 9.6, 10.2, 9.8, 9.6,
    ...      9.6, 9.4, 9.4, 9.4, 9.4, 9.6, 9.6, 9.4, 9.4, 9.0, 9.4, 9.4, 9.6,
    ...      9.4, 9.2, 8.8, 8.8, 9.2, 9.2, 9.6, 9.6, 9.8, 9.8, 10.0, 10.0, 9.4,
    ...      9.8, 8.8, 8.8, 8.8, 8.8, 9.6, 9.6, 9.6, 9.2, 9.2, 9.0, 9.0, 9.0,
    ...      9.4, 9.0, 9.0, 9.4, 9.4, 9.6, 9.4, 9.6, 9.6, 9.6, 10.0, 10.0, 9.6,
    ...      9.2, 9.2, 9.2, 9.0, 9.0, 9.6, 9.8, 10.2, 10.0, 10.0, 10.0, 9.4,
    ...      9.2, 9.6, 9.7, 9.7, 9.8, 9.8, 9.8, 10.0, 10.0, 8.6, 9.0, 9.4, 9.4,
    ...      9.4, 9.4, 9.4, 9.6, 10.0, 10.0, 9.8, 9.8, 9.7, 9.6, 9.4, 9.2, 9.0,
    ...      9.4, 9.6, 9.6, 9.6, 9.6, 9.6, 9.6, 9.0, 9.4, 9.4, 9.4, 9.6, 9.4,
    ...      9.6, 9.6, 9.8, 9.8, 9.8, 9.6, 9.2, 9.6, 9.2, 9.2, 9.6, 9.6, 9.6,
    ...      9.6, 9.6, 9.6, 10.0, 10.0, 10.4, 10.4, 9.8, 9.0, 9.6, 9.8, 9.6,
    ...      8.6, 8.0, 8.0, 8.0, 8.0, 8.4, 8.8, 8.4, 8.4, 9.0, 9.0, 9.4, 10.0,
    ...      10.0, 10.0, 10.2, 10.0, 10.0, 9.6, 9.0, 9.0, 8.6, 9.0, 9.6, 9.6,
    ...      9.0, 9.0, 8.9, 8.8, 8.7, 8.6, 8.3, 7.9]
    >>> # Actual values of series D at time points t=305,...,t=310
    >>> actual = [8.5, 8.7, 8.9, 9.1, 9.1, 9.1]
    >>> col_labels = ("Lead Time", "Orig. Series", "Forecast", "Deviation",
    ...               "Psi")
    >>> n_predict = 6
    >>> # Define times from t=1 to t=304
    >>> n_obs = len(x)
    >>> times = np.empty((n_obs,), dtype=np.int32)
    >>> for i in range(n_obs):
    ...     times[i] = i+1
    >>> # Candidate model (specific ARIMA model, with p0 = [3], q0 = [1],
    >>> # s0 = [1], d0 = [0])
    >>> cand_models = ([3], [1], [1], [0])
    >>> result = auto_arima(times, x, cand_models, critical=3.8,
    ...                     n_predict=n_predict)
    >>> print("\nSpecified ARIMA model\n")
    <BLANKLINE>
    Specified ARIMA model
    <BLANKLINE>
    >>> opt_model = result.opt_model
    >>> print("Optimum Model: p={0:d}, q={1:d}, s={2:d}, d={3:d}\n".format(
    ...     opt_model.ar.size, opt_model.ma.size, opt_model.s, opt_model.d))
    Optimum Model: p=3, q=1, s=1, d=0
    <BLANKLINE>
    >>> num_outliers = result.outlier_statistics[0].size
    >>> print("Number of outliers: {0:d}\n".format(num_outliers))
    Number of outliers: 1
    <BLANKLINE>
    >>> print("Outlier statistics:")
    Outlier statistics:
    >>> print("Time point  Outlier type")
    Time point  Outlier type
    >>> stat = result.outlier_statistics
    >>> for i in range(num_outliers):
    ...     print("{0:d}{1:>11s}".format(stat[0][i], stat[1][i]))
    ... #doctest: +NORMALIZE_WHITESPACE
    217         TC
    >>> print("\nAIC = {0:0.3f}".format(result.info_criteria_vals[0]))
    <BLANKLINE>
    AIC = 675.886
    >>> print("RSE = {0:0.3f}".format(result.residual_sigma))
    RSE = 0.287
    >>> np.set_printoptions(precision=3)
    >>> print("\nParameters:")
    <BLANKLINE>
    Parameters:
    >>> print("Model constant : {0:0.3f}\n".format(opt_model.const))
    Model constant : 1.893
    <BLANKLINE>
    >>> if (opt_model.ar.size > 0):
    ...     print("AR parameters : " + str(opt_model.ar))
    ... #doctest: +NORMALIZE_WHITESPACE
    AR parameters : [ 0.184  0.641 -0.029]
    >>> if (opt_model.ma.size > 0):
    ...     print("MA parameters : " + str(opt_model.ma))
    ... #doctest: +NORMALIZE_WHITESPACE
    MA parameters : [-0.743]
    >>> print("")
    <BLANKLINE>
    >>> fcast = result.outlier_forecast
    >>> # Print Forecast Table
    >>> print("                   * * * Forecast Table * * *")
    ... #doctest: +NORMALIZE_WHITESPACE
                       * * * Forecast Table * * *
    >>> print("{0:9s} {1:>15s} {2:>10s} {3:>12s} {4:>9s}".format(col_labels[0],
    ...     col_labels[1], col_labels[2], col_labels[3], col_labels[4]))
    ... #doctest: +NORMALIZE_WHITESPACE
    Lead Time    Orig. Series   Forecast    Deviation       Psi
    >>> for i in range(n_predict):
    ...     j = i+1
    ...     print("{0:9d} {1:15.4f} {2:10.4f} {3:12.4f} {4:9.4f}".format(j,
    ...         actual[i], fcast[0][i], fcast[1][i], fcast[2][i]))
    ... #doctest: +NORMALIZE_WHITESPACE
            1          8.5000     8.0471       0.5620    0.9274
            2          8.7000     8.2004       0.7664    0.8123
            3          8.9000     8.3347       0.8921    0.7153
            4          9.1000     8.4534       0.9784    0.6257
            5          9.1000     8.5570       1.0397    0.5504
            6          9.1000     8.6483       1.0847    0.4819
    >>> # Put back the default options
    >>> np.set_printoptions()

    References
    ----------
    .. [1] Chen, C. and L. Liu (1993), *Joint Estimation of Model Parameters
           and Outlier Effects in Time Series*, Journal of the American
           Statistical Association, Vol. 88, No.421.
    .. [2] Box, G., G. Jenkins and G. Reinsel (1994), *Time Series Analysis :
           Forecasting and Control*, Prentice Hall, New Jersey.

    """
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

    if _series.size < 2:
        raise ValueError("series must contain at least two elements")

    _nobs = _series.size

    if tpoints is None:
        raise TypeError("None not supported")

    _tpoints = _numpy.asarray(tpoints, order='C', dtype=_numpy.int32)

    if _tpoints.ndim != 1:
        raise ValueError("array of dimension {} not"
                         " supported".format(_tpoints.ndim))

    if _tpoints.size != _nobs:
        raise ValueError("array tpoints must be of the same size as array "
                         "series")

    for i in range(1, _nobs):
        if _tpoints[i] <= _tpoints[i - 1]:
            raise ValueError("entries in array tpoints must be in ascending "
                             "order")

    _nobs_act = tpoints[_nobs - 1] - tpoints[0] + 1

    if orders is None:
        raise TypeError("None not supported")

    # Based on the entries in the orders tuple, determine the correct
    # CNL auto_arima method to use in the model selection

    if len(orders) != 4:
        raise ValueError("tuple orders must be of length 4")

    if None in orders:
        raise TypeError("None not supported")

    _p = _numpy.asarray(orders[0], order='C', dtype=_numpy.int32)
    _q = _numpy.asarray(orders[1], order='C', dtype=_numpy.int32)
    _s = _numpy.asarray(orders[2], order='C', dtype=_numpy.int32)
    _d = _numpy.asarray(orders[3], order='C', dtype=_numpy.int32)

    if _p.ndim != 1:
        raise ValueError("array of dimension {} not"
                         " supported".format(_p.ndim))
    if _p.size == 0:
        raise ValueError("empty array not supported")

    if _q.ndim != 1:
        raise ValueError("array of dimension {} not"
                         " supported".format(_q.ndim))
    if _q.size == 0:
        raise ValueError("empty array not supported")

    if _s.ndim != 1:
        raise ValueError("array of dimension {} not"
                         " supported".format(_s.ndim))
    if _s.size == 0:
        raise ValueError("empty array not supported")

    if _d.ndim != 1:
        raise ValueError("array of dimension {} not"
                         " supported".format(_d.ndim))
    if _d.size == 0:
        raise ValueError("empty array not supported")

    _p = _numpy.sort(_p)  # sorted copy
    _q = _numpy.sort(_q)
    _s = _numpy.sort(_s)
    _d = _numpy.sort(_d)

    if _p[0] < 0:
        raise ValueError("all entries in array orders[0] must be non-negative")

    if _q[0] < 0:
        raise ValueError("all entries in array orders[1] must be non-negative")

    if _s[0] <= 0:
        raise ValueError("all entries in array orders[2] must be positive")

    if _d[0] < 0:
        raise ValueError("all entries in array orders[3] must be non-negative")

    _model = _numpy.empty((4,), dtype=_numpy.int32)

    # Determine method
    if _p.size == 1 and _q.size == 1:
        _method = 3
        _model[0] = _p[0]
        _model[1] = _q[0]
        _model[2] = _s[0]
        _model[3] = _d[0]
    elif (_q.size == 1 and _q[0] == 0 and (_p == range(_p.size)).all()):
        _method = 1
    else:
        _method = 2

    _n_p_initial = _p.size
    _n_q_initial = _q.size
    _n_s_initial = _s.size
    _n_d_initial = _d.size

    if _method in (1, 2):
        _s_initial = _numpy.empty((_n_s_initial,), dtype=_numpy.int32)
        _d_initial = _numpy.empty((_n_d_initial,), dtype=_numpy.int32)
        _s_initial[:] = _s[:]
        _d_initial[:] = _d[:]

    if _method == 2:  # Grid search
        _p_initial = _numpy.empty((_n_p_initial,), dtype=_numpy.int32)
        _q_initial = _numpy.empty((_n_q_initial,), dtype=_numpy.int32)
        _p_initial[:] = _p[:]
        _q_initial[:] = _q[:]

    if _method == 3 and _n_s_initial > 1:
        _s_initial = _numpy.empty((_n_s_initial,), dtype=_numpy.int32)
        _s_initial[:] = _s[:]

    if _method == 3 and _n_d_initial > 1:
        _d_initial = _numpy.empty((_n_d_initial,), dtype=_numpy.int32)
        _d_initial[:] = _d[:]

    if _method in (2, 3):
        _maxlag = int(max_lag)
    else:
        _maxlag = _n_p_initial - 1

    if not (0 < _maxlag < _nobs_act):
        raise ValueError("max_lag must be greater than zero and less than the"
                         " length of the series (including missing values)")

    _delta = float(delta)
    if not (0.0 < delta < 1.0):
        raise ValueError("delta must be greater than zero and less than one")

    _critical = float(critical)
    if _critical <= 0.0:
        raise ValueError("critical must be greater than zero")

    _epsilon = float(epsilon)
    if _epsilon <= 0.0:
        raise ValueError("epsilon must be greater than zero")

    _info_crit = int(information_criterion)
    if _info_crit not in (AIC, AICC, BIC):
        raise ValueError("information_criterion must be one of the named "
                         "constants AIC, AICC or BIC")

    _n_predict = int(n_predict)
    if _n_predict < 0:
        raise ValueError("n_predict must be non-negative")

    _confidence = float(confidence)
    if not (0.0 < _confidence < 100.0):
        raise ValueError("confidence must be in the open interval (0, 100)")

    # Prepare return arrays
    _residual = _numpy.empty((_nobs_act,), dtype=ref_type)
    _res_sigma = _ctypes.c_double()
    _outlier_stat = _numpy.empty((_nobs_act, 2), dtype=_numpy.int32)
    _num_outliers = _ctypes.c_int()
    _aic = _ctypes.c_double()
    _aicc = _ctypes.c_double()
    _bic = _ctypes.c_double()
    _outfree_series = _numpy.empty((_nobs_act, 2), dtype=ref_type)
    # Note: distinction between _n_predict > and = 0 not necessary
    _outfree_forecast = _numpy.empty((_n_predict, 3), dtype=ref_type)
    _outlier_forecast = _numpy.empty((_n_predict, 3), dtype=ref_type)
    n_x = 1 + max(_p) + max(_q)
    _x = _numpy.empty((n_x,), dtype=ref_type)

    # Prepare argument list
    args = []

    # Required arguments
    args.append(_nobs)
    args.append(_tpoints.ctypes.data_as(_ctypes.c_void_p))
    args.append(_series.ctypes.data_as(_ctypes.c_void_p))

    # Optional arguments
    args.append(_constants.IMSLS_METHOD)
    args.append(_method)
    args.append(_constants.IMSLS_MAX_LAG)
    args.append(_maxlag)
    args.append(_constants.IMSLS_MODEL)
    args.append(_model.ctypes.data_as(_ctypes.c_void_p))
    args.append(_constants.IMSLS_DELTA)
    args.append(_ctypes.c_double(_delta))
    args.append(_constants.IMSLS_CRITICAL)
    args.append(_ctypes.c_double(_critical))
    args.append(_constants.IMSLS_EPSILON)
    args.append(_ctypes.c_double(_epsilon))
    args.append(_constants.IMSLS_MODEL_SELECTION_CRITERION)
    args.append(_info_crit)

    if _method == 2:
        args.append(_constants.IMSLS_P_INITIAL)
        args.append(_n_p_initial)
        args.append(_p_initial.ctypes.data_as(_ctypes.c_void_p))
        args.append(_constants.IMSLS_Q_INITIAL)
        args.append(_n_q_initial)
        args.append(_q_initial.ctypes.data_as(_ctypes.c_void_p))

    if _method in (1, 2):
        args.append(_constants.IMSLS_S_INITIAL)
        args.append(_n_s_initial)
        args.append(_s_initial.ctypes.data_as(_ctypes.c_void_p))
        args.append(_constants.IMSLS_D_INITIAL)
        args.append(_n_d_initial)
        args.append(_d_initial.ctypes.data_as(_ctypes.c_void_p))

    if _method == 3 and _n_s_initial > 1:
        args.append(_constants.IMSLS_S_INITIAL)
        args.append(_n_s_initial)
        args.append(_s_initial.ctypes.data_as(_ctypes.c_void_p))

    if _method == 3 and _n_d_initial > 1:
        args.append(_constants.IMSLS_D_INITIAL)
        args.append(_n_d_initial)
        args.append(_d_initial.ctypes.data_as(_ctypes.c_void_p))

    args.append(_constants.IMSLS_RESIDUAL_USER)
    args.append(_residual.ctypes.data_as(_ctypes.c_void_p))
    args.append(_constants.IMSLS_RESIDUAL_SIGMA)
    args.append(_ctypes.byref(_res_sigma))
    args.append(_constants.IMSLS_NUM_OUTLIERS)
    args.append(_ctypes.byref(_num_outliers))
    args.append(_constants.IMSLS_OUTLIER_STATISTICS_USER)
    args.append(_outlier_stat.ctypes.data_as(_ctypes.c_void_p))
    args.append(_constants.IMSLS_AIC)
    args.append(_ctypes.byref(_aic))
    args.append(_constants.IMSLS_AICC)
    args.append(_ctypes.byref(_aicc))
    args.append(_constants.IMSLS_BIC)
    args.append(_ctypes.byref(_bic))
    args.append(_constants.IMSLS_OUT_FREE_SERIES_USER)
    args.append(_outfree_series.ctypes.data_as(_ctypes.c_void_p))
    if _n_predict > 0:
        args.append(_constants.IMSLS_NUM_PREDICT)
        args.append(_n_predict)
        args.append(_constants.IMSLS_CONFIDENCE)
        args.append(_ctypes.c_double(_confidence))
        args.append(_constants.IMSLS_OUT_FREE_FORECAST_USER)
        args.append(_outfree_forecast.ctypes.data_as(_ctypes.c_void_p))
        args.append(_constants.IMSLS_OUTLIER_FORECAST_USER)
        args.append(_outlier_forecast.ctypes.data_as(_ctypes.c_void_p))
    args.append(_constants.IMSLS_RETURN_USER)
    args.append(_x.ctypes.data_as(_ctypes.c_void_p))
    args.append(0)

    func = _auto_arima_func(_series.dtype)
    func(*args)

    result = _collections.namedtuple("AutoArimaResults",
                                     ["residual",
                                      "residual_sigma",
                                      "outlier_statistics",
                                      "info_criteria_vals",
                                      "outfree_series",
                                      "outfree_forecast",
                                      "outlier_forecast",
                                      "opt_model"]
                                     )

    optimum_model = _collections.namedtuple("OptimumModel",
                                            ["const",
                                             "ar",
                                             "ma",
                                             "s",
                                             "d"]
                                            )

    result.residual = _residual
    result.residual_sigma = _res_sigma.value

    _n_outliers = _num_outliers.value
    out_type_arr = ('IO', 'AO', 'LS', 'TC', 'UI')

    outlier_tp = _numpy.empty((_n_outliers,), dtype=_numpy.int32)
    outlier_tp[:] = _outlier_stat[0:_n_outliers, 0]
    outlier_type = _numpy.empty((_n_outliers,), dtype=object)

    for i in range(_n_outliers):
        _type = _outlier_stat[i, 1]
        outlier_type[i] = out_type_arr[_type]

    result.outlier_statistics = (outlier_tp, outlier_type)

    result.info_criteria_vals = (_aic.value, _aicc.value, _bic.value)

    result.outfree_series = _outfree_series

    outfree_fcst = _numpy.empty((_n_predict,), dtype=ref_type)
    outfree_stderrs = _numpy.empty((_n_predict,), dtype=ref_type)
    outfree_psi = _numpy.empty((_n_predict,), dtype=ref_type)

    outlier_fcst = _numpy.empty((_n_predict,), dtype=ref_type)
    outlier_stderrs = _numpy.empty((_n_predict,), dtype=ref_type)
    outlier_psi = _numpy.empty((_n_predict,), dtype=ref_type)

    if _n_predict > 0:
        outfree_fcst[:] = _outfree_forecast[:, 0]
        outfree_stderrs[:] = _outfree_forecast[:, 1]
        outfree_psi[:] = _outfree_forecast[:, 2]
        outlier_fcst[:] = _outlier_forecast[:, 0]
        outlier_stderrs[:] = _outlier_forecast[:, 1]
        outlier_psi[:] = _outlier_forecast[:, 2]

    result.outfree_forecast = (outfree_fcst, outfree_stderrs, outfree_psi)
    result.outlier_forecast = (outlier_fcst, outlier_stderrs, outlier_psi)

    n_ar = _model[0]
    n_ma = _model[1]
    _season = _model[2]
    _difference = _model[3]

    _constant = _x[0]
    _ar = _numpy.empty((n_ar,), dtype=ref_type)
    _ar[:] = _x[1:n_ar + 1]
    _ma = _numpy.empty((n_ma,), dtype=ref_type)
    _ma[:] = _x[n_ar + 1:n_ar + n_ma + 1]

    optimum_model.const = _constant
    optimum_model.ar = _ar
    optimum_model.ma = _ma
    optimum_model.s = _season
    optimum_model.d = _difference

    result.opt_model = optimum_model
    return result
