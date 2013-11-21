# coding=utf-8

from ctypes import c_int, c_uint, c_char_p, c_void_p, c_float, c_double, c_ushort, c_ubyte
from ctypes import addressof, cast, py_object, CFUNCTYPE, POINTER, Structure

import sys

from ctypes import cdll as dll

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


_declare = _DeclareFunction(dll.glfw3, c_func)

# ---- ret/arg helper functions ----

class object_p(c_void_p):
    @classmethod
    def from_param(cls, obj):
        return id(obj)

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

# ---- constant definitions ----

GLFW_NOT_INITIALIZED        = 0x00010001
GLFW_NO_CURRENT_CONTEXT     = 0x00010002
GLFW_INVALID_ENUM           = 0x00010003
GLFW_INVALID_VALUE          = 0x00010004
GLFW_OUT_OF_MEMORY          = 0x00010005
GLFW_API_UNAVAILABLE        = 0x00010006
GLFW_VERSION_UNAVAILABLE    = 0x00010007
GLFW_PLATFORM_ERROR         = 0x00010008
GLFW_FORMAT_UNAVAILABLE     = 0x00010009

GLFW_FOCUSED                = 0x00020001
GLFW_ICONIFIED              = 0x00020002
GLFW_RESIZABLE              = 0x00020003
GLFW_VISIBLE                = 0x00020004
GLFW_DECORATED              = 0x00020005

GLFW_CURSOR                 = 0x00033001
GLFW_STICKY_KEYS            = 0x00033002
GLFW_STICKY_MOUSE_BUTTONS   = 0x00033003

GLFW_CURSOR_NORMAL          = 0x00034001
GLFW_CURSOR_HIDDEN          = 0x00034002
GLFW_CURSOR_DISABLED        = 0x00034003

GLFW_MOUSE_BUTTON_1         = 0
GLFW_MOUSE_BUTTON_2         = 1
GLFW_MOUSE_BUTTON_3         = 2
GLFW_MOUSE_BUTTON_4         = 3
GLFW_MOUSE_BUTTON_5         = 4
GLFW_MOUSE_BUTTON_6         = 5
GLFW_MOUSE_BUTTON_7         = 6
GLFW_MOUSE_BUTTON_8         = 7
GLFW_MOUSE_BUTTON_LAST      = GLFW_MOUSE_BUTTON_8
GLFW_MOUSE_BUTTON_LEFT      = GLFW_MOUSE_BUTTON_1
GLFW_MOUSE_BUTTON_RIGHT     = GLFW_MOUSE_BUTTON_2
GLFW_MOUSE_BUTTON_MIDDLE    = GLFW_MOUSE_BUTTON_3

GLFW_KEY_ESCAPE = 256

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

# ---- callback prototypes ----

GLFWerrorfun            = c_func(c_void,    c_int, c_char_p)
GLFWwindowposfun        = c_func(c_void,    GLFWwindowP, c_int, c_int)
GLFWwindowsizefun       = c_func(c_void,    GLFWwindowP, c_int, c_int)
GLFWwindowclosefun      = c_func(c_void,    GLFWwindowP)
GLFWwindowrefreshfun    = c_func(c_void,    GLFWwindowP)
GLFWwindowfocusfun      = c_func(c_void,    GLFWwindowP, c_int)
GLFWwindowiconifyfun    = c_func(c_void,    GLFWwindowP)
GLFWframebuffersizefun  = c_func(c_void,    GLFWwindowP, c_int, c_int)
GLFWmousebuttonfun      = c_func(c_void,    GLFWwindowP, c_int, c_int, c_int)
GLFWcursorposfun        = c_func(c_void,    GLFWwindowP, c_double, c_double)
GLFWcursorenterfun      = c_func(c_void,    GLFWwindowP, c_int)
GLFWscrollfun           = c_func(c_void,    GLFWwindowP, c_double, c_double)
GLFWkeyfun              = c_func(c_void,    GLFWwindowP, c_int, c_int, c_int, c_int)
GLFWcharfun             = c_func(c_void,    GLFWwindowP, c_uint)
GLFWmonitorfun          = c_func(c_void,    GLFWmonitorP, c_int)

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
_declare('glfwGetGammaRamp', (GLFWgammarampP, ret_addr_p), GLFWmonitorP)
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

all_functions = list(_declare.dir.keys())

for func in all_functions:
    setattr(sys.modules[__name__], func, _declare.dir[func])

if __name__ == '__main__':
    @GLFWkeyfun
    def InputKey(window, key, scancode, action, mods):
        print(window, key, scancode, action, mods)

    def show_error(code, message):
        print(code, message)

    ShowError = GLFWerrorfun(show_error)
    print(glfwSetErrorCallback(ShowError))

    if not glfwInit():
        raise RuntimeError()

    print(glfwGetVersionString().decode())

    bestmode = 0, 0, None

    monitors = glfwGetMonitors()
    for monitor in monitors:
        vidmodes = glfwGetVideoModes(monitor)
        for vidmode in vidmodes:
            if (vidmode.height * vidmode.width) > bestmode[0] * bestmode[1]:
                bestmode = vidmode.width, vidmode.height, monitor


    glfwSetGamma(monitors[0], -1.0)
    gammar = glfwGetGammaRamp(monitors[0])
    glfwSetGammaRamp(monitors[0], gammar)

    window = glfwCreateWindow(800, 600, "Привет, Мир!".encode(), None, None)
    #window = glfwCreateWindow(bestmode[0], bestmode[1], "Привет, Мир!", monitor, None)
    if not window:
        glfwTerminate()
        raise SystemExit()

    glfwMakeContextCurrent(window)

    glfwSetClipboardString(window, "Тест".encode())
    print(glfwGetClipboardString(window).decode())

    glfwSwapInterval(1)

    size = glfwGetFramebufferSize(window)
    glfwSetWindowUserPointer(window, size)
    fps, was = 0, glfwGetTime()

    print(addressof(glfwSetKeyCallback(window, InputKey)))

    while not glfwWindowShouldClose(window):
        glfwSwapBuffers(window)

        fps, now = fps + 1, glfwGetTime()
        if now - was >= 1.0:
            # print (fps)
            fps, was = 0, now

        glfwPollEvents()

        if glfwGetKey(window, GLFW_KEY_ESCAPE):
            glfwSetWindowShouldClose(window, True)

    print (glfwGetWindowUserPointer(window))

    glfwDestroyWindow(window)

    glfwTerminate()

