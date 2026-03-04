# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import utilo

NO_DEFAULT = object()


@utilo.cacheme
def env(name: str, default=NO_DEFAULT, group: str = None):
    name = groupname(name, group)
    try:
        return os.environ[name]
    except KeyError as error:
        if default == NO_DEFAULT:
            raise error
    return default


def env_set(name: str, value: str, group: str = None):
    # TODO: MAKE THREAD SAFE?
    name = groupname(name, group)
    value = str(value)
    os.environ[name] = value
    utilo.cache_clear()


def env_del(name: str, group: str = None):
    name = groupname(name, group)
    del os.environ[name]
    utilo.cache_clear()


def env_load(path: str):
    assert os.path.exists(path), str(path)
    loaded = utilo.file_read(path)
    config = utilo.load_config(loaded, flat=True)
    for key, value in config.items():
        env_set(key, value)
    utilo.cache_clear()


def env_unload(path: str):
    assert os.path.exists(path), str(path)
    config = utilo.load_config(path, flat=True)
    for key in config.keys():
        env_del(key)
    utilo.cache_clear()


def env_dump() -> str:
    collected = []
    for key, value in os.environ.items():
        collected.append('{:<40}{}'.format(key, value))
    result = utilo.NEWLINE.join(collected)
    return result


def groupname(name, group):
    """\
    >>> groupname('first', 'master')
    'master_first'
    """
    if not group:
        return name
    return f'{group}_{name}'


def env_path_append(path: str):
    """\
    >>> env_path_append('/d/path/append')
    """
    base = f'{env("PATH")};{path}'
    env_set('PATH', base)
    utilo.debug(f'PATH:{base}')


def env_path_remove(path: str):
    """\
    >>> env_path_append('/d/path/not_there')
    >>> env_path_remove('/d/path/not_there')
    >>> env_path_remove('/d/path/not_there')
    Traceback (most recent call last):
    ...
    ValueError: path does not contain: /d/path/not_there
    """
    base = f'{env("PATH")}'
    remove = f';{path}'
    if remove not in base:
        raise ValueError(f'path does not contain: {path}')
    base = base.replace(remove, '')
    env_set('PATH', base)
