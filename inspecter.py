#!/usr/bin/env python

from __future__ import print_function

from functools import wraps
from pprint import pprint

import sys
import os
import platform
from sysconfig import get_config_vars

print("os.name =", os.name)
print("sys.platform =", sys.platform)

print("Attributes of platform")
for name in ['architecture',
 'dist',
 'java_ver',
 'libc_ver',
 'linux_distribution',
 'mac_ver',
 'machine',
 'node',
 'os',
 'platform',
 'processor',
 'python_branch',
 'python_build',
 'python_compiler',
 'python_implementation',
 'python_revision',
 'python_version',
 'python_version_tuple',
 'release',
 'system',
# 'system_alias',
 'uname',
# 'uname_result',
 'version',
 'win32_ver']:
    print("platform.%s = "%name, end='')
    A = getattr(platform, name, None)
    if callable(A):
        try:
            print(A())
        except Exception as e:
            print("Error:", e)
    else:
        print(A)

print("sysconfig variables")
pprint(get_config_vars())

print("inspect distutils")

from distutils.sysconfig import customize_compiler
from distutils.ccompiler import new_compiler

compiler = new_compiler(verbose=1, dry_run=1, force=1)
customize_compiler(compiler)

def snoop(obj, attr):
    orig = getattr(obj, attr)
    @wraps(orig)
    def wrapper(*args, **kws):
        print("SNOOP", attr, args, kws)
        return orig(*args, **kws)
    setattr(obj, attr, wrapper)

snoop(compiler, "spawn")

# dummy values for all options so we can see how they are translated
# into compiler arguments
# -I
compiler.set_include_dirs(['idirA','idirB'])
# -L
compiler.set_library_dirs(['ldirC','ldirD'])
# -rpath
if sys.platform != 'win32':
    # "don't know how to set runtime library search path for MSVC++"
    compiler.set_runtime_library_dirs(['rdirC','rdirD'])

# compiler.initialize("name") # for cross compile

# -D
compiler.define_macro("foo", "bar")

# -U
compiler.undefine_macro("baz")

# -l
compiler.set_libraries(["X","Y"])

compiler.set_link_objects(["blah.o"])

print("inspect compiler object")
for attr in ['preprocessor', 'compiler', 'compiler_so', 'compiler_exe',
             'compiler_cxx', 'linker_so', 'linker_exe', 'archiver']:
    A = getattr(compiler, attr, None)
    print(" compiler.", attr, A)


srcs = ["src.c", "other.cpp"]
lang = compiler.detect_language(srcs)
print("detect", srcs, 'as', lang)

print("Compile object code")
objs = compiler.compile(
    srcs,
    output_dir="/tmp/invalid",
    macros=[],
    include_dirs=[],
    extra_postargs=[],
    depends=[],
)

print("objects", objs)

print("Link shared object")
compiler.link_shared_object(
    objs,
    'output',
    libraries=[],
    library_dirs=[],
    runtime_library_dirs=[],
    extra_postargs=[],
    export_symbols=[],
    debug=1,
    build_temp='/tmp/other',
    target_lang=lang,
)
