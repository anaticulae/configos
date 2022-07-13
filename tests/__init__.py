# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila
import utilatest

import configo

TEST_DATA = utila.join(configo.ROOT, 'tests')
HVEXAMPLE = utila.join(TEST_DATA, 'hvexample')
RESULT = utila.join(TEST_DATA, 'examples/result')

run, fail = utilatest.create_cli_runner(configo)
