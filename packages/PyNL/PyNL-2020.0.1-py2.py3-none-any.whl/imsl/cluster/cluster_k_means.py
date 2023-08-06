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
"""Cluster-K-Means related functions."""
import ctypes as _ctypes
import numpy as _numpy

import imsl._constants as _constants
import imsl._imsllib as _imsllib
import collections as _collections


def _cluster_k_means_func(dtype):
    """Return the IMSL cluster_k_means function appropriate for dtype.

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
        return _imsllib.imsls_d_cluster_k_means
    else:
        return None


def _check_matrix(array, name, length):
    """Check array format and positivity of array entries.

    Parameters:
    -----------
    array : *ndarray*
        The array to be checked.

    name : *str*
        The array name.

    length : *int*
        The required minimum length of the array.

    """
    if array.ndim != 1:
        raise ValueError("array of dimension {} not"
                         " supported".format(array.ndim))

    if array.size < length:
        raise ValueError("array of size {} not"
                         " supported".format(array.size))

    # Check that entries in array are positive
    for i in range(length):
        if array[i] <= 0.0:
            raise ValueError("all entries in array {0} must be"
                             " greater than zero, but {0}[{1}] ="
                             " {2}".format(name, i, array[i]))


def cluster_k_means(obs, cluster_seeds, weights=None, frequencies=None,
                    max_iter=30, cluster_vars=None):
    r"""Perform a *K*-means (centroid) cluster analysis.

    Parameters
    ----------
    obs : *(M,N) array_like*
        Array of size *M* :math:`\times` *N* containing the observations to
        be clustered.
    cluster_seeds : *(n_clusters, L) array_like*
        Array containing the cluster seeds, i.e., estimates for the cluster
        centers. `L` denotes the number of columns of array `obs` used
        in the analysis; see argument `cluster_vars`.
    weights : *(M,) array_like, optional*
        Array of length `M` containing the weight of each observation of
        array `obs`.

        Default: `weights` = [1, 1, ..., 1].
    frequencies : *(M,) array_like, optional*
        Array of length `M` containing the frequency of each observation of
        array `obs`.

        Default: `frequencies` = [1, 1, ..., 1].
    max_iter : *int, optional*
        The maximum number of iterations.

        Default: `max_iter` = 30.
    cluster_vars : *(L,) array_like, optional*
        Array of length *L* containing the columns of `obs` to be used
        in computing the metric. The columns in array `obs` are
        numbered 0, 1, 2, ..., *N*-1.

        Default: `cluster_vars` = [0, 1, 2, ..., *N* - 1].

    Returns
    -------
    A named tuple with the following fields:

    membership : *(M,) ndarray*
        Array containing the cluster membership for each observation.

    history : *(n_iter, M) ndarray*
        Array of size `n_iter` :math:`\times` `M` containing the cluster
        membership of each observation in array `obs` per iteration.
        Note that `n_iter` is the number of completed iterations in
        the algorithm.

    means : *(n_clusters, L) ndarray*
        Array containing the cluster means.

    ssq : *(n_clusters,) ndarray*
        Array containing the within sum-of-squares for each cluster.

    counts : *(n_clusters,) ndarray*
        Array containing the number of observations in each cluster.

    Notes
    -----
    Function `cluster_k_means` is an implementation of Algorithm AS 136 by
    Hartigan and Wong ([1]_). It computes *K*-means (centroid) Euclidean metric
    clusters for an input matrix starting with initial estimates of the
    *K*-cluster means. The function allows for missing values coded as `NaN`
    (Not a Number) and for weights and frequencies.

    Let *p* be the number of variables to be used in computing the Euclidean
    distance between observations. The idea in *K*-means cluster analysis is
    to find a clustering (or grouping) of the observations so as to minimize
    the total within-cluster sums-of-squares. In this case, the total
    sums-of-squares within each cluster is computed as the sum of the
    centered sum-of-squares over all nonmissing values of each variable.

    That is,

    .. math::
        \phi = \sum_{i=1}^K \sum_{j=1}^p \sum_{m=1}^{n_i} f_{\nu_{im}}
        w_{\nu_{im}} \delta_{\nu_{im},j}(x_{\nu_{im},j}-\bar{x}_{ij})^2

    where :math:`\nu_{im}` denotes the row index of the `m`-th observation
    in the `i`-th cluster in the matrix `obs`; :math:`n_i` is the number of
    rows of `obs` assigned to group `i`; `f` denotes the frequency of the
    observation; `w` denotes its weight; :math:`\delta` is 0 if the `j`-th
    variable on observation :math:`\nu_{im}` is missing, otherwise
    :math:`\delta` is 1; and

    .. math::
       \bar{x}_{ij}

    is the average of the nonmissing observations for variable `j` in group
    `i`. This method sequentially processes each observation and reassigns
    it to another cluster if doing so results in a decrease of the total
    within-cluster sums-of-squares. See [1]_ or [2]_ for details.

    References
    ----------
    .. [1] Hartigan, J.A. and M.A. Wong (1979), *Algorithm AS 136: A K-means
           clustering algorithm*, Applied Statistics, 28, 100-108.

    .. [2] Hartigan, John A. (1975), *Clustering Algorithms*,
           John Wiley & Sons, New York.

    Examples
    --------
    This example performs *K*-means cluster analysis on Fisher's Iris data.
    The initial cluster seed for each iris type is an observation known to
    be in the iris type.

    >>> import numpy as np
    >>> import imsl.cluster as cluster
    >>> fisher_iris_data = np.array(
    ... [[1.0, 5.1, 3.5, 1.4, .2], [1.0, 4.9, 3.0, 1.4, .2],
    ... [1.0, 4.7, 3.2, 1.3, .2], [1.0, 4.6, 3.1, 1.5, .2],
    ... [1.0, 5.0, 3.6, 1.4, .2], [1.0, 5.4, 3.9, 1.7, .4],
    ... [1.0, 4.6, 3.4, 1.4, .3], [1.0, 5.0, 3.4, 1.5, .2],
    ... [1.0, 4.4, 2.9, 1.4, .2], [1.0, 4.9, 3.1, 1.5, .1],
    ... [1.0, 5.4, 3.7, 1.5, .2], [1.0, 4.8, 3.4, 1.6, .2],
    ... [1.0, 4.8, 3.0, 1.4, .1], [1.0, 4.3, 3.0, 1.1, .1],
    ... [1.0, 5.8, 4.0, 1.2, .2], [1.0, 5.7, 4.4, 1.5, .4],
    ... [1.0, 5.4, 3.9, 1.3, .4], [1.0, 5.1, 3.5, 1.4, .3],
    ... [1.0, 5.7, 3.8, 1.7, .3], [1.0, 5.1, 3.8, 1.5, .3],
    ... [1.0, 5.4, 3.4, 1.7, .2], [1.0, 5.1, 3.7, 1.5, .4],
    ... [1.0, 4.6, 3.6, 1.0, .2], [1.0, 5.1, 3.3, 1.7, .5],
    ... [1.0, 4.8, 3.4, 1.9, .2], [1.0, 5.0, 3.0, 1.6, .2],
    ... [1.0, 5.0, 3.4, 1.6, .4], [1.0, 5.2, 3.5, 1.5, .2],
    ... [1.0, 5.2, 3.4, 1.4, .2], [1.0, 4.7, 3.2, 1.6, .2],
    ... [1.0, 4.8, 3.1, 1.6, .2], [1.0, 5.4, 3.4, 1.5, .4],
    ... [1.0, 5.2, 4.1, 1.5, .1], [1.0, 5.5, 4.2, 1.4, .2],
    ... [1.0, 4.9, 3.1, 1.5, .2], [1.0, 5.0, 3.2, 1.2, .2],
    ... [1.0, 5.5, 3.5, 1.3, .2], [1.0, 4.9, 3.6, 1.4, .1],
    ... [1.0, 4.4, 3.0, 1.3, .2], [1.0, 5.1, 3.4, 1.5, .2],
    ... [1.0, 5.0, 3.5, 1.3, .3], [1.0, 4.5, 2.3, 1.3, .3],
    ... [1.0, 4.4, 3.2, 1.3, .2], [1.0, 5.0, 3.5, 1.6, .6],
    ... [1.0, 5.1, 3.8, 1.9, .4], [1.0, 4.8, 3.0, 1.4, .3],
    ... [1.0, 5.1, 3.8, 1.6, .2], [1.0, 4.6, 3.2, 1.4, .2],
    ... [1.0, 5.3, 3.7, 1.5, .2], [1.0, 5.0, 3.3, 1.4, .2],
    ... [2.0, 7.0, 3.2, 4.7, 1.4], [2.0, 6.4, 3.2, 4.5, 1.5],
    ... [2.0, 6.9, 3.1, 4.9, 1.5], [2.0, 5.5, 2.3, 4.0, 1.3],
    ... [2.0, 6.5, 2.8, 4.6, 1.5], [2.0, 5.7, 2.8, 4.5, 1.3],
    ... [2.0, 6.3, 3.3, 4.7, 1.6], [2.0, 4.9, 2.4, 3.3, 1.0],
    ... [2.0, 6.6, 2.9, 4.6, 1.3], [2.0, 5.2, 2.7, 3.9, 1.4],
    ... [2.0, 5.0, 2.0, 3.5, 1.0], [2.0, 5.9, 3.0, 4.2, 1.5],
    ... [2.0, 6.0, 2.2, 4.0, 1.0], [2.0, 6.1, 2.9, 4.7, 1.4],
    ... [2.0, 5.6, 2.9, 3.6, 1.3], [2.0, 6.7, 3.1, 4.4, 1.4],
    ... [2.0, 5.6, 3.0, 4.5, 1.5], [2.0, 5.8, 2.7, 4.1, 1.0],
    ... [2.0, 6.2, 2.2, 4.5, 1.5], [2.0, 5.6, 2.5, 3.9, 1.1],
    ... [2.0, 5.9, 3.2, 4.8, 1.8], [2.0, 6.1, 2.8, 4.0, 1.3],
    ... [2.0, 6.3, 2.5, 4.9, 1.5], [2.0, 6.1, 2.8, 4.7, 1.2],
    ... [2.0, 6.4, 2.9, 4.3, 1.3], [2.0, 6.6, 3.0, 4.4, 1.4],
    ... [2.0, 6.8, 2.8, 4.8, 1.4], [2.0, 6.7, 3.0, 5.0, 1.7],
    ... [2.0, 6.0, 2.9, 4.5, 1.5], [2.0, 5.7, 2.6, 3.5, 1.0],
    ... [2.0, 5.5, 2.4, 3.8, 1.1], [2.0, 5.5, 2.4, 3.7, 1.0],
    ... [2.0, 5.8, 2.7, 3.9, 1.2], [2.0, 6.0, 2.7, 5.1, 1.6],
    ... [2.0, 5.4, 3.0, 4.5, 1.5], [2.0, 6.0, 3.4, 4.5, 1.6],
    ... [2.0, 6.7, 3.1, 4.7, 1.5], [2.0, 6.3, 2.3, 4.4, 1.3],
    ... [2.0, 5.6, 3.0, 4.1, 1.3], [2.0, 5.5, 2.5, 4.0, 1.3],
    ... [2.0, 5.5, 2.6, 4.4, 1.2], [2.0, 6.1, 3.0, 4.6, 1.4],
    ... [2.0, 5.8, 2.6, 4.0, 1.2], [2.0, 5.0, 2.3, 3.3, 1.0],
    ... [2.0, 5.6, 2.7, 4.2, 1.3], [2.0, 5.7, 3.0, 4.2, 1.2],
    ... [2.0, 5.7, 2.9, 4.2, 1.3], [2.0, 6.2, 2.9, 4.3, 1.3],
    ... [2.0, 5.1, 2.5, 3.0, 1.1], [2.0, 5.7, 2.8, 4.1, 1.3],
    ... [3.0, 6.3, 3.3, 6.0, 2.5], [3.0, 5.8, 2.7, 5.1, 1.9],
    ... [3.0, 7.1, 3.0, 5.9, 2.1], [3.0, 6.3, 2.9, 5.6, 1.8],
    ... [3.0, 6.5, 3.0, 5.8, 2.2], [3.0, 7.6, 3.0, 6.6, 2.1],
    ... [3.0, 4.9, 2.5, 4.5, 1.7], [3.0, 7.3, 2.9, 6.3, 1.8],
    ... [3.0, 6.7, 2.5, 5.8, 1.8], [3.0, 7.2, 3.6, 6.1, 2.5],
    ... [3.0, 6.5, 3.2, 5.1, 2.0], [3.0, 6.4, 2.7, 5.3, 1.9],
    ... [3.0, 6.8, 3.0, 5.5, 2.1], [3.0, 5.7, 2.5, 5.0, 2.0],
    ... [3.0, 5.8, 2.8, 5.1, 2.4], [3.0, 6.4, 3.2, 5.3, 2.3],
    ... [3.0, 6.5, 3.0, 5.5, 1.8], [3.0, 7.7, 3.8, 6.7, 2.2],
    ... [3.0, 7.7, 2.6, 6.9, 2.3], [3.0, 6.0, 2.2, 5.0, 1.5],
    ... [3.0, 6.9, 3.2, 5.7, 2.3], [3.0, 5.6, 2.8, 4.9, 2.0],
    ... [3.0, 7.7, 2.8, 6.7, 2.0], [3.0, 6.3, 2.7, 4.9, 1.8],
    ... [3.0, 6.7, 3.3, 5.7, 2.1], [3.0, 7.2, 3.2, 6.0, 1.8],
    ... [3.0, 6.2, 2.8, 4.8, 1.8], [3.0, 6.1, 3.0, 4.9, 1.8],
    ... [3.0, 6.4, 2.8, 5.6, 2.1], [3.0, 7.2, 3.0, 5.8, 1.6],
    ... [3.0, 7.4, 2.8, 6.1, 1.9], [3.0, 7.9, 3.8, 6.4, 2.0],
    ... [3.0, 6.4, 2.8, 5.6, 2.2], [3.0, 6.3, 2.8, 5.1, 1.5],
    ... [3.0, 6.1, 2.6, 5.6, 1.4], [3.0, 7.7, 3.0, 6.1, 2.3],
    ... [3.0, 6.3, 3.4, 5.6, 2.4], [3.0, 6.4, 3.1, 5.5, 1.8],
    ... [3.0, 6.0, 3.0, 4.8, 1.8], [3.0, 6.9, 3.1, 5.4, 2.1],
    ... [3.0, 6.7, 3.1, 5.6, 2.4], [3.0, 6.9, 3.1, 5.1, 2.3],
    ... [3.0, 5.8, 2.7, 5.1, 1.9], [3.0, 6.8, 3.2, 5.9, 2.3],
    ... [3.0, 6.7, 3.3, 5.7, 2.5], [3.0, 6.7, 3.0, 5.2, 2.3],
    ... [3.0, 6.3, 2.5, 5.0, 1.9], [3.0, 6.5, 3.0, 5.2, 2.0],
    ... [3.0, 6.2, 3.4, 5.4, 2.3], [3.0, 5.9, 3.0, 5.1, 1.8]])
    >>> cluster_seeds = np.empty((3,4))
    >>> cluster_variables = np.array([1, 2, 3, 4])
    >>> # Assign initial cluster seeds
    >>> for i in range(4):
    ...    cluster_seeds[0][i] = fisher_iris_data[0][i+1]
    ...    cluster_seeds[1][i] = fisher_iris_data[50][i+1]
    ...    cluster_seeds[2][i] = fisher_iris_data[100][i+1]
    >>> # Perform the analysis
    >>> clusters = cluster.cluster_k_means(fisher_iris_data, cluster_seeds,
    ...                                    cluster_vars = cluster_variables)
    >>> # Print results
    >>> np.set_printoptions(precision=3)
    >>> print("Cluster Membership:\n\n" +
    ...       str(clusters.membership)) # doctest: +NORMALIZE_WHITESPACE
    Cluster Membership:
    <BLANKLINE>
    [1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
     1 1 1 1 1 1 1 1 1 1 1 1 1 2 2 3 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
     2 2 2 3 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 3 2 3 3 3 3 2 3 3 3 3
     3 3 2 2 3 3 3 3 2 3 2 3 2 3 3 2 2 3 3 3 3 3 2 3 3 3 3 2 3 3 3 2 3 3 3 2 3
     3 2]
    >>> print("\nCluster Means:\n\n" +
    ...       str(clusters.means)) # doctest: +NORMALIZE_WHITESPACE
    <BLANKLINE>
    Cluster Means:
    <BLANKLINE>
    [[5.006  3.428  1.462  0.246]
     [5.902  2.748  4.394  1.434]
     [6.85   3.074  5.742  2.071]]
    >>> print("\nCluster Sum of squares:\n\n" +
    ...       str(clusters.ssq)) # doctest: +NORMALIZE_WHITESPACE
    <BLANKLINE>
    Cluster Sum of squares:
    <BLANKLINE>
    [15.151  39.821  23.879]
    >>> print("\n# Observations in Each Cluster:\n\n" +
    ...       str(clusters.counts)) # doctest: +NORMALIZE_WHITESPACE
    <BLANKLINE>
    # Observations in Each Cluster:
    <BLANKLINE>
    [50 62 38]

    """
    if obs is None:
        raise TypeError("None not supported")
    # attempt to promote obs to a compatible type. In the following,
    # the compatible type is used as a reference type for promotion
    # of other arrays.
    _obs = _numpy.asarray(obs, order='C')
    ref_type = _numpy.promote_types(_numpy.float64, _obs.dtype)
    _obs = _numpy.asarray(_obs, dtype=ref_type)

    if (not _numpy.issubdtype(_obs.dtype, _numpy.float64)):
        raise ValueError("array type {} not supported".format(
            _obs.dtype.name))

    if not (_obs.ndim in (1, 2)):
        raise ValueError("array of dimension {} not"
                         " supported".format(_obs.ndim))

    if _obs.size == 0:
        raise ValueError("empty array not supported")

    if cluster_seeds is None:
        raise TypeError("None not supported")

    _cluster_seeds = _numpy.asarray(cluster_seeds, dtype=ref_type, order='C')

    if not (_cluster_seeds.ndim in (1, 2)):
        raise ValueError("array of dimension {} not"
                         " supported".format(_cluster_seeds.ndim))

    if _cluster_seeds.size == 0:
        raise ValueError("empty array not supported")

    n_obs = _obs.shape[0]
    if _obs.ndim == 1:
        n_cols_obs = 1
    else:
        n_cols_obs = _obs.shape[1]
    n_clusters = _cluster_seeds.shape[0]

    if not (n_clusters in range(2, n_obs + 1)):
        raise ValueError("number of {} clusters not"
                         " supported".format(n_clusters))

    n_cluster_vars = n_cols_obs

    weights_key = False
    frequencies_key = False
    cluster_vars_key = False

    if weights is not None:
        weights_key = True
        _weights = _numpy.asarray(weights, dtype=ref_type, order='C')
        _check_matrix(_weights, "weights", n_obs)

    if frequencies is not None:
        frequencies_key = True
        _frequencies = _numpy.asarray(frequencies, dtype=ref_type, order='C')
        _check_matrix(_frequencies, "frequencies", n_obs)

    _max_iter = int(max_iter)  # transform to same type as default value
    if _max_iter <= 0:
        raise ValueError("argument max_iter is {}, but must be "
                         "greater than zero".format(_max_iter))

    if cluster_vars is not None:
        cluster_vars_key = True
        # Note: It is necessary to make a copy of array cluster_vars
        # because CNL cluster_k_means modifies this array (though
        # it is declared as Input in the CNL documentation). Making a
        # copy keeps PyNL thread-safe.
        _cluster_vars = _numpy.array(cluster_vars, dtype=_numpy.int32)

        # Check shape of _cluster_vars
        if _cluster_vars.ndim != 1:
            raise ValueError("array of dimension {} not"
                             " supported".format(_cluster_vars.ndim))
        n_cluster_vars = _cluster_vars.size
        if n_cluster_vars == 0 or n_cluster_vars > n_cols_obs:
            raise ValueError("array of size {} not"
                             " supported".format(_cluster_vars.size))

        # Check entries in _cluster_vars
        temp = _numpy.zeros(n_cols_obs, dtype=_numpy.int32)
        for x in _cluster_vars:
            if x < 0 or x >= n_cols_obs:
                raise ValueError("array entry {} out of feasible"
                                 " bounds".format(x))
            temp[x] += 1

        # Check that the mapping is injective
        for x in temp:
            if x > 1:
                raise ValueError("array entries are not unique")

    # Check if _cluster_seeds has the correct column dimension
    if cluster_vars_key:
        array_name = "cluster_vars"
    else:
        array_name = "obs"

    # Check correct column dimension of array _cluster_seeds
    error = False
    if (_cluster_seeds.ndim == 1 and n_cluster_vars > 1):
        error = True
        col_num = 1
    elif (_cluster_seeds.ndim == 2
            and _cluster_seeds.shape[1] != n_cluster_vars):
        error = True
        col_num = _cluster_seeds.shape[1]

    if error:
        raise ValueError("column number of array cluster_seeds ({}) "
                         "does not match column number of array {} "
                         "({})".format(col_num, array_name,
                                       n_cluster_vars))

    args = []
    # Prepare required input argument list
    args.append(_ctypes.c_int(n_obs))
    args.append(_ctypes.c_int(n_cluster_vars))
    args.append(_obs.ctypes.data_as(_ctypes.c_void_p))
    args.append(_ctypes.c_int(n_clusters))
    args.append(_cluster_seeds.ctypes.data_as(_ctypes.c_void_p))

    # Now add the optional input arguments
    if weights_key:
        args.append(_constants.IMSLS_WEIGHTS)
        args.append(_weights.ctypes.data_as(_ctypes.c_void_p))

    if frequencies_key:
        args.append(_constants.IMSLS_FREQUENCIES)
        args.append(_frequencies.ctypes.data_as(_ctypes.c_void_p))

    args.append(_constants.IMSLS_MAX_ITERATIONS)
    args.append(_ctypes.c_int(_max_iter))

    if cluster_vars_key:
        args.append(_constants.IMSLS_X_COL_DIM)
        args.append(_ctypes.c_int(n_cols_obs))
        args.append(_constants.IMSLS_CLUSTER_VARIABLE_COLUMNS)
        args.append(_cluster_vars.ctypes.data_as(_ctypes.c_void_p))

    # Generate output arrays and add them to the argument list
    cluster_group = _numpy.empty(n_obs, dtype=_numpy.int32)
    args.append(_constants.IMSLS_RETURN_USER)
    args.append(cluster_group.ctypes.data_as(_ctypes.c_void_p))

    history = _numpy.empty((_max_iter, n_obs), dtype=_numpy.int32)
    n_itr = _ctypes.c_int()
    args.append(_constants.IMSLS_CLUSTER_HISTORY_USER)
    args.append(_ctypes.byref(n_itr))
    args.append(history.ctypes.data_as(_ctypes.c_void_p))

    means = _numpy.empty((n_clusters, n_cluster_vars), dtype=ref_type)
    args.append(_constants.IMSLS_CLUSTER_MEANS_USER)
    args.append(means.ctypes.data_as(_ctypes.c_void_p))

    ssq = _numpy.empty(n_clusters, dtype=ref_type)
    args.append(_constants.IMSLS_CLUSTER_SSQ_USER)
    args.append(ssq.ctypes.data_as(_ctypes.c_void_p))

    counts = _numpy.empty(n_clusters, dtype=_numpy.int32)
    args.append(_constants.IMSLS_CLUSTER_COUNTS_USER)
    args.append(counts.ctypes.data_as(_ctypes.c_void_p))

    args.append(0)

    func = _cluster_k_means_func(_obs.dtype)
    func(*args)

    result = _collections.namedtuple("cluster",
                                     ["membership",
                                      "history",
                                      "means",
                                      "ssq",
                                      "counts"]
                                     )

    if (n_itr.value < _max_iter):
        history_copy = history[0:n_itr.value, :]
    else:
        history_copy = history

    result.membership = cluster_group
    result.history = history_copy
    result.means = means
    result.ssq = ssq
    result.counts = counts

    return result
