# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

import configo
import tests


def test_cloud_config(testdir):
    source = tests.TEST_DATA
    utila.run(f'configo --generate -i {source} --noskip >> config.hv')
    configo.cloud_set('markers', testdir.tmpdir.join('config.hv'))
    configo.cloud_lookup('markers')
    assert configo.env(configo.holyname('markers'))
