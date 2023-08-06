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
"""Apriori related classes, methods, and functions."""
import ctypes as _ctypes

import numpy as _numpy

import imsl._constants as _constants
import imsl._imsllib as _imsllib


def _free_apriori_itemsets_func(dtype):
    """Return the IMSL free_apriori_itemsets function appropriate for dtype.

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
        return _imsllib.imsls_d_free_apriori_itemsets
    else:
        return None


def _free_association_rules_func(dtype):
    """Return the IMSL free_association_rules function appropriate for dtype.

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
        return _imsllib.imsls_d_free_association_rules
    else:
        return None


def _aggr_apriori_func(dtype):
    """Return the IMSL aggr_apriori function appropriate for dtype.

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
        return _imsllib.imsls_d_aggr_apriori
    else:
        return None


def frequent_itemsets(max_num_products, x, max_set_size=5,
                      min_pct_support=0.1):
    r"""Compute the frequent itemsets in a transaction set using Apriori.

    Parameters
    ----------
    max_num_products : *int*
        The maximum number of unique items or products that may be present
        in the transactions.
    x : *(n, 2) array_like*
        An array containing the transaction data. The first column of `x`
        contains the transaction IDs, and the second column contains the
        item IDs. Each row represents a transaction ID and item ID pair.
        The algorithm assumes that an individual transaction is complete
        within a single data set. That is, there is no matching of transaction
        IDs between different data sets.
    max_set_size : *int, optional*
        The maximum size of an itemset. Only frequent itemsets with
        `max_set_size` or fewer items are considered in the analysis.

    min_pct_support : *float, optional*
            The minimum percentage of transactions in which an item or itemset
            must be present to be considered frequent. `min_pct_support` must
            be in the interval [0,1].

    Returns
    -------
    *FrequentItemSets*
        An object of type :py:class:`~FrequentItemSets` containing the frequent
        itemsets.

    See Also
    --------
    FrequentItemSets : contains a full description of the Apriori algorithm.

    """
    _max_set_size = int(max_set_size)
    _max_num_products = int(max_num_products)
    _min_pct_support = float(min_pct_support)

    if _max_num_products < 1:
        raise ValueError("max_num_products must be greater than zero")

    if _max_set_size < 1:
        raise ValueError("max_set_size must be greater than zero")

    if not (0.0 <= _min_pct_support <= 1.0):
        raise ValueError("min_pct_support must be in the interval [0, 1]")

    if x is None:
        raise TypeError("None not supported")

    _x = _numpy.asarray(x, order='C', dtype=_numpy.int32)

    if _x.ndim != 2:
        raise ValueError("array of dimension {} not"
                         " supported".format(_x.ndim))

    if _x.shape[1] != 2:
        raise ValueError("array must have two columns")

    if _x.size == 0:
        raise ValueError("empty array not supported")

    _n_rows = _x.shape[0]
    itemsets = _ctypes.POINTER(_imsllib.imsls_d_apriori_itemsets)()

    args = []
    args.append(_constants.IMSLS_FREQUENT_ITEMSETS)
    args.append(_n_rows)
    args.append(_x.ctypes.data_as(_ctypes.c_void_p))
    args.append(_max_num_products)
    args.append(_max_set_size)
    args.append(_ctypes.c_double(_min_pct_support))
    args.append(_ctypes.byref(itemsets))
    args.append(0)

    func = _aggr_apriori_func(_numpy.float64)

    try:
        func(*args)

        n_trans = itemsets.contents.n_trans
        max_num_products = itemsets.contents.max_num_products
        max_set_size = itemsets.contents.max_set_size
        min_pct_support = itemsets.contents.min_pct_support

        # Construct imsls_d_apriori_itemsets structure in Python
        n_itemsets = itemsets.contents.n_itemsets
        # Create array type
        _arr = _imsllib.imsls_apriori_items * n_itemsets
        # Create instance
        _itemsets = _arr()
        ptr_itemsets = itemsets.contents.itemsets
        for j in range(n_itemsets):
            n_items = ptr_itemsets[j].n_items
            support = ptr_itemsets[j].support
            _item = _ctypes.c_int32 * n_items
            _items = _item()
            _items[0:n_items] = ptr_itemsets[j].items[0:n_items]
            # Instantiate the Python structure
            _itemsets[j] = _imsllib.imsls_apriori_items(n_items, _items,
                                                        support)

        # Build imsls_d_apriori_itemsets structure
        _apriori_struct = _imsllib.imsls_d_apriori_itemsets
        min_pct_supp = _ctypes.c_double(min_pct_support)
        _itemsets_struct = _apriori_struct(n_itemsets, _itemsets, n_trans,
                                           max_num_products, max_set_size,
                                           min_pct_supp)

    finally:
        # In any case, free the CNL structure to avoid memory leaks
        func = _free_apriori_itemsets_func(_numpy.float64)
        func(itemsets)

    item_sets_inst = FrequentItemSets()
    item_sets_inst._set_attributes(_itemsets_struct)
    return item_sets_inst


class FrequentItemSets():
    r"""Aggregate frequent itemsets and compute association rules.

    Notes
    -----
    Function :py:func:`~frequent_itemsets` and the methods of class
    :py:class:`~FrequentItemSets` perform the Apriori algorithm for association
    rule discovery. Association rules are statements of the form
    "if *X*, then *Y*", given with some measure of confidence.

    *1. Application Fields of Apriori*

    The main application for association rule discovery is market basket
    analysis, where *X* and *Y* are products or groups of products, and the
    occurrences are individual transactions, or "market baskets". The results
    help sellers learn relationships between different products they sell,
    supporting better marketing decisions. There are other applications for
    association rule discovery, such as the problem areas of text mining and
    bioinformatics. The Apriori algorithm ([1]_) is one of the most popular
    algorithms for association rule discovery in transactional data sets.

    *2. Application to a Single Set of Transactions*

    The Apriori algorithm consists of two stages when applied to a single
    transaction set. In the first and most critical stage, which is executed
    via function :py:func:`~frequent_itemsets`, the Apriori algorithm mines the
    transactions for frequent itemsets. An itemset is frequent if it appears
    in more than a minimum number of transactions. The number of transactions
    containing an itemset is known as its "support", and the minimum support
    (as a percentage of transactions) is a control parameter in the algorithm.
    The algorithm begins by finding the frequent single itemsets. Then the
    algorithm generates all two-item itemsets from the frequent single items
    and determines which among them are frequent. From the collection of
    frequent pairs, Apriori forms candidate three-item subsets and determines
    which are frequent, and so on. The algorithm stops, when either a maximum
    itemset size is reached, or when none of the candidate itemsets are
    frequent. In this way, the Apriori algorithm exploits the apriori
    property: for an itemset to be frequent, all of its proper subsets must
    also be frequent. At each step the problem is reduced to only the frequent
    subsets.

    In the second stage, executed via method :py:meth:`~association_rules`,
    the algorithm generates association rules. These are of the form
    :math:`X \Rightarrow Y` (read, "if *X*, then *Y*"), where *Y* and
    *X* are disjoint frequent itemsets. The confidence measure associated with
    the rule is defined as the proportion of transactions containing *X* that
    also contain *Y*. Denote the support of *X* (the number of transactions
    containing X) as :math:`S_X`, and the support of :math:`Z=X \cup Y` as
    :math:`S_Z`. The confidence of the rule :math:`X \Rightarrow Y` is the
    ratio :math:`S_Z/S_X`. Note that the confidence ratio is the conditional
    probability

    .. math::
        P[X|Y] =\frac{P[XY]}{P[X]}

    where :math:`P[XY]` denotes the probability of both *X* and *Y*. The
    probability of an itemset *X* is estimated by :math:`S_X/N`, where *N*
    is the total number of transactions.

    Another measure of the strength of the association is known as the lift,
    which is the ratio :math:`(S_ZN)/(S_XS_Y)`. Lift values close to 1.0
    suggest the sets are independent, and that they occur together by chance.
    Large lift values indicate a strong association. A minimum confidence
    threshold and a lift threshold can be specified.

    *3. Application to Blocks of Transactions (Aggregation)*

    Since the Apriori algorithm can operate on subsets of data, it can be used
    with distributed data or data sets larger than physical memory.
    Additionally, it may be useful in parallel computing environments where
    nodes can be programmed to calculate intermediate results in parallel.

    For each data set or block of transactions, call function
    :py:func:`~frequent_itemsets` to obtain the frequent itemsets for each
    block. The same parameter settings, such as minimum support percentage,
    must be used in each call.

    Then, call method :py:meth:`~union` to obtain the union of all frequent
    itemsets. The resulting sets serve as the "candidate" itemsets for the
    global set of transactions.

    An itemset which is frequent in one transaction set may or may not be
    frequent in the larger collection. To find the itemsets that are frequent
    over the entire set of transactions, use method :py:meth:`~frequency` to
    perform another pass through the individual blocks, this time counting
    the occurrence of each itemset in each transaction set.
    This step can be done in parallel.

    The next step is then to sum up the individual counts before filtering
    for the frequent itemsets. This is achieved by adding the frequency
    vectors returned by method :py:meth:`~frequency`. After this step, the
    frequencies of each candidate itemset over all of the transactions are
    known.

    In the final step, call method :py:func:`~update` to determine all
    itemsets that meet the threshold to be considered "frequent". This
    step completes the aggregation of the transactional data sets.

    Once the frequent itemsets are known, the strong association rules can be
    found using method :py:meth:`~association_rules`.

    The aggregation method is due to [3]_ and is also summarized and compared
    with other approaches in [2]_.

    References
    ----------
    .. [1] Agrawal, R., and Srikant, R. (1994), *Fast algorithms for mining
           association rules*, Proceedings of the 20th International
           Conference on Very Large Data Bases, Santiago, Chile,
           August 29 - September 1, 1994.

    .. [2] Rajamaran, A., and Ullman, J. D. (2011), *Mining of Massive
           Datasets*, Cambridge University Press, Cambridge, UK.

    .. [3] Savasere, A., Omiecinski, E., and Navathe, S. (1995), *An Efficient
           Algorithm for Mining Association Rules in Large Databases*,
           Proceedings of the 21st International Conference on Very Large
           Data Bases, Zurich, Switzerland, 1995.

    Examples
    --------
    *Example 1:*

    This example applies the Apriori algorithm to a data set consisting of 50
    transactions involving five different product IDs. The minimum support
    percentage is set to 0.30, giving a minimum required support of 15
    transactions. The frequent itemsets and strong association rules are
    printed.

    >>> import imsl.data_mining.apriori as apriori
    >>> max_num_products = 5
    >>> max_set_size = 10
    >>> min_pct_support = 0.30
    >>> confidence = 0.8
    >>> lift = 2.0
    >>> x = [[1,  3], [1,  2], [1,  1], [2,  1], [2,  2], [2,  4], [2,  5],
    ...     [3,  3], [4,  4], [4,  3], [4,  5], [4,  1], [5,  5], [6,  1],
    ...     [6,  2], [6,  3], [7,  5], [7,  3], [7,  2], [8,  3], [8,  4],
    ...     [8,  1], [8,  5], [8,  2], [9,  4], [10, 5], [10, 3], [11, 2],
    ...     [11, 3], [12, 4], [13, 4], [14, 2], [14, 3], [14, 1], [15, 3],
    ...     [15, 5], [15, 1], [16, 2], [17, 3], [17, 5], [17, 1], [18, 5],
    ...     [18, 1], [18, 2], [18, 3], [19, 2], [20, 4], [21, 1], [21, 4],
    ...     [21, 2], [21, 5], [22, 5], [22, 4], [23, 2], [23, 5], [23, 3],
    ...     [23, 1], [23, 4], [24, 3], [24, 1], [24, 5], [25, 3], [25, 5],
    ...     [26, 1], [26, 4], [26, 2], [26, 3], [27, 2], [27, 3], [27, 1],
    ...     [27, 5], [28, 5], [28, 3], [28, 4], [28, 1], [28, 2], [29, 4],
    ...     [29, 5], [29, 2], [30, 2], [30, 4], [30, 3], [31, 2], [32, 5],
    ...     [32, 1], [32, 4], [33, 4], [33, 1], [33, 5], [33, 3], [33, 2],
    ...     [34, 3], [35, 5], [35, 3], [36, 3], [36, 5], [36, 4], [36, 1],
    ...     [36, 2], [37, 1], [37, 3], [37, 2], [38, 4], [38, 2], [38, 3],
    ...     [39, 3], [39, 2], [39, 1], [40, 2], [40, 1], [41, 3], [41, 5],
    ...     [41, 1], [41, 4], [41, 2], [42, 5], [42, 1], [42, 4], [43, 3],
    ...     [43, 2], [43, 4], [44, 4], [44, 5], [44, 2], [44, 3], [44, 1],
    ...     [45, 4], [45, 5], [45, 3], [45, 2], [45, 1], [46, 2], [46, 4],
    ...     [46, 5], [46, 3], [46, 1], [47, 4], [47, 5], [48, 2], [49, 1],
    ...     [49, 4], [49, 3], [50, 3], [50, 4]]
    >>> itemsets = apriori.frequent_itemsets(max_num_products, x,
    ...                                      max_set_size=max_set_size,
    ...                                      min_pct_support=min_pct_support)
    >>> # Print frequent itemsets
    >>> print(itemsets)  #doctest: +NORMALIZE_WHITESPACE
    Frequent Itemsets (Out of 50  Transactions):
    Size   Support  Itemset
      1        27   { 1 }
      1        30   { 2 }
      1        33   { 3 }
      1        27   { 4 }
      1        27   { 5 }
      2        20   { 1  2 }
      2        22   { 1  3 }
      2        16   { 1  4 }
      2        19   { 1  5 }
      2        22   { 2  3 }
      2        16   { 2  4 }
      2        15   { 2  5 }
      2        16   { 3  4 }
      2        19   { 3  5 }
      2        17   { 4  5 }
      3        17   { 1  2  3 }
      3        15   { 1  3  5 }
    >>> # Print association rules
    >>> assoc_rules = itemsets.association_rules(confidence, lift)
    >>> for rule in assoc_rules:
    ...     print(rule)  #doctest: +NORMALIZE_WHITESPACE
    Association Rule (itemset X implies itemset Y):
    X = {1} ==> Y = {3}
      supp(X)=27, supp(Y)=33, supp(X U Y)=22
      conf=0.81, lift=1.23
    Association Rule (itemset X implies itemset Y):
    X = {1 2} ==> Y = {3}
      supp(X)=20, supp(Y)=33, supp(X U Y)=17
      conf=0.85, lift=1.29

    *Example 2:*

    This example shows how to apply the Apriori algorithm to separate blocks
    of data and combine results. The data are two separate blocks of 50
    transactions involving five different product IDs. The minimum support
    percentage is set to 0.30, providing a minimum required support of 30
    transactions overall. The frequent itemsets and strong association rules
    are printed.

    >>> import imsl.data_mining.apriori as apriori
    >>> max_num_products = 5
    >>> max_set_size = 4
    >>> min_pct_support = 0.30
    >>> confidence = 0.8
    >>> lift = 2.0
    >>> x1 = [[1,  3], [1,  2], [1,  1], [2,  1], [2,  2], [2,  4], [2,  5],
    ...      [3,  3], [4,  4], [4,  3], [4,  5], [4,  1], [5,  5], [6,  1],
    ...      [6,  2], [6,  3], [7,  5], [7,  3], [7,  2], [8,  3], [8,  4],
    ...      [8,  1], [8,  5], [8,  2], [9,  4], [10, 5], [10, 3], [11, 2],
    ...      [11, 3], [12, 4], [13, 4], [14, 2], [14, 3], [14, 1], [15, 3],
    ...      [15, 5], [15, 1], [16, 2], [17, 3], [17, 5], [17, 1], [18, 5],
    ...      [18, 1], [18, 2], [18, 3], [19, 2], [20, 4], [21, 1], [21, 4],
    ...      [21, 2], [21, 5], [22, 5], [22, 4], [23, 2], [23, 5], [23, 3],
    ...      [23, 1], [23, 4], [24, 3], [24, 1], [24, 5], [25, 3], [25, 5],
    ...      [26, 1], [26, 4], [26, 2], [26, 3], [27, 2], [27, 3], [27, 1],
    ...      [27, 5], [28, 5], [28, 3], [28, 4], [28, 1], [28, 2], [29, 4],
    ...      [29, 5], [29, 2], [30, 2], [30, 4], [30, 3], [31, 2], [32, 5],
    ...      [32, 1], [32, 4], [33, 4], [33, 1], [33, 5], [33, 3], [33, 2],
    ...      [34, 3], [35, 5], [35, 3], [36, 3], [36, 5], [36, 4], [36, 1],
    ...      [36, 2], [37, 1], [37, 3], [37, 2], [38, 4], [38, 2], [38, 3],
    ...      [39, 3], [39, 2], [39, 1], [40, 2], [40, 1], [41, 3], [41, 5],
    ...      [41, 1], [41, 4], [41, 2], [42, 5], [42, 1], [42, 4], [43, 3],
    ...      [43, 2], [43, 4], [44, 4], [44, 5], [44, 2], [44, 3], [44, 1],
    ...      [45, 4], [45, 5], [45, 3], [45, 2], [45, 1], [46, 2], [46, 4],
    ...      [46, 5], [46, 3], [46, 1], [47, 4], [47, 5], [48, 2], [49, 1],
    ...      [49, 4], [49, 3], [50, 3], [50, 4]]
    >>> x2 = [[1,  2], [1,  1], [1,  4], [1,  3], [2,  2], [2,  5], [2,  3],
    ...      [2,  1], [2,  4], [3,  5], [3,  4], [4,  2], [5,  4], [5,  2],
    ...      [5,  3], [5,  5], [6,  3], [6,  5], [7,  2], [7,  5], [7,  4],
    ...      [7,  1], [7,  3], [8,  2], [9,  2], [9,  4], [10, 4], [10, 2],
    ...      [11, 4], [11, 1], [12, 3], [12, 1], [12, 5], [12, 2], [13, 2],
    ...      [14, 3], [14, 4], [14, 2], [15, 2], [16, 5], [16, 2], [16, 4],
    ...      [17, 1], [18, 2], [18, 3], [18, 4], [19, 3], [19, 1], [19, 2],
    ...      [19, 4], [20, 5], [20, 1], [21, 5], [21, 4], [21, 1], [21, 3],
    ...      [22, 4], [22, 1], [22, 5], [23, 1], [23, 2], [24, 4], [25, 4],
    ...      [25, 3], [26, 5], [26, 2], [26, 3], [26, 4], [26, 1], [27, 2],
    ...      [27, 1], [27, 5], [27, 3], [28, 1], [28, 2], [28, 3], [28, 4],
    ...      [29, 5], [29, 2], [29, 1], [30, 5], [30, 3], [30, 2], [30, 4],
    ...      [31, 4], [31, 1], [32, 1], [32, 2], [32, 3], [32, 4], [32, 5],
    ...      [33, 3], [33, 2], [33, 4], [33, 5], [33, 1], [34, 3], [34, 4],
    ...      [34, 5], [34, 2], [35, 2], [35, 3], [36, 3], [36, 5], [36, 4],
    ...      [37, 1], [37, 4], [37, 2], [37, 3], [37, 5], [38, 5], [38, 3],
    ...      [38, 1], [38, 2], [39, 2], [39, 5], [40, 4], [40, 2], [41, 4],
    ...      [42, 4], [43, 5], [43, 4], [44, 5], [44, 4], [44, 3], [44, 2],
    ...      [44, 1], [45, 1], [45, 2], [45, 3], [45, 5], [45, 4], [46, 3],
    ...      [46, 4], [47, 4], [47, 5], [47, 2], [47, 3], [48, 5], [48, 3],
    ...      [48, 2], [48, 1], [48, 4], [49, 4], [49, 5], [50, 4], [50, 1]]
    >>> # Find frequent itemsets in x1 and x2.
    >>> itemsets1 = apriori.frequent_itemsets(max_num_products, x1,
    ...                                       max_set_size=max_set_size,
    ...                                       min_pct_support=min_pct_support)
    >>> itemsets2 = apriori.frequent_itemsets(max_num_products, x2,
    ...                                       max_set_size=max_set_size,
    ...                                       min_pct_support=min_pct_support)
    >>> # Take the union of itemsets1 and itemsets2.
    >>> cand_itemsets = itemsets1.union(itemsets2)
    >>> # Count the frequencies of each candidate itemset in each data set.
    >>> freq1 = cand_itemsets.frequency(x1)
    >>> freq2 = cand_itemsets.frequency(x2)
    >>> # Sum the frequencies.
    >>> freq = freq1 + freq2
    >>> # Determine which of the candidate itemsets are frequent.
    >>> itemsets = cand_itemsets.update(freq)
    >>> # Print the aggregated frequent itemsets.
    >>> print(itemsets)  #doctest: +NORMALIZE_WHITESPACE
    Frequent Itemsets (Out of 100  Transactions):
    Size   Support  Itemset
      1        51   { 1 }
      1        63   { 2 }
      1        60   { 3 }
      1        63   { 4 }
      1        54   { 5 }
      2        37   { 1  2 }
      2        38   { 1  3 }
      2        33   { 1  4 }
      2        35   { 1  5 }
      2        44   { 2  3 }
      2        38   { 2  4 }
      2        34   { 2  5 }
      2        38   { 3  4 }
      2        38   { 3  5 }
      2        37   { 4  5 }
      3        32   { 1  2  3 }
      3        31   { 2  3  4 }
    >>> # Generate and print the strong association rules.
    >>> assoc_rules = itemsets.association_rules(confidence, lift)
    >>> for rule in assoc_rules:
    ...     print(rule)  #doctest: +NORMALIZE_WHITESPACE
    Association Rule (itemset X implies itemset Y):
    X = {1 2} ==> Y = {3}
      supp(X)=37, supp(Y)=60, supp(X U Y)=32
      conf=0.86, lift=1.44
    Association Rule (itemset X implies itemset Y):
    X = {1 3} ==> Y = {2}
      supp(X)=38, supp(Y)=63, supp(X U Y)=32
      conf=0.84, lift=1.34
    Association Rule (itemset X implies itemset Y):
    X = {2 4} ==> Y = {3}
      supp(X)=38, supp(Y)=60, supp(X U Y)=31
      conf=0.82, lift=1.36
    Association Rule (itemset X implies itemset Y):
    X = {3 4} ==> Y = {2}
      supp(X)=38, supp(Y)=63, supp(X U Y)=31
      conf=0.82, lift=1.29

    """

    def __init__(self):   # public constructor
        """Instantiate Itemsets class."""
        self._n_itemsets = 0
        self._n_trans = 0
        self._max_num_products = 0
        self._max_set_size = 0
        self._min_pct_support = 0
        self._item_sets_struct = None
        self._support = None
        self._item_sets = []
        self._results = None

    def _set_attributes(self, item_sets_struct):  # "private" constructor
        self._n_itemsets = item_sets_struct.n_itemsets
        self._n_trans = item_sets_struct.n_trans
        self._max_num_products = item_sets_struct.max_num_products
        self._max_set_size = item_sets_struct.max_set_size
        self._min_pct_support = item_sets_struct.min_pct_support
        self._item_sets_struct = item_sets_struct

        _support = _numpy.empty((self._n_itemsets,), dtype=_numpy.int32)
        _item_sets = []

        for j in range(self._n_itemsets):
            temp = item_sets_struct.itemsets[j]
            n_items = temp.n_items
            _support[j] = temp.support
            _item_sets.append(tuple(temp.items[0:n_items]))

        self._support = _support
        self._item_sets = _item_sets
        self._results = self._print_itemsets()

    @property
    def n_trans(self):
        """Return the number of transactions used to construct the itemsets.

        Returns
        -------
        *int*
            The number of transactions used to construct the frequent itemsets.

        """
        return self._n_trans

    @property
    def max_num_products(self):
        """Return the maximum number of products.

        Returns
        -------
        *int*
            The maximum number of items or products in the transactions used
            to construct the frequent itemsets.

        """
        return self._max_num_products

    @property
    def max_set_size(self):
        """Return the maximum itemset size.

        Returns
        -------
        *int*
            The maximum size of an itemset.

        """
        return self._max_set_size

    @property
    def min_pct_support(self):
        """Return the minimum percentage of transaction support.

        Returns
        -------
        float
            The minimum percentage of transactions in which an itemset must
            be present to be considered frequent.

        """
        return self._min_pct_support

    @property
    def support(self):
        """Return the support for each itemset.

        Returns
        -------
        *(n_items,) ndarray*
            Array containing the number of transactions in which an itemset
            is present.

        """
        return self._support

    @property
    def item_sets(self):
        """Return the itemsets.

        Returns
        -------
        *generator object*
             A generator object containing the frequent itemsets as tuples
             of *int*.

        """
        return (x for x in self._item_sets)

    def union(self, *itemsets):
        r"""Compute the union of itemsets from different transaction sets.

        Parameters
        ----------
        itemsets : *tuple*
            A collection of :py:class:`~FrequentItemSets` instances containing
            information about the frequent itemsets to merge with the current
            instance.

        Returns
        -------
        *FrequentItemSets*
            An object of type :py:class:`~FrequentItemSets` containing the
            merged frequent itemsets.

        """
        if self._item_sets_struct is None:
            raise TypeError("None not supported")

        # If the tuple is empty, return the instance itself
        if len(itemsets) == 0:
            return self

        if (self._n_trans < 1):
            raise ValueError("n_trans must be greater than zero")

        if (self._n_itemsets < 1):
            raise ValueError("n_itemsets must be greater than zero")

        max_num_products = self.max_num_products
        max_set_size = self.max_set_size
        min_pct_support = self.min_pct_support

        start = 0
        stop = len(itemsets)

        for i in range(start, stop):
            if (itemsets[i] is None):
                raise TypeError("None not supported")

            if not (isinstance(itemsets[i], FrequentItemSets)):
                raise TypeError("Type of itemsets not supported")

            if (itemsets[i].n_trans < 1):
                raise ValueError("n_trans must be greater than zero")

            if (itemsets[i]._n_itemsets < 1):
                raise ValueError("n_itemsets must be greater than zero")

            if (itemsets[i].max_num_products != max_num_products):
                raise ValueError("max_num_products must be equal")

            if (itemsets[i].max_set_size != max_set_size):
                raise ValueError("max_set_size must be equal")

            if (itemsets[i].min_pct_support != min_pct_support):
                raise ValueError("min_pct_support must be equal")

        _itemsets_struct = None

        for i in range(0, stop):
            cand_itemsets = _ctypes.POINTER(
                _imsllib.imsls_d_apriori_itemsets)()

            args = []
            args.append(_constants.IMSLS_UNION)
            if i == 0:
                args.append(_ctypes.byref(self._item_sets_struct))
            else:
                args.append(_ctypes.byref(_itemsets_struct))
            args.append(_ctypes.byref(itemsets[i]._item_sets_struct))
            args.append(_ctypes.byref(cand_itemsets))
            args.append(0)

            func = _aggr_apriori_func(_numpy.float64)

            try:
                func(*args)

                n_trans = cand_itemsets.contents.n_trans
                max_num_products = cand_itemsets.contents.max_num_products
                max_set_size = cand_itemsets.contents.max_set_size
                min_pct_support = cand_itemsets.contents.min_pct_support

                # Construct imsls_d_apriori_itemsets structure in Python
                n_itemsets = cand_itemsets.contents.n_itemsets
                # Create array type
                _arr = _imsllib.imsls_apriori_items * n_itemsets
                # Create instance
                _itemsets = _arr()
                ptr_itemsets = cand_itemsets.contents.itemsets
                for j in range(n_itemsets):
                    n_items = ptr_itemsets[j].n_items
                    support = ptr_itemsets[j].support
                    _item = _ctypes.c_int32 * n_items
                    _items = _item()
                    _items[0:n_items] = ptr_itemsets[j].items[0:n_items]
                    # Instantiate the Python structure
                    _itemsets[j] = _imsllib.imsls_apriori_items(n_items,
                                                                _items,
                                                                support)

                # Build imsls_d_apriori_itemsets structure
                _apriori_struct = _imsllib.imsls_d_apriori_itemsets
                min_pct_supp = _ctypes.c_double(min_pct_support)
                _itemsets_struct = _apriori_struct(n_itemsets, _itemsets,
                                                   n_trans, max_num_products,
                                                   max_set_size, min_pct_supp)

            finally:
                # In any case, free the CNL structure to avoid memory leaks
                func = _free_apriori_itemsets_func(_numpy.float64)
                func(cand_itemsets)

        item_sets_inst = FrequentItemSets()
        item_sets_inst._set_attributes(_itemsets_struct)
        return item_sets_inst

    def frequency(self, x):
        r"""Count the frequency of each itemset in a transaction data set.

        Parameters
        ----------
        x : *(n, 2) array_like*
            An array of transaction ID and item ID pairs.

        Returns
        -------
        *ndarray*
            An array containing the number of occurrences of each candidate
            itemset in `x`.

        """
        if self._item_sets_struct is None:
            raise TypeError("None not supported")

        if x is None:
            raise TypeError("None not supported")

        _x = _numpy.asarray(x, order='C', dtype=_numpy.int32)

        if _x.ndim != 2:
            raise ValueError("array of dimension {} not"
                             " supported".format(_x.ndim))

        if _x.shape[1] != 2:
            raise ValueError("array must have two columns")

        if _x.size == 0:
            raise ValueError("empty array not supported")

        _n_rows = _x.shape[0]

        _n_itemsets = len(self._item_sets)

        _frequencies = _numpy.empty((_n_itemsets,), dtype=_numpy.int32)

        if (_n_itemsets <= 0):
            raise ValueError("The number of itemsets must be greater "
                             "than zero")

        freq = _ctypes.POINTER(_ctypes.c_int32)()

        args = []
        args.append(_constants.IMSLS_COUNT)
        args.append(_ctypes.byref(self._item_sets_struct))
        args.append(_n_rows)
        args.append(_x.ctypes.data_as(_ctypes.c_void_p))
        args.append(_ctypes.byref(freq))
        args.append(0)

        func = _aggr_apriori_func(_numpy.float64)

        try:
            func(*args)
            _frequencies[:] = freq[0:_n_itemsets]
        finally:
            if bool(freq):
                func = _imsllib.imsls_free
                func(freq)

        return _frequencies

    def update(self, frequencies):
        r"""Update the set of frequent itemsets in the candidate itemsets.

        Parameters
        ----------
        frequencies : *(n_items,) array_like*
            An array of length `n_items`, the number of candidate itemsets
            in the current instance, containing the frequencies for each
            itemset.

        Returns
        -------
        *FrequentItemSets*
            An object of type :py:class:`~FrequentItemSets` containing the
            updated frequent itemsets.

        """
        if self._item_sets_struct is None:
            raise TypeError("None not supported")

        if frequencies is None:
            raise TypeError("None not supported")

        _freqs = _numpy.asarray(frequencies, order='C', dtype=_numpy.int32)

        if _freqs.ndim != 1:
            raise ValueError("array of dimension {} not"
                             " supported".format(_freqs.ndim))

        if _freqs.size == 0:
            raise ValueError("empty array not supported")

        _n_itemsets = _freqs.size

        _new_itemsets = _ctypes.POINTER(_imsllib.imsls_d_apriori_itemsets)()

        args = []
        args.append(_constants.IMSLS_UPDATE_FREQ_ITEMSETS)
        args.append(_ctypes.byref(self._item_sets_struct))
        args.append(_n_itemsets)
        args.append(_freqs.ctypes.data_as(_ctypes.c_void_p))
        args.append(_ctypes.byref(_new_itemsets))
        args.append(0)

        func = _aggr_apriori_func(_numpy.float64)

        try:
            func(*args)

            n_trans = _new_itemsets.contents.n_trans
            max_num_products = _new_itemsets.contents.max_num_products
            max_set_size = _new_itemsets.contents.max_set_size
            min_pct_support = _new_itemsets.contents.min_pct_support

            # Construct imsls_d_apriori_itemsets structure in Python
            n_itemsets = _new_itemsets.contents.n_itemsets
            # Create array type
            _arr = _imsllib.imsls_apriori_items * n_itemsets
            # Create instance
            _itemsets = _arr()
            ptr_itemsets = _new_itemsets.contents.itemsets
            for j in range(n_itemsets):
                n_items = ptr_itemsets[j].n_items
                support = ptr_itemsets[j].support
                _item = _ctypes.c_int32 * n_items
                _items = _item()
                _items[0:n_items] = ptr_itemsets[j].items[0:n_items]
                # Instantiate the Python structure
                _itemsets[j] = _imsllib.imsls_apriori_items(n_items, _items,
                                                            support)

            # Build imsls_d_apriori_itemsets structure
            _apriori_struct = _imsllib.imsls_d_apriori_itemsets
            min_pct_supp = _ctypes.c_double(min_pct_support)
            _itemsets_struct = _apriori_struct(n_itemsets, _itemsets, n_trans,
                                               max_num_products, max_set_size,
                                               min_pct_supp)

        finally:
            # In any case, free the CNL structure to avoid memory leaks
            func = _free_apriori_itemsets_func(_numpy.float64)
            func(_new_itemsets)

        item_sets_inst = FrequentItemSets()
        item_sets_inst._set_attributes(_itemsets_struct)

        return item_sets_inst

    def association_rules(self, confidence, lift):
        r"""Compute strong association rules among itemsets.

        Parameters
        ----------
        confidence : *float*
            The minimum confidence used to determine the strong association
            rules. `confidence` must be in the interval [0,1].

            If either criterion, `confidence` or `lift` is exceeded, the
            association rule will be considered "strong".

        lift : *float*
            The minimum lift used to determine the strong association rules.
            `lift` must be non-negative.

            If either criterion, `confidence` or `lift`, is exceeded, the
            association rule will be considered "strong".

        Returns
        -------
        *generator object*
            A generator object of :py:class:`~AssociationRule` objects
            containing the strong association rules among the itemsets.

        """
        if self._item_sets_struct is None:
            raise TypeError("None not supported")

        _confidence = float(confidence)

        if not (0.0 <= _confidence <= 1.0):
            raise ValueError("confidence must be in the interval [0,1]")

        _lift = float(lift)

        if _lift < 0.0:
            raise ValueError("lift must be non-negative")

        _assoc_rules_cnl = _ctypes.POINTER(
            _imsllib.imsls_d_association_rules)()

        args = []
        args.append(_constants.IMSLS_ASSOCIATION_RULES)
        args.append(_ctypes.byref(self._item_sets_struct))
        args.append(_ctypes.c_double(_confidence))
        args.append(_ctypes.c_double(_lift))
        args.append(_ctypes.byref(_assoc_rules_cnl))
        args.append(0)

        func = _aggr_apriori_func(_numpy.float64)

        try:
            func(*args)
            # Yield AssociationRule instances
            n_rules = _assoc_rules_cnl.contents.n_rules
            ptr_rules = _assoc_rules_cnl.contents.rules
            for j in range(n_rules):
                n_x = ptr_rules[j].n_x
                n_y = ptr_rules[j].n_y
                confid = ptr_rules[j].confidence
                lift = ptr_rules[j].lift
                # Create copies of CNL arrays
                _x = _numpy.empty((n_x,), dtype=_numpy.int32)
                _x[0:n_x] = ptr_rules[j].x[0:n_x]
                _x = tuple(_x)
                _y = _numpy.empty((n_y,), dtype=_numpy.int32)
                _y[0:n_y] = ptr_rules[j].y[0:n_y]
                _y = tuple(_y)
                _support = _numpy.empty((3,), dtype=_numpy.int32)
                _support[0:3] = ptr_rules[j].support[0:3]
                _support = tuple(_support)
                # Build AssociationRule instance
                assoc_obj = AssociationRule()
                assoc_obj._set_attributes(_x, _y, _support, confid, lift)
                # Return association rule
                yield assoc_obj
        finally:
            # In any case, free the CNL structure to avoid memory leaks
            func = _free_association_rules_func(_numpy.float64)
            func(_assoc_rules_cnl)

    def _print_itemsets(self):
        result = "\nFrequent Itemsets (Out of {:d}  Transactions):\n".format(
            self._n_trans)
        result = ''.join([result, "Size   Support  Itemset\n"])
        for i in range(self._n_itemsets):
            tmp = self._item_sets[i]
            n_items = len(tmp)
            support = self._support[i]
            result = ''.join([result, "  {:d}   ".format(n_items)])
            result = ''.join([result, "     "])
            result = ''.join([result, "{:d}   ".format(support)])
            result = ''.join([result, "{"])
            for j in range(n_items):
                result = ''.join([result, " "])
                result = ''.join([result, "{:d} ".format(tmp[j])])
            result = ''.join([result, "}\n"])

        return result

    def __str__(self):
        """Compute the "informal" string representation of object."""
        return self._results


class AssociationRule():
    r"""Return information on an association rule.

    See Also
    --------
    FrequentItemSets : contains a full description of the Apriori algorithm.

    """

    def __init__(self):
        """Instantiate AssociationRules class."""
        self._support = None
        self._confidence = None
        self._lift = None
        self._x_components = None
        self._y_components = None
        self._results = None

    # "private" constructor
    def _set_attributes(self, x, y, support, confidence, lift):
        self._support = support
        self._confidence = confidence
        self._lift = lift
        self._x_components = x
        self._y_components = y
        self._results = self._print_assoc_rule()

    @property
    def x_components(self):
        """Return the `X` components of the association rule.

        Returns
        -------
        *tuple of int*
            A tuple containing the `X` components of the association rule.

        """
        return self._x_components

    @property
    def y_components(self):
        """Return the `Y` components of the association rule.

        Returns
        -------
        *tuple of int*
            A tuple containing the `Y` components of the association rule.

        """
        return self._y_components

    @property
    def support(self):
        r"""Return the support for the `Z`, `Y`, `X` components.

        Returns
        -------
        *tuple of int*
            A 3-tuple containing the support for the `Z` (:math:`=X \cup Y`),
            `X` and `Y` components of the association rule.

        """
        return self._support

    @property
    def confidence(self):
        """Return the confidence measure of the association rule.

        Returns
        -------
        *float*
            The confidence measure of the association rule.

        """
        return self._confidence

    @property
    def lift(self):
        """Return the lift measure of the association rule.

        Returns
        -------
        *float*
            The lift measure of the association rule.

        """
        return self._lift

    def _print_assoc_rule(self):
        result = "\nAssociation Rule (itemset X implies itemset Y):\n"
        n_x = len(self._x_components)
        n_y = len(self._y_components)
        if (n_x > 0 and n_y > 0):
            result = ''.join([result, "X = "])
            val = self._x_components[0]
            result = ''.join([result, "{"])
            result = ''.join([result, "{:d}".format(val)])
            for j in range(1, n_x):
                val = self._x_components[j]
                result = ''.join([result, " "])
                result = ''.join([result, "{:d}".format(val)])
            result = ''.join([result, "} ==>"])

            result = ''.join([result, " Y = "])

            val = self._y_components[0]
            result = ''.join([result, "{"])
            result = ''.join([result, "{:d}".format(val)])
            for j in range(1, n_y):
                val = self._y_components[j]
                result = ''.join([result, " "])
                result = ''.join([result, "{:d}".format(val)])
            result = ''.join([result, "}\n"])
            result = ''.join([result, "  supp(X)={:d}, supp(Y)={:d},".format(
                self._support[1], self._support[2])])
            result = ''.join([result, " supp(X U Y)={:d}\n".format(
                self._support[0])])
            result = ''.join([result, "  conf={:3.2f}, lift={:3.2f}\n".format(
                self._confidence, self._lift)])

        return result

    def __str__(self):
        """Compute the "informal" string representation of object."""
        return self._results
