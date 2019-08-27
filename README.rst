======
pyglfw
======

Python bindings for the `GLFW <http://www.glfw.org/>`_ library.

Home: https://github.com/pyglfw/pyglfw

Introduction
============

At the moment of development there were already available
numerous variants of bindings for the glfw library to python.
Besides driving by NIH syndrome these binding were developed
with following assumptions in mind:

 - Compatibility with GLFW version 3 and higher API.
 - Support for both Python2 (2.7) and Python3 (3.3+).
 - Provide low-level and pythonic API separately.
 - No external dependencies. Thus using ctypes.

Platforms
---------

During development these bindings were proven to work 
on all major operating systems environments including
Windows, OSX and Linux.

CPython implementations were tested against versions
of Python 2.7 and Python 3.3 with no serious issues found.

By the way testing was performed with PyPy. As a result there
were revealed issue with ctypes implemenation in PyPy. Issue
was fixed and should be available as a part of PyPy 2.2.2.


Licensing
---------

These bindings are distributed under the terms and
conditions of zlib license with the exception to files
in examples folder which are provided with no limitations
to use. Full text of license with copyright notice is
provided in the LICENSE file.

-------

Installation
============

Ensure you've installed GLFW shared library binary
according to instructions on project's page related
to installed operating system.

Project releases are available from pypi and could
be installed using pip or easy_install, i.e.:

::

    # pip install pyglfw

Moreover exe installables for the Windows platform
could be found on the project's home `download page`__

__ https://bitbucket.org/pyglfw/pyglfw/downloads

In addition, Ubuntu users are able to install pyglfw
using project's `PPA`__. Archive also provides packages
for glfw3 library itself and backported python-opengl.

__ https://launchpad.net/~pyglfw/+archive/pyglfw

Latest version could be installed from cloned source
with provided setup.py script. Following commands
depend on system used:


On Linux and OSX
----------------

::

    $ python ./setup.py sdist

then

::

    # easy_install dist/pyglfw-<ver>.tar.gz

or

::

    # pip install dist/pyglfw-<ver>.tar.gz


On Windows
----------

::

    > python.exe setup.py bdist_wininst

then run exe installer from dist folder.

-------

Libapi
======

Low-level **libapi** package serves as thin wrapper
above GLFW library. It's API mostly resemble one of
C library except functions that require pass-by-ref
parameters. As a rule of thumb all functions that
return void and fill several values via pass-by-ref
parameters are mapped to functions returning tuple
of values. And functions that return pointer to array
with number of items set via pass-by-ref parameter are 
mapped to functions returning list of items. I.e.:

::

    int major, minor, rev;
    glfwGetVersion(&major, &minor, &rev)

becomes

::

    major, minor, rev = glfwGetVersion()

and

::

    int n_items;
    GLFWmonitor **monitors = glfwGetMonitors(&n_items)

becomes

::
     
    monitors = glfwGetMonitors()


Special note should be done regarding window pointer
functions. glfwSetWindowPointer allows to set any 
python object as a window private data and retrieve
it back with glfwGetWindowPointer. However it's still
required to hold reference to this object in python
code. Also this functionality will not work with PyPy
implemetation due to lack of py_object support.

The requirement to hold references also spreads to
functions that are settings varios callbacks. Please
refer to *raw_api* in examples for usage primer.

Pyglfw
======

Pythonic **pyglfw** package handles following moments:

 - Encapsulation of struct pointers and functions API
   into objects with properties and methods.
 - Transparent usage of strings (either from python 2
   or from python 3).
 - Raising exceptions in case of errors.
 - Eliminates need to use of ctypes structures and
   ctypes-based callback prototypes.
 - Holds references for set to callback functions,
   so there is no need to hold them outside.
 - Provide pythonic types for callback functions.

and following functionality is restricted:

 - No get/set window pointers. Due to its ambiquity.
 - No set error callback. Error callback is used to
   raise exeptions.
 - Set callback methods doesn't return previously
   used callback. It's unable to certainly map them
   to python object in every case.
 - No check for extensions and proc address query.
   This should be handled with dedicated frameworks
   like PyOpenGL.

Side-by-Side
============

Here is side-by-side comparison of same operations
performed via low-level (libapi) and pythonic (pyglfw)
bindings.

Basics
------

libapi:

::

   from pyglfw.libapi import *

   glfwInit()

   glfwGetVersion()

   glfwTerminate()

   glfwPollEvents()

pyglfw:

::

   import pyglfw.pyglfw as glfw

   glfw.init()

   glfw.api_version()

   glfw.terminate()

   glfw.poll_events()

Monitors
--------

libapi:

::

   monitorp = glfwGetPrimaryMonitor()

   curmode = glfwGetVideoMode(monitorp)

   allmodes = glfwGetVideoModes(monitorp)

   @GLFWmonitorfun
   def on_monitor_event(monitor, event):
       if event == GLFW_CONNECTED:
           print(glfwGetMonitorName(monitor))

   glfwSetMonitorCallback(on_monitor_event)

pyglfw:

::

   monitor = glfw.get_primary_monitor()

   curmore = monitor.video_mode

   allmodes = monitor.video_modes

   def on_monitor_event(monitor, event):
       if event == glfw.Monitor.CONNECTED:
           print(monitor.name)

   glfw.Monitor.set_callback(on_monitor_event)

Hints
-----

libapi:

::

   glfwDefaultWindowHints()

   glfwWindowHint(GLFW_CLIENT_API, GLFW_OPENGL_API)

   w, h = curmode.width, curmode.height
   windowp = glfwCreateWindow(w, h, b'libapi', None, None)

   glfwDestroyWindow(windowp)

pyglfw:

::

   glfw.Window.hint()

   glfw.Window.hint(client_api=glfw.Window.OPENGL_API)

   w, h = curmode.width, curmode.height
   window = glfw.Window(w, h, 'pyglfw')

   window.close()

Swap
----

libapi:

::

   context = glfwGetCurrentContext()

   glfwMakeContextCurrent(windowp)

   glfwSwapInterval(0)

   glfwMakeContextCurrent(context)

   glfwMakeContextCurrent(windowp)

   glfwSwapBuffers(windowp)


pyglfw:

::

   # makes context current
   # and restores previous
   window.swap_interval(0)

   window.make_current()

   window.swap_buffers()

Windows
-------

libapi:

::

   if not glfwWindowShouldClose():
       glfwSetWindowTitle(b'libapi')

       size = glfwGetWindowSize()

       glfwShowWindow()

   is_visible = glfwGetWindowAttrib(GLFW_VISIBLE)

   client_api = glfwGetWindowAttrib(GLFW_CLIENT_API)

   glfwSetWindowAttrib(GLFW_FOCUSED, 1)

   @GLFWwindowsizefun
   def on_window_size(windowp, w, h):
       glfwSetWindowSize(windowp, size[0], size[1])

   glfwSetWindowSizeCallback(windowp, on_window_size)


pyglfw:

::

   if not window.should_close:
       window.set_title('pyglfw')

       size = window.size

       window.show()

   is_visible = window.visible

   client_api = window.client_api

   window.has_focus = True

   def on_window_size(window, w, h):
       window.size = size

   window.set_window_size_callback(on_window_size)

Inputs
------

libapi:

::

   mode = glfwGetInputMode(windowp, GLFW_STICKY_KEYS)

   glfwSetInputMode(windowp, GLFW_STICKY_MOUSE_BUTTONS, mode)

   is_escape = glfwGetKey(windowp, GLFW_ESCAPE)

   is_middle = glfwGetMouseButton(windowp, GLFW_MOUSE_BUTTON_MIDDLE)

   cursor_at = glfwGetCursorPos(windowp)

   @GLFWkeyfun
   def on_key(windowp, key, scancode, action, mods):
       if key == GLFW_ESCAPE:
           glfwSetWindowShouldClose(1)

   glfwSetKeyCallback(windowp, on_key)

   if glfwJoystickPresent(0):
       joy_name = glfwGetJoystickName(0)
       joy_axes = glfwGetJoystickAxes(0)

pyglfw:

::

   mode = window.sticky_keys

   window.sticky_mice = mode

   is_escape = window.keys.escape

   is_middle = window.mice.middle

   cursor_at = window.cursor_pos

   def on_key(window, key, scancode, action, mods):
       if key == glfw.Keys.ESCAPE:
           window.should_close = True

   window.set_key_callback(on_key)

   js = glfw.Joystick(0)

   if js:
       joy_name = js.name
       joy_axes = js.axes

