# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import importlib.util

import utila


def load_module(path: str):
    """\
    >>> load_module(__file__).__name__
    'configo.utils'
    """
    item = utila.file_name(path)
    parent = utila.file_name(utila.path_parent(path))
    spec = importlib.util.spec_from_file_location(
        f'{parent}.{item}',
        path,
    )
    try:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    except Exception:  # pylint:disable=broad-except
        return None
    return module
