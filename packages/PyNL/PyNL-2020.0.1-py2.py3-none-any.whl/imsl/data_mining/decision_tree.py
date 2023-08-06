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
"""DecisionTree related classes, methods, and functions."""
import ctypes as _ctypes
import numpy as _numpy

import imsl._constants as _constants
import imsl._imsllib as _imsllib
import collections as _collections


def _decision_tree_func(dtype):
    """Return the IMSL decision_tree function appropriate for dtype.

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
        return _imsllib.imsls_d_decision_tree
    else:
        return None


def _decision_tree_predict_func(dtype):
    """Return the IMSL decision_tree_predict function appropriate for dtype.

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
        return _imsllib.imsls_d_decision_tree_predict
    else:
        return None


def _decision_tree_free_func(dtype):
    """Return the IMSL decision_tree_free function appropriate for dtype.

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
        return _imsllib.imsls_d_decision_tree_free
    else:
        return None


class _ALACART():
    r"""Generate an ALACART tree generation method.

    Parameters
    ----------
    criteria : *int, optional*
        Specifies which criteria the ALACART method should use in the gain
        calculations to determine the best split at each node.

          +-----------+-----------------+
          |  criteria | Measure         |
          +===========+=================+
          |      0    | Shannon Entropy |
          +-----------+-----------------+
          |      1    | Gini Index      |
          +-----------+-----------------+
          |      2    | Deviance        |
          +-----------+-----------------+

        Default is 0.

    use_gain_ratio : *bool, optional*
        The ALACART method uses a gain ratio instead of just the gain to
        determine the best split.

        Default is False.

    n_surrogate_splits : *int, optional*
        Indicates the number of surrogate splits.

        Default is 0.

    """

    def __init__(self, criteria=0, use_gain_ratio=False, n_surrogate_splits=0):
        self.method_id = 1
        self.criteria = criteria
        self.use_gain_ratio = use_gain_ratio
        self.n_surrogate_splits = n_surrogate_splits

        self.criteria = int(self.criteria)
        if self.criteria not in (0, 1, 2):
            raise ValueError("valid splitting criteria are 0 (Shannon"
                             " Entropy), 1 (Gini Index), or 2 (Deviance)")

        if self.use_gain_ratio not in (True, False):
            raise ValueError("valid use_gain_ratio values are True or False")

        self.n_surrogate_splits = int(self.n_surrogate_splits)
        if self.n_surrogate_splits < 0:
            raise ValueError("number of surrogate splits must be greater"
                             " than or equal to 0")


class _C45():
    r"""Generate a C4.5 tree generation method.

    Parameters
    ----------
    criteria : *int, optional*
        Specifies which criteria the C4.5 method should use in the gain
        calculations to determine the best split at each node.

          +-----------+-----------------+
          |  criteria | Measure         |
          +===========+=================+
          |      0    | Shannon Entropy |
          +-----------+-----------------+
          |      1    | Gini Index      |
          +-----------+-----------------+
          |      2    | Deviance        |
          +-----------+-----------------+

        Default is 0.

    use_gain_ratio : *bool, optional*
        The C4.5 method uses a gain ratio instead of just the gain to determine
        the best split.

        Default is False.

    """

    def __init__(self, criteria=0, use_gain_ratio=False):
        self.method_id = 0
        self.criteria = criteria
        self.use_gain_ratio = use_gain_ratio

        self.criteria = int(self.criteria)
        if self.criteria not in (0, 1, 2):
            raise ValueError("valid splitting criteria are 0 (Shannon"
                             " Entropy), 1 (Gini Index), or 2 (Deviance)")

        if self.use_gain_ratio not in (True, False):
            raise ValueError("valid use_gain_ratio values are True or False")


class _CHAID():
    r"""Generate a CHAID tree generation method.

    Parameters
    ----------
    alphas : *tuple, optional*
        Tuple containing the significance levels. alphas[0] = significance
        level for split variable selection; alphas[1] = significance level for
        merging categories of a variable, and alphas[2] = significance level
        for splitting previously merged categories. Valid values are in the
        range 0 < alphas[1] < 1.0, and alphas[2] <= alphas[1].  Setting
        alphas[2] = -1.0 disables splitting of merged categories.

        Default is (0.05, 0.05, -1.0).

    """

    def __init__(self, alphas=(0.05, 0.05, -1.0)):
        self.method_id = 2
        self.alphas = alphas


class _QUEST():
    r"""Generate a QUEST tree generation method.

    Parameters
    ----------
    alpha : *float, optional*
        The significance level for split variable selection. Valid values are
        in the range 0 < alpha < 1.0.

        Default is 0.05.

    """

    def __init__(self, alpha=0.05):
        self.method_id = 3
        self.alpha = alpha


class _DecisionTree():
    r"""Generate a decision tree.

    Generate a decision tree for a single response variable and two or more
    predictor variables.

    Parameters
    ----------
    response_col_idx : *int*
        Column index of the response variable.

    var_type : *(N,) array_like*
        Array indicating the type of each variable.

          +----------------+------------------------------------+
          |  `var_type[i]` | Type                               |
          +================+====================================+
          |      0         | Categorical                        |
          +----------------+------------------------------------+
          |      1         | Ordered Discrete (Low, Med., High) |
          +----------------+------------------------------------+
          |      2         | Quantitative or Continuous         |
          +----------------+------------------------------------+
          |      3         | Ignore this variable               |
          +----------------+------------------------------------+

    method : *obj*
        Specifies the tree generation method.

          +----------+----------------------------+----------+-----------+
          |  method  | Method                     | Response | Predictor |
          |          |                            | var_type | var_type  |
          +==========+============================+==========+===========+
          | _C45     | C4.5                       | 0        | 0, 1, 2   |
          +----------+----------------------------+----------+-----------+
          | _ALACART | ALACART (Breiman, et. al.) | 0, 1, 2  | 0, 1, 2   |
          +----------+----------------------------+----------+-----------+
          | _CHAID   | CHAID                      | 0, 1, 2  | 0         |
          +----------+----------------------------+----------+-----------+
          | _QUEST   | QUEST                      | 0        | 0, 1, 2   |
          +----------+----------------------------+----------+-----------+

    min_n_node : *int, optional*
        Do not split a node if one of its child nodes will have fewer than
        min_n_node observations.

        Default is 7.

    min_split : *int, optional*
        Do not split a node if the node has fewer than min_split observations.

        Default is 21.

    max_x_cats : *int, optional*
        Allow for up to max_x_cats for categorical predictor variables.

        Default is 10.

    max_size : *int, optional*
        Stop growing the tree once it has reached max_size number of nodes.

        Default is 100.

    max_depth : *int, optional*
        Stop growing the tree once it has reached max_depth number of levels.

        Default is 10.

    priors : *(N,) array_like, optional*
        An array containing prior probabilities for class membership.  The
        argument is ignored for continuous response variables.  By default, the
        prior probabilities are estimated from the data.

    response_name : *string, optional*
        A string representing the name of the response variable.

        Default is "Y".

    var_names : *tuple, optional*
        A tuple containing strings representing the names of predictors.

        Default is "X0", "X1", etc.

    class_names : *tuple, optional*
        A tuple containing strings representing the names of the different
        classes in Y, assuming Y is of categorical type.

        Default is "0", "1", etc.

    categ_names : *tuple, optional*
        A tuple containing strings representing the names of the different
        category levels for each predictor of categorical type.

        Default is "0", "1", etc.

    """

    def __init__(self, response_col_idx, var_type, method, min_n_node=7,
                 min_split=21, max_x_cats=10, max_size=100, max_depth=10,
                 priors=None, response_name='Y', var_names=None,
                 class_names=None, categ_names=None):
        """Instantiate _DecisionTree class."""
        self._response_col_idx = response_col_idx
        self._var_type = var_type
        self._method = method
        _min_n_node = min_n_node
        _min_split = min_split
        _max_x_cats = max_x_cats
        _max_size = max_size
        _max_depth = max_depth
        self._priors = priors
        self._response_name = response_name
        self._var_names = var_names
        self._class_names = class_names
        self._categ_names = categ_names

        self._dtype = None
        # The IMSLS_N_FOLDS optional argument is not yet exposed in the PyNL
        # API; however, self._n_folds must be set to '1' because the desired
        # default value for this parameter in PyNL is '1' while the default
        # value for this optional argument in CNL is '10'.
        self._n_folds = 1
        self._result = None

        self._response_col_idx = int(self._response_col_idx)
        if self._response_col_idx < 0:
            raise ValueError("response_col_idx must be greater than or equal"
                             " to 0")

        if self._var_type is None:
            raise TypeError("None not supported")

        self._var_type = _numpy.array(self._var_type, dtype=_numpy.int32,
                                      order='C')

        if self._var_type.ndim != 1:
            raise ValueError("array of dimension {} not"
                             " supported".format(self._var_type.ndim))

        _min_n_node = int(_min_n_node)
        if not(0 < _min_n_node <= _min_split):
            raise ValueError("min_n_node must be between 0 and min_split")

        _min_split = int(_min_split)
        if _min_split <= 2:
            raise ValueError("min_split must be greater than 2")

        _max_x_cats = int(_max_x_cats)
        if _max_x_cats <= 0:
            raise ValueError("max_x_cats must be greater than 0")

        _max_size = int(_max_size)
        if _max_size <= 0:
            raise ValueError("max_size must be greater than 0")

        _max_depth = int(_max_depth)
        if _max_depth <= 0:
            raise ValueError("max_depth must be greater than 0")

        self._control = _numpy.array(
            (_min_n_node, _min_split, _max_x_cats, _max_size, _max_depth),
            dtype=_numpy.int32)

    def __del__(self):
        """Destroy _DecisionTree class."""
        if (self._dtype is not None) and (self._result is not None):
            # Append input arguments (required)
            args = []
            args.append(self._result)
            args.append(0)

            func = _decision_tree_free_func(self._dtype)
            func(*args)
            # Variable self._result still points to the freed memory block.
            # Therefore, to avoid that CNL's decison_tree_free is
            # called again (resulting in an error), set self._result to
            # None.
            self._result = None

    def __enter__(self):
        """Enter the runtime context related to _DecisionTree object."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit the runtime context related to _DecisionTree object."""
        return self.__del__()

    @property
    def n_classes(self):
        """Return number of classes assumed by response variable."""
        if self._result is None:
            return 0
        else:
            return self._result.contents.n_classes

    @property
    def n_levels(self):
        """Return number of levels or depth of tree."""
        if self._result is None:
            return 0
        else:
            return self._result.contents.n_levels

    @property
    def n_nodes(self):
        """Return number of nodes or size of tree."""
        if self._result is None:
            return 0
        else:
            return self._result.contents.n_nodes

    @property
    def n_preds(self):
        """Return number of predictors used in the model."""
        if self._result is None:
            return 0
        else:
            return self._result.contents.n_preds

    @property
    def pred_type(self):
        """Return types of predictor variables."""
        if self._result is None:
            return None
        else:
            return self._result.contents.pred_type

    @property
    def pred_n_values(self):
        """Return number of values of predictor variables."""
        if self._result is None:
            return 0
        else:
            return self._result.contents.pred_n_values

    @property
    def response_type(self):
        """Return type of the response variable."""
        if self._result is None:
            return None
        else:
            return self._result.contents.response_type

    @property
    def response_name(self):
        """Return name of the response variable."""
        return self._response_name

    @property
    def var_names(self):
        """Return names of the predictors."""
        return self._var_names

    @property
    def class_names(self):
        """Return names of different classes in *Y*."""
        return self._class_names

    @property
    def categ_names(self):
        """Return names of category levels for each categorical predictor."""
        return self._categ_names

    def train(self, training_data, weights=None):
        """
        Train a decision tree using training data and weights.

        Parameters
        ----------
        training_data : *(N,N) array_like*
            Array containing the data.

        weights : *(N,) array_like, optional*
            Array containing the case weights.

            Default is weights[i] = 1.0.

        """
        _training_data = training_data
        _weights = weights

        if _training_data is None:
            raise TypeError("None not supported")

        _training_data = _numpy.array(_training_data, order='C')

        # attempt to promote training_data to a compatible type.
        self._dtype = _numpy.promote_types(_numpy.float64,
                                           _training_data.dtype)
        _training_data = _numpy.asarray(_training_data, dtype=self._dtype,
                                        order='C')

        if (not _numpy.issubdtype(_training_data.dtype, _numpy.float64)):
            raise TypeError("array type {} not supported".format(
                _training_data.dtype.name))

        if _training_data.ndim != 2:
            raise ValueError("array of dimension {} not"
                             " supported".format(_training_data.ndim))

        if _training_data.size == 0:
            raise ValueError("empty array not supported")

        n_rows = training_data.shape[0]

        if _weights is not None:
            _weights = _numpy.asarray(_weights, dtype=self._dtype, order='C')
            if _weights.ndim != 1:
                raise ValueError("array of dimension {} not"
                                 " supported".format(_weights.ndim))
            n_weights = _weights.size
            if n_weights != n_rows:
                raise ValueError("length of weights must be equal to the"
                                 " number of rows in the training data")

        n_columns = training_data.shape[1]

        if self._response_col_idx >= n_columns:
            raise ValueError("response_col_idx must be less than the number of"
                             " columns in the training data")

        n_var_types = self._var_type.shape[0]

        if n_var_types != n_columns:
            raise ValueError("length of var_types must be equal to the number"
                             " of columns in the training data")

        if self._control[1] > n_rows:
            raise ValueError("min_split must be less than or equal to the"
                             " number of rows in the training data")

        if self._control[2] >= n_rows:
            raise ValueError("max_x_cats must be less than the number of rows"
                             " in the training data")

        # Note: CNL uses tolerance values to check feasibility of alpha, so
        # make only a reduced number of Python checks of the entries in alpha
        # here.
        alpha = getattr(self._method, "alpha", None)
        if (alpha is not None) and (not _numpy.isscalar(alpha)):
            raise ValueError("for method QUEST, alpha must be"
                             " a scalar")

        alphas = getattr(self._method, "alphas", None)
        if alphas is not None:
            alphas = _numpy.asarray(alphas, dtype=self._dtype, order='C')
            if alphas.ndim != 1:
                raise ValueError("array of dimension {} not"
                                 " supported".format(alphas.ndim))
            if alphas.size != 3:
                raise ValueError("for method CHAID, alphas must be "
                                 "of length 3")

            # Note: CNL documentation requires alphas[2] <= alphas[1] but
            # CNL code (fdectree.c) requires alphas[2] < alphas[1]
            if alphas[2] > alphas[1]:
                raise ValueError("for method CHAID, alphas[2] must "
                                 "be less than or equal to alphas[1]")

        if self._priors is not None:
            self._priors = _numpy.array(self._priors, dtype=self._dtype,
                                        order='C')
            if self._priors.ndim != 1:
                raise ValueError("array of dimension {} not"
                                 " supported".format(self._priors.ndim))

        if self._var_names is not None:
            n_vars = len(self._var_names)
            if n_vars != n_columns - 1:
                raise ValueError("length of var_names must be equal to the"
                                 " number of predictors in the training data")

        n_surrogate_splits = getattr(self._method, "n_surrogate_splits", None)
        if n_surrogate_splits is not None:
            if n_surrogate_splits > n_columns - 2:
                raise ValueError("number of surrogate splits must be less "
                                 "than or equal to the number of columns in "
                                 "the training data minus two")

        args = []

        # Append input arguments (required)
        args.append(n_rows)
        args.append(n_columns)
        args.append(_training_data.ctypes.data_as(_ctypes.c_void_p))
        args.append(self._response_col_idx)
        args.append(self._var_type.ctypes.data_as(_ctypes.c_void_p))

        # Append input arguments (optional)
        args.append(_constants.IMSLS_METHOD)
        args.append(self._method.method_id)

        criteria = getattr(self._method, "criteria", None)
        if criteria is not None:
            args.append(_constants.IMSLS_CRITERIA)
            args.append(criteria)

        use_gain_ratio = getattr(self._method, "use_gain_ratio", None)
        if (use_gain_ratio is not None) and (use_gain_ratio is True):
            args.append(_constants.IMSLS_RATIO)

        if _weights is not None:
            args.append(_constants.IMSLS_WEIGHTS)
            args.append(_weights.ctypes.data_as(_ctypes.c_void_p))

        args.append(_constants.IMSLS_CONTROL)
        args.append(self._control.ctypes.data_as(_ctypes.c_void_p))

        n_surrogate_splits = getattr(self._method, "n_surrogate_splits", None)
        if n_surrogate_splits is not None:
            args.append(_constants.IMSLS_N_SURROGATES)
            args.append(n_surrogate_splits)

        if alpha is not None:
            args.append(_constants.IMSLS_ALPHAS)
            alphas = _numpy.array([alpha, 0.05, -1.0], dtype=self._dtype)
            args.append(alphas.ctypes.data_as(_ctypes.c_void_p))

        if alphas is not None:
            args.append(_constants.IMSLS_ALPHAS)
            args.append(alphas.ctypes.data_as(_ctypes.c_void_p))

        if self._priors is not None:
            args.append(_constants.IMSLS_PRIORS)
            priors = _numpy.asarray(self._priors, dtype=self._dtype)
            args.append(priors.shape[0])
            args.append(priors.ctypes.data_as(_ctypes.c_void_p))

        args.append(_constants.IMSLS_N_FOLDS)
        args.append(self._n_folds)

        args.append(0)

        func = _decision_tree_func(self._dtype)
        self._result = func(*args)

        if self._class_names is not None:
            n_classes = len(self._class_names)
            if n_classes != self.n_classes:
                raise ValueError("length of class_names must be equal to the"
                                 " number of classes assumed by response"
                                 " variable")

        if self._categ_names is not None:
            n_categs = len(self._categ_names)
            sum_pred_n_values = 0
            for i in range(self.n_preds):
                sum_pred_n_values += self.pred_n_values[i]

            if n_categs != sum_pred_n_values:
                raise ValueError("length of categ_names must be equal to the"
                                 " number of values of each predictor"
                                 " variable")

    def predict(self, data, weights=None):
        """
        Compute predicted values using a decision tree.

        Parameters
        ----------
        data : *(M,N) array_like*
            Array containing the data.

        weights : *(M,) array_like, optional*
            Array containing the case weights.

            Default is weights[i] = 1.0.

        Returns
        -------
        A named tuple with the following fields:

        predictions : *(M,) ndarray*
            Array containing the predicted values.

        pred_err_ss : *float*
            The prediction error mean sum of squares.

        """
        if self._result is None:
            raise ValueError("decision tree has not been trained")

        _data = data
        _weights = weights

        if _data is None:
            raise TypeError("None not supported")

        _data = _numpy.asarray(_data, dtype=self._dtype, order='C')

        if _data.ndim != 2:
            raise ValueError("array of dimension {} not"
                             " supported".format(_data.ndim))

        if _data.size == 0:
            raise ValueError("empty array not supported")

        n_rows = _data.shape[0]
        n_columns = _data.shape[1]

        if n_columns != self._var_type.size:
            raise ValueError("Number of data columns must be equal to the"
                             " number of columns in the training data")

        if _weights is not None:
            _weights = _numpy.asarray(_weights, dtype=self._dtype, order='C')
            if _weights.ndim != 1:
                raise ValueError("array of dimension {} not"
                                 " supported".format(_weights.ndim))
            n_weights = _weights.size
            if n_weights != n_rows:
                raise ValueError("length of weights must be equal to the"
                                 " number of rows in the data")

        args = []

        # Append input arguments (required)
        args.append(n_rows)
        args.append(n_columns)
        args.append(_data.ctypes.data_as(_ctypes.c_void_p))
        args.append(self._var_type.ctypes.data_as(_ctypes.c_void_p))
        args.append(self._result)

        # Append input arguments (optional)
        n_surrogate_splits = getattr(self._method, "n_surrogate_splits", None)
        if n_surrogate_splits is not None:
            args.append(_constants.IMSLS_N_SURROGATES)
            args.append(n_surrogate_splits)

        args.append(_constants.IMSLS_X_RESPONSE_COL)
        args.append(self._response_col_idx)

        if _weights is not None:
            args.append(_constants.IMSLS_WEIGHTS)
            args.append(_weights.ctypes.data_as(_ctypes.c_void_p))

        # Append output arguments
        pred_err_ss = _ctypes.c_double()
        args.append(_constants.IMSLS_ERROR_SS)
        args.append(_ctypes.byref(pred_err_ss))

        predictions = _numpy.empty(n_rows, dtype=self._dtype)
        args.append(_constants.IMSLS_RETURN_USER)
        args.append(predictions.ctypes.data_as(_ctypes.c_void_p))

        args.append(0)

        func = _decision_tree_predict_func(self._dtype)
        func(*args)

        # Pack output arguments into a named tuple
        result = _collections.namedtuple("predictions",
                                         ["predictions",
                                          "pred_err_ss"]
                                         )

        result.predictions = predictions
        result.pred_err_ss = pred_err_ss.value

        return result

    def _print_node(self, tree, node_id, level, spaces):
        """Print the node of a _DecisionTree object."""
        # Generate the general information of a node. For example,
        # Node 0: Cost = 0.357, N = 14.0, Level = 0, Child Nodes:  1  4  5
        n_children = tree.nodes[node_id].n_children
        child_nodes_str = ''
        if n_children > 0 and tree.terminal_nodes[node_id] == 0:
            child_nodes_str = ', Child Nodes: '
            for i in range(n_children):
                child_nodes_str = ''.join([child_nodes_str, ' {} '.format(
                    tree.nodes[node_id].children_ids[i])])

        result = '{}Node {}: Cost = {:.3f}, N = {}, Level = {}{}\n'.format(
            spaces, tree.nodes[node_id].node_id, tree.nodes[node_id].cost,
            tree.nodes[node_id].n_cases, level, child_nodes_str)

        # Generate the rule information of a node. For example,
        # Rule: Outlook in: { Sunny } or
        # Rule: Humidity <= 77.500
        if node_id < tree.n_nodes and node_id > 0:
            rule_str = ''
            if self._var_names is None:
                rule_str = '{}Rule: X{}'.format(
                    spaces, tree.nodes[node_id].node_var_id)
            else:
                rule_str = '{}Rule: {}'.format(
                    spaces, self._var_names[tree.nodes[node_id].node_var_id])

            if tree.pred_type[tree.nodes[node_id].node_var_id] < 2:
                in_str = ' in: {'
                idx = 0
                for j in range(tree.nodes[node_id].node_var_id):
                    idx += tree.pred_n_values[j]

                n_vals = tree.pred_n_values[tree.nodes[node_id].node_var_id]
                for j in range(n_vals):
                    if tree.nodes[node_id].node_values_ind[j] == 1:
                        if self._categ_names is not None:
                            in_str = ''.join([in_str, ' {} '.format(
                                self._categ_names[idx + j])])
                in_str = ''.join([in_str, '}\n'])
                result = ''.join([result, ''.join([rule_str, in_str])])
            else:
                if node_id == tree.nodes[node_id].parent_id + 1:
                    rule_str = ''.join([rule_str, ' <= {:.3f}\n'.format(
                        tree.nodes[node_id].node_split_value)])
                else:
                    rule_str = ''.join([rule_str, ' > {:.3f}\n'.format(
                        tree.nodes[node_id].node_split_value)])

                result = ''.join([result, rule_str])

        # Generate the probability information of a node. For example,
        # P(Y=0) = 0.357
        # P(Y=1) = 0.643
        # Predicted Y: Play
        if tree.response_type < 2:
            for j in range(tree.n_classes):
                result = ''.join([result, ('{}P(Y={}) = {:.3f}\n'.format(
                    spaces, j,
                    self._result.contents.nodes[node_id].y_probs[j]))])

            if self._class_names is None:
                result = ''.join([result, ('{}Predicted {}: {}\n'.format(
                    spaces, self._response_name,
                    tree.nodes[node_id].predicted_class))])
            else:
                result = ''.join([result, ('{}Predicted {}: {}\n'.format(
                    spaces, self._response_name,
                    self._class_names[tree.nodes[node_id].predicted_class]))])

        # Call _print_node recursively to print the children of a node.
        if n_children > 0 and tree.terminal_nodes[node_id] == 0:
            spaces = spaces + '   '
            level = level + 1
            for j in range(n_children):
                child_id = tree.nodes[node_id].children_ids[j]
                result = ''.join([result, self._print_node(
                    tree, child_id, level, spaces)])

        return result

    def __str__(self):
        """Compute the "informal" string representation of object."""
        result = "Decision Tree:\n\n"
        if self._result is not None:
            tree = self._result.contents
            result = ''.join([result, self._print_node(
                tree, tree.nodes[0].node_id, 0, '')])
        return result


class ALACARTDecisionTree(_DecisionTree):
    r"""Generate a decision tree using the ALACART method.

    Generate a decision tree for a single response variable and two or more
    predictor variables using the ALACART method.

    Parameters
    ----------
    response_col_idx : *int*
        Column index of the response variable.

    var_type : *(N,) array_like*
        Array indicating the type of each variable.

        .. rst-class:: nowrap

            +----------------+------------------------------------+
            |  `var_type[i]` | Type                               |
            +================+====================================+
            |      0         | Categorical                        |
            +----------------+------------------------------------+
            |      1         | Ordered Discrete (Low, Med., High) |
            +----------------+------------------------------------+
            |      2         | Quantitative or Continuous         |
            +----------------+------------------------------------+
            |      3         | Ignore this variable               |
            +----------------+------------------------------------+

    criteria : *int, optional*
        Specifies which criteria the ALACART method should use in the gain
        calculations to determine the best split at each node.

        .. rst-class:: nowrap

            +-----------+-----------------+
            |  criteria | Measure         |
            +===========+=================+
            |      0    | Shannon Entropy |
            +-----------+-----------------+
            |      1    | Gini Index      |
            +-----------+-----------------+
            |      2    | Deviance        |
            +-----------+-----------------+

        Default is 0.

        Shannon Entropy
            Shannon Entropy is a measure of randomness or uncertainty. For a
            categorical variable having :math:`C` distinct values over a
            dataset :math:`S`, the Shannon Entropy is defined as

                :math:`\sum_{i=1}^{C}p_i\log(p_i)`

            where

                :math:`p_i = Pr(Y=i)`

            and where

                :math:`p_i \log(p_i) = 0`

            if :math:`p_i=0`.

        Gini Index
            Gini Index is a measure of statistical dispersion. For a
            categorical variable having :math:`C` distinct values over a
            dataset :math:`S`, the Gini index is defined as

                :math:`I(S)=\sum_{\begin{array}{c}i,j=1\\i\ne j\end{array}}^C
                p(i|S)p(j|S)=1-\sum^C_{i=1}p^2(i|S)`

            where :math:`p(i|S)` denotes the probability that the variable is
            equal to the state :math:`i` on the dataset :math:`S`.

        Deviance
            Deviance is a measure of the quality of fit. For a categorical
            variable having :math:`C` distinct values over a dataset :math:`S`,
            the Deviance measure is

                :math:`\sum_{i=1}^{C}n_i\log(p_i)`

            where

                :math:`p_i = Pr(Y=i)`

            and :math:`n_i` is the number of cases with :math:`Y=i` on the
            node.

    use_gain_ratio : *bool, optional*
        The ALACART method uses a gain ratio instead of just the gain to
        determine the best split.

        Default is False.

    n_surrogate_splits : *int, optional*
        Indicates the number of surrogate splits.

        Default is 0.

    min_n_node : *int, optional*
        Do not split a node if one of its child nodes will have fewer than
        min_n_node observations.

        Default is 7.

    min_split : *int, optional*
        Do not split a node if the node has fewer than min_split observations.

        Default is 21.

    max_x_cats : *int, optional*
        Allow for up to max_x_cats for categorical predictor variables.

        Default is 10.

    max_size : *int, optional*
        Stop growing the tree once it has reached max_size number of nodes.

        Default is 100.

    max_depth : *int, optional*
        Stop growing the tree once it has reached max_depth number of levels.

        Default is 10.

    priors : *(N,) array_like, optional*
        An array containing prior probabilities for class membership.  The
        argument is ignored for continuous response variables.  By default, the
        prior probabilities are estimated from the data.

    response_name : *string, optional*
        A string representing the name of the response variable.

        Default is "Y".

    var_names : *tuple, optional*
        A tuple containing strings representing the names of predictors.

        Default is "X0", "X1", etc.

    class_names : *tuple, optional*
        A tuple containing strings representing the names of the different
        classes in Y, assuming Y is of categorical type.

        Default is "0", "1", etc.

    categ_names : *tuple, optional*
        A tuple containing strings representing the names of the different
        category levels for each predictor of categorical type.

        Default is "0", "1", etc.

    Notes
    -----
    ALACART implements the method of Breiman, Friedman, Olshen and Stone
    ([1]_), the original authors and developers of CART(TM). CART(TM) is the
    trademarked name for Classification and Regression Trees. In ALACART, only
    binary splits are considered for categorical variables. That is, if X has
    values {A, B, C, D}, splits into only two subsets are considered, e.g., {A}
    and {B, C, D}, or {A, B} and {C, D}, are allowed, but a three-way split
    defined by {A}, {B} and {C,D} is not.

    For classification problems, ALACART uses a similar criterion to
    information gain called impurity. The method searches for a split that
    reduces the node impurity the most. For a given set of data S at a node,
    the node impurity for a C-class categorical response is a function of the
    class probabilities

    .. math::
       I(S)=\phi(p(1|S),p(2|S),\ldots,p(C|S))

    The measure function :math:`\phi(\cdot)` should be 0 for "pure" nodes,
    where all *Y* are in the same class, and maximum when *Y* is uniformly
    distributed across the classes.

    As only binary splits of a subset *S* are considered (:math:`S_1`,
    :math:`S_2` such that :math:`S=S_1\cup S_2` and
    :math:`S=S_1\cap S_2=\emptyset`), the reduction in impurity when splitting
    *S* into :math:`S_1`, :math:`S_2` is

    .. math::
       \Delta I=I(S)-q_1I\left(S_1\right)-q_2I\left(S_2\right)

    where

    .. math::
       q_j = Pr[S_j], j = 1,2

    is the node probability.

    The gain criteria and the reduction in impurity :math:`\Delta I` are
    similar concepts and equivalent when *I* is entropy and when only binary
    splits are considered. Another popular measure for the impurity at a node
    is the *Gini* index, given by

    .. math::
       I(S)=\sum_{\begin{array}{c}i,j=1\\i\ne j\end{array}}^C
       p(i|S)p(j|S)=1-\sum^C_{i=1}p^2(i|S)

    If *Y* is an ordered response or continuous, the problem is a regression
    problem. ALACART generates the tree using the same steps, except that
    node-level measures or loss-functions are the mean squared error (MSE) or
    mean absolute error (MAD) rather than node impurity measures.

    References
    ----------
    .. [1] Breiman, L., Friedman, J. H., Olshen, R. A., and Stone, C. J. (1984)
           Classification and Regression Trees, Chapman & Hall. For the latest
           information on CART visit: http://www.salford-systems.com/cart.php.

    Examples
    --------
    In this example, we use a small dataset with response variable, Play, which
    indicates whether a golfer plays (1) or does not play (0) golf under
    weather conditions measured by Temperature, Humidity, Outlook (Sunny (0),
    Overcast (1), Rainy (2)), and Wind (True (0), False (1)). A decision tree
    is generated by the ALACART method. The control parameters are adjusted
    because of the small data size, and no cross-validation or pruning is
    performed. Notice that ALACART splits on Outlook, then Temperature.

    >>> import numpy as np
    >>> import imsl.data_mining as dm
    >>> xy = np.array([[0, 85.0, 85.0, 0, 0],
    ...                [0, 80.0, 90.0, 1, 0],
    ...                [1, 83.0, 78.0, 0, 1],
    ...                [2, 70.0, 96.0, 0, 1],
    ...                [2, 68.0, 80.0, 0, 1],
    ...                [2, 65.0, 70.0, 1, 0],
    ...                [1, 64.0, 65.0, 1, 1],
    ...                [0, 72.0, 95.0, 0, 0],
    ...                [0, 69.0, 70.0, 0, 1],
    ...                [2, 75.0, 80.0, 0, 1],
    ...                [0, 75.0, 70.0, 1, 1],
    ...                [1, 72.0, 90.0, 1, 1],
    ...                [1, 81.0, 75.0, 0, 1],
    ...                [2, 71.0, 80.0, 1, 0]])
    >>> response_column_index = 4
    >>> var_type = np.array([0, 2, 2, 0, 0], dtype=int)
    >>> names = ["Outlook", "Temperature", "Humidity", "Wind"]
    >>> class_names = ["Don't Play", "Play"]
    >>> var_levels = ["Sunny", "Overcast", "Rainy", "False", "True"]
    >>> print("Decision Tree using Method ALACART:\n\n")
    ... #doctest: +NORMALIZE_WHITESPACE
    Decision Tree using Method ALACART:
    >>> with dm.ALACARTDecisionTree(response_column_index, var_type,
    ...                             min_n_node=2, min_split=3, max_x_cats=10,
    ...                             max_size=50, max_depth=10, var_names=names,
    ...                             class_names=class_names,
    ...                             categ_names=var_levels) as decision_tree:
    ...     decision_tree.train(xy)
    ...     print(decision_tree)
    ... #doctest: +NORMALIZE_WHITESPACE
    Decision Tree:
    Node 0: Cost = 0.357, N = 14.0, Level = 0, Child Nodes:  1  8
    P(Y=0) = 0.357
    P(Y=1) = 0.643
    Predicted Y: Play
       Node 1: Cost = 0.357, N = 10.0, Level = 1, Child Nodes:  2  7
       Rule: Outlook in: { Sunny  Rainy }
       P(Y=0) = 0.500
       P(Y=1) = 0.500
       Predicted Y: Don't Play
          Node 2: Cost = 0.214, N = 8.0, Level = 2, Child Nodes:  3  6
          Rule: Temperature <= 77.500
          P(Y=0) = 0.375
          P(Y=1) = 0.625
          Predicted Y: Play
             Node 3: Cost = 0.214, N = 6.0, Level = 3, Child Nodes:  4  5
             Rule: Temperature <= 73.500
             P(Y=0) = 0.500
             P(Y=1) = 0.500
             Predicted Y: Play
                Node 4: Cost = 0.071, N = 4.0, Level = 4
                Rule: Temperature <= 70.500
                P(Y=0) = 0.250
                P(Y=1) = 0.750
                Predicted Y: Play
                Node 5: Cost = 0.000, N = 2.0, Level = 4
                Rule: Temperature > 70.500
                P(Y=0) = 1.000
                P(Y=1) = 0.000
                Predicted Y: Don't Play
             Node 6: Cost = 0.000, N = 2.0, Level = 3
             Rule: Temperature > 73.500
             P(Y=0) = 0.000
             P(Y=1) = 1.000
             Predicted Y: Play
          Node 7: Cost = 0.000, N = 2.0, Level = 2
          Rule: Temperature > 77.500
          P(Y=0) = 1.000
          P(Y=1) = 0.000
          Predicted Y: Don't Play
       Node 8: Cost = 0.000, N = 4.0, Level = 1
       Rule: Outlook in: { Overcast }
       P(Y=0) = 0.000
       P(Y=1) = 1.000
       Predicted Y: Play

    """

    def __init__(self, response_col_idx, var_type, criteria=0,
                 use_gain_ratio=False, n_surrogate_splits=0, min_n_node=7,
                 min_split=21, max_x_cats=10, max_size=100, max_depth=10,
                 priors=None, response_name='Y', var_names=None,
                 class_names=None, categ_names=None):
        """Instantiate ALACARTDecisionTree class."""
        method = _ALACART(criteria=criteria, use_gain_ratio=use_gain_ratio,
                          n_surrogate_splits=n_surrogate_splits)
        _DecisionTree.__init__(self, response_col_idx, var_type, method,
                               min_n_node=min_n_node, min_split=min_split,
                               max_x_cats=max_x_cats, max_size=max_size,
                               max_depth=max_depth, priors=priors,
                               response_name=response_name,
                               var_names=var_names, class_names=class_names,
                               categ_names=categ_names)

    @property
    def n_surrogates(self):
        """Return number of surrogate splits searched for at each node."""
        if self._result is None:
            return 0
        else:
            return self._result.contents.n_surrogates


class C45DecisionTree(_DecisionTree):
    r"""Generate a decision tree using the C4.5 method.

    Generate a decision tree for a single response variable and two or more
    predictor variables using the C4.5 method.

    Parameters
    ----------
    response_col_idx : *int*
        Column index of the response variable.

    var_type : *(N,) array_like*
        Array indicating the type of each variable.

        .. rst-class:: nowrap

            +----------------+------------------------------------+
            |  `var_type[i]` | Type                               |
            +================+====================================+
            |      0         | Categorical                        |
            +----------------+------------------------------------+
            |      1         | Ordered Discrete (Low, Med., High) |
            +----------------+------------------------------------+
            |      2         | Quantitative or Continuous         |
            +----------------+------------------------------------+
            |      3         | Ignore this variable               |
            +----------------+------------------------------------+

    criteria : *int, optional*
        Specifies which criteria the C4.5 method should use in the gain
        calculations to determine the best split at each node.

        .. rst-class:: nowrap

            +-----------+-----------------+
            |  criteria | Measure         |
            +===========+=================+
            |      0    | Shannon Entropy |
            +-----------+-----------------+
            |      1    | Gini Index      |
            +-----------+-----------------+
            |      2    | Deviance        |
            +-----------+-----------------+

        Default is 0.

        Shannon Entropy
            Shannon Entropy is a measure of randomness or uncertainty. For a
            categorical variable having :math:`C` distinct values over a
            dataset :math:`S`, the Shannon Entropy is defined as

                :math:`\sum_{i=1}^{C}p_i\log(p_i)`

            where

                :math:`p_i = Pr(Y=i)`

            and where

                :math:`p_i \log(p_i) = 0`

            if :math:`p_i=0`.

        Gini Index
            Gini Index is a measure of statistical dispersion. For a
            categorical variable having :math:`C` distinct values over a
            dataset :math:`S`, the Gini index is defined as

                :math:`I(S)=\sum_{\begin{array}{c}i,j=1\\i\ne j\end{array}}^C
                p(i|S)p(j|S)=1-\sum^C_{i=1}p^2(i|S)`

            where :math:`p(i|S)` denotes the probability that the variable is
            equal to the state :math:`i` on the dataset :math:`S`.

        Deviance
            Deviance is a measure of the quality of fit. For a categorical
            variable having :math:`C` distinct values over a dataset :math:`S`,
            the Deviance measure is

                :math:`\sum_{i=1}^{C}n_i\log(p_i)`

            where

                :math:`p_i = Pr(Y=i)`

            and :math:`n_i` is the number of cases with :math:`Y=i` on the
            node.

    use_gain_ratio : *bool, optional*
        The C4.5 method uses a gain ratio instead of just the gain to determine
        the best split.

        Default is False.

    min_n_node : *int, optional*
        Do not split a node if one of its child nodes will have fewer than
        min_n_node observations.

        Default is 7.

    min_split : *int, optional*
        Do not split a node if the node has fewer than min_split observations.

        Default is 21.

    max_x_cats : *int, optional*
        Allow for up to max_x_cats for categorical predictor variables.

        Default is 10.

    max_size : *int, optional*
        Stop growing the tree once it has reached max_size number of nodes.

        Default is 100.

    max_depth : *int, optional*
        Stop growing the tree once it has reached max_depth number of levels.

        Default is 10.

    priors : *(N,) array_like, optional*
        An array containing prior probabilities for class membership.  The
        argument is ignored for continuous response variables.  By default, the
        prior probabilities are estimated from the data.

    response_name : *string, optional*
        A string representing the name of the response variable.

        Default is "Y".

    var_names : *tuple, optional*
        A tuple containing strings representing the names of predictors.

        Default is "X0", "X1", etc.

    class_names : *tuple, optional*
        A tuple containing strings representing the names of the different
        classes in Y, assuming Y is of categorical type.

        Default is "0", "1", etc.

    categ_names : *tuple, optional*
        A tuple containing strings representing the names of the different
        category levels for each predictor of categorical type.

        Default is "0", "1", etc.

    Notes
    -----
    The method C4.5 ([1]_) is a tree partitioning algorithm for a categorical
    response variable and categorical or quantitivate predictor variables. The
    procedure follows the general steps outlined above, using as splitting
    criterion the information *gain* or *gain ratio*. Specifically, the
    *entropy* or *uncertainty* in the response variable with *C* categories
    over the full training sample *S* is defined as

    .. math::
       E(S)=-\sum_{i=1}^Cp_i\mbox{log}\left(p_i\right)

    Where :math:`p_i=\mbox{Pr}[Y=i|S]` is the probability that the response
    takes on category *i* on the dataset *S*. This measure is widely known as
    the Shannon Entropy. Splitting the dataset further may either increase or
    decrease the entropy in the response variable. For example, the entropy of
    *Y* over a partitioning of *S* by *X*, a variable with *K* categories, is
    given by

    .. math::
       E(S,X)=-\sum_{k=1}^{K}\sum_{i=1}^{C_k}p\left(S_k\right)E\left(S_k\right)

    If any split defined by the values of a categorical predictor decreases the
    entropy in *Y*, then it is said to yield *information gain*:

    .. math::
       g(S,X)=E(S)-E(S,X)

    The best splitting variable according to the information gain criterion is
    the variable yielding the largest information gain, calculated in this
    manner. A modified criterion is the *gain ratio*:

    .. math::
       gR(S,X)=\frac{E(S)-E(S,X)}{E_X\left(S\right)}

    where

    .. math::
       E_x\left(S\right)=-\sum_{k=1}^K\nu_k\mbox{log}\left(\nu_k\right)

    with

    .. math::
       \nu_k=\mbox{Pr}[X=k|S]

    Note that :math:`E_X(S)` is just the entropy of the variable *X* over *S*.
    The gain ratio is thought to be less biased toward predictors with many
    categories. C4.5 treats the continuous variable similarly, except that only
    binary splits of the form :math:`X\le d` and :math:`X\gt d` are considered,
    where *d* is a value in the range of *X* on *S*. The best split is
    determined by the split variable and split point that gives the largest
    criterion value. It is possible that no variable meets the threshold for
    further splitting at the current node, in which case growing stops and the
    node becomes a *terminal* node. Otherwise, the node is split, creating two
    or more child nodes. Then, using the dataset partition defined by the
    splitting variable and split value, the very same procedure is repeated for
    each child node. Thus a collection of nodes and child-nodes are generated,
    or, in other words, the tree is *grown*. The growth stops after one or more
    different conditions are met.

    References
    ----------
    .. [1] Quinlan, J.R. (1993). C4.5 Programs for Machine Learning, Morgan
           Kaufmann. For the latest information on Quinlan's algorithms see
           http://www.rulequest.com/.

    Examples
    --------
    In this example, we use a small dataset with response variable, Play, which
    indicates whether a golfer plays (1) or does not play (0) golf under
    weather conditions measured by Temperature, Humidity, Outlook (Sunny (0),
    Overcast (1), Rainy (2)), and Wind (True (0), False (1)). A decision tree
    is generated by the C4.5 method. The control parameters are adjusted
    because of the small data size, and no cross-validation or pruning is
    performed. Notice that C4.5 splits on Outlook, then Humidity and Wind.

    >>> import numpy as np
    >>> import imsl.data_mining as dm
    >>> xy = np.array([[0, 85.0, 85.0, 0, 0],
    ...                [0, 80.0, 90.0, 1, 0],
    ...                [1, 83.0, 78.0, 0, 1],
    ...                [2, 70.0, 96.0, 0, 1],
    ...                [2, 68.0, 80.0, 0, 1],
    ...                [2, 65.0, 70.0, 1, 0],
    ...                [1, 64.0, 65.0, 1, 1],
    ...                [0, 72.0, 95.0, 0, 0],
    ...                [0, 69.0, 70.0, 0, 1],
    ...                [2, 75.0, 80.0, 0, 1],
    ...                [0, 75.0, 70.0, 1, 1],
    ...                [1, 72.0, 90.0, 1, 1],
    ...                [1, 81.0, 75.0, 0, 1],
    ...                [2, 71.0, 80.0, 1, 0]])
    >>> response_column_index = 4
    >>> var_type = np.array([0, 2, 2, 0, 0], dtype=int)
    >>> names = ["Outlook", "Temperature", "Humidity", "Wind"]
    >>> class_names = ["Don't Play", "Play"]
    >>> var_levels = ["Sunny", "Overcast", "Rainy", "False", "True"]
    >>> print("Decision Tree using Method C4.5:\n\n")
    ... #doctest: +NORMALIZE_WHITESPACE
    Decision Tree using Method C4.5:
    >>> with dm.C45DecisionTree(response_column_index, var_type,
    ...                         min_n_node=2, min_split=3, max_x_cats=10,
    ...                         max_size=50, max_depth=10, var_names=names,
    ...                         class_names=class_names,
    ...                         categ_names=var_levels) as decision_tree:
    ...     decision_tree.train(xy)
    ...     print(decision_tree)
    ... #doctest: +NORMALIZE_WHITESPACE
    Decision Tree:
    Node 0: Cost = 0.357, N = 14.0, Level = 0, Child Nodes:  1  4  5
    P(Y=0) = 0.357
    P(Y=1) = 0.643
    Predicted Y: Play
       Node 1: Cost = 0.143, N = 5.0, Level = 1, Child Nodes:  2  3
       Rule: Outlook in: { Sunny }
       P(Y=0) = 0.600
       P(Y=1) = 0.400
       Predicted Y: Don't Play
          Node 2: Cost = 0.000, N = 2.0, Level = 2
          Rule: Humidity <= 77.500
          P(Y=0) = 0.000
          P(Y=1) = 1.000
          Predicted Y: Play
          Node 3: Cost = 0.000, N = 3.0, Level = 2
          Rule: Humidity > 77.500
          P(Y=0) = 1.000
          P(Y=1) = 0.000
          Predicted Y: Don't Play
       Node 4: Cost = 0.000, N = 4.0, Level = 1
       Rule: Outlook in: { Overcast }
       P(Y=0) = 0.000
       P(Y=1) = 1.000
       Predicted Y: Play
       Node 5: Cost = 0.143, N = 5.0, Level = 1, Child Nodes:  6  7
       Rule: Outlook in: { Rainy }
       P(Y=0) = 0.400
       P(Y=1) = 0.600
       Predicted Y: Play
          Node 6: Cost = 0.000, N = 3.0, Level = 2
          Rule: Wind in: { False }
          P(Y=0) = 0.000
          P(Y=1) = 1.000
          Predicted Y: Play
          Node 7: Cost = 0.000, N = 2.0, Level = 2
          Rule: Wind in: { True }
          P(Y=0) = 1.000
          P(Y=1) = 0.000
          Predicted Y: Don't Play

    >>> import numpy as np
    >>> import imsl.data_mining as dm
    >>> xy = np.array([[2, 0, 2],
    ...                [1, 0, 0],
    ...                [2, 1, 3],
    ...                [0, 1, 0],
    ...                [1, 2, 0],
    ...                [2, 2, 3],
    ...                [2, 2, 3],
    ...                [0, 1, 0],
    ...                [0, 0, 0],
    ...                [0, 1, 0],
    ...                [1, 2, 0],
    ...                [2, 0, 2],
    ...                [0, 2, 0],
    ...                [2, 0, 1],
    ...                [0, 0, 0],
    ...                [2, 0, 1],
    ...                [1, 0, 0],
    ...                [0, 2, 0],
    ...                [2, 0, 1],
    ...                [1, 2, 0],
    ...                [0, 2, 2],
    ...                [2, 1, 3],
    ...                [1, 1, 0],
    ...                [2, 2, 3],
    ...                [1, 2, 0],
    ...                [2, 2, 3],
    ...                [2, 0, 1],
    ...                [2, 1, 3],
    ...                [1, 2, 0],
    ...                [1, 1, 0]])
    >>> response_column_index = 2
    >>> var_type = np.array([0, 0, 0], dtype=int)
    >>> names = ['Var1', 'Var2']
    >>> class_names = ["c1", "c2", "c3", "c4"]
    >>> response_name = 'Response'
    >>> var_levels = ["L1", "L2", "L3", "A", "B", "C"]
    >>> print("Decision Tree using Method C4.5:\n\n")
    ... #doctest: +NORMALIZE_WHITESPACE
    Decision Tree using Method C4.5:
    >>> with dm.C45DecisionTree(response_column_index, var_type,
    ...                         min_n_node=5, min_split=10, max_x_cats=10,
    ...                         max_size=50, max_depth=10,
    ...                         response_name=response_name, var_names=names,
    ...                         class_names=class_names,
    ...                         categ_names=var_levels) as decision_tree:
    ...     decision_tree.train(xy)
    ...     print(decision_tree)
    ... #doctest: +NORMALIZE_WHITESPACE
    Decision Tree:
    Node 0: Cost = 0.467, N = 30.0, Level = 0, Child Nodes:  1  2  3
    P(Y=0) = 0.533
    P(Y=1) = 0.133
    P(Y=2) = 0.100
    P(Y=3) = 0.233
    Predicted Response: c1
       Node 1: Cost = 0.033, N = 8.0, Level = 1
       Rule: Var1 in: { L1 }
       P(Y=0) = 0.875
       P(Y=1) = 0.000
       P(Y=2) = 0.125
       P(Y=3) = 0.000
       Predicted Response: c1
       Node 2: Cost = 0.000, N = 9.0, Level = 1
       Rule: Var1 in: { L2 }
       P(Y=0) = 1.000
       P(Y=1) = 0.000
       P(Y=2) = 0.000
       P(Y=3) = 0.000
       Predicted Response: c1
       Node 3: Cost = 0.200, N = 13.0, Level = 1
       Rule: Var1 in: { L3 }
       P(Y=0) = 0.000
       P(Y=1) = 0.308
       P(Y=2) = 0.154
       P(Y=3) = 0.538
       Predicted Response: c4

    """

    def __init__(self, response_col_idx, var_type, criteria=0,
                 use_gain_ratio=False, min_n_node=7, min_split=21,
                 max_x_cats=10, max_size=100, max_depth=10, priors=None,
                 response_name='Y', var_names=None, class_names=None,
                 categ_names=None):
        """Instantiate C45DecisionTree class."""
        method = _C45(criteria=criteria, use_gain_ratio=use_gain_ratio)
        _DecisionTree.__init__(self, response_col_idx, var_type, method,
                               min_n_node=min_n_node, min_split=min_split,
                               max_x_cats=max_x_cats, max_size=max_size,
                               max_depth=max_depth, priors=priors,
                               response_name=response_name,
                               var_names=var_names, class_names=class_names,
                               categ_names=categ_names)


class CHAIDDecisionTree(_DecisionTree):
    r"""Generate a decision tree using the CHAID method.

    Generate a decision tree for a single response variable and two or more
    predictor variables using the CHAID method.

    Parameters
    ----------
    response_col_idx : *int*
        Column index of the response variable.

    var_type : *(N,) array_like*
        Array indicating the type of each variable.

        .. rst-class:: nowrap

            +----------------+------------------------------------+
            |  `var_type[i]` | Type                               |
            +================+====================================+
            |      0         | Categorical                        |
            +----------------+------------------------------------+
            |      1         | Ordered Discrete (Low, Med., High) |
            +----------------+------------------------------------+
            |      2         | Quantitative or Continuous         |
            +----------------+------------------------------------+
            |      3         | Ignore this variable               |
            +----------------+------------------------------------+

    alphas : *tuple, optional*
        Tuple containing the significance levels. alphas[0] = significance
        level for split variable selection; alphas[1] = significance level for
        merging categories of a variable, and alphas[2] = significance level
        for splitting previously merged categories. Valid values are in the
        range 0 < alphas[1] < 1.0, and alphas[2] <= alphas[1].  Setting
        alphas[2] = -1.0 disables splitting of merged categories.

        Default is [0.05, 0.05, -1.0].

    min_n_node : *int, optional*
        Do not split a node if one of its child nodes will have fewer than
        min_n_node observations.

        Default is 7.

    min_split : *int, optional*
        Do not split a node if the node has fewer than min_split observations.

        Default is 21.

    max_x_cats : *int, optional*
        Allow for up to max_x_cats for categorical predictor variables.

        Default is 10.

    max_size : *int, optional*
        Stop growing the tree once it has reached max_size number of nodes.

        Default is 100.

    max_depth : *int, optional*
        Stop growing the tree once it has reached max_depth number of levels.

        Default is 10.

    priors : *(N,) array_like, optional*
        An array containing prior probabilities for class membership.  The
        argument is ignored for continuous response variables.  By default, the
        prior probabilities are estimated from the data.

    response_name : *string, optional*
        A string representing the name of the response variable.

        Default is "Y".

    var_names : *tuple, optional*
        A tuple containing strings representing the names of predictors.

        Default is "X0", "X1", etc.

    class_names : *tuple, optional*
        A tuple containing strings representing the names of the different
        classes in Y, assuming Y is of categorical type.

        Default is "0", "1", etc.

    categ_names : *tuple, optional*
        A tuple containing strings representing the names of the different
        category levels for each predictor of categorical type.

        Default is "0", "1", etc.

    Notes
    -----
    The method CHAID is appropriate only for categorical or discrete ordered
    predictor variables. Due to Kass ([1]_), CHAID is an acronym for chi-square
    automatic interaction detection. At each node,
    :py:func:`imsl.data_mining.CHAIDDecisionTree` looks for the best splitting
    variable. The approach is as follows: given a predictor variable *X*,
    perform a 2-way chi-squared test of association between each possible pair
    of categories of *X* with the categories of *Y*. The least significant
    result is noted and, if a threshold is met, the two categories of *X* are
    merged. Treating this merged category as a single category, repeat the
    series of tests and determine if there is further merging possible. If a
    merged category consists of three or more of the original categories of
    *X*, :py:func:`imsl.data_mining.CHAIDDecisionTree` calls for a step to test
    whether the merged categories should be split. This is done by forming all
    binary partitions of the merged category and testing each one against *Y*
    in a 2-way test of association. If the most significant result meets a
    threshold, then the merged category is split accordingly. As long as the
    threshold in this step is smaller than the threshold in the merge step, the
    splitting step and the merge step will not cycle back and forth. Once each
    predictor is processed in this manner, the predictor with the most
    significant qualifying 2-way test with *Y* is selected as the splitting
    variable, and its last state of merged categories defines the split at the
    given node. If none of the tests qualify (by having an adjusted p-value
    smaller than a threshold), then the node is not split. This growing
    procedure continues until one or more stopping conditions are met.

    References
    ----------
    .. [1] Kass, G.V. (1980). An Exploratory Technique for Investigating Large
           Quantities of Categorical Data, Applied Statistics, Vol. 29, No. 2,
           pp. 119-127.

    """

    def __init__(self, response_col_idx, var_type, alphas=(0.05, 0.05, -1.0),
                 min_n_node=7, min_split=21, max_x_cats=10, max_size=100,
                 max_depth=10, priors=None, response_name='Y', var_names=None,
                 class_names=None, categ_names=None):
        """Instantiate CHAIDDecisionTree class."""
        method = _CHAID(alphas=alphas)
        _DecisionTree.__init__(self, response_col_idx, var_type, method,
                               min_n_node=min_n_node, min_split=min_split,
                               max_x_cats=max_x_cats, max_size=max_size,
                               max_depth=max_depth, priors=priors,
                               response_name=response_name,
                               var_names=var_names, class_names=class_names,
                               categ_names=categ_names)


class QUESTDecisionTree(_DecisionTree):
    r"""Generate a decision tree using the QUEST method.

    Generate a decision tree for a single response variable and two or more
    predictor variables using the QUEST method.

    Parameters
    ----------
    response_col_idx : *int*
        Column index of the response variable.

    var_type : *(N,) array_like*
        Array indicating the type of each variable.

        .. rst-class:: nowrap

            +----------------+------------------------------------+
            |  `var_type[i]` | Type                               |
            +================+====================================+
            |      0         | Categorical                        |
            +----------------+------------------------------------+
            |      1         | Ordered Discrete (Low, Med., High) |
            +----------------+------------------------------------+
            |      2         | Quantitative or Continuous         |
            +----------------+------------------------------------+
            |      3         | Ignore this variable               |
            +----------------+------------------------------------+

    alpha : *float, optional*
        The significance level for split variable selection. Valid values are
        in the range 0 < alpha < 1.0.

        Default is 0.05.

    min_n_node : *int, optional*
        Do not split a node if one of its child nodes will have fewer than
        min_n_node observations.

        Default is 7.

    min_split : *int, optional*
        Do not split a node if the node has fewer than min_split observations.

        Default is 21.

    max_x_cats : *int, optional*
        Allow for up to max_x_cats for categorical predictor variables.

        Default is 10.

    max_size : *int, optional*
        Stop growing the tree once it has reached max_size number of nodes.

        Default is 100.

    max_depth : *int, optional*
        Stop growing the tree once it has reached max_depth number of levels.

        Default is 10.

    priors : *(N,) array_like, optional*
        An array containing prior probabilities for class membership.  The
        argument is ignored for continuous response variables.  By default, the
        prior probabilities are estimated from the data.

    response_name : *string, optional*
        A string representing the name of the response variable.

        Default is "Y".

    var_names : *tuple, optional*
        A tuple containing strings representing the names of predictors.

        Default is "X0", "X1", etc.

    class_names : *tuple, optional*
        A tuple containing strings representing the names of the different
        classes in Y, assuming Y is of categorical type.

        Default is "0", "1", etc.

    categ_names : *tuple, optional*
        A tuple containing strings representing the names of the different
        category levels for each predictor of categorical type.

        Default is "0", "1", etc.

    Notes
    -----
    The QUEST algorithm ([1]_) is appropriate for a categorical response
    variable and predictors of either categorical or quantitative type. For
    each categorical predictor, :py:func:`imsl.data_mining.QUESTDecisionTree`
    performs a multi-way chi-square test of association between the predictor
    and *Y*. For every continuous predictor,
    :py:func:`imsl.data_mining.QUESTDecisionTree` performs an ANOVA test to see
    if the means of the predictor vary among the groups of *Y*. Among these
    tests, the variable with the most significant result is selected as a
    potential splitting variable, say, :math:`X_j`. If the p-value (adjusted
    for multiple tests) is less than the specified splitting threshold, then
    :math:`X_j` is the splitting variable for the current node. If not,
    :py:func:`imsl.data_mining.QUESTDecisionTree` performs for each continuous
    variable *X* a Levene's test of homogeneity to see if the variance of *X*
    varies within the different groups of *Y*. Among these tests, we again find
    the predictor with the most significant result, say :math:`X_i`. If its
    p-value (adjusted for multiple tests) is less than the splitting threshold,
    :math:`X_i` is the splitting variable. Otherwise, the node is not split.

    Assuming a splitting variable is found, the next step is to determine how
    the variable should be split. If the selected variable :math:`X_j` is
    continuous, a split point *d* is determined by quadratic discriminant
    analysis (QDA) of :math:`X_j` into two populations determined by a binary
    partition of the response *Y*. The goal of this step is to group the
    classes of *Y* into two subsets or super classes, *A* and *B*. If there are
    only two classes in the response *Y*, the super classes are obvious.
    Otherwise, calculate the means and variances of :math:`X_j` in each of the
    classes of *Y*. If the means are all equal, put the largest-sized class
    into group *A* and combine the rest to form group *B*. If they are not all
    equal, use a *k*-means clustering method (*k* = 2) on the class means to
    determine *A* and *B*.

    :math:`X_j` in *A* and in *B* is assumed to be normally distributed with
    estimated means :math:`\bar{x}_{j|A}`, :math:`\bar{x}_{j|B}`, and variances
    :math:`S^2_j|A`, :math:`S^2_j|B`, respectively. The quadratic discriminant
    is the partition :math:`X_j\le d` and :math:`X_j\gt d` such that
    :math:`\mbox{Pr}\left(X_j,A\right)=\mbox{Pr}\left(X_j,B\right)`. The
    discriminant rule assigns an observation to *A* if :math:`x_{ij}\le d` and
    to *B* if :math:`x_{ij}\gt d`. For *d* to maximally discriminate, the
    probabilities must be equal.

    If the selected variable :math:`X_j` is categorical, it is first
    transformed using the method outlined in Loh and Shih ([1]_), and then QDA
    is performed as above. The transformation is related to the discriminant
    coordinate (CRIMCOORD) approach due to Gnanadesikan ([2]_).

    References
    ----------
    .. [1] Loh, W.-Y. and Shih, Y.-S. (1997). Split Selection Methods for
           Classification Trees, *Statistica Sinica*, 7, 815-840. For
           information on the latest version of QUEST see:
           http://www.stat.wisc.edu/~loh/quest.html.
    .. [2] Gnanadesikan, R. (1977). Methods for Statistical Data Analysis of
           Multivariate Observations. Wiley. New York.

    Examples
    --------
    This example applies the QUEST method to a simulated dataset with 50 cases
    and three predictors of mixed-type. A maximally grown tree under the
    default controls and the optimally pruned sub-tree obtained from
    cross-validation and minimal cost complexity pruning are produced. Notice
    that the optimally pruned tree consts of just the root node, whereas the
    maximal tree has five nodes and three levels.

    >>> import numpy as np
    >>> import imsl.data_mining as dm
    >>> xy = np.array([[2.0, 25.928690, 0.0, 0.0],
    ...                [1.0, 51.632450, 1.0, 1.0],
    ...                [1.0, 25.784321, 0.0, 2.0],
    ...                [0.0, 39.379478, 0.0, 3.0],
    ...                [2.0, 24.650579, 0.0, 2.0],
    ...                [2.0, 45.200840, 0.0, 2.0],
    ...                [2.0, 52.679600, 1.0, 3.0],
    ...                [1.0, 44.283421, 1.0, 3.0],
    ...                [2.0, 40.635231, 1.0, 3.0],
    ...                [2.0, 51.760941, 0.0, 3.0],
    ...                [2.0, 26.303680, 0.0, 1.0],
    ...                [2.0, 20.702299, 1.0, 0.0],
    ...                [2.0, 38.742729, 1.0, 3.0],
    ...                [2.0, 19.473330, 0.0, 0.0],
    ...                [1.0, 26.422110, 0.0, 0.0],
    ...                [2.0, 37.059860, 1.0, 0.0],
    ...                [1.0, 51.670429, 1.0, 3.0],
    ...                [0.0, 42.401562, 0.0, 3.0],
    ...                [2.0, 33.900269, 1.0, 2.0],
    ...                [1.0, 35.432819, 0.0, 0.0],
    ...                [1.0, 44.303692, 0.0, 1.0],
    ...                [0.0, 46.723869, 0.0, 2.0],
    ...                [1.0, 46.992619, 0.0, 2.0],
    ...                [0.0, 36.059231, 0.0, 3.0],
    ...                [2.0, 36.831970, 1.0, 1.0],
    ...                [1.0, 61.662571, 1.0, 2.0],
    ...                [0.0, 25.677139, 0.0, 3.0],
    ...                [1.0, 39.085670, 1.0, 0.0],
    ...                [0.0, 48.843410, 1.0, 1.0],
    ...                [1.0, 39.343910, 0.0, 3.0],
    ...                [2.0, 24.735220, 0.0, 2.0],
    ...                [1.0, 50.552509, 1.0, 3.0],
    ...                [0.0, 31.342630, 1.0, 3.0],
    ...                [1.0, 27.157949, 1.0, 0.0],
    ...                [0.0, 31.726851, 0.0, 2.0],
    ...                [0.0, 25.004080, 0.0, 3.0],
    ...                [1.0, 26.354570, 1.0, 3.0],
    ...                [2.0, 38.123428, 0.0, 1.0],
    ...                [0.0, 49.940300, 0.0, 2.0],
    ...                [1.0, 42.457790, 1.0, 3.0],
    ...                [0.0, 38.809479, 1.0, 1.0],
    ...                [0.0, 43.227989, 1.0, 1.0],
    ...                [0.0, 41.876240, 0.0, 3.0],
    ...                [2.0, 48.078201, 0.0, 2.0],
    ...                [0.0, 43.236729, 1.0, 0.0],
    ...                [2.0, 39.412941, 0.0, 3.0],
    ...                [1.0, 23.933460, 0.0, 2.0],
    ...                [2.0, 42.841301, 1.0, 3.0],
    ...                [2.0, 30.406691, 0.0, 1.0],
    ...                [0.0, 37.773891, 0.0, 2.0]])
    >>> response_column_index = 3
    >>> var_type = np.array([0, 2, 0, 0], dtype=int)
    >>> with dm.QUESTDecisionTree(response_column_index,
    ...                           var_type) as decision_tree:
    ...     decision_tree.train(xy)
    ...     print(decision_tree)
    ... #doctest: +NORMALIZE_WHITESPACE
    Decision Tree:
    Node 0: Cost = 0.620, N = 50.0, Level = 0, Child Nodes:  1  2
    P(Y=0) = 0.180
    P(Y=1) = 0.180
    P(Y=2) = 0.260
    P(Y=3) = 0.380
    Predicted Y: 3
       Node 1: Cost = 0.220, N = 17.0, Level = 1
       Rule: X1 <= 35.031
       P(Y=0) = 0.294
       P(Y=1) = 0.118
       P(Y=2) = 0.353
       P(Y=3) = 0.235
       Predicted Y: 2
       Node 2: Cost = 0.360, N = 33.0, Level = 1, Child Nodes:  3  4
       Rule: X1 > 35.031
       P(Y=0) = 0.121
       P(Y=1) = 0.212
       P(Y=2) = 0.212
       P(Y=3) = 0.455
       Predicted Y: 3
          Node 3: Cost = 0.180, N = 19.0, Level = 2
          Rule: X1 <= 43.265
          P(Y=0) = 0.211
          P(Y=1) = 0.211
          P(Y=2) = 0.053
          P(Y=3) = 0.526
          Predicted Y: 3
          Node 4: Cost = 0.160, N = 14.0, Level = 2
          Rule: X1 > 43.265
          P(Y=0) = 0.000
          P(Y=1) = 0.214
          P(Y=2) = 0.429
          P(Y=3) = 0.357
          Predicted Y: 2

    This example uses the dataset Kyphosis. The 81 cases represent 81 children
    who have undergone surgery to correct a type of spinal deformity known as
    Kyphosis. The response variable is the presence or absence of Kyphosis
    after the surgery. Three predictors are: Age of the patient in months;
    Start, the vertebra number where the surgery started; and Number, the
    number of vertebra involved in the surgery. This example uses the method
    QUEST to produce a maximal tree. It also requests predictions for a test
    dataset consisting of 10 "new" cases.

    >>> import numpy as np
    >>> import imsl.data_mining as dm
    >>> xy = np.array([[0.0, 71.0, 3.0, 5.0],
    ...                [0.0, 158.0, 3.0, 14.0],
    ...                [1.0, 128, 4.0, 5.0],
    ...                [0.0, 2.0, 5.0, 1.0],
    ...                [0.0, 1.0, 4.0, 15.0],
    ...                [0.0, 1.0, 2.0, 16.0],
    ...                [0.0, 61.0, 2.0, 17.0],
    ...                [0.0, 37.0, 3.0, 16.0],
    ...                [0.0, 113.0, 2.0, 16.0],
    ...                [1.0, 59.0, 6.0, 12.0],
    ...                [1.0, 82.0, 5.0, 14.0],
    ...                [0.0, 148.0, 3.0, 16.0],
    ...                [0.0, 18.0, 5.0, 2.0],
    ...                [0.0, 1.0, 4.0, 12.0],
    ...                [0.0, 168.0, 3.0, 18.0],
    ...                [0.0, 1.0, 3.0, 16.0],
    ...                [0.0, 78.0, 6.0, 15.0],
    ...                [0.0, 175.0, 5.0, 13.0],
    ...                [0.0, 80.0, 5.0, 16.0],
    ...                [0.0, 27.0, 4.0, 9.0],
    ...                [0.0, 22.0, 2.0, 16.0],
    ...                [1.0, 105.0, 6.0, 5.0],
    ...                [1.0, 96.0, 3.0, 12.0],
    ...                [0.0, 131.0, 2.0, 3.0],
    ...                [1.0, 15.0, 7.0, 2.0],
    ...                [0.0, 9.0, 5.0, 13.0],
    ...                [0.0, 8.0, 3.0, 6.0],
    ...                [0.0, 100.0, 3.0, 14.0],
    ...                [0.0, 4.0, 3.0, 16.0],
    ...                [0.0, 151.0, 2.0, 16.0],
    ...                [0.0, 31.0, 3.0, 16.0],
    ...                [0.0, 125.0, 2.0, 11.0],
    ...                [0.0, 130.0, 5.0, 13.0],
    ...                [0.0, 112.0, 3.0, 16.0],
    ...                [0.0, 140.0, 5.0, 11.0],
    ...                [0.0, 93.0, 3.0, 16.0],
    ...                [0.0, 1.0, 3.0, 9.0],
    ...                [1.0, 52.0, 5.0, 6.0],
    ...                [0.0, 20.0, 6.0, 9.0],
    ...                [1.0, 91.0, 5.0, 12.0],
    ...                [1.0, 73.0, 5.0, 1.0],
    ...                [0.0, 35.0, 3.0, 13.0],
    ...                [0.0, 143.0, 9.0, 3.0],
    ...                [0.0, 61.0, 4.0, 1.0],
    ...                [0.0, 97.0, 3.0, 16.0],
    ...                [1.0, 139.0, 3.0, 10.0],
    ...                [0.0, 136.0, 4.0, 15.0],
    ...                [0.0, 131.0, 5.0, 13.0],
    ...                [1.0, 121.0, 3.0, 3.0],
    ...                [0.0, 177.0, 2.0, 14.0],
    ...                [0.0, 68.0, 5.0, 10.0],
    ...                [0.0, 9.0, 2.0, 17.0],
    ...                [1.0, 139.0, 10.0, 6.0],
    ...                [0.0, 2.0, 2.0, 17.0],
    ...                [0.0, 140.0, 4.0, 15.0],
    ...                [0.0, 72.0, 5.0, 15.0],
    ...                [0.0, 2.0, 3.0, 13.0],
    ...                [1.0, 120.0, 5.0, 8.0],
    ...                [0.0, 51.0, 7.0, 9.0],
    ...                [0.0, 102.0, 3.0, 13.0],
    ...                [1.0, 130.0, 4.0, 1.0],
    ...                [1.0, 114.0, 7.0, 8.0],
    ...                [0.0, 81.0, 4.0, 1.0],
    ...                [0.0, 118.0, 3.0, 16.0],
    ...                [0.0, 118.0, 4.0, 16.0],
    ...                [0.0, 17.0, 4.0, 10.0],
    ...                [0.0, 195.0, 2.0, 17.0],
    ...                [0.0, 159.0, 4.0, 13.0],
    ...                [0.0, 18.0, 4.0, 11.0],
    ...                [0.0, 15.0, 5.0, 16.0],
    ...                [0.0, 158.0, 5.0, 14.0],
    ...                [0.0, 127.0, 4.0, 12.0],
    ...                [0.0, 87.0, 4.0, 16.0],
    ...                [0.0, 206.0, 4.0, 10.0],
    ...                [0.0, 11.0, 3.0, 15.0],
    ...                [0.0, 178.0, 4.0, 15.0],
    ...                [1.0, 157.0, 3.0, 13.0],
    ...                [0.0, 26.0, 7.0, 13.0],
    ...                [0.0, 120.0, 2.0, 13.0],
    ...                [1.0, 42.0, 7.0, 6.0],
    ...                [0.0, 36.0, 4.0, 13.0]])
    >>> xy_test = np.array([[0.0, 71.0, 3.0, 5.0],
    ...                     [1.0, 128.0, 4.0, 5.0],
    ...                     [0.0, 1.0, 4.0, 15.0],
    ...                     [0.0, 61.0, 6.0, 10.0],
    ...                     [0.0, 113.0, 2.0, 16.0],
    ...                     [1.0, 82.0, 5.0, 14.0],
    ...                     [0.0, 148.0, 3.0, 16.0],
    ...                     [0.0, 1.0, 4.0, 12.0],
    ...                     [0.0, 1.0, 3.0, 16.0],
    ...                     [0.0, 175.0, 5.0, 13.0]])
    >>> response_column_index = 0
    >>> var_type = np.array([0, 2, 2, 2], dtype=int)
    >>> names = ["Age", "Number", "Start"]
    >>> class_names = ["Absent", "Present"]
    >>> response_name = "Kyphosis"
    >>> with dm.QUESTDecisionTree(response_column_index, var_type,
    ...                           min_n_node=5, min_split=10, max_x_cats=10,
    ...                           max_size=50, max_depth=10,
    ...                           response_name=response_name, var_names=names,
    ...                           class_names=class_names) as decision_tree:
    ...    decision_tree.train(xy)
    ...    predictions = decision_tree.predict(xy_test)
    ...    print(decision_tree)
    ... #doctest: +NORMALIZE_WHITESPACE
    Decision Tree:
    Node 0: Cost = 0.210, N = 81.0, Level = 0, Child Nodes:  1  4
    P(Y=0) = 0.790
    P(Y=1) = 0.210
    Predicted Kyphosis: Absent
       Node 1: Cost = 0.074, N = 13.0, Level = 1, Child Nodes:  2  3
       Rule: Start <= 5.155
       P(Y=0) = 0.538
       P(Y=1) = 0.462
       Predicted Kyphosis: Absent
          Node 2: Cost = 0.025, N = 7.0, Level = 2
          Rule: Age <= 84.030
          P(Y=0) = 0.714
          P(Y=1) = 0.286
          Predicted Kyphosis: Absent
          Node 3: Cost = 0.025, N = 6.0, Level = 2
          Rule: Age > 84.030
          P(Y=0) = 0.333
          P(Y=1) = 0.667
          Predicted Kyphosis: Present
       Node 4: Cost = 0.136, N = 68.0, Level = 1, Child Nodes:  5  6
       Rule: Start > 5.155
       P(Y=0) = 0.838
       P(Y=1) = 0.162
       Predicted Kyphosis: Absent
          Node 5: Cost = 0.012, N = 6.0, Level = 2
          Rule: Start <= 8.862
          P(Y=0) = 0.167
          P(Y=1) = 0.833
          Predicted Kyphosis: Present
          Node 6: Cost = 0.074, N = 62.0, Level = 2, Child Nodes:  7  12
          Rule: Start > 8.862
          P(Y=0) = 0.903
          P(Y=1) = 0.097
          Predicted Kyphosis: Absent
             Node 7: Cost = 0.062, N = 28.0, Level = 3, Child Nodes:  8  9
             Rule: Start <= 13.092
             P(Y=0) = 0.821
             P(Y=1) = 0.179
             Predicted Kyphosis: Absent
                Node 8: Cost = 0.025, N = 15.0, Level = 4
                Rule: Age <= 91.722
                P(Y=0) = 0.867
                P(Y=1) = 0.133
                Predicted Kyphosis: Absent
                Node 9: Cost = 0.037, N = 13.0, Level = 4, Child Nodes:  10  11
                Rule: Age > 91.722
                P(Y=0) = 0.769
                P(Y=1) = 0.231
                Predicted Kyphosis: Absent
                   Node 10: Cost = 0.037, N = 6.0, Level = 5
                   Rule: Number <= 3.450
                   P(Y=0) = 0.500
                   P(Y=1) = 0.500
                   Predicted Kyphosis: Absent
                   Node 11: Cost = 0.000, N = 7.0, Level = 5
                   Rule: Number > 3.450
                   P(Y=0) = 1.000
                   P(Y=1) = 0.000
                   Predicted Kyphosis: Absent
             Node 12: Cost = 0.012, N = 34.0, Level = 3, Child Nodes:  13  14
             Rule: Start > 13.092
             P(Y=0) = 0.971
             P(Y=1) = 0.029
             Predicted Kyphosis: Absent
                Node 13: Cost = 0.012, N = 5.0, Level = 4
                Rule: Start <= 14.864
                P(Y=0) = 0.800
                P(Y=1) = 0.200
                Predicted Kyphosis: Absent
                Node 14: Cost = 0.000, N = 29.0, Level = 4
                Rule: Start > 14.864
                P(Y=0) = 1.000
                P(Y=1) = 0.000
                Predicted Kyphosis: Absent
    >>> print("\nPredictions for test data:\n")
    ... #doctest: +NORMALIZE_WHITESPACE
    Predictions for test data:
    >>> print("  {:5s} {:8s} {:7s} {:8s}".format(names[0], names[1], names[2],
    ...                                           response_name))
      Age   Number   Start   Kyphosis
    >>> n_rows = xy_test.shape[0]
    >>> for i in range(n_rows):
    ...     idx = int(predictions.predictions[i])
    ...     print("{:5.0f} {:8.0f} {:7.0f}   {}".format(xy_test[i, 1],
    ...                                                 xy_test[i, 2],
    ...                                                 xy_test[i, 3],
    ...                                                 class_names[idx]))
       71        3       5   Absent
      128        4       5   Present
        1        4      15   Absent
       61        6      10   Absent
      113        2      16   Absent
       82        5      14   Absent
      148        3      16   Absent
        1        4      12   Absent
        1        3      16   Absent
      175        5      13   Absent
    >>> print("\nMean squared prediction error: {}".format(
    ...     predictions.pred_err_ss))
    ... #doctest: +NORMALIZE_WHITESPACE
    Mean squared prediction error: 0.1

    """

    def __init__(self, response_col_idx, var_type, alpha=0.05, min_n_node=7,
                 min_split=21, max_x_cats=10, max_size=100, max_depth=10,
                 priors=None, response_name='Y', var_names=None,
                 class_names=None, categ_names=None):
        """Instantiate QUESTDecisionTree class."""
        method = _QUEST(alpha=alpha)
        _DecisionTree.__init__(self, response_col_idx, var_type, method,
                               min_n_node=min_n_node, min_split=min_split,
                               max_x_cats=max_x_cats, max_size=max_size,
                               max_depth=max_depth, priors=priors,
                               response_name=response_name,
                               var_names=var_names, class_names=class_names,
                               categ_names=categ_names)
