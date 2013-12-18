# coding=utf-8
###############################################################################
#
#  This file is part of pyglfw project which is subject to zlib license.
#  See the LICENSE file for details.
#
#  Copyright (c) 2013   Roman Valov <roman.valov@gmail.com>
#
###############################################################################


class NotInitializedError(Exception):
    pass


class NoCurrentContextError(Exception):
    pass


class GLFWInvalidEnumError(ValueError):
    pass


class GLFWInvalidValueError(ValueError):
    pass


class GLFWOutOfMemoryError(MemoryError):
    pass


class ApiUnavailableError(Exception):
    pass


class VersionUnavailableError(Exception):
    pass


class PlatformError(Exception):
    pass


class FormatUnavailableError(Exception):
    pass
