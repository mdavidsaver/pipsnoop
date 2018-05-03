#!/usr/bin/env python

from __future__ import print_function

import sys
import dtest

V = dtest.foo()
print("foo", V)
sys.exit(not (V==42))
