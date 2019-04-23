# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# Tis file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

from pytest import raises

from configo import check_startup
from configo import ready
from configo import todo


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
                'SHARED_TODO': 'ThisPathDoesNotExist',
                'SHARED_READY': 'ThisPathDoesNotExist'
            })

        with raises(SystemExit):
            todo()

        with raises(SystemExit):
            ready()


def test_startup():
    check_startup()
