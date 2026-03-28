# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest
import utilo

import configos

DUMP = """\
SHARED_SPACE                            /tmp/shared
HOSTNAME                                36049c61e901
SHLVL                                   2
HOME                                    /root
SHARED_READY                            /tmp/shared/ready
PATH                                    /opt/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
BAW                                     /tmp/dev
SHARED_TODO                             /tmp/shared/todo
PYLINTHOME                              /tmp/pylint
PYTEST_PLUGINS                          pytester
PWD                                     /var/workdir
SHARED_TMP                              /tmp/shared/tmp
PYTEST_VERSION                          9.0.2
"""

DUMP_SIZE_MIN = len(DUMP)


def test_env_dump():
    dumped = configos.env_dump()
    assert len(dumped) > DUMP_SIZE_MIN / 2


def test_env_get_set_del():
    with pytest.raises(KeyError):
        configos.env('abc')

    configos.env_set('abc', 10)
    assert configos.env('abc') == '10'

    configos.env_del('abc')
    with pytest.raises(KeyError):
        configos.env('abc')


CONFIG = """\
kiwi_rawmaker = 10
kiwi_rawmaker_asd = 15
ciwi_detector = Hier Spricht Helm
"""


def test_env_load_unload(td):
    config = td.tmpdir.join('config.ini')
    utilo.file_create(config, CONFIG)

    with pytest.raises(KeyError):
        configos.env('kiwi_rawmaker')

    configos.env_load(config)

    assert configos.env('kiwi_rawmaker') == '10'
    assert configos.env('kiwi_rawmaker_asd') == '15'
    assert configos.env('ciwi_detector') == 'Hier Spricht Helm'

    configos.env_unload(config)

    with pytest.raises(KeyError):
        configos.env('kiwi_rawmaker')


def test_env_unload(td):
    path = td.tmpdir.join('config.ini')
    utilo.file_create(path, CONFIG)
    before = configos.env_dump()
    configos.env_load(path)
    after = configos.env_dump()
    configos.env_unload(path)
    final = configos.env_dump()

    assert before != after
    assert final == before
