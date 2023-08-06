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
"""Module containing PyNL constants.

The following user-accessible named PyNL constants are defined:

+----------------------+----------------------------------------------+
|  Constant            | Meaning                                      |
+======================+==============================================+
| AIC                  |  Akaike's information criterion              |
+----------------------+----------------------------------------------+
| AICC                 |  Akaike's Corrected Information Criterion    |
+----------------------+----------------------------------------------+
| BIC                  |  Bayesian Information Criterion              |
+----------------------+----------------------------------------------+
| UNBOUNDED_ABOVE      |  No upper bound                              |
+----------------------+----------------------------------------------+
| UNBOUNDED_BELOW      |  No lower bound                              |
+----------------------+----------------------------------------------+
"""
UNBOUNDED_ABOVE = 1.0e30
UNBOUNDED_BELOW = -1.0e30
AIC = 0
AICC = 1
BIC = 2
