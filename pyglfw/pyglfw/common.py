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

if bytes is str:
    _unichr = unichr
    _unistr = unicode
else:
    _unichr = chr
    _unistr = str


def _utf(obj):
    if bytes is not str:
        obj = obj.encode()
    return obj


def _str(obj):
    if bytes is not str:
        obj = obj.decode()
    return obj


def api_version():
    return api.glfwGetVersion()


def api_version_string():
    return _str(api.glfwGetVersionString())


def init():
    return bool(api.glfwInit())


def terminate():
    api.glfwTerminate()


def poll_events():
    api.glfwPollEvents()


def wait_events():
    api.glfwWaitEvents()


def get_time():
    return api.glfwGetTime()


def set_time(nsec):
    api.glfwSetTime(nsec)
