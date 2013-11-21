# coding=utf-8

import sys

if sys.version_info.major < 3:
    unistr = unicode
else:
    unistr = str

import threading

local = threading.local()
local.error = None

def _error_check(func):
    def wrap(*args, **kwargs):
        result = func(*args, **kwargs)
        err, local.error = local.error, None
        if err:
            raise err
        return result
    return wrap

import libglfw as api

for name in api.all_functions:
    setattr(api, name, _error_check(getattr(api, name)))

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
    if str is unistr:
        message = message.decode()
    local.error = _error_map.get(code, RuntimeError)(message)

api.glfwSetErrorCallback(_error_raise)

def _utf(obj):
    if isinstance(obj, unistr):
        obj = obj.encode()
    return obj

def _str(obj):
    if isinstance(obj, bytes) and not isinstance(obj, str):
        obj = obj.decode()
    return obj


class Mice(object):
    def __init__(self, handle):
        self.handle = handle

    def __getitem__(self, index):
        return bool(api.glfwGetMouseButton(self.handle, index))

    @property
    def left(self):
        return self[0]

    @property
    def right(self):
        return self[1]

    @property
    def middle(self):
        return self[2]


class Keys(object):
    def __init__(self, handle):
        self.handle = handle

    def __getitem__(self, index):
        return bool(api.glfwGetKey(self.handle, index))

    @property
    def escape(self):
        return self[api.GLFW_KEY_ESCAPE]

class Window(object):
    _instance_ = {}

    def __init__(self, width, height, title, monitor=None, shared=None):
        self.handle = api.glfwCreateWindow(width, height, _utf(title), monitor, shared).get_void_p()
        self.__class__._instance_[self.handle.value] = self

        self.mice = Mice(self.handle)
        self.keys = Keys(self.handle)

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

    def swap_interval(self):
        raise NotImplementedError()

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
    def monitor(self):
        mon_handle = api.glfwGetWindowMonitor(self.handle)
        if bool(mon_handle):
            raise NotImplementedError()
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



def init():
    return bool(api.glfwInit())

def terminate():
    api.glfwTerminate()

def api_version():
    return api.glfwGetVersion()

def api_version_string():
    return _str(api.glfwGetVersionString())

def poll_events():
    api.glfwPollEvents()

def wait_events():
    api.glfwWaitEvents()


if __name__ == '__main__':
    init()

    w = Window(800, 600, api_version_string())
    w.make_current()

    while not w.should_close:
        w.swap_buffers()
        poll_events()

        if w.keys.escape:
            w.should_close = True

    terminate()