
======
pyglfw
======

Python bindings for the `GLFW <http://www.glfw.org/>`_ library.

Introduction
============

At the moment of development there were numerous
implementations of bindings for glfw library to python.
Besides NIH syndrome these binding were developed
with the following assumptions in mind:

 - Compatibility with GLFW version 3 and higher api.
 - Support for both Python2 (2.7) and Python3 (3.3+).
 - Provide low-level and pythonic api separately.
 - No external dependencies. Thus using ctypes.

Platforms
---------

During development these bindings were proven to work 
in all major operating systems environments including
Windows, OSX and Linux.

CPython implementations were tested against versions
of Python 2.7 and Python 3.3 with no issues.

By the way testing was performed with PyPy and reveals
issue with ctypes implemenation in PyPy. Issue was fixed
and should be available as a part of PyPy 2.2.2 release.


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

Ensure you've installed GLFW library itself according
to instructions on project's page.

At the moment these binding could be installed with
provided setup.py script. To do this retrieve sources
either cloning repository or downloading and unpacking
source archive. Following commands depend on system
used.


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

    > python setup.py bdist_wininst

then run exe installer from dist folder.

-------

Libapi
======

Low-level **libapi** package serves as thin wrapper
above GLFW library. It's api mostly resemble one of
C library except functions that require pass-by-ref
parameters. As a rule of thumb all functions that
return void and fill several values via pass-by-ref
parameters are mapped to functions returning tuple
of values. And functions that return pointer to array
with number of items via pass-by-ref parameter are 
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

 - Encapsulation of struct pointers and functions api
   into objects with properties and methods.
 - Transparent usage of strings (either from python 2
   or from python 3).
 - Raising exceptions in case of errors.
 - Eliminates need to use of ctypes structures and
   callback prototypes.
 - Holds references for set to callback functions.
 - Provide pythonic types for callbacks.

and following functionality is restricted:

 - No get/set window pointers. Due to its ambiquity.
 - No set error callback. Error callback is used to
   raise exeptions.
 - Set callback methods doesn't return previously
   used callback. It's unable to certainly map them
   to python object in all cases.

Side-by-Side
============

Basics
------

libapi:

::

   from pyglfw.libapi import *

   glfwInit()

   glfwGetVersion()

   glfwTerminate()

pyglfw:

::

   import pyglfw.pyglfw as glfw

   glfw.init()

   glfw.api_version()

   glfw.terminate()

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

   w, h = curmode[0], curmode[1]
   window = glfw.Window(w, h, 'pyglfw')

   window.close()

