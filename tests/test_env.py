# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest
import utila

import configo


def test_env_dump():
    dumped = configo.env_dump()
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


def test_env_load_unload(td):
    config = td.tmpdir.join('config.ini')
    utila.file_create(config, CONFIG)

    with pytest.raises(KeyError):
        configo.env('kiwi_rawmaker')

    configo.env_load(config)

    assert configo.env('kiwi_rawmaker') == '10'
    assert configo.env('kiwi_rawmaker_asd') == '15'
    assert configo.env('ciwi_detector') == 'Hier Spricht Helm'

    configo.env_unload(config)

    with pytest.raises(KeyError):
        configo.env('kiwi_rawmaker')


def test_env_unload(td):
    path = td.tmpdir.join('config.ini')
    utila.file_create(path, CONFIG)
    before = configo.env_dump()
    configo.env_load(path)
    after = configo.env_dump()
    configo.env_unload(path)
    final = configo.env_dump()

    assert before != after
    assert final == before
