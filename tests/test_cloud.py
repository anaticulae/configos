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
import tests


def test_cloud_config(td):
    program = 'markers'
    source = tests.TEST_DATA
    holyconfig = td.tmpdir.join('config.hv')
    utila.run(f'configo --generate -i {source} --noskip >> config.hv')
    configo.cloud_set(program, holyconfig)
    configo.cloud_lookup(program)
    holypath = configo.env(configo.holyname(program))
    assert holypath
    assert holypath == holyconfig
    # unload config
    configo.cloud_unset(program)
    with pytest.raises(KeyError):
        # config was unloaded
        configo.env(configo.holyname(program))
