# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest

import configos


def test_second_fine():
    _ = configos.HV_SECOND(default=32)


def test_second_failure():
    with pytest.raises(configos.InvalidHolyValue):
        _ = configos.HV_SECOND(default=-32)
    with pytest.raises(configos.InvalidHolyValue):
        _ = configos.HV_SECOND(default=16.0)


def test_api_prefix():
    _ = configos.HV_API(default='/api/v0')


def test_secret_key():
    value = 'iamimportant'
    secret = configos.HV_SECRET(default=value)
    assert isinstance(secret.value, bytes)


def test_xb():
    kb = configos.HV_KB(default=25)  # pylint:disable=C0103
    assert kb == 25 * 1024
    mb = configos.HV_MB(default=25)  # pylint:disable=C0103
    assert mb == 25 * 1024 * 1024
    gb = configos.HV_GB(default=25)  # pylint:disable=C0103
    assert gb == 25 * 1024 * 1024 * 1024
