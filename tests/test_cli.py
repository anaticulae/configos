# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utilotest

import tests


def test_cli(mp):
    tests.run('--help', mp=mp)


def test_cli_generate(mp, capsys):
    source = tests.TEST_DATA
    tests.run(
        f'--generate -i {source} --noskip',
        mp=mp,
    )
    stdout = utilotest.stdout(capsys)
    assert 'HELMUT = None' in stdout
    assert len(stdout) >= 861


def test_cli_result_show(mp):
    result = tests.RESULT
    tests.run(
        f'optimize --show {result}',
        mp=mp,
    )


# @utilotest.longrun
# def test_cli_create_run_show(td, mp):
#     root = configos.ROOT
#     plan = utilo.forward_slash(str(td.tmpdir.join('plan.hv')))
#     with utilo.capture_stdout() as buffer:
#         tests.run(
#             f'optimize --create {root}',
#             mp=mp,
#         )
#     plan_content = buffer()
#     utilo.file_create(plan, plan_content)
#     utilo.run('baw init myproject "helm is here"')
#     with utilo.capture_stdout() as buffer:
#         tests.run(
#             f'optimize -r 2 --run {plan} ',
#             mp=mp,
#         )
#     # determine result path out of logging
#     result = buffer().strip()
#     path = utilo.search(r'outdir\:[ ](.+?)\n', result)[1]
#     path = utilo.join(path, 'result')
#     tests.run(
#         f'optimize --show {path}',
#         mp=mp,
#     )
