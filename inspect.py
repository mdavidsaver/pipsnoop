#!/usr/bin/env python

from __future__ import print_function

from pprint import pprint

import platform
from sysconfig import get_config_vars

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
