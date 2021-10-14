# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""\
Environment variables:

>>> HC_RAWMAKER = 'rawmaker'
>>> HC_WORDS = '/c/holyclound/words341.hv'
"""

import utila

import configo


def cloud_lookup(program: str, base: str = None):
    envname = holyname(program)
    env = configo.env(envname)
    if env is None:
        return
    if base:
        configo.init(base)
    if utila.isfilepath(env):
        if not utila.exists(env):
            utila.error(f'invalid holy value path[env:{envname}]: {env}')
            return
        base = utila.path_parent(env)
        name = utila.file_name(env)
        # hv-file path
        configo.load(name=name, base=base)
        return
    # hv-file name
    configo.load(name=env)


def holyname(program: str) -> str:
    """\
    >>> holyname('rawmaker')
    'HC_RAWMAKER'
    """
    assert program
    program = program.upper()
    return f'HC_{program}'
