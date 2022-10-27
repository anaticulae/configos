# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest

import configo


def test_second_fine():
    _ = configo.HV_SECOND(default=32)


def test_second_failure():
    with pytest.raises(configo.InvalidHolyValue):
        _ = configo.HV_SECOND(default=-32)
    with pytest.raises(configo.InvalidHolyValue):
        _ = configo.HV_SECOND(default=16.0)


def test_api_prefix():
    _ = configo.HV_API(default='/api/v0')


def test_secret_key():
    value = 'iamimportant'
    secret = configo.HV_SECRET(default=value)
    assert isinstance(secret.value, bytes)
