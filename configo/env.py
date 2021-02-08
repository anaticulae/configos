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


def env(name: str, default=None):
    try:
        return os.environ[name]
    except KeyError as error:
        if default is None:
            raise error
    return default


def env_set(name: str, value: str):
    value = str(value)
    os.environ[name] = value


def env_del(name: str):
    del os.environ[name]


def load(path: str):
    assert os.path.exists(path), str(path)
    loaded = utila.file_read(path)
    config = utila.load_config(loaded, flat=True)
    for key, value in config.items():
        env_set(key, value)


def unload(path: str):
    assert os.path.exists(path), str(path)
    loaded = utila.file_read(path)  # TODO: REPLACE WITH UTILA CODE
    config = utila.load_config(loaded, flat=True)
    for key in config.keys():
        env_del(key)


def dump() -> str:
    collected = []
    for key, value in os.environ.items():
        collected.append('{:<40}{}'.format(key, value))
    result = utila.NEWLINE.join(collected)
    return result
