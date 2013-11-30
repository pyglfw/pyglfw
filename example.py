
import libglfw as api
from useglfw import glfw, Window, Keys, Mice

def key_callback(window, key, scancode, action, mods):
    if key == Keys.ESCAPE and action:
        window.should_close = True

class cb_autoname_Window(Window):
    key_callback = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_key_callback(self.__class__.key_callback)

class cb_attrfunc_Window(cb_autoname_Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def key_callback(self, key, scancode, action, mods):
        print("key=%s scancode=%s action=%s mods=%s" % (key, scancode, action, mods))
        key_callback(self, key, scancode, action, mods)

def cb_attrfunc():
    glfw.init()

    win = cb_attrfunc_Window(800, 600, "cb_attrfunc")
    win.make_current()

    while not win.should_close:

        win.swap_buffers()
        glfw.poll_events()

    glfw.terminate()

if __name__ == '__main__':
    cb_attrfunc()
