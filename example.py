
import libglfw as api
from useglfw import glfw, Window, Keys, Mice


class CallbackWindow(Window):
    def __init__(self, *args, **kwargs):
        super(CallbackWindow, self).__init__(*args, **kwargs)

        #self.set_key_callback(CallbackWindow.key_callback)
        #self.set_char_callback(CallbackWindow.char_callback)
        #self.set_scroll_callback(CallbackWindow.scroll_callback)
        #self.set_mouse_button_callback(CallbackWindow.mouse_button_callback)
        self.set_cursor_enter_callback(CallbackWindow.cursor_enter_callback)
        #self.set_cursor_pos_callback(CallbackWindow.cursor_pos_callback)
        #self.set_window_size_callback(CallbackWindow.window_size_callback)
        #self.set_window_pos_callback(CallbackWindow.window_pos_callback)
        #self.set_window_close_callback(CallbackWindow.window_close_callback)
        #self.set_window_refresh_callback(CallbackWindow.window_refresh_callback)
        self.set_window_focus_callback(CallbackWindow.window_focus_callback)
        self.set_window_iconify_callback(CallbackWindow.window_iconify_callback)
        #self.set_framebuffer_size_callback(CallbackWindow.framebuffer_size_callback)

    def key_callback(self, key, scancode, action, mods):
        print("keybrd: key=%s scancode=%s action=%s mods=%s" % (key, scancode, action, mods))

    def char_callback(self, char):
        print("unichr: char=%s" % char)

    def scroll_callback(self, off_x, off_y):
        print("scroll: x=%s y=%s" % (off_x, off_y))

    def mouse_button_callback(self, button, action, mods):
        print("button: button=%s action=%s mods=%s" % (button, action, mods))

    def cursor_enter_callback(self, status):
        print("cursor: status=%s" % status)

    def cursor_pos_callback(self, pos_x, pos_y):
        print("curpos: x=%s y=%s" % (pos_x, pos_y))

    def window_size_callback(self, wsz_w, wsz_h):
        print("window: w=%s h=%s" % (wsz_w, wsz_h))

    def window_pos_callback(self, pos_x, pos_y):
        print("window: x=%s y=%s" % (pos_x, pos_y))

    def window_close_callback(self):
        print("should: %s" % self.should_close)

    def window_refresh_callback(self):
        print("redraw")

    def window_focus_callback(self, status):
        print("active: status=%s" % status)

    def window_iconify_callback(self, status):
        print("hidden: status=%s" % status)

    def framebuffer_size_callback(self, fbs_x, fbs_y):
        print("buffer: x=%s y=%s" % (fbs_x, fbs_y))


def main():
    glfw.init()

    win = CallbackWindow(800, 600, "callback window")
    win.make_current()

    while not win.should_close:

        win.swap_buffers()
        glfw.poll_events()

        if win.keys.escape:
            win.should_close = True

    glfw.terminate()

if __name__ == '__main__':
    main()
