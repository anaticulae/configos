# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib
import os


@contextlib.contextmanager
def chdir(path: str):
    # TODO: MOVE TO UTILA
    assert os.path.exists(path)

    before = os.getcwd()

    os.chdir(path)
    try:
        yield
    except Exception:
        os.chdir(before)
        raise
    else:
        os.chdir(before)
