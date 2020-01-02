# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from configo import OneSideDINA4
from configo import OneSideDINA5


def test_configuration_access():
    border = OneSideDINA4.pageborder
    left, right, top, bottom = border  # pylint: disable=unused-variable


def test_different_pagesize():
    assert len(OneSideDINA4.pagesize) == len(OneSideDINA5.pagesize)
    assert len(OneSideDINA4.pagesize) == 2
    assert OneSideDINA4.pagesize != OneSideDINA5.pagesize

    assert len(OneSideDINA4.pageborder) == len(OneSideDINA5.pageborder)
