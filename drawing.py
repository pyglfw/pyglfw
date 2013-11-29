
from useglfw import glfw, Window, Keys, Mice, Joystick, Monitor
from OpenGL.GL import *
from math import *

class Render(object):
    def __init__(self, viewport):
        glDisable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def __call__(self, *args):
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClear(GL_COLOR_BUFFER_BIT)

        for _obj in args:
            _obj()

    def triangle(self, center, length=0.1):
        def draw():
            glBegin(GL_TRIANGLES)

            glVertex2f(center[0], center[1])
            glVertex2f(center[0] - length, center[1] + length)
            glVertex2f(center[0] + length, center[1] + length)

            glEnd()

        return draw


    def quad(self, center, length=0.1):
        def draw():
            glBegin(GL_QUADS)

            glVertex2f(center[0] - length, center[1] - length)
            glVertex2f(center[0] - length, center[1] + length)
            glVertex2f(center[0] + length, center[1] + length)
            glVertex2f(center[0] + length, center[1] - length)

            glEnd()


        return draw


class Domain(object):
    def __init__(self):
        self.cnt_x = 0
        self.cnt_y = 0

        self.pos_x = 0
        self.pos_y = 0

    @property
    def points(self):
        return [ (self.pos_x, self.pos_y) ]

    def mov(self, vel_x, vel_y):
        self.pos_x += vel_x
        self.pos_y += vel_y

    @property
    def pos(self):
        return (self.pos_x, self.pos_y)

    @pos.setter
    def pos(self, x_y):
        x, y = x_y
        self.pos_x = self.cnt_x + x
        self.pos_y = self.cnt_y + y



if __name__ == '__main__':

    glfw.init()

    vm = Monitor(0).video_modes[-1]

    win = Window(vm[0], vm[1], "nayadra", Monitor(0))
    win.swap_interval(0)

    jst = Joystick(0)

    with win:
        render = Render(win.fbsize)

    dom = Domain()

    while not win.should_close:
        glfw.poll_events()
        
        if win.keys.escape:
            win.should_close = True

        mov_x = round(jst.axes[0], 2) and jst.axes[0] or (float(win.keys.right) - float(win.keys.left))
        mov_y = round(jst.axes[1], 2) and jst.axes[1] or (float(win.keys.up) - float(win.keys.down))

        dom.mov(mov_x * 0.01, mov_y * 0.01)

#        dom.pos = jst.axes[0], jst.axes[1]

        with win:
            drawes = [ render.quad(p) for p in dom.points ]
            render(*drawes)

        win.swap_buffers()

    glfw.terminate()
