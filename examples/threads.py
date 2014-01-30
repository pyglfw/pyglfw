# coding=utf-8
# port of tests/threads.c from glfw

import sys
import math
import threading

import pyglfw.pyglfw as fw
from OpenGL.GL import *

running = True


class Thread(object):
    __slots__ = ['window', 'title', 'r', 'g', 'b', 'id']

    def __init__(self, title, r, g, b):
        self.title = title
        self.r = r
        self.g = g
        self.b = b


def thread_main(thread):
    thread.window.swap_interval(1)

    with thread.window:
        while running:
            v = math.fabs(math.sin(fw.get_time() * 2.0))
            glClearColor(thread.r * v, thread.g * v, thread.b * v, 0.0)
            glClear(GL_COLOR_BUFFER_BIT)
            thread.window.swap_buffers()

if __name__ == '__main__':
    threads = (Thread('Red', 1.0, 0.0, 0.0),
               Thread('Green', 0.0, 1.0, 0.0),
               Thread('Blue', 0.0, 0.0, 1.0))

    if not fw.init():
        sys.exit(1)

    fw.Window.hint(visuble=False)

    for i, t in enumerate(threads):
        t.window = fw.Window(200, 200, t.title)
        t.window.pos = 200 + 250 * i, 200
        t.window.show()

        t.id = threading.Thread(None, thread_main, t.title, (t,))
        t.id.start()

    while running:
        fw.wait_events()

        for i, t in enumerate(threads):
            if t.window.should_close:
                running = False

    for i, t in enumerate(threads):
        t.id.join()

    sys.exit(0)
