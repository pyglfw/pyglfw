# coding=utf-8
###############################################################################
#
#  This file is part of pyglfw project which is subject to zlib license.
#  See the LICENSE file for details.
#
#  Copyright (c) 2013   Roman Valov <roman.valov@gmail.com>
#
###############################################################################

from ctypes import c_int, c_uint, c_char_p, c_void_p
from ctypes import c_float, c_double, c_ushort, c_ubyte
from ctypes import cast, py_object, CFUNCTYPE, POINTER, Structure

c_void = None
c_func = CFUNCTYPE

# ---- definition helper factory ----


class DeclareFunction(object):
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

        signature = name, self.lib
        func = self.fun(restype, *argtypes)(signature, tuple(paramflags))
        if errcheck:
            func.errcheck = errcheck

        self.dir[name] = func


# ---- ret/arg helper functions ----


class object_p(c_void_p):
    @classmethod
    def from_param(cls, obj):
        return c_void_p(id(obj))


def ret_object(obj, func, args):
    return cast(obj, py_object).value


def ret_list_p(icount):
    def sz_array_p(obj, func, args):
        return [obj[i] for i in range(args[icount].value)]
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


def ret_ramp_p(obj, func, args):
    _gramp = obj.contents
    return (
        [_gramp.red[i]     for i in range(_gramp.size)],
        [_gramp.green[i]   for i in range(_gramp.size)],
        [_gramp.blue[i]    for i in range(_gramp.size)],
    )


def cast_from_tuple(func):
    def ramp_from_param(cls, obj):
        if not (len(obj[0]) == len(obj[1]) == len(obj[2])):
            raise ValueError("Object must be tuple of 3 same size sequences")

        size = len(obj[0])

        red =   (c_ushort * size)(*obj[0])
        green = (c_ushort * size)(*obj[1])
        blue =  (c_ushort * size)(*obj[2])

        obj = GLFWgammaramp(size=size, red=red, green=green, blue=blue)

        return func(obj)
    return ramp_from_param


def _RAMPPTR(cls):
    cls = POINTER(cls)
    cls.from_param = classmethod(cast_from_tuple(cls.from_param))
    return cls


# ---- datatype definitions ----


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


GLFWgammarampP = _RAMPPTR(GLFWgammaramp)


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
