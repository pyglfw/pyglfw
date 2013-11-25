# coding=utf-8

import sys

if sys.version_info.major < 3:
    _unistr = unicode
else:
    _unistr = str
    xrange = range

import threading

_local = threading.local()
_local.error = None

def _error_check(func):
    def wrap(*args, **kwargs):
        result = func(*args, **kwargs)
        err, _local.error = _local.error, None
        if err:
            raise err
        return result
    return wrap

import libglfw as api

for _name in api.all_functions:
    setattr(api, _name, _error_check(getattr(api, _name)))

class NotInitializedError(Exception): pass
class NoCurrentContextError(Exception): pass
class _InvalidEnumError(ValueError): pass
class _InvalidValueError(ValueError): pass
class _OutOfMemoryError(MemoryError): pass
class ApiUnavailableError(Exception): pass
class VersionUnavailableError(Exception): pass
class PlatformError(Exception): pass
class FormatUnavailableError(Exception): pass
    
_error_map = {
              api.GLFW_NOT_INITIALIZED :        NotInitializedError,
              api.GLFW_NO_CURRENT_CONTEXT :     NoCurrentContextError,
              api.GLFW_INVALID_ENUM :           _InvalidEnumError,
              api.GLFW_INVALID_VALUE :          _InvalidValueError,
              api.GLFW_OUT_OF_MEMORY :          _OutOfMemoryError,
              api.GLFW_API_UNAVAILABLE :        ApiUnavailableError,
              api.GLFW_VERSION_UNAVAILABLE :    VersionUnavailableError,
              api.GLFW_PLATFORM_ERROR :         PlatformError,
              api.GLFW_FORMAT_UNAVAILABLE :     FormatUnavailableError,
              }

@api.GLFWerrorfun
def _error_raise(code, message):
    if str is _unistr:
        message = message.decode()
    _local.error = _error_map.get(code, RuntimeError)(message)

api.glfwSetErrorCallback(_error_raise)

def _utf(obj):
    if isinstance(obj, _unistr):
        obj = obj.encode()
    return obj

def _str(obj):
    if isinstance(obj, bytes) and not isinstance(obj, str):
        obj = obj.decode()
    return obj


class Mice(object):
    def __init__(self, handle):
        self.handle = handle
        self.ntotal = api.GLFW_MOUSE_BUTTON_LAST + 1

    def __len__(self):
        return (self.ntotal)

    def __getitem__(self, index):
        if isinstance(index, int):
            if (index < 0):
                index += self.ntotal
            elif (index >= self.ntotal):
                raise IndexError("Index %i is out of range" % index)

            return bool(api.glfwGetMouseButton(self.handle, index))
        elif isinstance(index, slice):
            return [ self[i] for i in xrange(*index.indices(self.ntotal)) ]
        else:
            raise TypeError("Index %i is not supported" % index)

    LEFT = api.GLFW_MOUSE_BUTTON_LEFT

    @property
    def left(self):
        return self[api.GLFW_MOUSE_BUTTON_LEFT]

    RIGHT = api.GLFW_MOUSE_BUTTON_RIGHT

    @property
    def right(self):
        return self[api.GLFW_MOUSE_BUTTON_RIGHT]

    MIDDLE = api.GLFW_MOUSE_BUTTON_MIDDLE

    @property
    def middle(self):
        return self[api.GLFW_MOUSE_BUTTON_MIDDLE]


class _Keys(object):
    def __init__(self, handle):
        self.handle = handle

    def __getitem__(self, index):
        if isinstance(index, int):
            return bool(api.glfwGetKey(self.handle, index))

def _keyattrs_():
    _keyattribs_ = {}
    _key_prefix_ = 'GLFW_KEY_'
    _key_prelen_ = len(_key_prefix_)

    for name, item in vars(api).items():
        if name.startswith(_key_prefix_):
            _name_ = name[_key_prelen_:]
            if _name_[0] in [ '0', '1', '2', '3', '4', '5', '6', '7', '8', '9' ]:
                _name_ = 'NUM_' + _name_
            _name_ = _name_.upper()
            _prop_ = _name_.lower()

            _keyattribs_[_name_] = item
            if _prop_ == 'last' or _prop_ == 'unknown':
                continue
            _keyattribs_[_prop_] = property(lambda self, item=item: self[item])

    return _keyattribs_


Keys = type('Keys', (_Keys,), _keyattrs_())

class Joystick(object):
    def __init__(self, joyidx):
        self.joyidx = joyidx

    def __nonzero__(self):
        return bool(api.glfwJoystickPresent(self.joyidx))

    def __bool__(self):
        return bool(api.glfwJoystickPresent(self.joyidx))

    @property
    def name(self):
        return _str(api.glfwGetJoystickName(self.joyidx))

    @property
    def axes(self):
        return api.glfwGetJoystickAxes(self.joyidx)

    @property
    def buttons(self):
        return api.glfwGetJoystickButtons(self.joyidx)


class Monitor(object):
    _instance_ = []

    def __eq__(self, other):
        return self.handle == other.handle

    def __ne__(self, other):
        return not (self == other)

    @api.GLFWmonitorfun
    def _monitor_callback(_monitor, _event):
        monobj = super(Monitor, Monitor).__new__(Monitor)
        monobj.handle = _monitor.get_void_p()

        if _event == api.GLFW_DISCONNECTED:
            Monitor._instance_.remove(monobj)
        elif _event == api.GLFW_CONNECTED:
            Monitor._instance_ += [ monobj ]
        else:
            raise ValueError("Unknown monitor event")

    def __new__(cls, monidx):
        if not cls._instance_:
            for midx, _moni_ in enumerate(api.glfwGetMonitors()):
                monobj = super(Monitor, cls).__new__(cls)
                monobj.handle = _moni_.get_void_p()

                cls._instance_ += [ monobj ]

            api.glfwSetMonitorCallback(cls._monitor_callback)

        return cls._instance_[monidx]


    @property
    def pos(self):
        return api.glfwGetMonitorPos(self.handle)

    @property
    def name(self):
        return _str(api.glfwGetMonitorName(self.handle))

    @property
    def physical_size(self):
        return api.glfwGetMonitorPhysicalSize(self.handle)

    @property
    def video_mode(self):
        _vidmode = api.glfwGetVideoMode(self.handle)
        return _vidmode.width, _vidmode.height, (_vidmode.redBits, _vidmode.greenBits, _vidmode.blueBits), _vidmode.refreshRate

    @property
    def video_modes(self):
        _vidmodes = api.glfwGetVideoModes(self.handle)
        return [ (vm.width, vm.height, (vm.redBits, vm.greenBits, vm.blueBits), vm.refreshRate) for vm in _vidmodes ]

    def set_gamma(self, gamma):
        api.glfwSetGamma(self.handle, gamma)

    @property
    def gamma_ramp(self):
        return api.glfwGetGammaRamp(self.handle)

    @gamma_ramp.setter
    def gamma_ramp(self, rgb_ramp):
        api.glfwSetGammaRamp(self.handle, rgb_ramp)


class Window(object):
    _instance_ = {}
    _contexts_ = []

    def __init__(self, width, height, title, monitor=None, shared=None):
        mon_handle = monitor and monitor.handle or None
        shr_handle = shared and shared.handle or None

        self.handle = api.glfwCreateWindow(width, height, _utf(title), mon_handle, shr_handle).get_void_p()
        self.__class__._instance_[self.handle.value] = self

        self.mice = Mice(self.handle)
        self.keys = Keys(self.handle)

    def __enter__(self):
        api.glfwMakeContextCurrent(self.handle)
        self.__class__._contexts_ += [ self ]
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        _ctx = self.__class__._contexts_ and self.__class__._contexts_.pop().handle
        api.glfwMakeContextCurrent(_ctx)
        return False

    def make_current(self):
        api.glfwMakeContextCurrent(self.handle)

    @classmethod
    def find_current(cls):
        find_handle = api.glfwGetCurrentContext().get_void_p()
        if bool(find_handle):
            return cls._instance_.get(find_handle.value)
        else:
            return None

    def close(self):
        api.glfwDestroyWindow(self.handle)

    @property
    def should_close(self):
        return bool(api.glfwWindowShouldClose(self.handle))

    @should_close.setter
    def should_close(self, flag):
        api.glfwSetWindowShouldClose(self.handle, flag)

    def swap_buffers(self):
        api.glfwSwapBuffers(self.handle)

    def swap_interval(self, interval):
        with self:
            api.glfwSwapInterval(interval)

    def set_title(self, title):
        api.glfwSetWindowTitle(self.handle, title)

    @property
    def fbsize(self):
        return api.glfwGetFramebufferSize(self.handle)

    @property
    def pos(self):
        return api.glfwGetWindowPos(self.handle)

    @pos.setter
    def pos(self, x_y):
        api.glfwSetWindowPos(self.handle, *x_y)

    @property
    def size(self):
        return api.glfwGetWindowSize(self.handle)

    @size.setter
    def size(self, x_y):
        api.glfwSetWindowSize(self.handle, *x_y)

    def iconify(self):
        api.glfwIconityWindow(self.handle)

    def restore(self):
        api.glfwRestoreWindow(self.handle)

    @property
    def iconified(self):
        return bool(api.glfwGetWindowAttrib(self.handle, api.GLFW_ICONIFIED))

    @iconified.setter
    def iconified(self, flag):
        if flag:
            self.iconify()
        else:
            self.restore()

    def hide(self):
        api.glfwHideWindow(self.handle)

    def show(self):
        api.glfwShowWindow(self.handle)

    @property
    def visible(self):
        return bool(api.glfwGetWindowAttrib(self.handle, api.GLFW_VISIBLE))

    @visible.setter
    def visible(self, flag):
        if flag:
            self.show()
        else:
            self.hide()

    @property
    def has_focus(self):
        return bool(api.glfwGetWindowAttrib(self.handle, api.GLFW_FOCUSED))

    @property
    def resizable(self):
        return bool(api.glfwGetWindowAttrib(self.handle, api.GLFW_RESIZABLE))

    @property
    def decorated(self):
        return bool(api.glfwGetWindowAttrib(self.handle, api.GLFW_DECORATED))

    @property
    def context_version(self):
        return (
                api.glfwGetWindowAttrib(self.handle, api.GLFW_CONTEXT_VERSION_MAJOR),
                api.glfwGetWindowAttrib(self.handle, api.GLFW_CONTEXT_VERSION_MINOR),
                api.glfwGetWindowAttrib(self.handle, api.GLFW_CONTEXT_REVISION),
               )

    @property
    def debug_context(self):
        return bool(api.glfwGetWindowAttrib(self.handle, api.GLFW_OPENGL_DEBUG_CONTEXT))

    @property
    def forward_compat(self):
        return bool(api.glfwGetWindowAttrib(self.handle, api.GLFW_OPENGL_FORWARD_COMPAT))

    OPENGL_API = api.GLFW_OPENGL_API
    OPENGL_ES_API = api.GLFW_OPENGL_ES_API

    @property
    def client_api(self):
        return api.glfwGetWindowAttrib(self.handle, api.GLFW_CLIENT_API)

    CORE_PROFILE = api.GLFW_OPENGL_CORE_PROFILE
    COMPAT_PROFILE = api.GLFW_OPENGL_COMPAT_PROFILE
    ANY_PROFILE = api.GLFW_OPENGL_ANY_PROFILE

    @property
    def opengl_profile(self):
        return api.glfwGetWindowAttrib(self.handle, api.GLFW_OPENGL_PROFILE)

    NO_ROBUSTNESS = api.GLFW_NO_ROBUSTNESS
    NO_RESET_NOTIFICATION = api.GLFW_NO_RESET_NOTIFICATION
    LOSE_CONTEXT_ON_RESET = api.GLFW_LOSE_CONTEXT_ON_RESET

    @property
    def context_robustness(self):
        return api.glfwGetWindowAttrib(self.handle, api.GLFW_CONTEXT_ROBUSTNESS)

    @staticmethod
    def hint(hints=None, no_defaults=False, **kwargs):
        if hints and kwargs:
            raise ValueError("Hints should be passed via object or via kwargs")

        if not hints:
            hints = Hints(**kwargs)

        if not hints._hints or not no_defaults:
            api.glfwDefaultWindowHints()

        for hint, value in hints._hints.items():
            api.glfwWindowHint(hint, value)

    @property
    def monitor(self):
        _monitor = api.glfwGetWindowMonitor(self.handle)
        if bool(_monitor):
            monobj = super(Monitor, Monitor).__new__(Monitor)
            monobj.handle = _monitor.get_void_p()
            return monobj
        else:
            return None

    @property
    def clipboard(self):
        return _str(api.glfwGetClipboardString(self.handle))

    @clipboard.setter
    def clipboard(self, buffer):
        api.glfwSetClipboardString(self.handler, _utf(buffer))

    _cursor_modes_get = {
                            api.GLFW_CURSOR_DISABLED : None,
                            api.GLFW_CURSOR_HIDDEN : False,
                            api.GLFW_CURSOR_NORMAL : True,
                        }

    _cursor_modes_set = {
                            None : api.GLFW_CURSOR_DISABLED,
                            False : api.GLFW_CURSOR_HIDDEN,
                            True : api.GLFW_CURSOR_NORMAL,
                        }

    @property
    def cursor_mode(self):
        return self._cursor_modes_get.get(api.glfwGetInputMode(self.handle, api.GLFW_CURSOR), None)

    @cursor_mode.setter
    def cursor_mode(self, mode):
        api.glfwSetInputMode(self.handle, api.GLFW_CURSOR, self._cursor_modes_set.get(mode, None))

    @property
    def sticky_keys(self):
        return bool(api.glfwGetInputMode(self.handle, api.GLFW_STICKY_KEYS))

    @sticky_keys.setter
    def sticky_keys(self, flag):
        api.glfwSetInputMode(self.handle, api.GLFW_STICKY_KEYS, flag)

    @property
    def sticky_mice(self):
        return bool(api.glfwGetInputMode(self.handle, api.GLFW_STICKY_MOUSE_BUTTONS))

    @sticky_mice.setter
    def sticky_mice(self, flag):
        api.glfwSetInputMode(self.handle, api.GLFW_STICKY_MOUSE_BUTTONS, flag)


    @property
    def cursor_pos(self):
        return api.glfwGetCursorPos(self.handle)

    @cursor_pos.setter
    def cursor_pos(self, x_y):
        api.glfwSetCursorPos(self.handle, *x_y)


    @classmethod
    def _callback(cls, functype, func):
        if not func:
            return None
        def wrap(handle, *args, **kwargs):
            window = cls._instance_.get(handle.get_void_p().value, None)
            func(window, *args, **kwargs)
        return functype(wrap)


class _HintsBase(object):
    _hint_map_ = {
                    'resizable' :           api.GLFW_RESIZABLE,
                    'visible' :             api.GLFW_VISIBLE,
                    'decorated' :           api.GLFW_DECORATED,
                    'red_bits' :            api.GLFW_RED_BITS,
                    'green_bits' :          api.GLFW_GREEN_BITS,
                    'blue_bits' :           api.GLFW_BLUE_BITS,
                    'alpha_bits' :          api.GLFW_ALPHA_BITS,
                    'depth_bits' :          api.GLFW_DEPTH_BITS,
                    'stencil_bits' :        api.GLFW_STENCIL_BITS,
                    'accum_red_bits' :      api.GLFW_ACCUM_RED_BITS,
                    'accum_green_bits' :    api.GLFW_ACCUM_GREEN_BITS,
                    'accum_blue_bits' :     api.GLFW_ACCUM_BLUE_BITS,
                    'accum_alpha_bits' :    api.GLFW_ACCUM_ALPHA_BITS,
                    'aux_buffers' :         api.GLFW_AUX_BUFFERS,
                    'samples' :             api.GLFW_SAMPLES,
                    'refresh_rate' :        api.GLFW_REFRESH_RATE,
                    'stereo' :              api.GLFW_STEREO,
                    'srgb_capable' :        api.GLFW_SRGB_CAPABLE,
                    'client_api' :          api.GLFW_CLIENT_API,
                    'context_ver_major' :   api.GLFW_CONTEXT_VERSION_MAJOR,
                    'context_ver_minor' :   api.GLFW_CONTEXT_VERSION_MINOR,
                    'context_robustness' :  api.GLFW_CONTEXT_ROBUSTNESS,
                    'debug_context' :       api.GLFW_OPENGL_DEBUG_CONTEXT,
                    'forward_compat' :      api.GLFW_OPENGL_FORWARD_COMPAT,
                    'opengl_profile' :      api.GLFW_OPENGL_PROFILE,

                 }

    _over_map_ = {
                    'context_version' :     (
                                                api.GLFW_CONTEXT_VERSION_MAJOR,
                                                api.GLFW_CONTEXT_VERSION_MINOR,
                                            ),

                    'rgba_bits' :           (
                                                api.GLFW_RED_BITS,
                                                api.GLFW_GREEN_BITS,
                                                api.GLFW_BLUE_BITS,
                                                api.GLFW_ALPHA_BITS,
                                            ),

                    'rgba_accum_bits' :     (
                                                api.GLFW_ACCUM_RED_BITS,
                                                api.GLFW_ACCUM_GREEN_BITS,
                                                api.GLFW_ACCUM_BLUE_BITS,
                                                api.GLFW_ACCUM_ALPHA_BITS,
                                            ),
                }

    def __init__(self, **kwargs):
        self._hints = {}

        for k,v in kwargs.items():
            if k in self.__class__._hint_map_ or k in self.__class__._over_map_:
                setattr(self, k, v)

    def __getitem__(self, index):
        if index in self.__class__._hint_map_.values():
            return self._hints.get(index, None)
        else:
            raise TypeError()

    def __setitem__(self, index, value):
        if index in self.__class__._hint_map_.values():
            if value is None:
                if index in self._hints:
                    del self._hints[index]
            elif isinstance(value, int):
                self._hints[index] = value
        else:
            raise TypeError()

    def __delitem__(self, index):
        if index in self.__class__._hint_map_.values():
            if index in self._hints:
                del self._hints[index]
        else:
            raise TypeError()


def _hntprops_(hint_map, over_map):
    prop_map = {}

    def _hint_property(hint):
        def _get(self):
            return self[hint]
        def _set(self, value):
            self[hint] = value
        def _del(self):
            del self[hint]

        return property(_get, _set, _del)

    for prop, hint in hint_map.items():
        prop_map[prop] = _hint_property(hint)

    def _over_property(over):
        def _get(self):
            value = [ self[hint] for hint in over ]
            return tuple(value)
        def _set(self, value):
            for hint, v in zip(over, value):
                self[hint] = v
        def _del(self):
            for hint in over:
                del self[hint]

        return property(_get, _set, _del)

    for prop, over in over_map.items():
        prop_map[prop] = _over_property(over)

    return prop_map


Hints = type('Hints', (_HintsBase,), _hntprops_(_HintsBase._hint_map_, _HintsBase._over_map_))



class glfw(object):
    def __init__(self):
        raise TypeError("Objects of this class cannot be created")

    api_version = api.glfwGetVersionString()
    api_verinfo = api.glfwGetVersion()

    @staticmethod
    def init():
        return bool(api.glfwInit())

    @staticmethod
    def terminate():
        api.glfwTerminate()

    @staticmethod
    def poll_events():
        api.glfwPollEvents()

    @staticmethod
    def wait_events():
        api.glfwWaitEvents()

    @staticmethod
    def get_time():
        return api.glfwGetTime()

    @staticmethod
    def set_time(nsec):
        api.glfwSetTime(nsec)


if __name__ == '__main__':
    glfw.init()

    Window.hint(context_version=(3,2))

    w = Window(800, 600, glfw.api_version)
    w.make_current()

    print(w.context_version)

    k = w.keys

    while not w.should_close:
        w.swap_buffers()
        glfw.poll_events()

        if k.escape:
            w.should_close = True

    glfw.terminate()