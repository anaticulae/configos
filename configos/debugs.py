# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utilo

import configos

DEBUG = 'KIWI_DEBUG'


def debug() -> bool:
    try:
        current = configos.env(DEBUG)
    except KeyError:
        return False
    result = utilo.str2bool(current)
    return result


def debug_set():
    configos.env_set(DEBUG, 'True')


def debug_unset():
    configos.env_set(DEBUG, 'False')
