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
"""

import functools

CACHE_SMALL = 16
CACHE_MEDIUM = 32
CACHE_LARGE = 64

cache_small = functools.lru_cache(maxsize=CACHE_SMALL)
cache_medium = functools.lru_cache(maxsize=CACHE_MEDIUM)
cache_large = functools.lru_cache(maxsize=CACHE_LARGE)
