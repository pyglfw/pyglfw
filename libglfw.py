# coding=utf-8

from ctypes import c_int, c_uint, c_char_p, c_void_p, c_float, c_double, c_ushort, c_ubyte
from ctypes import addressof, cast, py_object, CFUNCTYPE, POINTER, Structure

import sys

from ctypes import cdll

c_void = None
c_func = CFUNCTYPE

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

GLFW_RED_BITS               = 0x00021001
GLFW_GREEN_BITS             = 0x00021002
GLFW_BLUE_BITS              = 0x00021003
GLFW_ALPHA_BITS             = 0x00021004
GLFW_DEPTH_BITS             = 0x00021005
GLFW_STENCIL_BITS           = 0x00021006
GLFW_ACCUM_RED_BITS         = 0x00021007
GLFW_ACCUM_GREEN_BITS       = 0x00021008
GLFW_ACCUM_BLUE_BITS        = 0x00021009
GLFW_ACCUM_ALPHA_BITS       = 0x0002100A
GLFW_AUX_BUFFERS            = 0x0002100B
GLFW_STEREO                 = 0x0002100C
GLFW_SAMPLES                = 0x0002100D
GLFW_SRGB_CAPABLE           = 0x0002100E
GLFW_REFRESH_RATE           = 0x0002100F

GLFW_CLIENT_API             = 0x00022001
GLFW_CONTEXT_VERSION_MAJOR  = 0x00022002
GLFW_CONTEXT_VERSION_MINOR  = 0x00022003
GLFW_CONTEXT_REVISION       = 0x00022004
GLFW_CONTEXT_ROBUSTNESS     = 0x00022005
GLFW_OPENGL_FORWARD_COMPAT  = 0x00022006
GLFW_OPENGL_DEBUG_CONTEXT   = 0x00022007
GLFW_OPENGL_PROFILE         = 0x00022008

GLFW_OPENGL_API             = 0x00030001
GLFW_OPENGL_ES_API          = 0x00030002

GLFW_NO_ROBUSTNESS          =         0
GLFW_NO_RESET_NOTIFICATION  = 0x00031001
GLFW_LOSE_CONTEXT_ON_RESET  = 0x00031002

GLFW_OPENGL_ANY_PROFILE     =         0
GLFW_OPENGL_CORE_PROFILE    = 0x00032001
GLFW_OPENGL_COMPAT_PROFILE  = 0x00032002

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

GLFW_KEY_UNKNOWN            = -1

GLFW_KEY_SPACE              = 32
GLFW_KEY_APOSTROPHE         = 39
GLFW_KEY_COMMA              = 44
GLFW_KEY_MINUS              = 45
GLFW_KEY_PERIOD             = 46
GLFW_KEY_SLASH              = 47
GLFW_KEY_0                  = 48
GLFW_KEY_1                  = 49
GLFW_KEY_2                  = 50
GLFW_KEY_3                  = 51
GLFW_KEY_4                  = 52
GLFW_KEY_5                  = 53
GLFW_KEY_6                  = 54
GLFW_KEY_7                  = 55
GLFW_KEY_8                  = 56
GLFW_KEY_9                  = 57
GLFW_KEY_SEMICOLON          = 59
GLFW_KEY_EQUAL              = 61
GLFW_KEY_A                  = 65
GLFW_KEY_B                  = 66
GLFW_KEY_C                  = 67
GLFW_KEY_D                  = 68
GLFW_KEY_E                  = 69
GLFW_KEY_F                  = 70
GLFW_KEY_G                  = 71
GLFW_KEY_H                  = 72
GLFW_KEY_I                  = 73
GLFW_KEY_J                  = 74
GLFW_KEY_K                  = 75
GLFW_KEY_L                  = 76
GLFW_KEY_M                  = 77
GLFW_KEY_N                  = 78
GLFW_KEY_O                  = 79
GLFW_KEY_P                  = 80
GLFW_KEY_Q                  = 81
GLFW_KEY_R                  = 82
GLFW_KEY_S                  = 83
GLFW_KEY_T                  = 84
GLFW_KEY_U                  = 85
GLFW_KEY_V                  = 86
GLFW_KEY_W                  = 87
GLFW_KEY_X                  = 88
GLFW_KEY_Y                  = 89
GLFW_KEY_Z                  = 90
GLFW_KEY_LEFT_BRACKET       = 91
GLFW_KEY_BACKSLASH          = 92
GLFW_KEY_RIGHT_BRACKET      = 93
GLFW_KEY_GRAVE_ACCENT       = 96
GLFW_KEY_WORLD_1            = 161
GLFW_KEY_WORLD_2            = 162

GLFW_KEY_ESCAPE             = 256
GLFW_KEY_ENTER              = 257
GLFW_KEY_TAB                = 258
GLFW_KEY_BACKSPACE          = 259
GLFW_KEY_INSERT             = 260
GLFW_KEY_DELETE             = 261
GLFW_KEY_RIGHT              = 262
GLFW_KEY_LEFT               = 263
GLFW_KEY_DOWN               = 264
GLFW_KEY_UP                 = 265
GLFW_KEY_PAGE_UP            = 266
GLFW_KEY_PAGE_DOWN          = 267
GLFW_KEY_HOME               = 268
GLFW_KEY_END                = 269
GLFW_KEY_CAPS_LOCK          = 280
GLFW_KEY_SCROLL_LOCK        = 281
GLFW_KEY_NUM_LOCK           = 282
GLFW_KEY_PRINT_SCREEN       = 283
GLFW_KEY_PAUSE              = 284
GLFW_KEY_F1                 = 290
GLFW_KEY_F2                 = 291
GLFW_KEY_F3                 = 292
GLFW_KEY_F4                 = 293
GLFW_KEY_F5                 = 294
GLFW_KEY_F6                 = 295
GLFW_KEY_F7                 = 296
GLFW_KEY_F8                 = 297
GLFW_KEY_F9                 = 298
GLFW_KEY_F10                = 299
GLFW_KEY_F11                = 300
GLFW_KEY_F12                = 301
GLFW_KEY_F13                = 302
GLFW_KEY_F14                = 303
GLFW_KEY_F15                = 304
GLFW_KEY_F16                = 305
GLFW_KEY_F17                = 306
GLFW_KEY_F18                = 307
GLFW_KEY_F19                = 308
GLFW_KEY_F20                = 309
GLFW_KEY_F21                = 310
GLFW_KEY_F22                = 311
GLFW_KEY_F23                = 312
GLFW_KEY_F24                = 313
GLFW_KEY_F25                = 314
GLFW_KEY_KP_0               = 320
GLFW_KEY_KP_1               = 321
GLFW_KEY_KP_2               = 322
GLFW_KEY_KP_3               = 323
GLFW_KEY_KP_4               = 324
GLFW_KEY_KP_5               = 325
GLFW_KEY_KP_6               = 326
GLFW_KEY_KP_7               = 327
GLFW_KEY_KP_8               = 328
GLFW_KEY_KP_9               = 329
GLFW_KEY_KP_DECIMAL         = 330
GLFW_KEY_KP_DIVIDE          = 331
GLFW_KEY_KP_MULTIPLY        = 332
GLFW_KEY_KP_SUBTRACT        = 333
GLFW_KEY_KP_ADD             = 334
GLFW_KEY_KP_ENTER           = 335
GLFW_KEY_KP_EQUAL           = 336
GLFW_KEY_LEFT_SHIFT         = 340
GLFW_KEY_LEFT_CONTROL       = 341
GLFW_KEY_LEFT_ALT           = 342
GLFW_KEY_LEFT_SUPER         = 343
GLFW_KEY_RIGHT_SHIFT        = 344
GLFW_KEY_RIGHT_CONTROL      = 345
GLFW_KEY_RIGHT_ALT          = 346
GLFW_KEY_RIGHT_SUPER        = 347
GLFW_KEY_MENU               = 348
GLFW_KEY_LAST               = GLFW_KEY_MENU

GLFW_CONNECTED              = 0x00040001
GLFW_DISCONNECTED           = 0x00040002


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
else:
    lib = cdll.LoadLibrary('libglfw.so.3')

_declare = _DeclareFunction(lib, c_func)

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
    glfwSetErrorCallback(ShowError)

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

    glfwDestroyWindow(window)

    glfwTerminate()

