from distutils.core import setup

setup(name='pyglfw',
      version='0.2.0',
      description='Python bindings for the GLFW library',
      url='https://bitbucket.org/pyglfw/pyglfw',
      author='Roman Valov',
      author_email='roman.valov@gmail.com',
      license='zlib',
      packages=['pyglfw', 'pyglfw.libapi', 'pyglfw.pyglfw'],
      long_description=open('README.rst').read(),
      classifiers=(
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: zlib/libpng License',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Topic :: Multimedia',
          'Topic :: Games/Entertainment',
          'Topic :: Software Development :: Libraries',
          )
      )
