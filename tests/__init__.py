# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utilo
import utilotest

import configos

TEST_DATA = utilo.join(configos.ROOT, 'tests')
HVEXAMPLE = utilo.join(TEST_DATA, 'hvexample', exist=True)
RESULT = utilo.join(TEST_DATA, 'examples/result', exist=True)

run, fail = utilotest.create_cli_runner(configos)
