# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import utilotest

import configo


@utilotest.longrun
def test_generate_rawmaker():
    import rawmaker  # pylint:disable=C0415
    source = os.path.join(rawmaker.ROOT, 'rawmaker')
    generated = configo.generate(source)
    assert '[rawmaker.' in generated
    assert 'DIFF_MAX = [' in generated
