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
"""Generate IMSLLib object."""
import ctypes as _ctypes
import os as _os
import sys as _sys
import threading as _threading
import warnings as _warnings

import imsl._constants as _constants
import imsl._structures as _structures
import imsl.error as _error

__all__ = ()

_NOTE = 1
_ALERT = 2
_WARNING = 3
_FATAL = 4
_TERMINAL = 5
_WARNING_IMMEDIATE = 6
_FATAL_IMMEDIATE = 7


def _set_severities(imsllib, type_, value, libtype, *args):
    cargs = []
    for arg in args:
        cargs.append(type_)
        cargs.append(arg)
        cargs.append(value)
    cargs.append(0)

    if libtype == "math":
        imsllib.imsl_error_options(*cargs)
    elif libtype == "stat":
        imsllib.imsls_error_options(*cargs)
    else:
        raise ValueError("input string has value {} which is not"
                         " supported".format(libtype))


_callinfo = _threading.local()


def _error_handler(severity, code, function_name, message):
    messages = _callinfo.__dict__.setdefault('messages', [])
    if severity in (_NOTE, _ALERT, _WARNING, _WARNING_IMMEDIATE):
        msgtype = _error.IMSLWarning
    else:
        msgtype = _error.IMSLError
    msg = msgtype(bytes.decode(message))
    msg._code = code
    msg._internal_function_name = bytes.decode(function_name)
    msg._severity = severity
    messages.append(msg)


def _err_check(result, func, arguments):
    messages = _callinfo.__dict__.setdefault('messages', [])
    _callinfo.messages = []
    for message in messages:
        if message._severity in (_NOTE, _ALERT, _WARNING, _WARNING_IMMEDIATE):
            _warnings.warn(message, stacklevel=3)
        else:
            raise message
    return result


class _IMSLLib(object):
    """Load the CNL library and expose the functions as Python callables."""

    def __init__(self):
        # Store thread local information
        self._thr_local = _threading.local()

        self._imsllib = self._load_library(self._imslcmath_libname,
                                           _os.environ)
        self._imslslib = self._load_library(self._imslcstat_libname,
                                            _os.environ)

        # Set default actions for each warning level.
        _warnings.filterwarnings("always",
                                 category=_error.IMSLWarning,
                                 append=True)
        # For functions that aren't involved in error checking, register an
        # error checking callback.

        self._expose_structures()

        self.expose("imsl_d_lin_sol_gen", None, _err_check, "math")
        self.expose("imsl_z_lin_sol_gen", None, _err_check, "math")
        self.expose("imsl_d_eig_gen", None, _err_check, "math")
        self.expose("imsl_z_eig_gen", None, _err_check, "math")
        self.expose("imsl_d_lin_lsq_lin_constraints", None, _err_check, "math")
        self.expose("imsls_d_cluster_k_means", None, _err_check, "stat")
        self.expose("imsls_d_decision_tree",
                    _ctypes.POINTER(self.imsls_d_decision_tree),
                    _err_check, "stat")
        self.expose("imsls_d_decision_tree_predict", None, _err_check, "stat")
        self.expose("imsls_d_decision_tree_free", None, None, "stat")
        self.expose("imsls_d_garch", None, _err_check, "stat")
        self.expose("imsls_random_seed_set", None, _err_check, "stat")
        self.expose("imsls_d_random_normal", None, _err_check, "stat")
        self.expose("imsls_d_random_uniform", None, _err_check, "stat")
        self.expose("imsls_d_lfcn", None, _err_check, "stat")
        self.expose("imsl_d_sparse_lin_prog", None, _err_check, "math")
        self.expose("imsl_d_read_mps",
                    _ctypes.POINTER(_structures.imsl_d_mps),
                    _err_check, "math")
        self.expose("imsl_d_mps_free", None, _err_check, "math")
        self.expose("imsls_d_logistic_regression", None, _err_check, "stat")
        self.expose("imsls_d_logistic_reg_predict", None, _err_check, "stat")
        self.expose("imsls_d_auto_arima", None, _err_check, "stat")
        self.expose("imsls_d_pls_regression", None, _err_check, "stat")
        self.expose("imsls_d_aggr_apriori", None, _err_check, "stat")
        self.expose("imsls_d_free_apriori_itemsets", None, _err_check, "stat")
        self.expose("imsls_d_free_association_rules", None, _err_check, "stat")
        self.expose("imsls_free", None, None, "stat")

    def enable_callback(self):
        """Enable CNL level tracing in the current thread of execution."""
        if not hasattr(self._thr_local, "print_callback"):
            # Enable printing for all severities in IMSL
            _set_severities(self._imsllib, _constants.IMSL_SET_PRINT, 1,
                            "math", _NOTE, _ALERT, _WARNING, _FATAL,
                            _TERMINAL, _WARNING_IMMEDIATE, _FATAL_IMMEDIATE)

            _set_severities(self._imslslib, _constants.IMSLS_SET_PRINT, 1,
                            "stat", _NOTE, _ALERT, _WARNING, _FATAL,
                            _TERMINAL, _WARNING_IMMEDIATE, _FATAL_IMMEDIATE)

            # Disable stopping for all severities in IMSL (an exception will
            # be thrown in Python for any FATAL, TERMINAL or FATAL_IMMEDIATE
            # errors)
            _set_severities(self._imsllib, _constants.IMSL_SET_STOP, 0,
                            "math", _NOTE, _ALERT, _WARNING, _FATAL,
                            _TERMINAL, _WARNING_IMMEDIATE, _FATAL_IMMEDIATE)

            _set_severities(self._imslslib, _constants.IMSLS_SET_STOP, 0,
                            "stat", _NOTE, _ALERT, _WARNING, _FATAL,
                            _TERMINAL, _WARNING_IMMEDIATE, _FATAL_IMMEDIATE)

            # Register a Python callback function to capture any messages
            # printed by IMSL.
            CBFUNC = _ctypes.CFUNCTYPE(None, _ctypes.c_int, _ctypes.c_long,
                                       _ctypes.c_char_p, _ctypes.c_char_p)
            self._thr_local.print_callback = CBFUNC(_error_handler)

            self._imsllib.imsl_error_options(
                _constants.IMSL_ERROR_PRINT_PROC,
                self._thr_local.print_callback, 0)

            self._imslslib.imsls_error_options(
                _constants.IMSLS_ERROR_PRINT_PROC,
                self._thr_local.print_callback, 0)

    def expose(self, function, restype, errcheck, lib):
        """Expose a function from CNL for use in PyNL.

        Args:
            function: The name of the function to expose.
            restype: The ctypes result type of the function.
            errcheck: A callback function to be invoked after the function
                      completes to determine if any errors occurred.
            lib: A string indicating the CNL library the function is
                 coming from. Use "math" for CNL Math functions and
                 "stat" for CNL Stat functions.
        """
        if lib == "math":
            loadlib = self._imsllib
        elif lib == "stat":
            loadlib = self._imslslib
        else:
            raise ValueError("input string has value {} which is not"
                             " supported".format(lib))

        getattr(loadlib, function).restype = restype

        def err_call(result, func, arguments):
            try:
                return errcheck(result, func, arguments)
            except Exception:
                if result is not None:
                    if function == "imsls_d_decision_tree":
                        loadlib.imsls_d_decision_tree_free(result)
                raise

        if errcheck:
            getattr(loadlib, function).errcheck = err_call

        def invoke(*args, **kwargs):
            self.enable_callback()
            return getattr(loadlib, function)(*args, **kwargs)

        setattr(self, function, invoke)

    def _imsls_version(self):
        self._imslslib.imsls_version.restype = _ctypes.c_char_p
        imsls_version = self._imslslib.imsls_version(
            _constants.IMSLS_LIBRARY_VERSION)
        imsls_version = imsls_version.decode('ascii')

        # The version is the last space-separated component of the
        # returned string.
        imsls_version = imsls_version.split()[-1]
        imsls_version = [int(ver) for ver in imsls_version.split('.')]
        imsls_major_version, imsls_minor_version = imsls_version[0:2]

        return imsls_major_version, imsls_minor_version

    def _expose_structures(self):
        imsls_major_version, imsls_minor_version = self._imsls_version()

        self.imsl_d_mps = _structures.imsl_d_mps
        self.imsl_d_sparse_elem = _structures.imsl_d_sparse_elem
        self.imsls_apriori_items = _structures.imsls_apriori_items
        self.imsls_d_apriori_itemsets = _structures.imsls_d_apriori_itemsets
        self.imsls_d_association_rules = _structures.imsls_d_association_rules
        self.imsls_d_model = _structures.imsls_d_model
        self.imsls_d_rule_components = _structures.imsls_d_rule_components

        if (imsls_major_version >= 2016):
            self.imsls_d_decision_tree = _structures.imsls_d_decision_tree
            self.imsls_d_tree_node = _structures.imsls_d_tree_node
        else:
            self.imsls_d_decision_tree = _structures.imsls_d_decision_tree_v8_6
            self.imsls_d_tree_node = _structures.imsls_d_tree_node_v8_6

    def _load_env(self, varname, env):
        try:
            return env[varname]
        except KeyError:
            ext = {'nt': '.bat',
                   'posix': '.sh'}
            msg = ("Environment variable '{varname}' not found, did you"
                   " run cnlsetup{ext}?")
            raise LookupError(msg.format(varname=varname, ext=ext[_os.name]))

    def _load_library(self, libname, env):
        cnl_dir = self._load_env('CNL_DIR', env)
        lib_arch = self._load_env('LIB_ARCH', env)

        libname = _os.path.join(cnl_dir, lib_arch, 'lib', libname)

        try:
            return _ctypes.cdll.LoadLibrary(libname)
        except OSError as exception:
            if _os.name == 'posix':
                # An error occurred loading the library, likely due to a
                # missing libgomp dependency. Try loading libgomp explicitly,
                # however if this fails, propagate the original failure.
                try:
                    _ctypes.CDLL('libgomp.so.1', _ctypes.RTLD_GLOBAL)
                    return _ctypes.cdll.LoadLibrary(libname)
                except Exception:
                    raise exception
            else:
                raise

    @property
    def _imslcmath_libname(self):
        libname = {'nt': 'imslcmath_imsl_dll.dll',
                   'posix': 'libimslcmath_imsl.so'}
        return libname[_os.name]

    @property
    def _imslcstat_libname(self):
        libname = {'nt': 'imslcstat_imsl_dll.dll',
                   'posix': 'libimslcstat_imsl.so'}
        return libname[_os.name]


_imsllib = _IMSLLib()


def expose_imsl_members(lib):
    module = _sys.modules[__name__]
    for member in dir(lib):
        if member.startswith('imsl'):
            setattr(module, member, getattr(lib, member))


expose_imsl_members(_imsllib)
