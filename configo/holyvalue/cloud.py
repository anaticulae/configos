# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""\
Environment variables:

>>> HC_RAWMAKER = 'rawmaker'
>>> HC_WORDS = '/c/holyclound/words341.hv'
"""

import utilo

import configo

HC_CLOUD_BASE = 'HC_CLOUD_BASE'


def cloud_lookup(program: str, base: str = None):
    envname = holyname(program)
    env = configo.env(envname, default=None)
    if env is None:
        return
    if base:
        configo.init(base)
    if utilo.isfilepath(env):
        if not utilo.exists(env):
            utilo.error(f'invalid holy value path[env:{envname}]: {env}')
            return
        base = utilo.path_parent(env)
        name = utilo.file_name(env)
        # hv-file path
        configo.load(name=name, base=base)
        return
    # hv-file name
    configo.load(name=env)


def cloud_set(program: str, namepath: str = None):
    if not namepath:
        namepath = program
    program = holyname(program)
    configo.env_set(program, value=namepath)


def cloud_unset(program: str):
    program = holyname(program)
    configo.env_del(program)


def cloud_base_set(path: str):
    if path is None:
        configo.env_del(HC_CLOUD_BASE)
        return
    configo.env_set(HC_CLOUD_BASE, path)


def cloud_base() -> str:
    result = configo.env(HC_CLOUD_BASE, default=None)
    return result


def holyname(program: str) -> str:
    """\
    >>> holyname('rawmaker')
    'HC_RAWMAKER'
    """
    assert program
    program = program.upper()
    return f'HC_{program}'
