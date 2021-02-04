# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest
import utila

import configo


def test_env_dump(testdir):
    dumped = configo.dump_env()
    assert len(dumped) > 1000


def test_env_get_set_del():
    with pytest.raises(KeyError):
        configo.env('abc')

    configo.env_set('abc', 10)
    assert configo.env('abc') == '10'

    configo.env_del('abc')
    with pytest.raises(KeyError):
        configo.env('abc')


CONFIG = """\
kiwi_rawmaker = 10
kiwi_rawmaker_asd = 15
ciwi_detector = Hier Spricht Helm
"""


def test_env_load_unload(testdir):
    utila.file_create('config.ini', CONFIG)

    with pytest.raises(KeyError):
        configo.env('kiwi_rawmaker')

    configo.load_env('config.ini')

    assert configo.env('kiwi_rawmaker') == '10'
    assert configo.env('kiwi_rawmaker_asd') == '15'
    assert configo.env('ciwi_detector') == 'Hier Spricht Helm'

    configo.unload_env('config.ini')

    with pytest.raises(KeyError):
        configo.env('kiwi_rawmaker')
