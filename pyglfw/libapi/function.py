# coding=utf-8
###############################################################################
#
#  This file is part of pyglfw project which is subject to zlib license.
#  See the LICENSE file for details.
#
#  Copyright (c) 2013   Roman Valov <roman.valov@gmail.com>
#
###############################################################################

import sys

from ctypes import cdll

from .c_helper import *

if sys.platform == 'win32':
    _lib = cdll.glfw3
elif sys.platform == 'darwin':
    _lib = cdll.LoadLibrary('libglfw3.dylib')
else:
    _lib = cdll.LoadLibrary('libglfw.so.3')

_declare = DeclareFunction(_lib, c_func)

# ---- function definition ----

# ==== common ====

_declare('glfwInit', c_int)
_declare('glfwTerminate')
_declare('glfwGetVersion', c_void, (POINTER(c_int),), (POINTER(c_int),), (POINTER(c_int),))
_declare('glfwGetVersionString', c_char_p)
_declare('glfwSetErrorCallback', GLFWerrorfun, GLFWerrorfun)

_declare('glfwExtensionSupported', c_int, c_char_p)
_declare('glfwGetProcAddress', c_void_p, c_char_p)

_declare('glfwGetTime', c_double)
_declare('glfwSetTime', c_void, c_double)

_declare('glfwGetClipboardString', c_char_p, GLFWwindowP)
_declare('glfwSetClipboardString', c_void, GLFWwindowP, c_char_p)

# ==== screen ====

_declare('glfwGetMonitors', (POINTER(GLFWmonitorP), ret_list_p(0)), (POINTER(c_int),))
_declare('glfwGetPrimaryMonitor', GLFWmonitorP)
_declare('glfwGetMonitorPos', c_void, GLFWmonitorP, (POINTER(c_int),), (POINTER(c_int),))
_declare('glfwGetMonitorPhysicalSize', c_void, GLFWmonitorP, (POINTER(c_int),), (POINTER(c_int),))
_declare('glfwGetMonitorName', c_char_p, GLFWmonitorP)
_declare('glfwSetMonitorCallback', GLFWmonitorfun, GLFWmonitorfun)

_declare('glfwGetVideoMode', (GLFWvidmodeP, ret_addr_p), GLFWmonitorP)
_declare('glfwGetVideoModes', (GLFWvidmodeP, ret_list_p(1)), GLFWmonitorP, (POINTER(c_int),))

_declare('glfwSetGamma', c_void, GLFWmonitorP, c_float)
_declare('glfwGetGammaRamp', (GLFWgammarampP, ret_ramp_p), GLFWmonitorP)
_declare('glfwSetGammaRamp', c_void, GLFWmonitorP, GLFWgammarampP)

# ==== window ====

_declare('glfwCreateWindow', GLFWwindowP, c_int, c_int, c_char_p, c_void_p, c_void_p)
_declare('glfwDestroyWindow', c_void, GLFWwindowP)
_declare('glfwMakeContextCurrent', c_void, GLFWwindowP)
_declare('glfwGetCurrentContext', GLFWwindowP)
_declare('glfwSwapBuffers', c_void, GLFWwindowP)
_declare('glfwSwapInterval', c_void, c_int)

_declare('glfwDefaultWindowHints', c_void)
_declare('glfwWindowHint', c_void, c_int, c_int)
_declare('glfwGetWindowMonitor', GLFWmonitorP, GLFWwindowP)
_declare('glfwGetWindowAttrib', c_int, GLFWwindowP, c_int)
_declare('glfwWindowShouldClose', c_int, GLFWwindowP)
_declare('glfwSetWindowShouldClose', c_void, GLFWwindowP, c_int)
_declare('glfwSetWindowUserPointer', c_void, GLFWwindowP, object_p)
_declare('glfwGetWindowUserPointer', (c_void_p, ret_object), GLFWwindowP)

_declare('glfwSetWindowTitle', c_void, GLFWwindowP, c_char_p)
_declare('glfwGetWindowPos', c_void, GLFWwindowP, (POINTER(c_int),), (POINTER(c_int),))
_declare('glfwSetWindowPos', c_void, GLFWwindowP, c_int, c_int)
_declare('glfwGetWindowSize', c_void, GLFWwindowP, (POINTER(c_int),), (POINTER(c_int),))
_declare('glfwSetWindowSize', c_void, GLFWwindowP, c_int, c_int)
_declare('glfwGetFramebufferSize', c_void, GLFWwindowP, (POINTER(c_int),), (POINTER(c_int),))

_declare('glfwIconifyWindow', c_void, GLFWwindowP)
_declare('glfwRestoreWindow', c_void, GLFWwindowP)
_declare('glfwShowWindow', c_void, GLFWwindowP)
_declare('glfwHideWindow', c_void, GLFWwindowP)

_declare('glfwSetWindowPosCallback', GLFWwindowposfun, GLFWwindowP, GLFWwindowposfun)
_declare('glfwSetWindowSizeCallback', GLFWwindowsizefun, GLFWwindowP, GLFWwindowsizefun)
_declare('glfwSetWindowCloseCallback', GLFWwindowclosefun, GLFWwindowP, GLFWwindowclosefun)
_declare('glfwSetWindowRefreshCallback', GLFWwindowrefreshfun, GLFWwindowP, GLFWwindowrefreshfun)
_declare('glfwSetWindowFocusCallback', GLFWwindowfocusfun, GLFWwindowP, GLFWwindowfocusfun)
_declare('glfwSetWindowIconifyCallback', GLFWwindowiconifyfun, GLFWwindowP, GLFWwindowiconifyfun)
_declare('glfwSetFramebufferSizeCallback', GLFWframebuffersizefun, GLFWwindowP, GLFWframebuffersizefun)

# ==== events ====

_declare('glfwPollEvents', c_void)
_declare('glfwWaitEvents', c_void)

_declare('glfwGetInputMode', c_int, GLFWwindowP, c_int)
_declare('glfwSetInputMode', c_void, GLFWwindowP, c_int, c_int)

_declare('glfwGetKey', c_int, GLFWwindowP, c_int)
_declare('glfwGetMouseButton', c_int, GLFWwindowP, c_int)
_declare('glfwGetCursorPos', c_void, GLFWwindowP, (POINTER(c_double),), (POINTER(c_double),))
_declare('glfwSetCursorPos', c_void, GLFWwindowP, c_double, c_double)

_declare('glfwJoystickPresent', c_int, c_int)
_declare('glfwGetJoystickAxes', (POINTER(c_float), ret_list_p(1)), c_int, (POINTER(c_int),))
_declare('glfwGetJoystickButtons', (POINTER(c_ubyte), ret_list_p(1)), c_int, (POINTER(c_int),))
_declare('glfwGetJoystickName', c_char_p, c_int)

_declare('glfwSetKeyCallback', GLFWkeyfun, GLFWwindowP, GLFWkeyfun)
_declare('glfwSetCharCallback', GLFWcharfun, GLFWwindowP, GLFWcharfun)
_declare('glfwSetMouseButtonCallback', GLFWmousebuttonfun, GLFWwindowP, GLFWmousebuttonfun)
_declare('glfwSetCursorPosCallback', GLFWcursorposfun, GLFWwindowP, GLFWcursorposfun)
_declare('glfwSetCursorEnterCallback', GLFWcursorenterfun, GLFWwindowP, GLFWcursorenterfun)
_declare('glfwSetScrollCallback', GLFWscrollfun, GLFWwindowP, GLFWscrollfun)
