# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os
from os import makedirs
from os.path import join

from pytest import raises

from configo import check_startup
from configo import ready
from configo import todo
from configo.share import COMMON
from configo.share import READY
from configo.share import TODO
from configo.share import environment
from configo.share import export


def test_missing_environment(monkeypatch):
    """The communication folder for the view and pdf-mining is defined by
    shared folder `SHARED_TODO` and `SHARED_READY`"""
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


def test_export_import(tmpdir, monkeypatch):
    with monkeypatch.context() as context:
        # Remove all environment vars
        context.setattr(os, 'environ', {})

        todo = join(tmpdir, 'todo')
        ready = join(tmpdir, 'ready')
        common = join(tmpdir, 'common')

        for item in [todo, ready, common]:
            makedirs(item)

        export(common, todo, ready)
        common_, todo_, ready_, = environment(True)
        print(todo)

        assert todo_ == todo
        assert ready_ == ready
        assert common_ == common


def test_without_folder_configuration(monkeypatch):

    with monkeypatch.context() as context:
        # Remove all environment vars
        context.setattr(os, 'environ', {})

        with raises(SystemExit):
            environment()


def test_with_wrong_folder_configuration(monkeypatch):
    """The communication folder for the view and pdf-mining is defined by
    shared folder `SHARED_TODO` and `SHARED_READY`"""

    with monkeypatch.context() as context:
        # Remove all environment vars
        context.setattr(
            os, 'environ', {
                'SHARED_SPACE': 'NO_PATH',
                'SHARED_TODO': 'NO_PATH',
                'SHARED_READY': 'NO_PATH',
            })

        with raises(SystemExit):
            environment(check=True)
