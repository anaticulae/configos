# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utilatest

import tests


def test_cli(monkeypatch):
    tests.run('--help', monkeypatch=monkeypatch)


def test_cli_generate(monkeypatch, capsys):
    source = tests.TEST_DATA
    tests.run(
        f'--generate -i {source} --noskip',
        monkeypatch=monkeypatch,
    )
    stdout = utilatest.stdout(capsys)
    assert 'HELMUT = None' in stdout
    assert len(stdout) >= 861


def test_cli_result_show(monkeypatch):
    result = tests.RESULT
    tests.run(
        f'optimize --show {result}',
        monkeypatch=monkeypatch,
    )
