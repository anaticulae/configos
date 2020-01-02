# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import pytest

import configo
import configo.directory


def test_missing_environment(monkeypatch):
    """The communication folder for the view and pdf-mining is defined by
    shared folder `SHARED_TODO` and `SHARED_READY`"""
    with monkeypatch.context() as context:
        # Remove all environment vars
        context.setattr(os, 'environ', {})

        with pytest.raises(SystemExit):
            configo.check_startup()

        with pytest.raises(SystemExit):
            configo.todo()

        with pytest.raises(SystemExit):
            configo.ready()


def test_wrong_todo(monkeypatch):
    with monkeypatch.context() as context:
        context.setattr(
            os, 'environ', {
                configo.directory.TODO: 'ThisPathDoesNotExist',
                configo.directory.READY: 'ThisPathDoesNotExist',
                configo.directory.COMMON: 'ThisPathDoesNotExist',
            })

        with pytest.raises(SystemExit):
            configo.todo(check=True)

        with pytest.raises(SystemExit):
            configo.ready(check=True)


def test_startup(testdir, monkeypatch):
    root = str(testdir)
    ready = os.path.join(root, 'ready')
    tmp = os.path.join(root, 'tmp')
    todo = os.path.join(root, 'todo')
    for item in [ready, tmp, todo]:
        os.makedirs(item)

    with monkeypatch.context() as context:
        context.setattr(
            os, 'environ', {
                configo.directory.TODO: todo,
                configo.directory.READY: ready,
                configo.directory.TMP: tmp,
                configo.directory.COMMON: root
            })
        configo.check_startup()


def test_export_import(tmpdir, monkeypatch):
    with monkeypatch.context() as context:
        # Remove all environment vars
        context.setattr(os, 'environ', {})

        todo = os.path.join(tmpdir, 'todo')  #pylint:disable=W0621
        ready = os.path.join(tmpdir, 'ready')  #pylint:disable=W0621
        common = os.path.join(tmpdir, 'common')

        for item in [todo, ready, common]:
            os.makedirs(item)

        configo.export(common, todo, ready)
        common_, todo_, ready_, = configo.environment(True)

        assert todo_ == todo
        assert ready_ == ready
        assert common_ == common


def test_without_folder_configuration(monkeypatch):

    with monkeypatch.context() as context:
        # Remove all environment vars
        context.setattr(os, 'environ', {})

        with pytest.raises(SystemExit):
            configo.environment()


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

        with pytest.raises(SystemExit):
            configo.environment(check=True)
