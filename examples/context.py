# coding=utf-8

from pyglfw import *

if __name__ == '__main__':
    init()

    for cver in [ (3,3,True), (3,2,True), (3,1,False), (3,0,False) ]:
        try:
            if cver[2]:
                Window.hint(context_version=cver[:2],forward_compat=True,opengl_profile=Window.CORE_PROFILE)
            else:
                Window.hint(context_version=cver[:2])
            w = Window(800, 600, "Тест: %s" % api_version_string())
            break
        except (PlatformError, VersionUnavailableError) as e:
            print("%s %s" % (cver, e))

    w.make_current()

    print(w.context_version)

    k = w.keys

    while not w.should_close:
        w.swap_buffers()
        poll_events()

        if k.escape:
            w.should_close = True

    terminate()

