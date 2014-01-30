# coding=utf-8
# port of tests/sharing.c from glfw

import pyglfw.pyglfw as fw
import array
import random

from OpenGL.GL import *
from OpenGL.GLU import *

WIDTH = 400
HEIGHT = 400
OFFSET = 50


def open_window(title, share, posX, posY):
    fw.Window.hint(visible=False)
    window = fw.Window(WIDTH, HEIGHT, title, None, share)

    window.swap_interval(1)
    window.pos = posX, posY
    window.show()

    return window.make_current()


def create_texture():
    pixels = array.array('B',
                        (random.randint(0, 255) for i in range(256 * 256)))

    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)

    glTexImage2D(GL_TEXTURE_2D, 0, GL_LUMINANCE, 256, 256, 0,
                 GL_LUMINANCE, GL_UNSIGNED_BYTE, pixels.tostring())
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    return texture


def draw_quad(texture):
    width, height = fw.Window.find_current().framebuffer_size

    glViewport(0, 0, width, height)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0.0, 1.0, 0.0, 1.0)

    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)

    glBegin(GL_QUADS)

    glTexCoord2f(0.0, 0.0)
    glVertex2f(0.0, 0.0)

    glTexCoord2f(1.0, 0.0)
    glVertex2f(1.0, 0.0)

    glTexCoord2f(1.0, 1.0)
    glVertex2f(1.0, 1.0)

    glTexCoord2f(0.0, 1.0)
    glVertex2f(0.0, 1.0)

    glEnd()


if __name__ == '__main__':
    import sys

    if not fw.init():
        sys.exit(1)

    windows = [None, None]
    windows[0] = open_window('First', None, OFFSET, OFFSET)

    texture = create_texture()

    x, y = windows[0].pos
    width, height = windows[0].size

    windows[1] = open_window('Second', windows[0], x + width + OFFSET, y)

    with windows[0]:
        glColor3f(0.6, 0.0, 0.6)
    with windows[1]:
        glColor3f(0.6, 0.6, 0.0)

    while not windows[0].should_close and not windows[1].should_close:
        with windows[0]:
            draw_quad(texture)

        with windows[1]:
            draw_quad(texture)

        windows[0].swap_buffers()
        windows[1].swap_buffers()

        fw.wait_events()

    fw.terminate()
    sys.exit(0)
