#!/usr/bin/env python

from setuptools import setup, Extension

import dsocmd

dso = Extension('demo', ['foo.c'],
                define_macros = [('BUILD_FOO', None)])

ext = Extension('dtest', ['bar.c'],
                library_dirs=['.'],
                libraries=['demo'])

setup(
    name='pipsnoop',
    version="0.1",
    packages=['pipsnoop', 'pipsnoop.test'],
    ext_modules = [ext],
    x_dsos = [dso],
    cmdclass = {
        'build_dso':dsocmd.build_dso,
        'build_ext':dsocmd.build_ext,
    },
)
