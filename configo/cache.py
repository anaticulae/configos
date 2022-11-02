# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""\
>>> @cache_large
... def hello():
...    pass
>>> hello()
>>> @cache_small
... def wello():
...    print('hello')
>>> wello()
hello
>>> wello()
>>> wello()
"""

import functools

import utila

CACHE_SMALL = 32
CACHE_MEDIUM = 512
CACHE_LARGE = 4096

# TODO: MAY ONLY USE UTILA.CACHE???
cache_small = functools.partial(utila.cacheme, maxsize=CACHE_SMALL)
cache_medium = functools.partial(utila.cacheme, maxsize=CACHE_MEDIUM)
cache_large = functools.partial(utila.cacheme, maxsize=CACHE_LARGE)
