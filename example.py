
import libglfw as api
from useglfw import glfw, Window, Keys, Mice

def key_callback(window, key, scancode, action, mods):
    if key == Keys.ESCAPE:
        window.should_close = True


# ---- decorator for the defined window object ----         # pyglet

# ---- predefined window attr to be overloaded ----         # wxpython

class cb_autoname_Window(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def set_key_callback(self, callback=None, _set=True):
        if not _set:
            callback = None
        elif not callback:
            callback = self.key_callback

        self._key_callback = self._callback(api.GLFWkeyfun, callback)
        api.glfwSetKeyCallback(self.handle, self._key_callback)

# ---- set_handler / get_handler window method ----         # pyqt / pyside / pygtk

class cb_handling_Window(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._key_callback = None

    def set_key_callback(self, callback):
        if callback:
            self._key_callback = self._callback(api.GLFWkeyfun, callback)
            api.glfwSetKeyCallback(self.handle, self._key_callback)

def cb_handling():
    glfw.init()

    w = cb_handling_Window(800, 600, "cb_property")
    w.set_key_callback(key_callback)
    w.make_current

    while not w.should_close:

        w.swap_buffers()
        glfw.poll_events()

    glfw.terminate()

# ---- setting/getting handler window property ----         # this

class cb_property_Window(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._key_callback = None

    @property
    def key_callback(self):
        return self._key_callback

    @key_callback.setter
    def key_callback(self, callback):
        self._key_callback = self._callback(api.GLFWkeyfun, callback)
        api.glfwSetKeyCallback(self.handle, self._key_callback)

def cb_property():
    glfw.init()

    w = cb_property_Window(800, 600, "cb_property")
    w.key_callback = None
    w.key_callback = key_callback
    w.make_current

    while not w.should_close:

        w.swap_buffers()
        glfw.poll_events()

    glfw.terminate()


if __name__ == '__main__':
    cb_handling()
