# coding=utf-8
# port of tests/windows.c from glfw

import sys
import pyglfw.pyglfw as fw

from OpenGL.GL import *

titles = "Foo", "Bar", "Baz", "Quux"
colors = ((0.0, 0.0, 1.0, 0.0), (1.0, 0.0, 0.0, 0.0),
         (0.0, 1.0, 0.0, 0.0), (1.0, 1.0, 0.0, 0.0))

if __name__ == '__main__':
    running = True
    windows = [None, None, None, None]

    if not fw.init():
        sys.exit(1)

    fw.Window.hint(visible=False)

    for i in range(4):
        windows[i] = fw.Window(200, 200, titles[i])
        if not windows[i]:
            fw.terminate()
            sys.exit(1)

        windows[i].make_current()
        glClearColor(*colors[i])

        windows[i].pos = 100 + (i & 1) * 300, 100 + (i >> 1) * 300
        windows[i].show()

    while running:
        for i in range(4):
            windows[i].make_current()

            glClear(GL_COLOR_BUFFER_BIT)
            windows[i].swap_buffers()

            if windows[i].should_close:
                running = False

        fw.poll_events()

    fw.terminate()
    sys.exit(0)
