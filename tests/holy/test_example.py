# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utilatest

import configo


@utilatest.longrun
def test_generate_rawmaker():
    import rawmaker  # pylint:disable=C0415
    generated = configo.generate(rawmaker.ROOT)
    assert '[rawmaker.rawmaker.' in generated
    assert '# default:' in generated
