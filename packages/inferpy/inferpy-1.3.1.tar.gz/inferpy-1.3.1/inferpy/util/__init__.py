# -*- coding: utf-8 -*-
#

"""
Package with modules defining functions, classes and variables which are
useful for the main functionality provided by inferpy
"""


from .common import floatx, set_floatx
from .runtime import tf_run_allowed, tf_run_ignored, set_tf_run
from . import iterables
from . import interceptor
from . import name
from .session import get_session, set_session, clear_session, new_session, init_uninit_vars


__all__ = [
    'floatx',
    'set_floatx',
    'iterables',
    'interceptor',
    'set_tf_run',
    'tf_run_allowed',
    'tf_run_ignored',
    'name',
    'get_session',
    'set_session',
    'clear_session',
    'new_session',
    'init_uninit_vars'
]
