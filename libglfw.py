# coding=utf-8

import ctypes

# features:
#   - u_char_p: transparently pass bytes, str and unicode objects to functions expecting "const char *"
#   - u_char_p: transparently receive str from functions returning "const char *"
#   - define: transparently define outparam functions without wrapper
#   - define: transparently define functions in specific namespace

from ctypes import c_int, c_char_p, c_void_p, c_float, c_double, c_ushort, POINTER, Structure

import sys

if sys.version_info[0] < 3:
    uni_str = unicode
else:
    uni_str = str

class u_char_p(ctypes.c_char_p):
    @classmethod
    def from_param(cls, obj):
        if isinstance(obj, uni_str):
            obj = obj.encode()
        return ctypes.c_char_p(obj)

def ret_char_p(obj, func, args):
    if str is uni_str:
        obj = obj.decode()
    return obj

class object_p(ctypes.c_void_p):
    @classmethod
    def from_param(cls, obj):
        return id(obj)

def ret_object(obj, func, args):
    return ctypes.cast(obj, ctypes.py_object).value

def ret_list_p(icount):
    def sz_array_p(obj, func, args):
        return [ obj[i] for i in range(args[icount].value) ]
    return sz_array_p

def ret_addr_p(obj, func, args):
    return obj.contents

c_void = None
func = ctypes.CFUNCTYPE

_glfw = ctypes.windll.glfw3

class Define(object):
    def __init__(self, lib, functype, export=None):
        self.lib = lib
        self.fun = functype

        if export is None: export = sys.modules[__name__]
        self.exp = export

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

        setattr(self.exp, name, func)


class GLFWwindow(Structure):
    pass

GLFWwindowP = POINTER(GLFWwindow)

class GLFWmonitor(Structure):
    pass

GLFWmonitorP = POINTER(GLFWmonitor)

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


# ---- function definition ----

define = Define(_glfw, func)

# common
define('glfwInit', c_int)
define('glfwTerminate')

define('glfwGetVersion', c_void, (POINTER(c_int),), (POINTER(c_int),), (POINTER(c_int),))
define('glfwGetVersionString', (c_char_p, ret_char_p))

define('glfwExtensionSupported', c_int, u_char_p)
define('glfwGetProcAddress', c_void_p, u_char_p)

define('glfwGetTime', c_double)
define('glfwSetTime', c_void, c_double)

define('glfwGetClipboardString', (c_char_p, ret_char_p), GLFWwindowP)
define('glfwSetClipboardString', c_void, GLFWwindowP, u_char_p)

# screen

define('glfwGetPrimaryMonitor', GLFWmonitorP)
define('glfwGetMonitorName', (c_char_p, ret_char_p), GLFWmonitorP)
define('glfwGetMonitorPos', c_void, GLFWmonitorP, (POINTER(c_int),), (POINTER(c_int),))
define('glfwGetMonitorPhysicalSize', c_void, GLFWmonitorP, (POINTER(c_int),), (POINTER(c_int),))

define('glfwGetMonitors', (POINTER(GLFWmonitorP), ret_list_p(0)), (POINTER(c_int),))
define('glfwGetVideoMode', (GLFWvidmodeP, ret_addr_p), GLFWmonitorP)
define('glfwGetVideoModes', (GLFWvidmodeP, ret_list_p(1)), c_void_p, (POINTER(c_int),))

define('glfwSetGamma', c_void, GLFWmonitorP, c_float)
define('glfwGetGammaRamp', (GLFWgammarampP, ret_addr_p), GLFWmonitorP)
define('glfwSetGammaRamp', c_void, GLFWmonitorP, GLFWgammarampP)


# window
define('glfwCreateWindow', GLFWwindowP, c_int, c_int, u_char_p, c_void_p, c_void_p)
define('glfwDestroyWindow', GLFWwindowP)
define('glfwMakeContextCurrent', c_void, GLFWwindowP)
define('glfwGetCurrentContext', GLFWwindowP)
define('glfwWindowShouldClose', c_int, GLFWwindowP)
define('glfwSetWindowShouldClose', c_void, GLFWwindowP, c_int)
define('glfwSwapBuffers', c_void, GLFWwindowP)
define('glfwSwapInterval', c_void, c_int)

define('glfwGetFramebufferSize', c_void, GLFWwindowP, (POINTER(c_int),), (POINTER(c_int),))

define('glfwSetWindowUserPointer', c_void, GLFWwindowP, object_p)
define('glfwGetWindowUserPointer', (c_void_p, ret_object), GLFWwindowP)

# events
define('glfwGetKey', c_int, GLFWwindowP, c_int)
define('glfwPollEvents')

# cbfunc

GLFWerrorfun = func(c_void, c_int, c_char_p)

class GLFWerrorfunP(object):
    _wrapback_ = None

    @classmethod
    def from_param(cls, obj):
        #wrapback = None
        if not obj:
            cls._wrapback_ = None
        elif callable(obj):
            def wrap_cbfun(code, message):
                if str is uni_str:
                    message = message.decode()
                return obj(code, message)
            cls._wrapback_ = GLFWerrorfun(wrap_cbfun)
        else:
            cls._wrapback_ = GLFWerrorfun(obj)
        return cls._wrapback_

define('glfwSetErrorCallback', GLFWerrorfun, GLFWerrorfunP)

GLFWkeyfun = func(c_void, GLFWwindowP, c_int, c_int, c_int, c_int)

class GLFWkeyfunP(object):
    _wrapback_ = None

    @classmethod
    def from_param(cls, obj):
        print(cls)
        if not obj:
            cls._wrapback_ = None
        elif isinstance(obj, GLFWkeyfun):
            cls._wrapback_ = obj
        elif callable(obj):
            cls._wrapback_ = GLFWkeyfun(obj)
            print(cls._wrapback_)
        else:
            cls._wrapback_ = GLFWkeyfun(obj)
        return cls._wrapback_

define('glfwSetKeyCallback', GLFWkeyfun, GLFWwindowP, GLFWkeyfunP)

GLFW_KEY_ESCAPE = 256

def InputKey(window, key, scancode, action, mods):
    print(window, key, scancode, action, mods)

def ShowError(code, message):
    print(code, message)

if __name__ == '__main__':
    glfwSetErrorCallback(ShowError)


    #print(glfwSetErrorCallback(None))
    #print(glfwSetErrorCallback(None))

    if not glfwInit():
        raise RuntimeError()

    print(glfwGetVersionString())

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

    window = glfwCreateWindow(800, 600, "Привет, Мир!", None, None)
    #window = glfwCreateWindow(bestmode[0], bestmode[1], "Привет, Мир!", monitor, None)
    if not window:
        glfwTerminate()
        raise SystemExit()

    glfwMakeContextCurrent(window)

    glfwSetClipboardString(window, "Тест")
    print(glfwGetClipboardString(window))


    print('WGL_EXT_swap_control', glfwExtensionSupported('WGL_EXT_swap_control'), glfwGetProcAddress('wglSwapIntervalEXT'))
    print('GLX_MESA_swap_control', glfwExtensionSupported('GLX_MESA_swap_control'), glfwGetProcAddress('glXSwapIntervalMESA'))

    glfwSwapInterval(1)

    size = glfwGetFramebufferSize(window)
    glfwSetWindowUserPointer(window, size)
    fps, was = 0, glfwGetTime()

    glfwSetKeyCallback(window, InputKey)

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
    print (glfwSetKeyCallback(window, None))

    glfwDestroyWindow(window)

    glfwTerminate()

