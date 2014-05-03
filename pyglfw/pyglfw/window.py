# coding=utf-8
###############################################################################
#
#  This file is part of pyglfw project which is subject to zlib license.
#  See the LICENSE file for details.
#
#  Copyright (c) 2013   Roman Valov <roman.valov@gmail.com>
#
###############################################################################

from . import _wrapapi as api
from .common import _str, _utf, _unichr
from .hint import Hints
from .inputs import Keys, Mice
from .monitor import _monitor_obj
from threading import local


class Window(object):
    _instance_ = {}
    _contexts_ = local()

    def __init__(self, width, height, title, monitor=None, shared=None):
        mon_handle = monitor and monitor.handle or None
        shr_handle = shared and shared.handle or None
        win_handle = api.glfwCreateWindow(width, height, _utf(title),
                                          mon_handle, shr_handle)

        self.handle = win_handle.get_void_p()
        self.__class__._instance_[self.handle.value] = self

        self.mice = Mice(self.handle)
        self.keys = Keys(self.handle)

        self._key_callback = None
        self._char_callback = None
        self._scroll_callback = None
        self._cursor_enter_callback = None
        self._cursor_pos_callback = None
        self._mouse_button_callback = None

        self._window_pos_callback = None
        self._window_size_callback = None
        self._window_close_callback = None
        self._window_refresh_callback = None
        self._window_focus_callback = None
        self._window_iconify_callback = None
        self._framebuffer_size_callback = None

    def __enter__(self):
        if not hasattr(Window._contexts_, 'ctxstack'):
            Window._contexts_.ctxstack = []
        Window._contexts_.ctxstack += [self.find_current()]

        api.glfwMakeContextCurrent(self.handle)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if not Window._contexts_.ctxstack:
            raise RuntimeError('Corrupted context stack')

        _ctx = Window._contexts_.ctxstack.pop()
        api.glfwMakeContextCurrent(_ctx and _ctx.handle or _ctx)
        return False

    @classmethod
    def swap_current(cls, _ctx):
        if hasattr(Window._contexts_, 'ctxstack') and \
           Window._contexts_.ctxstack:
            raise RuntimeError('This function cannot be used inside `with`')
        api.glfwMakeContextCurrent(_ctx and _ctx.handle or _ctx)
        return _ctx

    def make_current(self):
        return self.swap_current(self)

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
    def framebuffer_size(self):
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
        api.glfwIconifyWindow(self.handle)

    def restore(self):
        api.glfwRestoreWindow(self.handle)

    def _get_attrib(self, attrib):
        return api.glfwGetWindowAttrib(self.handle, attrib)

    @property
    def iconified(self):
        return bool(self._get_attrib(api.GLFW_ICONIFIED))

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
        return bool(self._get_attrib(api.GLFW_VISIBLE))

    @visible.setter
    def visible(self, flag):
        if flag:
            self.show()
        else:
            self.hide()

    @property
    def has_focus(self):
        return bool(self._get_attrib(api.GLFW_FOCUSED))

    @property
    def resizable(self):
        return bool(self._get_attrib(api.GLFW_RESIZABLE))

    @property
    def decorated(self):
        return bool(self._get_attrib(api.GLFW_DECORATED))

    @property
    def context_version(self):
        return (self._get_attrib(api.GLFW_CONTEXT_VERSION_MAJOR),
                self._get_attrib(api.GLFW_CONTEXT_VERSION_MINOR),
                self._get_attrib(api.GLFW_CONTEXT_REVISION))

    @property
    def debug_context(self):
        return bool(self._get_attrib(api.GLFW_OPENGL_DEBUG_CONTEXT))

    @property
    def forward_compat(self):
        return bool(self._get_attrib(api.GLFW_OPENGL_FORWARD_COMPAT))

    OPENGL_API = api.GLFW_OPENGL_API
    OPENGL_ES_API = api.GLFW_OPENGL_ES_API

    @property
    def client_api(self):
        return self._get_attrib(api.GLFW_CLIENT_API)

    CORE_PROFILE = api.GLFW_OPENGL_CORE_PROFILE
    COMPAT_PROFILE = api.GLFW_OPENGL_COMPAT_PROFILE
    ANY_PROFILE = api.GLFW_OPENGL_ANY_PROFILE

    @property
    def opengl_profile(self):
        return self._get_attrib(api.GLFW_OPENGL_PROFILE)

    NO_ROBUSTNESS = api.GLFW_NO_ROBUSTNESS
    NO_RESET_NOTIFICATION = api.GLFW_NO_RESET_NOTIFICATION
    LOSE_CONTEXT_ON_RESET = api.GLFW_LOSE_CONTEXT_ON_RESET

    @property
    def context_robustness(self):
        return self._get_attrib(api.GLFW_CONTEXT_ROBUSTNESS)

    @staticmethod
    def hint(hints=None, **kwargs):
        if hints and kwargs:
            raise ValueError("Hints should be passed via object or via kwargs")

        if not hints:
            hints = Hints(**kwargs)

        if not hints._hints:
            api.glfwDefaultWindowHints()

        for hint, value in hints._hints.items():
            api.glfwWindowHint(hint, value)

    @property
    def monitor(self):
        moni = api.glfwGetWindowMonitor(self.handle)
        if bool(moni):
            return _monitor_obj(moni)
        else:
            return None

    @property
    def clipboard(self):
        return _str(api.glfwGetClipboardString(self.handle))

    @clipboard.setter
    def clipboard(self, buffer):
        api.glfwSetClipboardString(self.handler, _utf(buffer))

    _cursor_modes_get = {
        api.GLFW_CURSOR_DISABLED: None,
        api.GLFW_CURSOR_HIDDEN: False,
        api.GLFW_CURSOR_NORMAL: True,
    }

    _cursor_modes_set = {
        None: api.GLFW_CURSOR_DISABLED,
        False: api.GLFW_CURSOR_HIDDEN,
        True: api.GLFW_CURSOR_NORMAL,
    }

    @property
    def cursor_mode(self):
        libapi_cm = api.glfwGetInputMode(self.handle, api.GLFW_CURSOR)
        return self._cursor_modes_get.get(libapi_cm, None)

    @cursor_mode.setter
    def cursor_mode(self, mode):
        pyglfw_cm = self._cursor_modes_set.get(mode, None)
        api.glfwSetInputMode(self.handle, api.GLFW_CURSOR, pyglfw_cm)

    @property
    def sticky_keys(self):
        return bool(api.glfwGetInputMode(self.handle, api.GLFW_STICKY_KEYS))

    @sticky_keys.setter
    def sticky_keys(self, flag):
        api.glfwSetInputMode(self.handle, api.GLFW_STICKY_KEYS, flag)

    @property
    def sticky_mice(self):
        return bool(api.glfwGetInputMode(self.handle,
                                         api.GLFW_STICKY_MOUSE_BUTTONS))

    @sticky_mice.setter
    def sticky_mice(self, flag):
        api.glfwSetInputMode(self.handle, api.GLFW_STICKY_MOUSE_BUTTONS, flag)

    @property
    def cursor_pos(self):
        return api.glfwGetCursorPos(self.handle)

    @cursor_pos.setter
    def cursor_pos(self, x_y):
        api.glfwSetCursorPos(self.handle, *x_y)

    PRESS = api.GLFW_PRESS
    RELEASE = api.GLFW_RELEASE
    REPEAT = api.GLFW_REPEAT

    MOD_SHIFT = api.GLFW_MOD_SHIFT
    MOD_CONTROL = api.GLFW_MOD_CONTROL
    MOD_ALT = api.GLFW_MOD_ALT
    MOD_SUPER = api.GLFW_MOD_SUPER

    @classmethod
    def _wcb(cls, functype, func):
        if not func:
            return None

        def wrap(handle, *args, **kwargs):
            window = cls._instance_.get(handle.get_void_p().value, None)
            func(window, *args, **kwargs)
        return functype(wrap)

    def set_key_callback(self, callback):
        self._key_callback = self._wcb(api.GLFWkeyfun, callback)
        api.glfwSetKeyCallback(self.handle, self._key_callback)

    def set_char_callback(self, callback):
        def wrap(self, char):
            char = _unichr(char)
            callback(self, char)
        self._char_callback = self._wcb(api.GLFWcharfun, wrap)
        api.glfwSetCharCallback(self.handle, self._char_callback)

    def set_scroll_callback(self, callback):
        self._scroll_callback = self._wcb(api.GLFWscrollfun,
                                          callback)
        api.glfwSetScrollCallback(self.handle,
                                  self._scroll_callback)

    def set_cursor_enter_callback(self, callback):
        def wrap(self, flag):
            flag = bool(flag)
            callback(self, flag)
        self._cursor_enter_callback = self._wcb(api.GLFWcursorenterfun,
                                                wrap)
        api.glfwSetCursorEnterCallback(self.handle,
                                       self._cursor_enter_callback)

    def set_cursor_pos_callback(self, callback):
        self._cursor_pos_callback = self._wcb(api.GLFWcursorposfun,
                                              callback)
        api.glfwSetCursorPosCallback(self.handle,
                                     self._cursor_pos_callback)

    def set_mouse_button_callback(self, callback):
        self._mouse_button_callback = self._wcb(api.GLFWmousebuttonfun,
                                                callback)
        api.glfwSetMouseButtonCallback(self.handle,
                                       self._mouse_button_callback)

    def set_window_pos_callback(self, callback):
        self._window_pos_callback = self._wcb(api.GLFWwindowposfun,
                                              callback)
        api.glfwSetWindowPosCallback(self.handle,
                                     self._window_pos_callback)

    def set_window_size_callback(self, callback):
        self._window_size_callback = self._wcb(api.GLFWwindowsizefun,
                                               callback)
        api.glfwSetWindowSizeCallback(self.handle,
                                      self._window_size_callback)

    def set_window_close_callback(self, callback):
        self._window_close_callback = self._wcb(api.GLFWwindowclosefun,
                                                callback)
        api.glfwSetWindowCloseCallback(self.handle,
                                       self._window_close_callback)

    def set_window_refresh_callback(self, callback):
        self._window_refresh_callback = self._wcb(api.GLFWwindowrefreshfun,
                                                  callback)
        api.glfwSetWindowRefreshCallback(self.handle,
                                         self._window_refresh_callback)

    def set_window_focus_callback(self, callback):
        def wrap(self, flag):
            flag = bool(flag)
            callback(self, flag)
        self._window_focus_callback = self._wcb(api.GLFWwindowfocusfun,
                                                wrap)
        api.glfwSetWindowFocusCallback(self.handle,
                                       self._window_focus_callback)

    def set_window_iconify_callback(self, callback):
        def wrap(self, flag):
            flag = bool(flag)
            callback(self, flag)
        self._window_iconify_callback = self._wcb(api.GLFWwindowiconifyfun,
                                                  wrap)
        api.glfwSetWindowIconifyCallback(self.handle,
                                         self._window_iconify_callback)

    def set_framebuffer_size_callback(self, callback):
        self._framebuffer_size_callback = self._wcb(api.GLFWframebuffersizefun,
                                                    callback)
        api.glfwSetFramebufferSizeCallback(self.handle,
                                           self._framebuffer_size_callback)
