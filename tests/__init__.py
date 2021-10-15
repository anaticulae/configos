# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools
import os

import utilatest

import configo
import configo.cli

TEST_DATA = os.path.join(configo.ROOT, 'tests')
HVEXAMPLE = os.path.join(TEST_DATA, 'hvexample')
RESULT = os.path.join(TEST_DATA, 'examples/result')

#pylint: disable=invalid-name
run = functools.partial(
    utilatest.run_command,
    main=configo.cli.main,
    process=configo.PROCESS,
    success=True,
)

failure = functools.partial(
    utilatest.run_command,
    main=configo.cli.main,
    process=configo.PROCESS,
    success=False,
)
