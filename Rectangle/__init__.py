"""Rectangle is a highly extensive python module for rectangle, color and different package management.

It works best as one central high-level package that works over multiple rendering systems, and for multiple 
purposes, such as physics or layout in tkinter."""

from sys import version_info
from warnings import warn
if version_info < (3, 10):
    warn("Python 3.10 or higher is required for python Rectangle. Some features may not work properly.", RuntimeWarning)

from .core import *
__all__ = core.__all__