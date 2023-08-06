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
"""Structures needed by PyNL."""

from ctypes import POINTER, Structure, c_char, c_char_p, c_double, c_int

# CNL Version <= 8.6 Structures


class imsls_d_tree_node_v8_6 (Structure):
    """Class for Decision Tree node structure."""

    _fields_ = [('node_id', c_int),
                ('parent_id', c_int),
                ('node_var_id', c_int),
                ('n_children', c_int),
                ('children_ids', POINTER(c_int)),
                ('node_values_ind', POINTER(c_int)),
                ('node_prob', POINTER(c_double)),
                ('cost', c_double),
                ('y_probs', POINTER(c_double)),
                ('predicted_val', c_double),
                ('n_cases', c_double),
                ('surrogate_info', POINTER(c_double)),
                ('predicted_class', c_int),
                ('node_split_value', c_double)]


class imsls_d_decision_tree_v8_6 (Structure):
    """Class for Decision Tree structure."""

    _fields_ = [('n_levels', c_int),
                ('n_nodes', c_int),
                ('response_type', c_int),
                ('pred_type', POINTER(c_int)),
                ('pred_n_values', POINTER(c_int)),
                ('n_classes', c_int),
                ('n_preds', c_int),
                ('n_surrogates', c_int),
                ('terminal_nodes', POINTER(c_int)),
                ('nodes', POINTER(imsls_d_tree_node_v8_6))]

# Current CNL Structures


class imsl_d_sparse_elem (Structure):
    """Class for triplet structure."""

    _fields_ = [
        ('row', c_int),
        ('col', c_int),
        ('val', c_double)]


class imsl_d_mps (Structure):
    """Class for MPS structure."""

    _fields_ = [
        ('filename', c_char_p),
        ('name', c_char * 9),
        ('nrows', c_int),
        ('ncolumns', c_int),
        ('nonzeros', c_int),
        ('nhessian', c_int),
        ('ninteger', c_int),
        ('nbinary', c_int),
        ('objective', POINTER(c_double)),
        ('constraint', POINTER(imsl_d_sparse_elem)),
        ('hessian', POINTER(imsl_d_sparse_elem)),
        ('lower_range', POINTER(c_double)),
        ('upper_range', POINTER(c_double)),
        ('lower_bound', POINTER(c_double)),
        ('upper_bound', POINTER(c_double)),
        ('variable_type', POINTER(c_int)),
        ('name_objective', c_char * 9),
        ('name_rhs', c_char * 9),
        ('name_ranges', c_char * 9),
        ('name_bounds', c_char * 9),
        ('name_row', POINTER(c_char_p)),
        ('name_column', POINTER(c_char_p)),
        ('positive_infinity', c_double),
        ('negative_infinity', c_double),
        ('objective_constant', c_double)]


class imsls_d_tree_node (Structure):
    """Class for Decision Tree node structure."""

    _fields_ = [('node_id', c_int),
                ('parent_id', c_int),
                ('node_var_id', c_int),
                ('n_children', c_int),
                ('children_ids', POINTER(c_int)),
                ('node_values_ind', POINTER(c_int)),
                ('n_cases', c_int),
                ('node_prob', POINTER(c_double)),
                ('cost', c_double),
                ('y_probs', POINTER(c_double)),
                ('predicted_val', c_double),
                ('n_cases', c_double),
                ('surrogate_info', POINTER(c_double)),
                ('predicted_class', c_int),
                ('node_split_value', c_double)]


class imsls_d_decision_tree (Structure):
    """Class for Decision Tree structure."""

    _fields_ = [('n_levels', c_int),
                ('n_nodes', c_int),
                ('response_type', c_int),
                ('pred_type', POINTER(c_int)),
                ('pred_n_values', POINTER(c_int)),
                ('n_classes', c_int),
                ('n_preds', c_int),
                ('n_surrogates', c_int),
                ('terminal_nodes', POINTER(c_int)),
                ('nodes', POINTER(imsls_d_tree_node))]


class imsls_d_model (Structure):
    """Class for logistic regression model structure."""

    _fields_ = [('n_obs', c_int),
                ('n_updates', c_int),
                ('n_coefs', c_int),
                ('loglike', c_double),
                ('meany', POINTER(c_double)),
                ('coefs', POINTER(c_double)),
                ('stderrs', POINTER(c_double)),
                ('hess', POINTER(c_double)),
                ('grad', POINTER(c_double))]


class imsls_apriori_items(Structure):
    """Class for Apriori items."""

    _fields_ = [('n_items', c_int),
                ('items', POINTER(c_int)),
                ('support', c_int)]


class imsls_d_apriori_itemsets(Structure):
    """Class for Apriori itemsets."""

    _fields_ = [('n_itemsets', c_int),
                ('itemsets', POINTER(imsls_apriori_items)),
                ('n_trans', c_int),
                ('max_num_products', c_int),
                ('max_set_size', c_int),
                ('min_pct_support', c_double)]


class imsls_d_rule_components (Structure):
    """Class for Apriori association rules components."""

    _fields_ = [('n_x', c_int),
                ('x', POINTER(c_int)),
                ('n_y', c_int),
                ('y', POINTER(c_int)),
                ('support', c_int * 3),
                ('confidence', c_double),
                ('lift', c_double)]


class imsls_d_association_rules (Structure):
    """Class for Apriori association rules."""

    _fields_ = [('n_rules', c_int),
                ('rules', POINTER(imsls_d_rule_components))]
