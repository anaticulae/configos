# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utilo

import configo


def evaluate(inpath: list, noskip=False) -> int:
    """\
    Could not locate any holy value on this file. 1 means failure.
    >>> evaluate([__file__])
    1
    """
    skip = None if noskip else skips
    for path in inpath:
        if not utilo.exists(path):
            utilo.error(f'input does not exists: {path}')
            return utilo.FAILURE
    done = False
    for item in inpath:
        collected = configo.generate(item, skips=skip)
        if not collected:
            continue
        utilo.print_banner(text=item, symbol='#')
        utilo.log(collected)
        done = True
    if not done:
        utilo.error('could not locate any HolyValue')
        return utilo.FAILURE
    return utilo.SUCCESS


def skips(item: str) -> bool:
    """\
    >>> skips('config/tests/__init.py')
    True
    """
    item = str(item)
    return 'build' in item or 'tests' in item
