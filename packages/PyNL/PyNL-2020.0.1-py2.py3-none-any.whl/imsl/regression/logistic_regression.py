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
"""LogisticRegression related classes, methods, and functions."""
import collections as _collections
import ctypes as _ctypes

import numpy as _numpy
from scipy.stats import norm as _normal

import imsl._constants as _constants
import imsl._imsllib as _imsllib


def _logistic_regression_func(dtype):
    """Return the IMSL logistic_regression function appropriate for dtype.

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
        return _imsllib.imsls_d_logistic_regression
    else:
        return None


class ResponseFormatAll():
    r"""Generate a matrix containing counts for all response classes.

    Parameters
    ----------
    class_counts : *(n_obs, n_classes) array_like*
        Array of `n_obs` observations containing the counts for all
        `n_classes` response classes.

    """

    def __init__(self, class_counts):
        """Instantiate ResponseFormatAll class."""
        if class_counts is None:
            raise TypeError("None not supported")

        _class_counts = _numpy.asarray(class_counts, order='C')

        # attempt to promote class_counts to a compatible type.
        common_type = _numpy.promote_types(_numpy.float64, _class_counts.dtype)
        self._class_counts = _numpy.asarray(_class_counts, dtype=common_type)

        if (not _numpy.issubdtype(self._class_counts.dtype, _numpy.float64)):
            raise TypeError("array type {} not supported".format(
                self._class_counts.dtype.name))

        if self._class_counts.ndim != 2:
            raise ValueError("array of dimension {} not"
                             " supported".format(self._class_counts.ndim))

        if self._class_counts.size == 0:
            raise ValueError("empty array not supported")

        if self._class_counts.shape[1] < 2:
            raise ValueError("array must have at least two columns")

    @property
    def class_counts_matrix(self):
        """Return the full matrix of response class counts.

        Returns
        -------
        *(n_obs, n_classes) ndarray*
            Array containing the response counts for all `n_classes`
            response categories and all `n_obs` observations.

        """
        return _numpy.copy(self._class_counts)


class ResponseFormatRef():
    r"""Generate a class counts matrix from a matrix without reference counts.

    Parameters
    ----------
    class_counts : *(n_obs, n_classes-1) array_like*
        Array of `n_obs` observations containing the response class counts for
        all `n_classes` response categories excluding the reference category.

    frequencies : *(n_obs,) array_like, optional*
        Array containing the number of replications or trials for each
        of the observations.

        Default: `frequencies = 1`

    """

    def __init__(self, class_counts, frequencies=None):
        """Instantiate ResponseFormatRef class."""
        if class_counts is None:
            raise TypeError("None not supported")

        _class_counts = _numpy.asarray(class_counts, order='C')

        # attempt to promote class_counts to a compatible type.
        common_type = _numpy.promote_types(_numpy.float64, _class_counts.dtype)
        self._class_counts = _numpy.asarray(_class_counts, dtype=common_type)

        if (not _numpy.issubdtype(self._class_counts.dtype, _numpy.float64)):
            raise TypeError("array type {} not supported".format(
                self._class_counts.dtype.name))

        if self._class_counts.ndim not in (1, 2):
            raise ValueError("array of dimension {} not"
                             " supported".format(self._class_counts.ndim))

        if self._class_counts.size == 0:
            raise ValueError("empty array not supported")

        if frequencies is not None:
            # NOTE: In the CNL docu of logistic_regression, array
            # frequencies is declared as int but in flogreg.c it
            # is declared as float. The documentation should be
            # adjusted.
            self._frequencies = _numpy.asarray(frequencies, order='C',
                                               dtype=common_type)

            if self._frequencies.ndim != 1:
                raise ValueError("array of dimension {} not"
                                 " supported".format(self._frequencies.ndim))

            if self._frequencies.size != self._class_counts.shape[0]:
                raise ValueError("arrays class_counts and frequencies must"
                                 " have the same number of rows")

            # Check entries in frequencies
            for i in range(0, self._frequencies.size):
                if self._frequencies[i] < 0:
                    raise ValueError("entries in array frequencies must be"
                                     " greater than or equal to zero")

        # Construct full response matrix
        n_rows = self._class_counts.shape[0]
        if self._class_counts.ndim == 1:
            n_cols = 2
            self._counts_matrix = _numpy.empty((n_rows, n_cols),
                                               dtype=common_type)
            self._counts_matrix[:, 0] = self._class_counts[:]
        else:
            n_cols = self._class_counts.shape[1] + 1
            self._counts_matrix = _numpy.empty((n_rows, n_cols),
                                               dtype=common_type)
            self._counts_matrix[:, :-1] = self._class_counts[:, :]

        for i in range(0, n_rows):
            sum_row = self._counts_matrix[i, :-1].sum()

            if frequencies is None:
                ref_categ_counts = 1.0 - sum_row
            else:
                ref_categ_counts = self._frequencies[i] - sum_row

            if ref_categ_counts < 0:
                raise ValueError("number of counts for the reference category"
                                 " must be greater than or equal to zero")

            self._counts_matrix[i, -1] = ref_categ_counts

    @property
    def class_counts_matrix(self):
        """Return the full matrix of response class counts.

        Returns
        -------
        *(n_obs, n_classes) ndarray*
            Array containing the response counts for all `n_classes`
            response categories and all `n_obs` observations. The
            counts for the reference category are located in the
            last column of the array.

        """
        return self._counts_matrix


class ResponseFormatID():
    r"""Generate a matrix of class counts from a vector of response class IDs.

    Parameters
    ----------
    class_id : *(n_obs,) array_like*
        Vector that contains in location *i* the group or class number to
        which observation *i* belongs.

    n_classes : *int*
        The number of response categories.

    """

    def __init__(self, class_id, n_classes):
        """Instantiate ResponseFormatID class."""
        if class_id is None:
            raise TypeError("None not supported")

        self._class_id = _numpy.asarray(class_id, dtype=_numpy.float64)

        if self._class_id.ndim != 1:
            raise ValueError("array of dimension {} not"
                             " supported".format(self._class_id.ndim))

        if self._class_id.size == 0:
            raise ValueError("empty array not supported")

        self._n_classes = int(n_classes)

        if self._n_classes < 2:
            raise ValueError("n_classes must be greater than or equal to two")

        n_rows = self._class_id.size
        n_cols = self._n_classes

        miny = _numpy.amin(self._class_id)
        maxy = _numpy.amax(self._class_id)

        if maxy - miny + 1 > n_cols:
            raise ValueError("n_classes must be at least as large as the "
                             "difference between the maximum and minimum "
                             "entry in class_id plus one")

        self._counts_matrix = _numpy.zeros((n_rows, n_cols),
                                           dtype=_numpy.float64)

        for i in range(n_rows):
            col_ind = int(self._class_id[i] - miny)
            self._counts_matrix[i, col_ind] = 1

    @property
    def class_counts_matrix(self):
        """Return the full matrix of response class counts.

        Returns
        -------
        *(n_obs, n_classes) ndarray*
            Array containing the response class counts for all `n_classes`
            response categories and all `n_obs` observations.

        """
        return self._counts_matrix


class LogisticRegression():
    r"""Generate a logistic regression model.

    Generate a binomial or multinomial logistic regression model using
    iteratively re-weighted least squares.

    Parameters
    ----------
    n_predictors : *int*
        The number of predictors in the model.

    n_classes : *int*
        The number of discrete outcomes, or classes, in the model.

    ref_class : *int, optional*
        A number specifying which class or outcome category to use as the
        reference class. Outcome categories are assumed to be numbered
        1,..., `n_classes`.

        Default: `ref_class` = `n_classes`.

    intercept : *bool, optional*
        Specifies if the model will include an intercept (constant).

        Default: `intercept` = `True`.

    x_interact : *(n_x_interact, 2) array_like, optional*
        Array providing pairs of column indices of the predictor variables
        that define the interaction terms in the model. Adjacent indices should
        be unique. For example, suppose there are two independent variables
        *x0* and *x1*. To fit a model that includes their interaction term
        *x0x1*, set `x_interact = [[0, 1]]`

        Default: No interaction terms are included.

    Notes
    -----
    Class `LogisticRegression` fits a logistic regression model for discrete
    dependent variables with two or more mutually exclusive outcomes or
    classes.

    *1. Binary Response Classes*

    For a binary response *y*, the objective is to model the conditional
    probability of success, :math:`\pi_1(x)=\Pr(y=1|x)`, where
    :math:`x=(x_1,x_2,\ldots,x_p)^T` is a realization of *p* independent
    variables (predictors). Logistic regression models the conditional
    probability, :math:`\pi_1(x)`, using the cdf of the logistic distribution.
    In particular,

    .. math::
        \pi_1(x) = \frac{\exp(\eta_1)}{1+\exp(\eta_1)}
                 \equiv \frac{1}{1+\exp(-\eta_1)}\;,

    where

    .. math::
        \eta_1 = \beta_{10}+x^T\beta_1

    and

    .. math::
        \beta_{10},\; \beta_1=(\beta_{11}, \beta_{12},\ldots,\beta_{1p})^T

    are unknown coefficients that are to be estimated.

    Solving for the linear component :math:`\eta_1` results in the *log-odds*
    or *logit* transformation of :math:`\pi_1(x)`:

    .. math::
        \text{logit}(\pi_1(x)) = \log \frac{\pi_1(x)}{1-\pi_1(x)} = \eta_1

    Given a set of *N* observations :math:`(y_i, x_i)`, where :math:`y_i`
    follows a binomial :math:`(n, \pi)` distribution with parameters *n* = 1
    and :math:`\pi = \pi_1(x_i)`, the likelihood and log-likelihood are,
    respectively,

    .. math::
        L = \prod_{i=1}^N \pi(x_i)^{y_i}(1-\pi(x_i))^{1-y_i}

    .. math::
        l = \sum_{i=1}^N \left\{ y_i \log\left(\frac{\pi(x_i)}{1-\pi(x_i)}
        \right)+\log(1-\pi(x_i)) \right\}

    The log-likelihood in terms of the parameters :math:`{\beta_{10}, \beta_1}`
    is therefore

    .. math::
        l(\beta_{10},\beta_1) = \sum_{i=1}^N \left\{ y_i\eta_{i1}-
        \log(1+\exp(\eta_{i1})) \right\}

    where

    .. math::
        \eta_{i1} = \beta_{10}+x_i^T\beta_1

    With a binary outcome, only one probability needs to be modeled. The second
    probability can be obtained from the constraint
    :math:`\pi_1(x)+\pi_2(x)=1`. If each :math:`y_i` is the number of successes
    in :math:`n_i` independent trials, the log-likelihood becomes

    .. math::
        l = \sum_{i=1}^N \left\{ y_i \log\left(\frac{\pi(x_i)}{1-\pi(x_i)}
        \right)+n_i \log(1-\pi(x_i)) \right\}

    or

    .. math::
        l(\beta_{10},\beta_1) = \sum_{i=1}^N \left\{ y_i\eta_{i1}-
        n_i \log(1+\exp(\eta_{i1})) \right\}

    To test the significance of the model, the log-likelihood of the fitted
    model is compared to that of an intercept-only model. In particular,
    :math:`G = -2(l(\beta_{10},0)-l(\beta_{10},\beta_1))` is a
    likelihood-ratio test statistic, and under the null hypothesis
    :math:`H_0:\beta_{11}=\beta_{12}=\ldots=\beta_{1p}=0`, *G* is distributed
    as chi-squared with *p-1* degrees of freedom. A significant result suggests
    that at least one parameter in the model is non-zero. See [2]_ for further
    discussion.

    *2. More than 2 Response Classes*

    In the multinomial case, the response vector is
    :math:`y_i=(y_{i1}, y_{i2},\ldots,y_{iK})^T`, where :math:`y_{ik}=1` when
    the *i* -th observation belongs to class *k* and :math:`y_{ik}=0`,
    otherwise.
    Furthermore, because the outcomes are mutually exclusive,

    .. math::
        \sum_{k=1}^Ky_{ik} = 1 \,,

    and

    .. math::
        \pi_1(x)+\pi_2(x)+\ldots+\pi_K(x) = 1.

    The last class *K* serves as the baseline or reference class in the sense
    that it is not modeled directly but found from

    .. math::
        \pi_K(x) = 1 - \sum_{k=1}^{K-1}\pi_k(x) \,.

    If there are multiple trials, i.e. :math:`n_i>1`, then the constraint on
    the responses is

    .. math::
        \sum_{k=1}^K y_{ik} = n_i \,.

    Define

    .. math::
        \beta_{m0},\; \beta_m:=(\beta_{m1},\ldots,\beta_{mp})^T

    as the regression coefficients of response class *m*, *m=1,...,K*.

    For *i=1,...,N* and *m=1,...,K*, set

    .. math::
        \eta_{im} = \beta_{m0} + x_i^T \beta_m

    and

    .. math::
       \pi_m(x_i) := \pi_{im} = \frac{\exp(\eta_{im})}{1+\sum_{k=1}^{K-1}
       \exp(\eta_{ik})}

    The log-likelihood in the multinomial case becomes

    .. math::
        l(\beta_{10},\beta_1,\ldots,\beta_{K0},\beta_K) =
        \sum_{i=1}^N\left\{\sum_{l=1}^Ky_{il}\eta_{il}-
        n_i\log\left(\sum_{j=1}^K\exp(\eta_{ij})\right)\right\}\,.

    The constraint

    .. math::
        \sum_{k=1}^K\pi_{ik} = 1

    is handled by setting :math:`\eta_{iK}=0` for the *K*-th class, reducing
    the full vector of regression coefficients to

    .. math::
        \beta := (\beta_{10},\beta_1,\beta_{20},\beta_2,\ldots,\beta_{K-1,0},
        \beta_{K-1})^T\,.

    Then, the log-likelihood is

    .. math::
        l(\beta) =
        \sum_{i=1}^N\left\{\sum_{l=1}^{K-1}y_{il}\eta_{il}-n_i\log\left(1+
        \sum_{j=1}^{K-1} \exp(\eta_{ij})\right)\right\}

    or

    .. math::
        l(\beta) =
        \sum_{i=1}^N\left\{\sum_{l=1}^{K-1}y_{il}(\beta_{l0}+x_i^T\beta_l)
        -n_i\log\left(1+\sum_{j=1}^{K-1}\exp(\beta_{j0}+x_i^T\beta_j)\right)
        \right\}\,.

    Note that for the multinomial case, the log-odds (or logit) is

    .. math::
        \log \frac{\pi_{il}}{\pi_{iK}} = \beta_{l0}+x_i^T\beta_l,
        \; l=1,\ldots,K-1\,.

    Each of the logits involves the odds ratio of being in class *l* versus
    class *K*, the reference class.

    *3. Maximum-Likelihood Estimation*

    Maximum likelihood estimates can be obtained by solving the score equation
    for each parameter:

    .. math::
        \begin{array}{rcl}
        \frac{\partial l(\beta)}{\partial \beta_{mj}}&=&
        \sum_{i=1}^N\left\{x_{ij}y_{im}-n_i
        \frac{x_{ij}\exp(\eta_{im})}{1+\sum_{k=1}^{K-1}\exp(\eta_{ik})}
        \right\}\\
        &=& \sum_{i=1}^N \left\{x_{ij}\left(y_{im}-n_i\pi_{im}\right)
        \right\}\\
        &\stackrel{!}{=}&0\,.
        \end{array}

    Here, :math:`x_{ij}` denotes the *j*-th component of observation
    :math:`x_i`, and :math:`x_{i0}:=1`.

    To solve the score equations, the class employs a method known as
    *iteratively re-weighted least squares* or IRLS. In this case, the IRLS
    is equivalent to the Newton-Raphson algorithm ([1]_, [5]_).

    The Newton-Raphson iteration is

    .. math::
        \beta^{n+1} = \beta^n - \mathbf{H}^{-1}(\beta^n)
        \mathbf{G}(\beta^n)\,,

    where :math:`\mathbf{H}` denotes the Hessian of the log-likelihood, i.e.,
    the matrix of second partial derivatives defined by

    .. math::
        \frac{\partial^2 l(\beta)}{\partial \beta_{\nu k}\partial \beta_{mj}}=
        -\sum_{i=1}^Nn_ix_{ij}
        \frac{\partial \pi_{im}}{\partial \beta_{\nu k}}=
        \left\{ \begin{array}{ll}
               -\sum_{i=1}^Nn_ix_{ij}x_{ik}\pi_{im}(1-\pi_{im})\,, & \nu =m\\
               \sum_{i=1}^N n_i x_{ij}x_{ik}\pi_{im}\pi_{i\nu}\,, & \nu \ne m
               \end{array}
        \right.

    and :math:`\mathbf{G}` denotes the gradient of the log-likelihood, the
    vector of first partial derivatives,

    .. math::
        \frac{\partial l(\beta)}{\partial \beta_{mj}}\,.

    Both the gradient and the Hessian are evaluated at the most recent estimate
    of the parameters, :math:`\beta^n`. The iteration continues until
    convergence or until maximum iterations are reached. Following the theory
    of likelihood estimation ([3]_), standard errors are obtained from Fisher's
    information matrix :math:`-\mathbf{H}^{-1}` evaluated at the final
    estimates.

    *4. Model Aggregation*

    When methods `fit` (with optional argument `update`) or `aggregate` are
    called, estimates of the same model from separate fits are combined
    using the method presented in [6]_. To illustrate, let :math:`\beta_1`
    and :math:`\beta_2` be the MLEs from separate fits to two different sets
    of data, and let :math:`\mathbf{H_1}` and :math:`\mathbf{H_2}` be the
    associated Hessian matrices. Then, the combined estimate

    .. math::
        \beta=(\mathbf{H_1} + \mathbf{H_2})^{-1}
        (\mathbf{H_1}\beta_1 + \mathbf{H_2}\beta_2)

    approximates the MLE of the combined data set. The model structure contains
    the combined estimates as well as other elements; see the attributes of
    the `LogisticRegression` class.

    References
    ----------
    .. [1] Hastie, Trevor, Robert Tibshirani, and Jerome Friedman (2009),
           *The Elements of Statistical Learning: Data Mining, Inference,
           and Prediction*, 2nd ed., Springer, New York.

    .. [2] Hosmer, David W., Stanley Lemeshow, and Rodney X. Sturdivant (2013),
           *Applied Logistic Regression*, Third Edition, John Wiley & Sons,
           New Jersey.

    .. [3] Kendall, Maurice G., and Alan Stuart (1979), *The Advanced Theory
           of Statistics, Volume 2: Inference and Relationship*, 4th ed.,
           Oxford University Press, New York.

    .. [4] Prentice, Ross L. (1976), *A generalization of the probit and
           logit methods for dose response curves*, Biometrics, 32, 761-768.

    .. [5] Thisted, Ronald. A. (1988), *Elements of Statistical Computing:
           Numerical Computation*, Chapman & Hall, New York.

    .. [6] Xi, Ruibin, Nan Lin, and Yixin Chen (2008), *Compression and
           Aggregation for Logistic Regression Analysis in Data Cubes*,
           IEEE Transactions on Knowledge and Data Engineering, Vol. 1, No. 1.

    Examples
    --------
    *Example 1:*

    The first example is from [4]_ and involves the mortality of beetles after
    five hours exposure to eight different concentrations of carbon disulphide.
    The table below lists the number of beetles exposed (*N*) to each
    concentration level of carbon disulphide (`x1`, given as log dosage) and
    the number of deaths which result (`y1`):

    +----------------+-------------------------------+----------------------+
    | **Log Dosage** | **Number of Beetles Exposed** | **Number of Deaths** |
    +================+===============================+======================+
    |    1.690       |             59                |          6           |
    +----------------+-------------------------------+----------------------+
    |    1.724       |             60                |         13           |
    +----------------+-------------------------------+----------------------+
    |    1.755       |             62                |         18           |
    +----------------+-------------------------------+----------------------+
    |    1.784       |             56                |         28           |
    +----------------+-------------------------------+----------------------+
    |    1.811       |             63                |         52           |
    +----------------+-------------------------------+----------------------+
    |    1.836       |             59                |         53           |
    +----------------+-------------------------------+----------------------+
    |    1.861       |             62                |         61           |
    +----------------+-------------------------------+----------------------+
    |    1.883       |             60                |         60           |
    +----------------+-------------------------------+----------------------+

    The number of deaths at each concentration level is the binomial response
    (`n_classes = 2`) and the log-dosage is the single predictor variable.
    Note that this example illustrates the use of class `ResponseFormatRef`
    to generate the matrix of response class counts. The reference class is
    defined as the class of beetles that survive a certain log dosage.

    >>> import numpy as np
    >>> import imsl.regression as reg
    >>> y1 = np.array([6.0, 13.0, 18.0, 28.0, 52.0, 53.0, 61.0, 60.0])
    >>> x1 = np.array([1.69, 1.724, 1.755, 1.784, 1.811, 1.836, 1.861, 1.883])
    >>> freqs = np.array([59.0, 60.0, 62.0, 56.0, 63.0, 59.0, 62.0, 60.0])
    >>> n_predictors = 1
    >>> n_classes = 2
    >>> response_counts = reg.ResponseFormatRef(y1, frequencies=freqs)
    >>> model = reg.LogisticRegression(n_predictors, n_classes)
    >>> model.fit(x1, response_counts)
    >>> np.set_printoptions(precision=2)
    >>> print("Coefficient estimates:\n" +
    ...       str(model.coefficients)) #doctest: +NORMALIZE_WHITESPACE
    Coefficient estimates:
    [[-60.76  34.3 ]
     [  0.     0.  ]]

    *Example 2:*

    In the second example, the response is a multinomial random variable
    with four outcome classes. The three predictor variables represent two
    categorical variables and one continuous variable. A subset of two
    predictor variables along with the intercept defines the logistic
    regression model. For each observation, the ID of the outcome class is
    defined in array `y`.
    A test of significance is performed.

    >>> import numpy as np
    >>> import imsl.regression as reg
    >>> from scipy.stats import chi2
    >>> # Array of predictors
    >>> x = np.array([[3, 25.92869, 1], [2,51.63245, 2], [2, 25.78432, 1],
    ...               [1, 39.37948, 1], [3,24.65058, 1], [3, 45.20084, 1],
    ...               [3, 52.6796, 2], [2, 44.28342, 2], [3, 40.63523, 2],
    ...               [3, 51.76094, 1], [3, 26.30368, 1], [3, 20.70230, 2],
    ...               [3, 38.74273, 2], [3,19.47333, 1], [2, 26.42211, 1],
    ...               [3, 37.05986, 2], [2, 51.67043, 2], [1, 42.40156, 1],
    ...               [3, 33.90027, 2], [2, 35.43282, 1], [2, 44.30369, 1],
    ...               [1, 46.72387, 1], [2, 46.99262, 1], [1, 36.05923, 1],
    ...               [3, 36.83197, 2], [2, 61.66257, 2], [1, 25.67714, 1],
    ...               [2, 39.08567, 2], [1, 48.84341, 2], [2, 39.34391, 1],
    ...               [3, 24.73522, 1], [2, 50.55251, 2], [1, 31.34263, 2],
    ...               [2, 27.15795, 2], [1, 31.72685, 1], [1, 25.00408, 1],
    ...               [2, 26.35457, 2], [3, 38.12343, 1], [1, 49.9403, 1],
    ...               [2, 42.45779, 2], [1, 38.80948, 2], [1, 43.22799, 2],
    ...               [1, 41.87624, 1], [3, 48.0782, 1], [1, 43.23673, 2],
    ...               [3, 39.41294, 1], [2, 23.93346, 1], [3, 42.8413, 2],
    ...               [3, 30.40669, 1], [1, 37.77389, 1]])
    >>> x1 = np.asarray(x[:, 0:2])
    >>> # Array of response IDs
    >>> y = np.array([1, 2, 3, 4, 3, 3, 4, 4, 4, 4, 2, 1, 4, 1, 1, 1,
    ... 4, 4, 3, 1, 2, 3, 3, 4, 2, 3, 4, 1, 2, 4, 3, 4, 4, 1, 3, 4, 4,
    ... 2, 3, 4, 2, 2, 4, 3, 1, 4, 3, 4, 2, 3])
    >>> n_predictors = 2
    >>> n_classes = 4
    >>> response_counts = reg.ResponseFormatID(y, n_classes)
    >>> model = reg.LogisticRegression(n_predictors, n_classes)
    >>> model.fit(x1, response_counts)
    >>> n_coefs = model.n_coeffs
    >>> lrstat = model.likeli_ratio_test_stat
    >>> dof = n_coefs * (n_classes - 1) - (n_classes - 1)
    >>> model_pval = 1.0 - chi2.cdf(lrstat, dof)
    >>> np.set_printoptions(formatter={'float': '{: 0.3f}'.format})
    >>> print("Coefficients:\n" +
    ...       str(model.coefficients)) #doctest: +NORMALIZE_WHITESPACE
    Coefficients:
    [[ 2.292  0.408 -0.111]
     [-1.162  0.245 -0.002]
     [-0.067  0.178 -0.017]
     [ 0.000  0.000  0.000]]
    >>> print("Standard Errors:\n" +
    ...       str(model.stderrs)) #doctest: +NORMALIZE_WHITESPACE
    Standard Errors:
    [[ 2.259  0.548  0.051]
     [ 2.122  0.500  0.044]
     [ 1.862  0.442  0.039]]
    >>> print("\nLog-likelihood: {0:5.2f}".
    ...       format(model.log_likeli)) #doctest: +NORMALIZE_WHITESPACE
    Log-likelihood: -62.92
    >>> print("\nLR test statistic: {0:5.2f}".
    ...       format(lrstat)) #doctest: +NORMALIZE_WHITESPACE
    LR test statistic:  7.68
    >>> print("{0:2d} deg. freedom, p-value: {1:5.4f}".format(
    ...       dof, model_pval)) #doctest: +NORMALIZE_WHITESPACE
    6 deg. freedom, p-value: 0.2623
    >>> # Put back the default options
    >>> np.set_printoptions()

    *Example 3:*

    The third example uses the same data as in the second example and an
    additional set of 50 observations using the same data generating process.
    The model structure includes all three predictor variables and an
    intercept, and a single model fit is approximated from two separate model
    fits. Example 3 also includes a fit on the full data set for comparison
    purposes.

    >>> import numpy as np
    >>> import imsl.regression as reg
    >>> # Array 1 of predictors
    >>> x1 = np.array([[3, 25.92869, 1], [2,51.63245, 2], [2, 25.78432, 1],
    ...                [1, 39.37948, 1], [3,24.65058, 1], [3, 45.20084, 1],
    ...                [3, 52.6796, 2], [2, 44.28342, 2], [3, 40.63523, 2],
    ...                [3, 51.76094, 1], [3, 26.30368, 1], [3, 20.70230, 2],
    ...                [3, 38.74273, 2], [3,19.47333, 1], [2, 26.42211, 1],
    ...                [3, 37.05986, 2], [2, 51.67043, 2], [1, 42.40156, 1],
    ...                [3, 33.90027, 2], [2, 35.43282, 1], [2, 44.30369, 1],
    ...                [1, 46.72387, 1], [2, 46.99262, 1], [1, 36.05923, 1],
    ...                [3, 36.83197, 2], [2, 61.66257, 2], [1, 25.67714, 1],
    ...                [2, 39.08567, 2], [1, 48.84341, 2], [2, 39.34391, 1],
    ...                [3, 24.73522, 1], [2, 50.55251, 2], [1, 31.34263, 2],
    ...                [2, 27.15795, 2], [1, 31.72685, 1], [1, 25.00408, 1],
    ...                [2, 26.35457, 2], [3, 38.12343, 1], [1, 49.9403, 1],
    ...                [2, 42.45779, 2], [1, 38.80948, 2], [1, 43.22799, 2],
    ...                [1, 41.87624, 1], [3, 48.0782, 1], [1, 43.23673, 2],
    ...                [3, 39.41294, 1], [2, 23.93346, 1], [3, 42.8413, 2],
    ...                [3, 30.40669, 1], [1, 37.77389, 1]])
    >>> # Array 2 of predictors
    >>> x2 = np.array([[1, 35.66064, 1], [1, 26.68771, 1], [3, 23.11251, 2],
    ...                [3, 58.14765, 1], [2, 44.95038, 1], [3, 42.45634, 1],
    ...                [3, 34.97379, 2], [3, 53.54269, 2], [2, 32.57257, 2],
    ...                [1, 46.91201, 1], [1, 30.93306, 1], [1, 51.63743, 2],
    ...                [1, 34.67712, 2], [3, 53.84584, 1], [3, 14.97474, 1],
    ...                [2, 44.4485, 2], [2, 47.10448, 1], [3, 43.96467, 1],
    ...                [3, 55.55741, 2], [2, 36.63123, 2], [3, 32.35164, 2],
    ...                [2, 55.75668, 1], [1, 36.83637, 2], [3, 46.7913, 1],
    ...                [3, 44.24153, 2], [2, 49.94011, 1], [2, 41.91916, 1],
    ...                [3, 24.78584, 2], [3, 50.79019, 2], [2, 39.97886, 2],
    ...                [1, 34.42149, 2], [2, 41.93271, 2], [1, 28.59433, 2],
    ...                [2, 38.47255, 2], [3, 32.11676, 2], [3, 37.19347, 1],
    ...                [1, 52.89337, 1], [1, 34.64874, 1], [2, 48.61935, 2],
    ...                [2, 33.99104, 1], [3, 38.32489, 2], [1, 35.53967, 2],
    ...                [1, 29.59645, 1], [2, 21.14665, 1], [2, 51.11257, 2],
    ...                [1, 34.20155, 1], [1, 44.40374, 1], [2, 49.67626, 2],
    ...                [3, 58.35377, 1], [1, 28.03744, 1]])
    >>> # Array 1 of response counts
    >>> y1 = np.array([1, 2, 3, 4, 3, 3, 4, 4, 4, 4, 2, 1, 4, 1, 1, 1, 4, 4,
    ...                3, 1, 2, 3, 3, 4, 2, 3, 4, 1, 2, 4, 3, 4, 4, 1, 3, 4,
    ...                4, 2, 3, 4, 2, 2, 4, 3, 1, 4, 3, 4, 2, 3])
    >>> # Array 2 of response counts
    >>> y2 = np.array([1, 4, 1, 4, 1, 1, 3, 1, 2, 4, 3, 1, 3, 2, 4, 4, 4, 2,
    ...                3, 2, 1, 4, 4, 4, 4, 3, 1, 1, 3, 1, 4, 2, 4, 2, 1, 2,
    ...                3, 1, 1, 4, 1, 2, 4, 3, 4, 2, 4, 3, 2, 4])
    >>> x3 = np.empty((100, 3))
    >>> y3 = np.empty((100,))
    >>> n_predictors = 3
    >>> n_classes = 4
    >>> resp1 = reg.ResponseFormatID(y1, n_classes)
    >>> # Fit first model to x1, resp1
    >>> model1 = reg.LogisticRegression(n_predictors, n_classes)
    >>> model1.fit(x1, resp1)
    >>> np.set_printoptions(formatter={'float': '{: 0.3f}'.format})
    >>> print("First Model Coefficients:\n" +
    ...       str(model1.coefficients)) #doctest: +NORMALIZE_WHITESPACE
    First Model Coefficients:
    [[ 1.691  0.350 -0.137  1.057]
     [-1.254  0.242 -0.004  0.115]
     [ 1.032  0.278  0.016 -1.954]
     [ 0.000  0.000  0.000  0.000]]
    >>> print("First Model Standard Errors:\n" +
    ...       str(model1.stderrs)) #doctest: +NORMALIZE_WHITESPACE
    First Model Standard Errors:
    [[ 2.389  0.565  0.061  1.025]
     [ 2.197  0.509  0.047  0.885]
     [ 2.007  0.461  0.043  0.958]]
    >>> # Update first model with x2, y2
    >>> resp2 = reg.ResponseFormatID(y2, n_classes)
    >>> model1.fit(x2, resp2, update=True)
    >>> print("Combined Model Coefficients:\n" +
    ...       str(model1.coefficients)) #doctest: +NORMALIZE_WHITESPACE
    Combined Model Coefficients:
    [[-1.169  0.649 -0.038  0.608]
     [-1.935  0.435  0.002  0.215]
     [-0.193  0.282  0.002 -0.630]
     [ 0.000  0.000  0.000  0.000]]
    >>> print("Combined Model Standard Errors:\n" +
    ...       str(model1.stderrs)) #doctest: +NORMALIZE_WHITESPACE
    Combined Model Standard Errors:
    [[ 1.489  0.359  0.029  0.588]
     [ 1.523  0.358  0.030  0.584]
     [ 1.461  0.344  0.030  0.596]]
    >>> # Combine data, using model1 instance
    >>> y3[0:50] = y1[:]
    >>> y3[50:100] = y2[:]
    >>> x3[0:50, :] = x1[:, :]
    >>> x3[50:100, :] = x2[:, :]
    >>> resp3 = reg.ResponseFormatID(y3, n_classes)
    >>> model1.fit(x3, resp3)
    >>> print("Full Data Model Coefficients:\n" +
    ...       str(model1.coefficients)) #doctest: +NORMALIZE_WHITESPACE
    Full Data Model Coefficients:
    [[-1.009  0.640 -0.051  0.764]
     [-2.008  0.436  0.003  0.263]
     [-0.413  0.299  0.004 -0.593]
     [ 0.000  0.000  0.000  0.000]]
    >>> print("Full Data Model Standard Errors:\n" +
    ...       str(model1.stderrs)) #doctest: +NORMALIZE_WHITESPACE
    Full Data Model Standard Errors:
    [[ 1.466  0.350  0.029  0.579]
     [ 1.520  0.357  0.029  0.581]
     [ 1.389  0.336  0.028  0.577]]
    >>> # Put back the default options
    >>> np.set_printoptions()

    """

    def __init__(self, n_predictors, n_classes, ref_class=None,
                 intercept=True, x_interact=None):
        """Instantiate LogisticRegression class."""
        _n_predictors = int(n_predictors)
        if (_n_predictors < 1):
            raise ValueError("the number of predictor variables must"
                             " be greater than zero")
        _n_classes = int(n_classes)
        if (_n_classes < 2):
            raise ValueError("the number of response classes must"
                             " be greater than one")

        if ref_class is None:
            _ref_class = _n_classes
        else:
            _ref_class = int(ref_class)
            if not(1 <= _ref_class <= n_classes):
                raise ValueError("the reference class number must be in the"
                                 " range (1, n_classes+1)")

        _intercept = int(intercept)
        if _intercept not in (0, 1):
            raise ValueError("intercept must be True or False")

        _n_x_interact = 0
        if x_interact is not None:
            _x_interact = _numpy.asarray(x_interact, order='C',
                                         dtype=_numpy.int32)
            if _x_interact.ndim != 2:
                raise ValueError("array of dimension {} not"
                                 " supported".format(_x_interact.ndim))

            if _x_interact.size == 0:
                raise ValueError("empty array not supported")

            if _x_interact.shape[1] != 2:
                raise ValueError("array of column dimension {} not"
                                 " supported".format(_x_interact.shape[1]))

            _n_x_interact = _x_interact.shape[0]

            # Check x_interact values
            for i in range(_n_x_interact):
                error = False
                if not(0 <= _x_interact[i, 0] < _n_predictors):
                    error = True
                if not(0 <= _x_interact[i, 1] < _n_predictors):
                    error = True

                if error:
                    raise ValueError("entries of array x_interact must be "
                                     "greater than or equal to zero and less "
                                     "than n_predictors")
                if _x_interact[i, 0] == _x_interact[i, 1]:
                    raise ValueError("per row entries in array x_interact "
                                     "must be different")

        self._n_predictors = _n_predictors
        self._n_classes = _n_classes
        self._ref_class = _ref_class
        self._intercept = _intercept
        if x_interact is None:
            self._x_interact = None
            self._n_x_interact = 0
        else:
            self._x_interact = _x_interact
            self._n_x_interact = _n_x_interact
        self._coefficients = None
        self._lrstat = None
        self._n_obs = 0
        self._n_updates = 0
        self._n_coeffs = _intercept + _n_predictors + _n_x_interact
        self._loglike = None
        self._model = None

        self._meany = _numpy.zeros((_n_classes,), dtype=_numpy.float64)
        self._struct_coefs = _numpy.zeros((_n_classes - 1, self._n_coeffs),
                                          dtype=_numpy.float64)
        self._stderrs = _numpy.zeros((_n_classes - 1, self._n_coeffs),
                                     dtype=_numpy.float64)
        nn = (_n_classes - 1) * self._n_coeffs
        self._hess = _numpy.zeros((nn, nn), dtype=_numpy.float64)
        self._grad = _numpy.zeros((nn,), dtype=_numpy.float64)
        self._coefficients = _numpy.zeros((_n_classes, self._n_coeffs),
                                          dtype=_numpy.float64)
        self._before_first_fit_call = True
        self._common_type = None

    @property
    def coefficients(self):
        """Return the logistic regression coefficients.

        Returns
        -------
        *(n_classes, n_coeffs) ndarray*
            Array containing the regression coefficients.

        Notes
        -----
        The last row (row `n_classes`) of the returned array represents
        the reference class and is set to all zeros. If
        `ref_class < n_classes`, rows `ref_class` and `n_classes` are swapped,
        i.e. the coefficients for class `n_classes` will be returned in row
        `ref_class` and vice versa.

        """
        if self._model is not None:
            return _numpy.copy(self._coefficients)
        else:
            return None

    @property
    def likeli_ratio_test_stat(self):
        """Return the likelihood ratio test statistic.

        Returns
        -------
        *float*
            The value of the likelihood ratio test statistic.

        """
        return self._lrstat

    @property
    def n_obs(self):
        """Return the total number of observations.

        Returns
        -------
        *int*
            The total number of observations used in the model since the last
            or before the first model fit.

        """
        return self._n_obs

    @property
    def n_updates(self):
        """Return the number of updates.

        Returns
        -------
        *int*
            The number of model updates and aggregations since the last or
            before the first model fit.

        """
        return self._n_updates

    @property
    def n_coeffs(self):
        """Return the number of coefficients in the model."""
        return self._n_coeffs

    @property
    def log_likeli(self):
        """Return the log-likelihood at the estimated coefficients."""
        if self._model is None:
            return None
        else:
            return self._loglike

    @property
    def class_means(self):
        """Return the overall means for each class variable.

        Returns
        -------
        *(n_classes,) ndarray*
            Array containing the overall means.

        """
        if self._model is None:
            return None
        else:
            return _numpy.copy(self._meany)

    @property
    def stderrs(self):
        """Return the standard errors for the estimated coefficients.

        Returns
        -------
        *(n_classes-1, n_coeffs) ndarray*
            Array containing the estimated standard errors for the
            estimated regression coefficients.

        """
        if self._model is None:
            return None
        else:
            return _numpy.copy(self._stderrs)

    @property
    def hessian(self):
        """Return the Hessian of the log-likelihood.

        Returns
        -------
        *((n_classes-1)*n_coeffs, (n_classes-1)*n_coeffs) ndarray*
            Array containing the estimated Hessian matrix at the
            estimated coefficients.

        """
        if self._model is None:
            return None
        else:
            return _numpy.copy(self._hess)

    @property
    def gradient(self):
        """Return the Gradient of the log-likelihood.

        Returns
        -------
        *((n_classes-1)*n_coeffs,) ndarray*
            Array containing the estimated gradient at the estimated
            coefficients.

        """
        if self._model is None:
            return None
        else:
            return _numpy.copy(self._grad)

    @property
    def ref_class(self):
        """Return the number of the reference class."""
        return self._ref_class

    @property
    def intercept(self):
        """Return information about an intercept in the model.

        Returns
        -------
        *bool*
            *True*, if an intercept is present, *False* otherwise.

        """
        return bool(self._intercept)

    @property
    def n_predictors(self):
        """Return the number of predictors."""
        return self._n_predictors

    @property
    def n_x_interact(self):
        """Return the number of interaction terms in the model."""
        return self._n_x_interact

    @property
    def n_classes(self):
        """Return the number of classes (categories) in the model."""
        return self._n_classes

    def fit(self, x, y, update=False, guess=None, tol=None, max_iter=20):
        r"""Fit or update the logistic regression model using the given data.

        Parameters
        ----------
        x : *(n_obs,) or (n_obs,n_predictors) array_like*
            Array containing `n_obs` samples of the `n_predictors` predictor
            variables.

        y : *Object*
            An object of type `ResponseFormatRef`, `ResponseFormatID` or
            `ResponseFormatAll`, containing information on the responses
            corresponding to the predictor variables. Essentially, from `y`
            attribute `class_counts_matrix`, the `n_obs` by `n_classes` matrix
            containing the response counts, is used.

        update : *bool, optional*
            If *True*, method `fit` updates the actual logistic regression
            fit by generating a fit to the new data `x`, `y` and aggregating
            it with the existing fit.
            If *False*, method `fit` replaces the current fit with a new
            fit based on the training data `x`, `y`.

            Default: `update` = *False*.

        guess : *(n_classes,) or (n_classes, n_coeffs) array_like, optional*
            Initial guess of the regression coefficients. Here,
            `n_coeffs` = `n_predictors+n_x_interact` if no intercept term is
            included, and `n_coeffs` = `n_predictors+n_x_interact+1` if an
            intercept term is included.

            By default, an initial guess is computed internally.

        tol : *float, optional*
            Convergence tolerance. Iteration completes when the normed
            difference between successive estimates is less than `tol` or
            `max_iter` iterations are reached.

            Default: `tol` = 100.0 * `eps`, where `eps` denotes machine
            epsilon.

        max_iter : *int, optional*
            The maximum number of iterations.

        Notes
        -----
        The iteration stops when the estimates converge within tolerance, when
        maximum iterations are reached, or when the gradient converges within
        tolerance, whichever event occurs first. When the gradient converges
        before the coefficient estimates converge, a condition in the data
        known as complete or quasi-complete separation may be present.
        Separation in the data means that one or more independent variables
        perfectly predicts the response. When detected, the method stops the
        iteration, issues a warning, and returns the current values of the
        model estimates. Some of the coefficient estimates and standard errors
        may not be reliable. Furthermore, overflow issues may occur before the
        gradient converges. In such cases, the method throws an exception.

        """
        _update = int(update)
        if _update not in (0, 1):
            raise ValueError("update must be True or False")

        if x is None:
            raise TypeError("None not supported")

        _x = _numpy.asarray(x, order='C')

        # attempt to promote x to a compatible type.
        if (_update == 0 or self._before_first_fit_call):
            common_type = _numpy.promote_types(_numpy.float64, _x.dtype)
            self._common_type = common_type
        else:
            common_type = self._common_type

        _x = _numpy.asarray(_x, dtype=common_type)

        if (not _numpy.issubdtype(_x.dtype, _numpy.float64)):
            raise TypeError("array type {} not supported".format(
                _x.dtype.name))

        if _x.ndim not in (1, 2):
            raise ValueError("array of dimension {} not"
                             " supported".format(_x.ndim))

        if _x.size == 0:
            raise ValueError("empty array not supported")

        if ((_x.ndim == 1 and self._n_predictors != 1)
                or (_x.ndim == 2 and _x.shape[1] != self._n_predictors)):
            raise ValueError("number of columns in x must be equal to the "
                             "number of predictors in the model")

        _nobs = _x.shape[0]

        if y is None:
            raise TypeError("None not supported")

        if not (isinstance(y, ResponseFormatRef)
                or isinstance(y, ResponseFormatID)
                or isinstance(y, ResponseFormatAll)):
            raise TypeError("Type of y not supported")

        _y = y.class_counts_matrix
        _y = _numpy.asarray(_y, dtype=common_type, order='C')

        if (_y.shape[0] != _nobs):
            raise ValueError("number of rows of y must be equal to the "
                             "number of rows of x")

        if (_y.shape[1] != self._n_classes):
            raise ValueError("number of columns of y must be equal to the"
                             " number of response classes in the model")

        _frequencies = _numpy.zeros((_nobs,), dtype=common_type)
        for i in range(_nobs):
            _frequencies[i] = _y[i, :].sum()

        if guess is not None:
            _guess = _numpy.asarray(guess, dtype=common_type, order='C')
            if _guess.size == 0:
                raise ValueError("empty array not supported")

            if _guess.ndim not in (1, 2):
                raise ValueError("array of dimension {} not"
                                 " supported".format(_guess.ndim))

            if (_guess.shape[0] != self._n_classes):
                raise ValueError("number of rows of guess must be equal to "
                                 "the number of response classes in the "
                                 "model")

            if ((_guess.ndim == 1 and self._n_coeffs != 1)
                    or (_guess.ndim == 2
                        and _guess.shape[1] != self._n_coeffs)):
                raise ValueError("number of columns in guess must be equal "
                                 "to the number of coefficients in the model")

        if tol is not None:
            _tol = float(tol)
            if _tol <= 0.0:
                raise ValueError("tol must be greater than zero")

        _max_iter = int(max_iter)
        if (_max_iter < 0):
            raise ValueError("max_iter must be nonnegative")

        # do the computations
        if (_update == 0 or self._before_first_fit_call):
            nextModel = _ctypes.POINTER(_imsllib.imsls_d_model)()
        else:
            nextModel = _ctypes.POINTER(_imsllib.imsls_d_model)(self._model)

        lrstat = _ctypes.c_double()

        args = []
        args.append(_nobs)
        args.append(self._n_predictors)
        args.append(self._n_classes)
        args.append(_x.ctypes.data_as(_ctypes.c_void_p))
        args.append(_y.ctypes.data_as(_ctypes.c_void_p))

        # Add the optional input arguments
        args.append(_constants.IMSLS_FREQUENCIES)
        args.append(_frequencies.ctypes.data_as(_ctypes.c_void_p))
        args.append(_constants.IMSLS_REFERENCE_CLASS)
        args.append(self._ref_class)

        if self._intercept == 0:
            args.append(_constants.IMSLS_NO_INTERCEPT)

        if self._n_x_interact > 0:
            args.append(_constants.IMSLS_X_INTERACTIONS)
            args.append(self._n_x_interact)
            args.append(self._x_interact.ctypes.data_as(_ctypes.c_void_p))

        if tol is not None:
            args.append(_constants.IMSLS_TOLERANCE)
            args.append(_ctypes.c_double(_tol))

        args.append(_constants.IMSLS_MAX_ITER)
        args.append(_max_iter)

        self._coefficients = _numpy.asarray(self._coefficients,
                                            dtype=common_type)

        if guess is not None:
            _init = 1
            args.append(_constants.IMSLS_INIT_INPUT)
            args.append(_init)
            # copy _guess into _coefficients
            if _guess.ndim == 1:
                self._coefficients[:, 0] = _guess[:]
            else:
                self._coefficients[:, :] = _guess[:, :]

        args.append(_constants.IMSLS_NEXT_RESULTS)
        args.append(_ctypes.byref(nextModel))

        args.append(_constants.IMSLS_COEFFICIENTS)
        args.append(self._coefficients.ctypes.data_as(_ctypes.c_void_p))

        # Note: Use of optional argument IMSLS_LRSTAT will issue
        # an IMSL warning if the model has no intercept. Could
        # be avoided by ignoring the optional argument in this case,
        # but the warning message seems informative.
        args.append(_constants.IMSLS_LRSTAT)
        args.append(_ctypes.byref(lrstat))

        args.append(0)

        func = _logistic_regression_func(_x.dtype)
        # Use try-finally statement to correctly free imsls_f_model
        # structure in the case where IMSL warnings are turned into
        # exceptions.
        try:
            func(*args)
            if (_update == 0 or self._before_first_fit_call):
                # Mimic CNL structure in Python
                self._meany = _numpy.asarray(self._meany, dtype=common_type)
                self._struct_coefs = _numpy.asarray(self._struct_coefs,
                                                    dtype=common_type)
                self._stderrs = _numpy.asarray(self._stderrs,
                                               dtype=common_type)
                self._hess = _numpy.asarray(self._hess, dtype=common_type)
                self._grad = _numpy.asarray(self._grad, dtype=common_type)

                # Copy CNL results into numpy arrays
                n_classes = self._n_classes
                n_coefs = self._n_coeffs
                nn = (n_classes - 1) * n_coefs
                self._meany[:] = nextModel.contents.meany[0:n_classes]
                for i in range(n_classes - 1):
                    temp = nextModel.contents.coefs[i * n_coefs:
                                                    (i + 1) * n_coefs]
                    self._struct_coefs[i, :] = temp
                    temp = nextModel.contents.stderrs[i * n_coefs:
                                                      (i + 1) * n_coefs]
                    self._stderrs[i, :] = temp

                self._grad[:] = nextModel.contents.grad[0:nn]

                for i in range(nn):
                    self._hess[i, :] = nextModel.contents.hess[i * nn:(i + 1)
                                                               * nn]

                data_type = _ctypes.POINTER(_ctypes.c_double)
                model = _imsllib.imsls_d_model

                # Build CNL structure with Python arrays
                self._model = model(nextModel.contents.n_obs,
                                    nextModel.contents.n_updates,
                                    nextModel.contents.n_coefs,
                                    nextModel.contents.loglike,
                                    self._meany.ctypes.data_as(data_type),
                                    self._struct_coefs.ctypes.data_as(
                                        data_type),
                                    self._stderrs.ctypes.data_as(data_type),
                                    self._hess.ctypes.data_as(data_type),
                                    self._grad.ctypes.data_as(data_type))

                self._before_first_fit_call = False
                self._n_obs = _nobs
                self._n_updates = 0
                self._loglike = nextModel.contents.loglike
                self._lrstat = lrstat.value
            else:  # pure update step
                self._n_obs += _nobs
                self._n_updates += 1
                self._loglike = nextModel.contents.loglike
                self._lrstat = lrstat.value
        finally:
            if (_update == 0 or self._before_first_fit_call):
                # Check if nextModel is a NULL-pointer
                if bool(nextModel):
                    imsls_free = _imsllib.imsls_free
                    # Free nextModel CNL structure
                    if bool(nextModel.contents.meany):
                        imsls_free(nextModel.contents.meany)
                    if bool(nextModel.contents.coefs):
                        imsls_free(nextModel.contents.coefs)
                    if bool(nextModel.contents.stderrs):
                        imsls_free(nextModel.contents.stderrs)
                    if bool(nextModel.contents.hess):
                        imsls_free(nextModel.contents.hess)
                    if bool(nextModel.contents.grad):
                        imsls_free(nextModel.contents.grad)
                    imsls_free(nextModel)

    def predict(self, data, responses=None, frequencies=None, confidence=95.0):
        r"""Predict responses for new predictor samples.

        Parameters
        ----------
        data : *(n,) or (n, n_predictors) array_like*
            Array containing the values of the `n_predictors` predictor
            variables. Each of the `n` rows of `data` describes one predictor
            sample.

        responses : *Object, optional*
            An object of type `ResponseFormatRef`, `ResponseFormatID` or
            `ResponseFormatAll`, containing information on the actual
            responses corresponding to the predictor variables. Essentially,
            from `responses` attribute `class_counts_matrix`, the `n` by
            `n_classes` matrix containing the response counts, is used.

        frequencies : *(n,) array_like, optional*
            Array containing the number of replications or trials for each
            of the `n` observations. `frequencies` is not used if optional
            argument `responses` is present.

            Default: `frequencies = 1`.

        confidence : *float, optional*
            Confidence level used in the calculation of the prediction
            intervals. For each predicted value, `confidence` % prediction
            intervals are provided.

        Returns
        -------
        A named tuple with the following fields:

        predictions : *(n, n_classes) ndarray*
            Array containing the predicted responses.

        pred_limits : *tuple*
            A two-element tuple consisting of two ndarrays of format
            *(n, n_classes)* containing lower (in *pred_limits[0]*) and
            upper (in *pred_limits[1]*) prediction limits.

        pred_err : *float*
            The mean squared prediction error when `responses` is present.
            Set to `numpy.NaN` otherwise.

        Notes
        -----
        Method `predict` calculates the predicted outcomes for a binomial or
        multinomial response variable given an estimated logistic regression
        model and new observations of the predictor variables.

        For a binary response *y*, the objective is to estimate the conditional
        probability of success, :math:`\pi_1(x)=\Pr(y=1|x)`, where
        :math:`x=(x_1,x_2,\ldots,x_p)^T` is a realization of *p* predictors.
        In particular, the estimated probability of success is

        .. math::
            \hat{\pi}_1(x) = \frac{\exp(\hat{\eta}_1)}{1+\exp(\hat{\eta}_1)}\,,

        where

        .. math::
            \hat{\eta}_1 = \hat{\beta}_{10}+x^T\hat{\beta}_1

        and

        .. math::
            \hat{\beta}_{10},\; \hat{\beta}_1=(\hat{\beta}_{11},
            \hat{\beta}_{12},\ldots,\hat{\beta}_{1p})^T

        are the coefficient estimates.
        Then, :math:`\hat{y}=n_i\pi_1(x_i)`. That is, :math:`\hat{y}` is the
        expected value of the response under the estimated model given the
        values of the predictor variables.

        Similarly, for a multinomial response, with class *K* the reference
        class,

        .. math::
            \hat{\pi}_k(x)=
            \frac{\exp(\hat{\eta}_{ik})}{\sum_{l=1}^K\exp(\hat{\eta}_{il})}=
            \frac{\exp(\hat{\eta}_{ik})}
            {1+\sum_{l=1}^{K-1}\exp(\hat{\eta}_{il})}\,.

        Then,

        .. math::
            \hat{\pi}_K(x)= 1 - \sum_{l=1}^{K-1}\hat{\pi}_l(x)\,,

        and :math:`\hat{y}_k=n_i\pi_k(x_i)`. If the actual responses are given,
        the mean squared prediction error is

        .. math::
            \text{mspe}=\frac{1}{NK}\sum_{k=1}^K\sum_{i=1}^N
            (\hat{y}_{ik} - y_{ik})^2\,.

        By default, 100(1-:math:`\alpha`)% prediction intervals are provided
        for the predicted values by first finding the prediction standard
        errors, *SE*, of the logits,
        :math:`\hat{\eta}_{ik}=\hat{\beta}_{0k}+x_i^T\hat{\beta}_k`, and then
        evaluating

        .. math::
            \frac{\exp(\hat{\eta}_{ik}\pm z_{\alpha/2}SE(\hat{\eta}_{ik}))}
            {1+\sum_{l=1}^{K-1}\exp(\hat{\eta}_{il}\pm z_{\alpha/2}
            SE(\hat{\eta}_{il}))}

        to obtain the upper and lower limits for :math:`\hat{\pi}_k(x_i)`,
        where :math:`z_{\alpha/2}` is the upper :math:`\alpha/2` quantile of
        the standard normal distribution. Note that properties of the
        prediction intervals are valid only if the new observations are inside
        the range of the original data used to fit the model. Generally, the
        model should not be used to extrapolate outside the range of the
        original data. See [1]_ for further details.

        References
        ----------
        .. [1] Hosmer, David W., Stanley Lemeshow, and Rodney X. Sturdivant
               (2013), *Applied Logistic Regression*, Third Edition, John
               Wiley & Sons, New Jersey.

        .. [2] Prentice, Ross L. (1976), *A generalization of the probit and
               logit methods for dose response curves*, Biometrics, 32,
               761-768.

        Examples
        --------
        *Example 1:*

        The model fit to the beetle mortality data of [2]_ is used to predict
        the expected mortality at three new doses. For the original data, see
        *Example 1* of class `LogisticRegression`.

        +----------------+-----------------------+----------------------+
        | **Log Dosage** | **Number of Beetles** | **Number of Deaths** |
        |                | **Exposed**           |                      |
        +================+=======================+======================+
        |    1.66        |      16               |         ??           |
        +----------------+-----------------------+----------------------+
        |    1.87        |      22               |         ??           |
        +----------------+-----------------------+----------------------+
        |    1.71        |      11               |         ??           |
        +----------------+-----------------------+----------------------+

        >>> import numpy as np
        >>> import imsl.regression as reg
        >>> y1 = np.array([6, 13, 18, 28, 52, 53, 61, 60])
        >>> x1 = np.array([1.69, 1.724, 1.755, 1.784, 1.811,
        ...                1.836, 1.861, 1.883])
        >>> x2 = np.array([1.66, 1.87, 1.71])
        >>> freqs1 = np.array([59, 60, 62, 56, 63, 59, 62, 60])
        >>> freqs2 = np.array([16, 22, 11])
        >>> n_predictors = 1
        >>> n_classes = 2
        >>> resp1 = reg.ResponseFormatRef(y1, frequencies=freqs1)
        >>> model = reg.LogisticRegression(n_predictors, n_classes)
        >>> model.fit(x1, resp1)
        >>> np.set_printoptions(precision=2)
        >>> print("Coefficient estimates:\n" +
        ...       str(model.coefficients)) #doctest: +NORMALIZE_WHITESPACE
        Coefficient estimates:
        [[-60.76  34.3 ]
         [  0.     0.  ]]
        >>> yhat = model.predict(x2, frequencies=freqs2)
        >>> print("Dose\t N\tExpected Deaths")  #doctest: +NORMALIZE_WHITESPACE
        Dose     N      Expected Deaths
        >>> for i in range(x2.size):
        ...     print("{0:4.2f}\t{1:2.1f}\t\t{2:5.2f}".format(x2[i],
        ...           freqs2[i],
        ...           yhat.predictions[i, 0]))  #doctest: +NORMALIZE_WHITESPACE
        1.66    16.0             0.34
        1.87    22.0            21.28
        1.71    11.0             1.19

        *Example 2:*

        A logistic regression model is fit to artificial (noisy) data with
        four classes and three predictor variables and used to predict class
        probabilities at 10 new values of the predictor variables. Also shown
        are the mean squared prediction error and upper and lower limits of the
        95% prediction interval for each predicted value.

        >>> import numpy as np
        >>> import imsl.regression as reg
        >>> from scipy.stats import chi2
        >>> # Array of predictors
        >>> x = np.array([[3, 25.92869, 1], [2,51.63245, 2], [2, 25.78432, 1],
        ...               [1, 39.37948, 1], [3,24.65058, 1], [3, 45.20084, 1],
        ...               [3, 52.6796, 2], [2, 44.28342, 2], [3, 40.63523, 2],
        ...               [3, 51.76094, 1], [3, 26.30368, 1], [3, 20.70230, 2],
        ...               [3, 38.74273, 2], [3,19.47333, 1], [2, 26.42211, 1],
        ...               [3, 37.05986, 2], [2, 51.67043, 2], [1, 42.40156, 1],
        ...               [3, 33.90027, 2], [2, 35.43282, 1], [2, 44.30369, 1],
        ...               [1, 46.72387, 1], [2, 46.99262, 1], [1, 36.05923, 1],
        ...               [3, 36.83197, 2], [2, 61.66257, 2], [1, 25.67714, 1],
        ...               [2, 39.08567, 2], [1, 48.84341, 2], [2, 39.34391, 1],
        ...               [3, 24.73522, 1], [2, 50.55251, 2], [1, 31.34263, 2],
        ...               [2, 27.15795, 2], [1, 31.72685, 1], [1, 25.00408, 1],
        ...               [2, 26.35457, 2], [3, 38.12343, 1], [1, 49.9403, 1],
        ...               [2, 42.45779, 2], [1, 38.80948, 2], [1, 43.22799, 2],
        ...               [1, 41.87624, 1], [3, 48.0782, 1], [1, 43.23673, 2],
        ...               [3, 39.41294, 1], [2, 23.93346, 1], [3, 42.8413, 2],
        ...               [3, 30.40669, 1], [1, 37.77389, 1]])
        >>> # Array of response IDs
        >>> y = np.array([1, 2, 3, 4, 3, 3, 4, 4, 4, 4, 2, 1, 4, 1, 1, 1,
        ...               4, 4, 3, 1, 2, 3, 3, 4, 2, 3, 4, 1, 2, 4, 3, 4,
        ...               4, 1, 3, 4, 4, 2, 3, 4, 2, 2, 4, 3, 1, 4, 3, 4,
        ...               2, 3])
        >>> newx = np.array([[2, 25.92869, 1], [2, 51.63245, 2],
        ...                  [1, 25.78432, 1], [3, 39.37948, 1],
        ...                  [3, 24.65058, 1], [3, 45.20084, 1],
        ...                  [2, 52.6796, 2], [3, 44.28342, 2],
        ...                  [3,40.63523,2],  [3, 51.76094, 1]])
        >>> newy =  np.array([3, 2, 1, 1, 4, 3, 2, 2, 1, 2])
        >>> n_predictors = 3
        >>> n_classes = 4
        >>> resp = reg.ResponseFormatID(y, n_classes)
        >>> resp_new = reg.ResponseFormatID(newy, n_classes)
        >>> model = reg.LogisticRegression(n_predictors, n_classes)
        >>> model.fit(x, resp)
        >>> yhat = model.predict(newx, responses=resp_new)
        >>> n_coefs = model.n_coeffs
        >>> lrstat = model.likeli_ratio_test_stat
        >>> dof = n_coefs * (n_classes-1) - (n_classes-1)
        >>> model_pval = 1.0 - chi2.cdf(lrstat, dof)
        >>> print("Model Fit Summary:\n" +
        ...       "Log-likelihood: {0:5.2f}\n".format(model.log_likeli) +
        ...       "LR test statistic: {0:5.2f}\n".format(lrstat) +
        ...       "Degrees of freedom: {0:2d}\n".format(dof) +
        ...       "P-value: {0:5.4f}".format(model_pval))
        ... #doctest: +NORMALIZE_WHITESPACE
        Model Fit Summary:
        Log-likelihood: -58.58
        LR test statistic: 16.37
        Degrees of freedom:  9
        P-value: 0.0595
        >>> print("Prediction Summary:\n" +
        ...       "Mean squared prediction error: {0:4.2f}".format(
        ...                                                 yhat.pred_err))
        ... #doctest: +NORMALIZE_WHITESPACE
        Prediction Summary:
        Mean squared prediction error: 0.21
        >>> print("Obs Class Estimate Lower Upper")
        Obs Class Estimate Lower Upper
        >>> for j in range(newx.shape[0]):
        ...     for i in range(n_classes):
        ...         print(" {0:2d}\t{1:d}     {2:4.2f}   {3:4.2f}  "
        ...               "{4:4.2f}".format(j+1, i+1,
        ...                                 yhat.predictions[j, i],
        ...                                 yhat.pred_limits[0][j, i],
        ...                                 yhat.pred_limits[1][j, i]))
        ... #doctest: +NORMALIZE_WHITESPACE
          1 1     0.26   0.14  0.35
          1 2     0.14   0.06  0.20
          1 3     0.31   0.18  0.36
          1 4     0.29   0.10  0.62
          2 1     0.04   0.01  0.14
          2 2     0.27   0.11  0.39
          2 3     0.12   0.04  0.25
          2 4     0.57   0.22  0.85
          3 1     0.23   0.07  0.38
          3 2     0.13   0.04  0.20
          3 3     0.28   0.12  0.34
          3 4     0.36   0.08  0.77
          4 1     0.06   0.02  0.14
          4 2     0.16   0.07  0.24
          4 3     0.49   0.28  0.54
          4 4     0.29   0.08  0.63
          5 1     0.34   0.17  0.41
          5 2     0.13   0.06  0.19
          5 3     0.30   0.17  0.34
          5 4     0.22   0.05  0.60
          6 1     0.03   0.00  0.09
          6 2     0.16   0.06  0.24
          6 3     0.53   0.27  0.60
          6 4     0.29   0.07  0.67
          7 1     0.04   0.01  0.13
          7 2     0.27   0.10  0.40
          7 3     0.13   0.04  0.26
          7 4     0.57   0.21  0.86
          8 1     0.14   0.04  0.26
          8 2     0.29   0.12  0.37
          8 3     0.12   0.04  0.21
          8 4     0.46   0.15  0.80
          9 1     0.21   0.08  0.33
          9 2     0.27   0.12  0.35
          9 3     0.10   0.03  0.19
          9 4     0.42   0.14  0.77
         10 1     0.01   0.00  0.05
         10 2     0.15   0.04  0.24
         10 3     0.57   0.23  0.67
         10 4     0.28   0.05  0.73

        """
        # A model fit must exist before method predict can be called
        if self._model is None:
            raise RuntimeError("Methods fit or aggregate must be called "
                               "before the predict call")

        _n_predictors = self._n_predictors
        _n_classes = self._n_classes
        _coefs = self._coefficients
        _common_type = self._common_type

        if data is None:
            raise TypeError("None not supported")

        # attempt to promote data to the reference data type.
        _data = _numpy.asarray(data, dtype=_common_type, order='C')

        if _data.ndim not in (1, 2):
            raise ValueError("array of dimension {} not"
                             " supported".format(_data.ndim))

        if _data.size == 0:
            raise ValueError("empty array not supported")

        if ((_data.ndim == 1 and _n_predictors != 1)
                or (_data.ndim == 2 and _data.shape[1] != _n_predictors)):
            raise ValueError("number of columns in data must be equal to the "
                             "number of predictors in the model")

        _nobs = _data.shape[0]

        if responses is not None:
            if not (isinstance(responses, ResponseFormatRef)
                    or isinstance(responses, ResponseFormatID)
                    or isinstance(responses, ResponseFormatAll)):
                raise TypeError("Type of responses not supported")

            _y = responses.class_counts_matrix
            _y = _numpy.asarray(_y, dtype=_common_type, order='C')

            if (_y.shape[0] != _nobs):
                raise ValueError("number of rows of responses must be equal "
                                 "to the number of rows of data")

            if (_y.shape[1] != _n_classes):
                raise ValueError("number of columns of responses must be "
                                 "equal to the number of response classes "
                                 "in the model")

            # Note: In CNL (flogpred.c), array frequencies is declared as
            # float, whereas the CNL docu states that the array is of type
            # int. The docu should be corrected.
            _frequencies = _numpy.empty((_nobs,), dtype=_common_type)
            for i in range(_nobs):
                _frequencies[i] = _y[i, :].sum()

        else:
            if frequencies is not None:
                _frequencies = _numpy.asarray(frequencies,
                                              dtype=_common_type,
                                              order='C')
                if _frequencies.ndim != 1:
                    raise ValueError("array of dimension {} not"
                                     " supported".format(_frequencies.ndim))

                if _frequencies.size != _nobs:
                    raise ValueError("number of elements in array frequencies "
                                     "must be equal to the number of rows in "
                                     "array data")

                # Check entries in frequencies
                for i in range(0, _nobs):
                    if _frequencies[i] < 0:
                        raise ValueError("entries in array frequencies must be"
                                         " greater than or equal to zero")
            else:
                _frequencies = _numpy.ones((_nobs,), dtype=_common_type)

        _confid = float(confidence)
        if (_confid <= 0.0 or _confid >= 100.0):
            raise ValueError("the confidence level must be between "
                             "0 and 100")

        # Compute prediction outcomes, upper and lower prediction limits
        _confid /= 100.0
        _n_intercept = self._intercept
        _hessian = self._hess
        _xinteract = self._x_interact

        _yhat, _low_lim, _up_lim = _mnl_probs(_data, _frequencies, _coefs,
                                              _hessian, _confid, _n_intercept,
                                              _xinteract)

        result = _collections.namedtuple("LogRegPredResults",
                                         ["predictions",
                                          "pred_limits",
                                          "pred_err"]
                                         )

        result.predictions = _yhat
        result.pred_limits = (_low_lim, _up_lim)

        # Compute mean squared prediction error
        if responses is not None:
            if (_n_classes != self.ref_class):
                base_class = self.ref_class
                _yt = _numpy.array(_y)
                # interchange columns
                for j in range(_nobs):
                    tmp_val = _yt[j, base_class - 1]
                    _yt[j, base_class - 1] = _yt[j, _n_classes - 1]
                    _yt[j, _n_classes - 1] = tmp_val
            else:
                _yt = _y

            tmp_val = 0.0
            for j in range(_nobs):
                for i in range(_n_classes):
                    err = _yt[j, i] - _yhat[j, i]
                    tmp_val += err * err

            tmp_val = tmp_val / (_nobs * _n_classes)
            result.pred_err = tmp_val
        else:
            result.pred_err = _numpy.NaN

        return result

    def aggregate(self, *models):
        r"""Combine separate fits of the logistic regression model.

        Parameters
        ----------
        models : *tuple*
            A collection of `LogisticRegression` instances. All objects
            in the collection must describe the same logistic regression
            model as the current instance.

        Notes
        -----
        Let `a`, `b`, `c` be `LogisticRegression` instances with the same
        model structure. If `c` has a fit, then `c.aggregate(a, b)`
        aggregates the fits described by `a`, `b` and `c`. If `c` has
        no existing fit, then `c.aggregate(a, b)` aggregates fits `a` and
        `b` in `c`.

        Examples
        --------
        A logistic regression model consisting of three predictor variables,
        an intercept and four response classes is fit to two different data
        sets. The two model fits are then aggregated. Regression coefficients
        and coefficient standard errors are printed for the individual fits
        and the aggregated model.

        >>> import numpy as np
        >>> import imsl.regression as reg
        >>> y1 = np.array([6, 13, 18, 28, 52, 53, 61, 60])
        >>> x1 = np.array([1.69, 1.724, 1.755, 1.784, 1.811,
        ...                1.836, 1.861, 1.883])
        >>> # Array 1 of predictors
        >>> x1 = np.array([[3, 25.92869, 1], [2,51.63245, 2],
        ...                [2, 25.78432, 1], [1, 39.37948, 1],
        ...                [3,24.65058, 1], [3, 45.20084, 1],
        ...                [3, 52.6796, 2], [2, 44.28342, 2],
        ...                [3, 40.63523, 2], [3, 51.76094, 1],
        ...                [3, 26.30368, 1], [3, 20.70230, 2],
        ...                [3, 38.74273, 2], [3,19.47333, 1],
        ...                [2, 26.42211, 1], [3, 37.05986, 2],
        ...                [2, 51.67043, 2], [1, 42.40156, 1],
        ...                [3, 33.90027, 2], [2, 35.43282, 1],
        ...                [2, 44.30369, 1], [1, 46.72387, 1],
        ...                [2, 46.99262, 1], [1, 36.05923, 1],
        ...                [3, 36.83197, 2], [2, 61.66257, 2],
        ...                [1, 25.67714, 1], [2, 39.08567, 2],
        ...                [1, 48.84341, 2], [2, 39.34391, 1],
        ...                [3, 24.73522, 1], [2, 50.55251, 2],
        ...                [1, 31.34263, 2], [2, 27.15795, 2],
        ...                [1, 31.72685, 1], [1, 25.00408, 1],
        ...                [2, 26.35457, 2], [3, 38.12343, 1],
        ...                [1, 49.9403, 1], [2, 42.45779, 2],
        ...                [1, 38.80948, 2], [1, 43.22799, 2],
        ...                [1, 41.87624, 1], [3, 48.0782, 1],
        ...                [1, 43.23673, 2], [3, 39.41294, 1],
        ...                [2, 23.93346, 1], [3, 42.8413, 2],
        ...                [3, 30.40669, 1], [1, 37.77389, 1]])
        >>> # Array 2 of predictors
        >>> x2 = np.array([[1, 35.66064, 1], [1, 26.68771, 1],
        ...                [3, 23.11251, 2], [3, 58.14765, 1],
        ...                [2, 44.95038, 1], [3, 42.45634, 1],
        ...                [3, 34.97379, 2], [3, 53.54269, 2],
        ...                [2, 32.57257, 2], [1, 46.91201, 1],
        ...                [1, 30.93306, 1], [1, 51.63743, 2],
        ...                [1, 34.67712, 2], [3, 53.84584, 1],
        ...                [3, 14.97474, 1], [2, 44.4485, 2],
        ...                [2, 47.10448, 1], [3, 43.96467, 1],
        ...                [3, 55.55741, 2], [2, 36.63123, 2],
        ...                [3, 32.35164, 2], [2, 55.75668, 1],
        ...                [1, 36.83637, 2], [3, 46.7913, 1],
        ...                [3, 44.24153, 2], [2, 49.94011, 1],
        ...                [2, 41.91916, 1], [3, 24.78584, 2],
        ...                [3, 50.79019, 2], [2, 39.97886, 2],
        ...                [1, 34.42149, 2], [2, 41.93271, 2],
        ...                [1, 28.59433, 2], [2, 38.47255, 2],
        ...                [3, 32.11676, 2], [3, 37.19347, 1],
        ...                [1, 52.89337, 1], [1, 34.64874, 1],
        ...                [2, 48.61935, 2], [2, 33.99104, 1],
        ...                [3, 38.32489, 2], [1, 35.53967, 2],
        ...                [1, 29.59645, 1], [2, 21.14665, 1],
        ...                [2, 51.11257, 2], [1, 34.20155, 1],
        ...                [1, 44.40374, 1], [2, 49.67626, 2],
        ...                [3, 58.35377, 1], [1, 28.03744, 1]])
        >>> # Array 1 of response IDs
        >>> y1 = np.array([1, 2, 3, 4, 3, 3, 4, 4, 4, 4, 2, 1, 4, 1, 1, 1, 4,
        ...                4, 3, 1, 2, 3, 3, 4, 2, 3, 4, 1, 2, 4, 3, 4, 4, 1,
        ...                3, 4, 4, 2, 3, 4, 2, 2, 4, 3, 1, 4, 3, 4, 2, 3])
        >>> # Array 2 of response IDs
        >>> y2 = np.array([1, 4, 1, 4, 1, 1, 3, 1, 2, 4, 3, 1, 3, 2, 4, 4, 4,
        ...                2, 3, 2, 1, 4, 4, 4, 4, 3, 1, 1, 3, 1, 4, 2, 4, 2,
        ...                1, 2, 3, 1, 1, 4, 1, 2, 4, 3, 4, 2, 4, 3, 2, 4])
        >>> n_predictors = 3
        >>> n_classes = 4
        >>> resp1 = reg.ResponseFormatID(y1, n_classes)
        >>> # Fit first model to x1, resp1
        >>> model1 = reg.LogisticRegression(n_predictors, n_classes)
        >>> model1.fit(x1, resp1)
        >>> np.set_printoptions(formatter={'float': '{: 0.3f}'.format})
        >>> print("First Model Coefficients:\n" +
        ...       str(model1.coefficients)) #doctest: +NORMALIZE_WHITESPACE
        First Model Coefficients:
        [[ 1.691  0.350 -0.137  1.057]
         [-1.254  0.242 -0.004  0.115]
         [ 1.032  0.278  0.016 -1.954]
         [ 0.000  0.000  0.000  0.000]]
        >>> print("\nFirst Model Standard Errors:\n" +
        ...       str(model1.stderrs)) #doctest: +NORMALIZE_WHITESPACE
        First Model Standard Errors:
        [[ 2.389  0.565  0.061  1.025]
         [ 2.197  0.509  0.047  0.885]
         [ 2.007  0.461  0.043  0.958]]
        >>> # Fit second model to x2, resp2
        >>> resp2 = reg.ResponseFormatID(y2, n_classes)
        >>> model2 = reg.LogisticRegression(n_predictors, n_classes)
        >>> model2.fit(x2, resp2)
        >>> print("\nSecond Model Coefficients:\n" +
        ...       str(model2.coefficients)) #doctest: +NORMALIZE_WHITESPACE
        Second Model Coefficients:
        [[-2.668  0.758 -0.016  1.050]
         [-2.719  0.611  0.006  0.511]
         [-3.281  0.229  0.025  0.812]
         [ 0.000  0.000  0.000  0.000]]
        >>> print("\nSecond Model Standard Errors:\n" +
        ...       str(model2.stderrs)) #doctest: +NORMALIZE_WHITESPACE
        Second Model Standard Errors:
        [[ 2.042  0.485  0.038  0.777]
         [ 2.187  0.522  0.041  0.829]
         [ 2.334  0.545  0.045  0.853]]
        >>> # Aggregate models
        >>> model1.aggregate(model2)
        >>> print("\nAggregated Model Coefficients:\n" +
        ...       str(model1.coefficients)) #doctest: +NORMALIZE_WHITESPACE
        Aggregated Model Coefficients:
        [[-1.169  0.649 -0.038  0.608]
         [-1.935  0.435  0.002  0.215]
         [-0.193  0.282  0.002 -0.630]
         [ 0.000  0.000  0.000  0.000]]
        >>> print("\nAggregated Model Standard Errors:\n" +
        ...       str(model1.stderrs)) #doctest: +NORMALIZE_WHITESPACE
        Aggregated Model Standard Errors:
        [[ 1.489  0.359  0.029  0.588]
         [ 1.523  0.358  0.030  0.584]
         [ 1.461  0.344  0.030  0.596]]
        >>> # Put back the default options
        >>> np.set_printoptions()

        """
        # If the tuple is empty, return immediately
        if len(models) == 0:
            return
        # First check if all models have the same structure
        # Note on precision: If the current LogisticRegression instance has a
        # model defined (self._model not None), then the precision of the
        # aggregation will be the precision of the instance. If no model is
        # defined in the instance, the smallest data type to which all
        # models to aggregate can be promoted is the chosen precision.
        if self._model is not None:
            _common_type = self._common_type
        else:
            _common_type = _numpy.float64
        _model_avail = False
        _n_predictors = self.n_predictors
        _n_classes = self.n_classes
        _ref_class = self.ref_class
        _intercept = self.intercept
        _n_x_interact = self.n_x_interact
        for model in models:
            if model is None:
                raise TypeError("None not supported")

            if not (isinstance(model, LogisticRegression)):
                raise TypeError("Type of model not supported")

            if model._model is not None:
                if _model_avail is False:
                    _model_avail = True
                if model.n_predictors != _n_predictors:
                    raise ValueError("Models have different number of "
                                     "predictors")
                if model.n_classes != _n_classes:
                    raise ValueError("Models have different number of "
                                     "response classes")
                if model.ref_class != _ref_class:
                    raise ValueError("Models have different reference classes")
                if model.intercept != _intercept:
                    raise ValueError("Models differ in existence of an"
                                     " intercept term")
                if model.n_x_interact != _n_x_interact:
                    raise ValueError("Models have different number "
                                     "of interaction terms")
                # For extremely thorough testing, it might be better
                # to also test if the entries in _x_interact and
                # model._x_interact are identical (possibly after
                # permutation). The aggregation will also work if
                # that is not the case. It's the user's responsibility
                # to guarantee that this requirement is fulfilled.

        # if no model to aggregate is available, return
        if not _model_avail:
            return

        ind = []
        i = 0
        for model in models:
            if (model._model is not None):
                ind.append(i)
            i += 1

        model_None = False
        if (self._model is None) and (len(ind) > 0):
            # Copy first model into current instance
            model_None = True
            index = ind[0]
            model = models[index]
            model_type = _imsllib.imsls_d_model
            dtype = _ctypes.POINTER(_ctypes.c_double)
            prec = _numpy.float64
            prec_ctypes = _ctypes.c_double
            null_ptr = _ctypes.POINTER(_ctypes.c_double)()
            self._coefficients = _numpy.asarray(self._coefficients,
                                                dtype=_common_type)
            self._coefficients[:, :] = model.coefficients[:, :]
            self._lrstat = prec(model.likeli_ratio_test_stat)
            self._n_obs = model.n_obs
            self._n_updates = model.n_updates
            self._loglike = prec(model.log_likeli)
            self._meany = _numpy.asarray(self._meany, dtype=_common_type)
            self._meany[:] = model.class_means[:]
            self._struct_coefs = _numpy.asarray(self._struct_coefs,
                                                dtype=_common_type)
            self._struct_coefs[:, :] = model._struct_coefs[:, :]
            self._stderrs = _numpy.asarray(self._stderrs, dtype=_common_type)
            self._stderrs[:, :] = model.stderrs[:, :]
            self._hess = _numpy.asarray(self._hess, dtype=_common_type)
            self._hess[:, :] = model.hessian[:, :]
            self._grad = _numpy.asarray(self._grad, dtype=_common_type)
            self._grad[:] = model.gradient[:]
            self._before_first_fit_call = False
            self._common_type = _common_type
            loglike = prec_ctypes(model._model.loglike)
            # Build CNL structure with Python arrays
            self._model = model_type(model._model.n_obs,
                                     model._model.n_updates,
                                     model._model.n_coefs,
                                     loglike,
                                     self._meany.ctypes.data_as(dtype),
                                     self._struct_coefs.ctypes.data_as(dtype),
                                     self._stderrs.ctypes.data_as(dtype),
                                     self._hess.ctypes.data_as(dtype),
                                     self._grad.ctypes.data_as(dtype))

        # Aggregate models
        if model_None:
            start = 1
        else:
            start = 0
        stop = len(ind)

        for i in range(start, stop):
            index = ind[i]
            prev_model = models[index]
            _prev_model = prev_model._model
            null_ptr = _ctypes.POINTER(_ctypes.c_double)()
            _prev_model = _ctypes.POINTER(_imsllib.imsls_d_model)(_prev_model)
            _next_model = _ctypes.POINTER(_imsllib.imsls_d_model)(self._model)
            lrstat = _ctypes.c_double()

            args = []
            args.append(self._n_obs)
            args.append(self._n_predictors)
            args.append(self._n_classes)
            args.append(null_ptr)
            args.append(null_ptr)

            # Add the optional input arguments
            args.append(_constants.IMSLS_PREV_RESULTS)
            args.append(_prev_model)

            args.append(_constants.IMSLS_NEXT_RESULTS)
            args.append(_ctypes.byref(_next_model))

            args.append(_constants.IMSLS_COEFFICIENTS)
            args.append(self._coefficients.ctypes.data_as(_ctypes.c_void_p))

            # Note: Use of optional argument IMSLS_LRSTAT will issue
            # an IMSL warning if the model has no intercept. Could
            # be avoided by ignoring the optional argument in this case,
            # but the warning message seems informative.
            args.append(_constants.IMSLS_LRSTAT)
            args.append(_ctypes.byref(lrstat))

            args.append(0)

            func = _logistic_regression_func(self._common_type)
            func(*args)

            self._n_obs += prev_model.n_obs
            self._n_updates += 1
            self._loglike = _next_model.contents.loglike
            self._lrstat = lrstat.value


def _mnl_probs(x, freqs, coefs, hessian, confid, n_intercept, xinteract):
    """Compute lower and upper prediction limits.

    Parameters
    ----------
    x : *(n,) or (n, n_predictors) ndarray*
        Array of `n` observations containing the predictor samples.

    coefs : *(n_classes, n_coeffs) ndarray*
        Array containing the regression coefficients.

    hessian : *((n_classes-1)*n_coeffs, (n_classes-1)*n_coeffs) ndarray*
        Array containing the estimated Hessian of the log-likelihood.

    confid : *float*
        Confidence level used in the calculation of the prediction intervals.

    n_intercept : *int*
        Indicates if an intercept term is present (0 - no, 1 - yes).

    xinteract : *(n_x_interact, 2) ndarray*
        Array providing pairs of column indices of the predictor variables
        that define the interaction terms in the model.

    Returns
    -------
    *(low, up) tuple*
        A 2-element tuple consisting of two ndarrays of format *(n, n_classes)*
        containing lower (in *low*) and upper (in *up*) prediction limits.

    """
    n_obs = x.shape[0]
    n_class = coefs.shape[0]
    n_coefs = coefs.shape[1]

    if x.ndim == 1:
        n_preds = 1
    else:
        n_preds = x.shape[1]

    if xinteract is None:
        n_xinteract = 0
    else:
        n_xinteract = xinteract.shape[0]

    if x.ndim == 1:
        temp = _numpy.empty((n_obs, 1), dtype=x.dtype)
        temp[:, 0] = x[:]
        x = temp

    # Compute lower and upper limits in double precision to avoid
    # exponential overflow.
    pj = _numpy.zeros((n_class,), dtype=_numpy.float64)
    predict = _numpy.zeros((n_obs, n_class,), dtype=_numpy.float64)
    low_limit = _numpy.zeros((n_obs, n_class,), dtype=_numpy.float64)
    upp_limit = _numpy.zeros((n_obs, n_class,), dtype=_numpy.float64)

    maxpj = _numpy.finfo(_numpy.float64).tiny
    z_val = _normal.ppf((confid + 1.0) / 2.0)

    var = _mnl_var(x, hessian, n_class, n_coefs, n_intercept, xinteract)

    for j in range(n_obs):
        for i in range(n_class):
            etaji = 0.0
            etaji = etaji + coefs[i, 0] * n_intercept
            index1 = n_intercept
            # calculate the main effects
            for k in range(n_preds):
                if _numpy.isnan(x[j, k]):
                    raise ValueError("array contains missing values")
                etaji = etaji + coefs[i, index1] * x[j, k]
                index1 += 1
            # add the interaction terms, if any
            for k in range(n_xinteract):
                col1 = xinteract[k, 0]
                col2 = xinteract[k, 1]
                etaji = etaji + coefs[i, index1] * x[j, col1] * x[j, col2]
                index1 += 1
            pj[i] = etaji
            if (pj[i] >= maxpj):
                maxpj = pj[i]

        # In var, we have estimated variance for each of the linear
        # predictors (logits):
        # for each class (n_classes-1) and each new observation.  We get
        # lower and upper CI values for the linear predictor, then we
        # plug-in the values to the probability estimates, to get the upper
        # and lower CI values for the probability.  Hosmer and Lemeshow
        # (section 2.5)
        # sum pj over the classes and avoid overflow
        sumpj = 0.0
        sumupper = 0.0
        sumlower = 0.0
        sumlower2 = 0.0
        sumupper2 = 0.0
        for i in range(n_class):
            # lower CI value index
            if (i < n_class - 1):
                low_limit[j, i] = pj[i] - z_val * _numpy.sqrt(var[i, j])
                sumlower += _numpy.exp(low_limit[j, i])

            # upper CI value index
            if (i < n_class - 1):
                upp_limit[j, i] = pj[i] + z_val * _numpy.sqrt(var[i, j])
                sumupper += _numpy.exp(upp_limit[j, i])

            pj[i] = pj[i] - maxpj
            pj[i] = _numpy.exp(pj[i])
            sumpj = sumpj + pj[i]

        for i in range(n_class):
            # lower CI value index
            if (i < n_class - 1):
                temp = _numpy.exp(low_limit[j, i]) / (1.0 + sumlower)
                low_limit[j, i] = temp
                sumlower2 += temp
            else:
                low_limit[j, i] = 1.0 - sumupper2

            # upper CI value index
            if (i < n_class - 1):
                temp = _numpy.exp(upp_limit[j, i]) / (1.0 + sumupper)
                upp_limit[j, i] = temp
                # using the constraint to get the CI for the reference class
                sumupper2 += temp
            else:
                upp_limit[j, i] = 1.0 - sumlower2

        # divide by sumpj
        pj[:] = pj[:] / sumpj
        # here are the predicted values
        predict[j, :] = freqs[j] * pj[:]

    predict = _numpy.asarray(predict, dtype=x.dtype)
    low_limit = _numpy.asarray(low_limit, dtype=x.dtype)
    upp_limit = _numpy.asarray(upp_limit, dtype=x.dtype)

    return predict, low_limit, upp_limit


def _mnl_var(x, hessian, n_class, n_coefs, n_intercept, xinteract):
    """Compute variances for each of the linear predictors.

    Parameters
    ----------
    x : *(n, n_predictors) ndarray*
        Array of `n` observations containing the predictor samples.

    hessian : *((n_class-1)*n_coefs, (n_class-1)*n_coefs) ndarray*
        Array containing the estimated Hessian of the log-likelihood.

    n_class : *int*
        The number of response classes.

    n_coefs : *int*
        The number of model coefficients.

    n_intercept : *int*
        Indicates if an intercept term is present (0 - no, 1 - yes).

    xinteract : *(n_x_interact, 2) ndarray*
        Array providing pairs of column indices of the predictor variables
        that define the interaction terms in the model.

    Returns
    -------
    *(n_class-1, n_obs) ndarray*
        Array containing the variances.

    """
    n_obs = x.shape[0]
    if xinteract is None:
        n_xinteract = 0
    else:
        n_xinteract = xinteract.shape[0]

    n_preds = x.shape[1]

    xnew = _numpy.zeros((n_coefs,), dtype=x.dtype)
    nn = n_coefs * (n_class - 1)
    hessi = _numpy.empty((nn, nn), dtype=x.dtype)
    work = _numpy.empty((n_coefs, n_coefs), dtype=x.dtype)
    var = _numpy.empty((n_class - 1, n_obs), dtype=x.dtype)

    # take the negative to make the Hessian positive definite
    hessi[:, :] = -hessian

    # compute the inverse hessian
    hessi = _numpy.linalg.inv(hessi)

    # get observation
    for j in range(n_obs):
        index1 = n_intercept
        if n_intercept > 0:
            xnew[0] = 1.0
        xnew[index1:index1 + n_preds] = x[j, 0:n_preds]
        index1 += n_preds
        # add the interaction terms, if any
        for k in range(n_xinteract):
            col1 = xinteract[k, 0]
            col2 = xinteract[k, 1]
            xnew[index1] = x[j, col1] * x[j, col2]
            index1 += 1
        # calculate upper and lower limits
        # compute trans(xnew) * inv(-Hess) * xnew
        for i in range(n_class - 1):
            col_id = i * n_coefs
            for k in range(n_coefs):
                row_id = col_id + k
                work[k, :] = hessi[row_id, col_id:col_id + n_coefs]
            temp = _numpy.dot(work, xnew)
            var[i, j] = _numpy.dot(temp, xnew)

    return var
