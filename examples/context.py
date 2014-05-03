# coding=utf-8

from pyglfw.pyglfw import *

if __name__ == '__main__':
    init()

    versions = (3, 3, True), (3, 2, True), (3, 1, False), (3, 0, False)

    for vermaj, vermin, iscore in versions:
        try:
            Window.hint()
            Window.hint(context_version=(vermaj, vermin))
            if iscore:
                Window.hint(forward_compat=True)
                Window.hint(opengl_profile=Window.CORE_PROFILE)
            w = Window(800, 600, "Тест: %s" % api_version_string())
            break
        except (PlatformError, VersionUnavailableError, ValueError) as e:
            iscore_str = 'CORE' if iscore else ''
            print("%s.%s %s: %s" % (vermaj, vermin, iscore_str, e))
    else:
        raise SystemExit("Proper OpenGL 3.x context not found")

    print(w.context_version)

    assert Window.find_current() is None

    Window.swap_current(w)

    assert Window.find_current() is w

    Window.swap_current(None)

    assert Window.find_current() is None

    w.make_current()

    assert Window.find_current() is w

    k = w.keys

    while not w.should_close:
        with w:
            w.swap_buffers()
            poll_events()

            if k.escape:
                w.should_close = True

    assert Window.find_current() is w

    w.close()

    assert Window.find_current() is None

    terminate()
