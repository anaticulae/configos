# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest

import configo.cli.optimization
import tests


@pytest.mark.skip(reason='investigate later')
def test_plan_create():
    todo = [tests.HVEXAMPLE]
    plan = configo.cli.optimization.create_plan(todo)
    assert 'TESTS.HVEXAMPLE.SECOND' in plan
