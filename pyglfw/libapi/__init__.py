# coding=utf-8
###############################################################################
#
#  This file is part of pyglfw project which is subject to zlib license.
#  See the LICENSE file for details.
#
#  Copyright (c) 2013   Roman Valov <roman.valov@gmail.com>
#
###############################################################################

from .constant import *

from .c_helper import GLFWmonitorP
from .c_helper import GLFWwindowP
from .c_helper import GLFWvidmodeP
from .c_helper import GLFWgammarampP

from .c_helper import GLFWerrorfun
from .c_helper import GLFWwindowposfun
from .c_helper import GLFWwindowsizefun
from .c_helper import GLFWwindowclosefun
from .c_helper import GLFWwindowrefreshfun
from .c_helper import GLFWwindowfocusfun
from .c_helper import GLFWwindowiconifyfun
from .c_helper import GLFWframebuffersizefun
from .c_helper import GLFWmousebuttonfun
from .c_helper import GLFWcursorposfun
from .c_helper import GLFWcursorenterfun
from .c_helper import GLFWscrollfun
from .c_helper import GLFWkeyfun
from .c_helper import GLFWcharfun
from .c_helper import GLFWmonitorfun

from . import function

_all_functions = function._declare.dir

from sys import modules as _sys_modules

for _func_ in _all_functions:
    setattr(_sys_modules[__name__], _func_, function._declare.dir[_func_])
