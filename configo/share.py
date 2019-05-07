# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Access location of global share:

The structure of these loations is:

    +common
    +--todo
    +--ready

"""
import os

from utila import FAILURE
from utila import logging_error

TODO = 'SHARED_TODO'
READY = 'SHARED_READY'
COMMON = 'SHARED_SPACE'


def ready(check: bool = False):
    """Return path to finished jobs

    Args:
        check(bool): check existence of path
    Returns:
        path from global variable
    Raises:
        SystemExit if check is True and path does not exists
        SystemExit if global env var does not exist
    """
    return _path_from_env(READY, check=check)


def todo(check: bool = False):
    """Return path todo with jobs to work

    Args:
        check(bool): check existence of path
    Returns:
        path from global variable
    Raises:
        SystemExit if check is True and path does not exists
        SystemExit if global env var does not exist
    """
    return _path_from_env(TODO, check=check)


def share(check: bool = False):
    """Return path to shared folder

    Args:
        check(bool): check existence of path
    Returns:
        path from global variable
    Raises:
        SystemExit if check is True and path does not exists
        SystemExit if global env var does not exist
    """
    return _path_from_env(COMMON, check=check)


def export(common: str, todo: str, ready: str):
    """Set environment variables"""
    os.environ[COMMON] = str(common)
    os.environ[TODO] = str(todo)
    os.environ[READY] = str(ready)


def environment(check: bool = False):
    """Return `SHARED_TODO` and `SHARED_READY` folder"""
    todo_ = todo(check=check)
    ready_ = ready(check=check)
    common = share(check=check)

    return common, todo_, ready_


def _path_from_env(env: str, check: bool = False):
    """Access global env variable"""
    assert env
    try:
        path = os.environ[env]
        if check and not os.path.exists(path):
            logging_error('Path does not exists: %s' % path)
            exit(FAILURE)
        return path
    except KeyError:
        logging_error('Missing environment var `%s`' % env)
        exit(FAILURE)


def check_startup():
    """Check that global environments are set"""
    ready(check=True)
    todo(check=True)
    share(check=True)
