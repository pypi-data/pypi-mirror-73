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
"""Exception classes common to all PyNL packages."""


class IMSLError(Exception):
    """Encapsulate an error reported by PyNL.

    Parameters
    ----------
    message : str
        Description of the error.

    Attributes
    ----------
    message : str
        Description of the error.

    """

    def __init__(self, message):
        """Instantiate IMSLError class."""
        self.message = message
        self._code = 0
        self._internal_function_name = ""
        self._severity = 0

    def __str__(self):
        """Return error message string."""
        return "{message}".format(message=self.message)


class IMSLWarning(Warning):
    """
    Encapsulate a warning reported by PyNL.

    Parameters
    ----------
    message : str
        Description of the warning.

    Attributes
    ----------
    message : str
        Description of the warning.

    """

    def __init__(self, message):
        """Instantiate IMSLWarning class."""
        self.message = message
        self._code = 0
        self._internal_function_name = ""
        self._severity = 0

    def __str__(self):
        """Return warning message string."""
        return "{message}".format(message=self.message)
