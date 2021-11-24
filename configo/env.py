# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import utila

NO_DEFAULT = object()


def env(name: str, default=NO_DEFAULT, group: str = None):
    if group:
        name = f'{group}_{name}'
    try:
        return os.environ[name]
    except KeyError as error:
        if default == NO_DEFAULT:
            raise error
    return default


def env_set(name: str, value: str, group: str = None):
    if group:
        name = f'{group}_{name}'
    value = str(value)
    os.environ[name] = value


def env_del(name: str, group: str = None):
    if group:
        name = f'{group}_{name}'
    del os.environ[name]


def env_load(path: str):
    assert os.path.exists(path), str(path)
    loaded = utila.file_read(path)
    config = utila.load_config(loaded, flat=True)
    for key, value in config.items():
        env_set(key, value)


def env_unload(path: str):
    assert os.path.exists(path), str(path)
    config = utila.load_config(path, flat=True)
    for key in config.keys():
        env_del(key)


def env_dump() -> str:
    collected = []
    for key, value in os.environ.items():
        collected.append('{:<40}{}'.format(key, value))
    result = utila.NEWLINE.join(collected)
    return result
