# coding=utf-8
###############################################################################
#
#  This file is part of pyglfw project which is subject to zlib license.
#  See the LICENSE file for details.
#
#  Copyright (c) 2013   Roman Valov <roman.valov@gmail.com>
#
###############################################################################

import threading

_local = threading.local()


def _error_check(func):
    def wrap(*args, **kwargs):
        _local.error = None
        result = func(*args, **kwargs)
        err, _local.error = _local.error, None
        if err:
            raise err
        return result
    return wrap

from sys import modules as _sys_modules

from ..libapi import *
from ..libapi import _all_functions

for _func_ in _all_functions:
    setattr(_sys_modules[__name__], _func_,
            _error_check(_all_functions[_func_]))

from .errors import *

_error_map = {
    GLFW_NOT_INITIALIZED:     NotInitializedError,
    GLFW_NO_CURRENT_CONTEXT:  NoCurrentContextError,
    GLFW_INVALID_ENUM:        GLFWInvalidEnumError,
    GLFW_INVALID_VALUE:       GLFWInvalidValueError,
    GLFW_OUT_OF_MEMORY:       GLFWOutOfMemoryError,
    GLFW_API_UNAVAILABLE:     ApiUnavailableError,
    GLFW_VERSION_UNAVAILABLE: VersionUnavailableError,
    GLFW_PLATFORM_ERROR:      PlatformError,
    GLFW_FORMAT_UNAVAILABLE:  FormatUnavailableError,
}


@GLFWerrorfun
def _error_raise(code, message):
    if bytes is not str:
        message = message.decode()
    _local.error = _error_map.get(code, RuntimeError)(message)

glfwSetErrorCallback(_error_raise)
