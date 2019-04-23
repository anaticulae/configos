# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# Tis file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

from utila import FAILURE
from utila import logging_error


def ready():
    """Return path to finished jobs"""
    return _path_from_env('SHARED_READY')


def todo():
    """Return path todo with jobs to work"""
    return _path_from_env('SHARED_TODO')


def share():
    """Return path to shared folder"""
    return _path_from_env('SHARED_SPACE')


def _path_from_env(env: str):
    assert env
    try:
        path = os.environ[env]
        if not os.path.exists(path):
            logging_error('Path does not exists: %s' % path)
            exit(FAILURE)
        return path
    except KeyError:
        logging_error('MISSING environment var `%s`' % env)
        exit(FAILURE)


def check_startup():
    """Check that global environments are set"""
    ready()
    todo()
