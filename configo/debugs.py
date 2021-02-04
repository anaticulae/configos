# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

import configo

DEBUG = 'KIWI_DEBUG'


def debug() -> bool:
    try:
        current = configo.env(DEBUG)
    except KeyError:
        return False
    current = utila.str2bool(current)
    return current


def debug_set():
    configo.env_set(DEBUG, 'True')


def debug_unset():
    configo.env_set(DEBUG, 'False')
