# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Access path's of global data share. These locations are stored in
global environment variables:

+ SHARED_READY
+ SHARED_SPACE
+ SHARED_TMP
+ SHARED_TODO

Use `configo.export()` to change these variables.
"""

import os

import utila

TODO = 'SHARED_TODO'
READY = 'SHARED_READY'
COMMON = 'SHARED_SPACE'
TMP = 'SHARED_TMP'


def ready(check: bool = False) -> str:
    """Return path to finished jobs.

    Args:
        check(bool): check existence of path
    Returns:
        path from global variable
    Raises:
        SystemExit if check is True and path does not exists
        SystemExit if global env var does not exist
    """
    return _path_from_env(READY, check=check)


def todo(check: bool = False) -> str:
    """Return path todo with jobs to work.

    Args:
        check(bool): check existence of path
    Returns:
        path from global variable
    Raises:
        SystemExit if check is True and path does not exists
        SystemExit if global env var does not exist
    """
    return _path_from_env(TODO, check=check)


def share(check: bool = False) -> str:
    """Return path to shared folder.

    Args:
        check(bool): check existence of path
    Returns:
        path from global variable
    Raises:
        SystemExit if check is True and path does not exists
        SystemExit if global env var does not exist
    """
    return _path_from_env(COMMON, check=check)


def tmp(check: bool = False) -> str:
    """Return path to tmp folder.

    Args:
        check(bool): check existence of path
    Returns:
        path from global variable
    Raises:
        SystemExit if check is True and path does not exists
        SystemExit if global env var does not exist
    """
    return _path_from_env(TMP, check=check)


def export(common: str, todo: str, ready: str):  # pylint:disable=W0621
    """Set environment variables"""
    os.environ[COMMON] = str(common)
    os.environ[TODO] = str(todo)
    os.environ[READY] = str(ready)


def environment(check: bool = False):
    """Return `SHARED_TODO` and `SHARED_READY` folder."""
    todo_ = todo(check=check)
    ready_ = ready(check=check)
    common = share(check=check)

    return common, todo_, ready_


def _path_from_env(env: str, check: bool = False):
    """Access global env variable."""
    assert env
    try:
        path = os.environ[env]
        if check and not os.path.exists(path):
            utila.error('Path does not exists: %s' % path)
            exit(utila.FAILURE)
        return path
    except KeyError:
        utila.error('Missing environment var `%s`' % env)
        exit(utila.FAILURE)


def check_startup():
    """Check that global environments are set."""
    ready(check=True)
    share(check=True)
    tmp(check=True)
    todo(check=True)
