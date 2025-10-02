"""Test import the library and print essential information"""

import platform
import sys

import TEMPLATE

print("Python interpreter:", sys.executable)
print("Python version    :", sys.version)
print("Platform          :", platform.platform())
print("Library path      :", TEMPLATE.__file__)
print("Library version   :", TEMPLATE.__version__)
