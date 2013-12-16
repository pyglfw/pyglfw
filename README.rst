
======
pyglfw
======

Python bindings for the `GLFW <http://www.glfw.org/>`_ library.

Introduction
============
        About GLFW
        Other bindings


These binding were developed with the following 
assumptions in mind:

 - Compatibility with GLFW version 3 and higher api.
 - Support for both Python2 (2.7) and Python3 (3.3+).
 - Provide pythonic api.
 - No external dependencies. Thus using ctypes.



 

        Supported
 - Support for CPython and PyPy implementations.
 - Support for 

Licensing
---------

These bindings are distributed under the terms and
conditions of zlib license with the exception to files
in examples folder which are provided with no limitations
to use. Full text of license with copyright notice is
provided in the LICENSE file.

Installation
============

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

    > python ./setup.py bdist_wininst

then run exe installer from dist folder.

Ensure you've installed GLFW library itself
according to instructions on project's page.

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

Pyglfw usage
============
        About
        Side-by-Side



