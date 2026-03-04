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
import tests


def test_cloud_config(td):
    program = 'markers'
    source = tests.TEST_DATA
    holyconfig = td.tmpdir.join('config.hv')
    utilo.run(f'configos --generate -i {source} --noskip >> config.hv')
    configos.cloud_set(program, holyconfig)
    configos.cloud_lookup(program)
    holypath = configos.env(configos.holyname(program))
    assert holypath
    assert holypath == holyconfig
    # unload config
    configos.cloud_unset(program)
    with pytest.raises(KeyError):
        # config was unloaded
        configos.env(configos.holyname(program))
