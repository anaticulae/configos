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


def evaluate(inpath: list, noskip=False) -> int:
    skip = None if noskip else skips
    for path in inpath:
        if not utila.exists(path):
            utila.error(f'input does not exists: {path}')
            return utila.FAILURE
    done = False
    for item in inpath:
        collected = configo.generate(item, skips=skip)
        if not collected:
            continue
        utila.print_banner(text=item, symbol='#')
        utila.log(collected)
        done = True
    if not done:
        utila.error('could not locate any HolyValue')
        return utila.FAILURE
    return utila.SUCCESS


def skips(item: str) -> bool:
    item = str(item)
    return 'build' in item or 'tests' in item
