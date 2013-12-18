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
from .common import _str


def _monitor_obj(moni):
    monobj = super(Monitor, Monitor).__new__(Monitor)
    monobj.handle = moni.get_void_p()
    return monobj


class VideoMode(object):
    __slots__ = 'width', 'height', 'bits', 'refresh_rate'

    def __init__(self, vm):
        self.width = vm.width
        self.height = vm.height
        self.bits = (vm.redBits, vm.greenBits, vm.blueBits)
        self.refresh_rate = vm.refreshRate


class Monitor(object):
    _callback_ = None

    CONNECTED = api.GLFW_CONNECTED
    DISCONNECTED = api.GLFW_DISCONNECTED

    def __eq__(self, other):
        return self.handle.value == other.handle.value

    def __ne__(self, other):
        return not (self == other)

    @staticmethod
    def set_callback(callback):
        if not callback:
            Monitor._callback_ = None
        else:
            def wrap(handle, *args, **kwargs):
                callback(_monitor_obj(handle), *args, **kwargs)
            Monitor._callback_ = api.GLFWmonitorfun(wrap)
        api.glfwSetMonitorCallback(Monitor._callback_)

    def __init__(self):
        raise TypeError("Objects of this class cannot be created")

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
        return VideoMode(api.glfwGetVideoMode(self.handle))

    @property
    def video_modes(self):
        return [VideoMode(vm) for vm in api.glfwGetVideoModes(self.handle)]

    def set_gamma(self, gamma):
        api.glfwSetGamma(self.handle, gamma)

    @property
    def gamma_ramp(self):
        return api.glfwGetGammaRamp(self.handle)

    @gamma_ramp.setter
    def gamma_ramp(self, rgb_ramp):
        api.glfwSetGammaRamp(self.handle, rgb_ramp)


def get_monitors():
    return [_monitor_obj(moni) for moni in api.glfwGetMonitors()]


def get_primary_monitor():
    return _monitor_obj(api.glfwGetPrimaryMonitor())
