
from useglfw import glfw, Window, Keys, Mice, Joystick, Monitor
from OpenGL.GL import *
from math import *

class Render(object):
    def __init__(self, viewport):
        glViewport(0, 0, viewport[0], viewport[1])
        glDisable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def __call__(self, object):
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClear(GL_COLOR_BUFFER_BIT)

        glBegin(GL_TRIANGLES)

        for pt in object:
            glVertex2f(*pt)

        glEnd()


class Domain(object):
    def __init__(self):
        self.cnt_x = 0
        self.cnt_y = 0

        self.pos_x = 0
        self.pos_y = 0

    def left(self):
        self.pos_x -= 0.01

    def right(self):
        self.pos_x += 0.01

    def down(self):
        self.pos_y -= 0.01

    def up(self):
        self.pos_y += 0.01

    @property
    def object(self):
        head0 = (self.pos_x, self.pos_y)
        wing1 = (self.pos_x + 0.03, self.pos_y - 0.03)
        wing2 = (self.pos_x - 0.03, self.pos_y - 0.03)

        return [ head0, wing1, wing2 ]

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

#        if win.keys.left or jst.axes[0] == -1:
#            dom.left()
#
#        if win.keys.right or jst.axes[0] == +1:
#            dom.right()
#
#        if win.keys.up or jst.axes[1] == +1:
#            dom.up()
#
#        if win.keys.down or jst.axes[1] == -1:
#            dom.down()

        dom.pos = jst.axes[0], jst.axes[1]

        with win:
            render(dom.object)

        win.swap_buffers()

    glfw.terminate()
