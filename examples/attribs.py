# coding=utf-8

import pyglfw.pyglfw as glfw

client_api_map = {
    glfw.Window.OPENGL_API: 'OPENGL',
    glfw.Window.OPENGL_ES_API: 'OPENGL ES'
}

opengl_profile_map = {
    glfw.Window.CORE_PROFILE: 'CORE',
    glfw.Window.COMPAT_PROFILE: 'COMPAT',
    glfw.Window.ANY_PROFILE: 'ANY'
}

context_robustness_map = {
    glfw.Window.LOSE_CONTEXT_ON_RESET: 'LOSE_CONTEXT_ON_RESET',
    glfw.Window.NO_RESET_NOTIFICATION: 'NO_RESET_NOTIFICATION',
    glfw.Window.NO_ROBUSTNESS: 'NO_ROBUSTNESS'
}

cursor_mode_map = {
    None: 'DISABLED',
    False: 'HIDDEN',
    True: 'NORMAL'
}


def dump_window_info(window):
    print("window %s" % (window))
    print("has focus: %s" % window.has_focus)
    print("iconified: %s" % window.iconified)
    print("visible: %s" % window.visible)
    print("resizable: %s" % window.resizable)
    print("decorated: %s" % window.decorated)
    print("client api: %s" % client_api_map[window.client_api])
    print("context version: %s.%s.%s" % window.context_version)
    print("forward compat: %s" % window.forward_compat)
    print("debug context: %s" % window.debug_context)
    print("opengl profile: %s" % opengl_profile_map[window.opengl_profile])
    print("context robustness: %s" %
          context_robustness_map[window.context_robustness])
    print("cursor mode: %s" % cursor_mode_map[window.cursor_mode])
    print("sticky keys: %s" % window.sticky_keys)
    print("sticky mice: %s" % window.sticky_mice)
    print("")


if __name__ == '__main__':
    glfw.init()

    w = glfw.Window(800, 600, "")

    w.make_current()

    while not w.should_close:
        w.swap_buffers()
        glfw.poll_events()

        if w.keys.escape:
            w.should_close = True
        if w.keys.space:
            dump_window_info(w)

    glfw.terminate()
