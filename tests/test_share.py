# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# Tis file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os
from os import makedirs
from os.path import join

from configo import check_startup
from configo import ready
from configo import todo
from configo.share import COMMON
from configo.share import READY
from configo.share import TODO
from pytest import raises


def test_missing_environment(monkeypatch):
    with monkeypatch.context() as context:
        # Remove all environment vars
        context.setattr(os, 'environ', {})

        with raises(SystemExit):
            check_startup()

        with raises(SystemExit):
            todo()

        with raises(SystemExit):
            ready()


def test_wrong_todo(monkeypatch):
    with monkeypatch.context() as context:
        context.setattr(
            os, 'environ', {
                TODO: 'ThisPathDoesNotExist',
                READY: 'ThisPathDoesNotExist',
                COMMON: 'ThisPathDoesNotExist',
            })

        with raises(SystemExit):
            todo(check=True)

        with raises(SystemExit):
            ready(check=True)


def test_startup(tmpdir, monkeypatch):
    makedirs(join(tmpdir, 'todo'))
    makedirs(join(tmpdir, 'ready'))
    with monkeypatch.context() as context:
        context.setattr(
            os, 'environ', {
                TODO: join(tmpdir, 'todo'),
                READY: join(tmpdir, 'ready'),
                COMMON: tmpdir
            })
        check_startup()
