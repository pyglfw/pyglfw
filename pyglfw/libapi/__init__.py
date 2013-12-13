# coding=utf-8

from ctypes import c_int, c_uint, c_char_p, c_void_p, c_float, c_double, c_ushort, c_ubyte
from ctypes import addressof, cast, py_object, CFUNCTYPE, POINTER, Structure

import sys

from ctypes import cdll

from .constant import *

c_void = None
c_func = CFUNCTYPE

# ---- definition helper factory ----

class _DeclareFunction(object):
    def __init__(self, lib, functype):
        self.lib = lib
        self.fun = functype
        self.dir = {}

    def __call__(self, name, restype=c_void, *argtypes):

        errcheck = None
        if isinstance(restype, (list, tuple)):
            errcheck = restype[1]
            restype = restype[0]

        paramflags = list(argtypes)
        argtypes = list(argtypes)
        for idx, arg in enumerate(argtypes):
            if isinstance(arg, (list, tuple)):
                argtypes[idx] = arg[0]
                paramflags[idx] = arg[1:] and arg[1:] or (2,)
            else:
                argtypes[idx] = arg
                paramflags[idx] = (1,)


        func = self.fun(restype, *argtypes)((name, self.lib), tuple(paramflags))
        if errcheck: func.errcheck = errcheck

        self.dir[name] = func

if sys.platform == 'win32':
    lib = cdll.glfw3
elif sys.platform == 'darwin':
    lib = cdll.LoadLibrary('libglfw3.dylib')
else:
    lib = cdll.LoadLibrary('libglfw.so.3')

_declare = _DeclareFunction(lib, c_func)

# ---- ret/arg helper functions ----

class object_p(c_void_p):
    @classmethod
    def from_param(cls, obj):
        return c_void_p(id(obj))

def ret_object(obj, func, args):
    return cast(obj, py_object).value

def ret_list_p(icount):
    def sz_array_p(obj, func, args):
        return [ obj[i] for i in range(args[icount].value) ]
    return sz_array_p

def ret_addr_p(obj, func, args):
    return obj.contents

def allow_void_p_param(func):
    def cast_from_void_p(cls, obj):
        if isinstance(obj, c_void_p):
            return cast(obj, cls)
        elif not obj:
            return None
        else:
            return func(obj)
    return cast_from_void_p

def get_void_p(obj):
    return cast(obj, c_void_p)

def _POINTER(cls):
    cls = POINTER(cls)
    cls.from_param = classmethod(allow_void_p_param(cls.from_param))
    cls.get_void_p = get_void_p
    return cls

def _FUNCPTR(cls):
    cls.from_param = classmethod(allow_void_p_param(cls.from_param))
    cls.get_void_p = get_void_p
    return cls

# ---- structure definitions ----

class GLFWwindow(Structure):
    pass

GLFWwindowP = _POINTER(GLFWwindow)

class GLFWmonitor(Structure):
    pass

GLFWmonitorP = _POINTER(GLFWmonitor)

class GLFWvidmode(Structure):
    _fields_ = [
                ("width",       c_int),
                ("height",      c_int),
                ("redBits",     c_int),
                ("greenBits",   c_int),
                ("blueBits",    c_int),
                ("refreshRate", c_int),
               ]

GLFWvidmodeP = POINTER(GLFWvidmode)

class GLFWgammaramp(Structure):
    _fields_ = [
                ("red",     POINTER(c_ushort)),
                ("green",   POINTER(c_ushort)),
                ("blue",    POINTER(c_ushort)),
                ("size",    c_int)
               ]

GLFWgammarampP = POINTER(GLFWgammaramp)

def ret_ramp_p(obj, func, args):
    _gramp = obj.contents
    return (
                [ _gramp.red[i]     for i in range(_gramp.size) ],
                [ _gramp.green[i]   for i in range(_gramp.size) ],
                [ _gramp.blue[i]    for i in range(_gramp.size) ],
           )

def cast_from_tuple(func):
    def ramp_from_param(cls, obj):
        if not (len(obj[0]) == len(obj[1]) == len(obj[2])):
            raise ValueError("Object must be tuple of three equal-length sequences")

        size = len(obj[0])

        red =   (c_ushort * size)(*obj[0])
        green = (c_ushort * size)(*obj[1])
        blue =  (c_ushort * size)(*obj[2])

        obj = GLFWgammaramp(size=size, red=red, green=green, blue=blue)

        return func(obj)
    return ramp_from_param

GLFWgammarampP.from_param = classmethod(cast_from_tuple(GLFWgammarampP.from_param))

# ---- callback prototypes ----

GLFWerrorfun            = _FUNCPTR(c_func(c_void,    c_int, c_char_p))
GLFWwindowposfun        = _FUNCPTR(c_func(c_void,    GLFWwindowP, c_int, c_int))
GLFWwindowsizefun       = _FUNCPTR(c_func(c_void,    GLFWwindowP, c_int, c_int))
GLFWwindowclosefun      = _FUNCPTR(c_func(c_void,    GLFWwindowP))
GLFWwindowrefreshfun    = _FUNCPTR(c_func(c_void,    GLFWwindowP))
GLFWwindowfocusfun      = _FUNCPTR(c_func(c_void,    GLFWwindowP, c_int))
GLFWwindowiconifyfun    = _FUNCPTR(c_func(c_void,    GLFWwindowP, c_int))
GLFWframebuffersizefun  = _FUNCPTR(c_func(c_void,    GLFWwindowP, c_int, c_int))
GLFWmousebuttonfun      = _FUNCPTR(c_func(c_void,    GLFWwindowP, c_int, c_int, c_int))
GLFWcursorposfun        = _FUNCPTR(c_func(c_void,    GLFWwindowP, c_double, c_double))
GLFWcursorenterfun      = _FUNCPTR(c_func(c_void,    GLFWwindowP, c_int))
GLFWscrollfun           = _FUNCPTR(c_func(c_void,    GLFWwindowP, c_double, c_double))
GLFWkeyfun              = _FUNCPTR(c_func(c_void,    GLFWwindowP, c_int, c_int, c_int, c_int))
GLFWcharfun             = _FUNCPTR(c_func(c_void,    GLFWwindowP, c_uint))
GLFWmonitorfun          = _FUNCPTR(c_func(c_void,    GLFWmonitorP, c_int))

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
_declare('glfwGetVideoModes', (GLFWvidmodeP, ret_list_p(1)), c_void_p, (POINTER(c_int),))

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

_all_functions = list(_declare.dir.keys())

for _func_ in _all_functions:
    setattr(sys.modules[__name__], _func_, _declare.dir[_func_])

