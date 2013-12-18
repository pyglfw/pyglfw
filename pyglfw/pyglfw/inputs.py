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
            return [self[i] for i in range(*index.indices(self.ntotal))]
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
            if _name_[0] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
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
