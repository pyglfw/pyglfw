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


class _HintsBase(object):
    _hint_map_ = {
        'resizable':           api.GLFW_RESIZABLE,
        'visible':             api.GLFW_VISIBLE,
        'decorated':           api.GLFW_DECORATED,
        'red_bits':            api.GLFW_RED_BITS,
        'green_bits':          api.GLFW_GREEN_BITS,
        'blue_bits':           api.GLFW_BLUE_BITS,
        'alpha_bits':          api.GLFW_ALPHA_BITS,
        'depth_bits':          api.GLFW_DEPTH_BITS,
        'stencil_bits':        api.GLFW_STENCIL_BITS,
        'accum_red_bits':      api.GLFW_ACCUM_RED_BITS,
        'accum_green_bits':    api.GLFW_ACCUM_GREEN_BITS,
        'accum_blue_bits':     api.GLFW_ACCUM_BLUE_BITS,
        'accum_alpha_bits':    api.GLFW_ACCUM_ALPHA_BITS,
        'aux_buffers':         api.GLFW_AUX_BUFFERS,
        'samples':             api.GLFW_SAMPLES,
        'refresh_rate':        api.GLFW_REFRESH_RATE,
        'stereo':              api.GLFW_STEREO,
        'srgb_capable':        api.GLFW_SRGB_CAPABLE,
        'client_api':          api.GLFW_CLIENT_API,
        'context_ver_major':   api.GLFW_CONTEXT_VERSION_MAJOR,
        'context_ver_minor':   api.GLFW_CONTEXT_VERSION_MINOR,
        'context_robustness':  api.GLFW_CONTEXT_ROBUSTNESS,
        'debug_context':       api.GLFW_OPENGL_DEBUG_CONTEXT,
        'forward_compat':      api.GLFW_OPENGL_FORWARD_COMPAT,
        'opengl_profile':      api.GLFW_OPENGL_PROFILE,
    }

    _over_map_ = {
        'context_version':     (api.GLFW_CONTEXT_VERSION_MAJOR,
                                api.GLFW_CONTEXT_VERSION_MINOR,),

        'rgba_bits':           (api.GLFW_RED_BITS,
                                api.GLFW_GREEN_BITS,
                                api.GLFW_BLUE_BITS,
                                api.GLFW_ALPHA_BITS,),

        'rgba_accum_bits':     (api.GLFW_ACCUM_RED_BITS,
                                api.GLFW_ACCUM_GREEN_BITS,
                                api.GLFW_ACCUM_BLUE_BITS,
                                api.GLFW_ACCUM_ALPHA_BITS,),
    }

    def __init__(self, **kwargs):
        self._hints = {}

        for k, v in kwargs.items():
            is_hint = k in self.__class__._hint_map_
            is_over = k in self.__class__._over_map_
            if is_hint or is_over:
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
            value = [self[hint] for hint in over]
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


Hints = type('Hints',
             (_HintsBase,),
             _hntprops_(_HintsBase._hint_map_, _HintsBase._over_map_))
