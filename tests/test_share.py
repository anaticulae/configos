# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import pytest

import configos
import configos.directory


def test_missing_environment(mp):
    """The communication folder for the view and pdf-mining is defined by
    shared folder `SHARED_TODO` and `SHARED_READY`"""
    with mp.context() as context:
        # Remove all environment vars
        context.setattr(os, 'environ', {})

        with pytest.raises(SystemExit):
            configos.check_startup()

        with pytest.raises(SystemExit):
            configos.todo()

        with pytest.raises(SystemExit):
            configos.ready()


def test_wrong_todo(mp):
    with mp.context() as context:
        context.setattr(
            os, 'environ', {
                configos.directory.TODO: 'ThisPathDoesNotExist',
                configos.directory.READY: 'ThisPathDoesNotExist',
                configos.directory.COMMON: 'ThisPathDoesNotExist',
            })

        with pytest.raises(SystemExit):
            configos.todo(check=True)

        with pytest.raises(SystemExit):
            configos.ready(check=True)


def test_startup(td, mp):
    root = str(td)
    ready = os.path.join(root, 'ready')
    tmp = os.path.join(root, 'tmp')
    todo = os.path.join(root, 'todo')
    for item in (ready, tmp, todo):
        os.makedirs(item)

    with mp.context() as context:
        context.setattr(
            os, 'environ', {
                configos.directory.TODO: todo,
                configos.directory.READY: ready,
                configos.directory.TMP: tmp,
                configos.directory.COMMON: root
            })
        configos.check_startup()


def test_export_import(tmpdir, mp):
    with mp.context() as context:
        # Remove all environment vars
        context.setattr(os, 'environ', {})

        todo = os.path.join(tmpdir, 'todo')  #pylint:disable=W0621
        ready = os.path.join(tmpdir, 'ready')  #pylint:disable=W0621
        common = os.path.join(tmpdir, 'common')

        for item in (todo, ready, common):
            os.makedirs(item)

        configos.export(common, todo, ready)
        common_, todo_, ready_, = configos.environment(True)

        assert todo_ == todo
        assert ready_ == ready
        assert common_ == common


def test_without_folder_configuration(mp):

    with mp.context() as context:
        # Remove all environment vars
        context.setattr(os, 'environ', {})

        with pytest.raises(SystemExit):
            configos.environment()


def test_with_wrong_folder_configuration(mp):
    """The communication folder for the view and pdf-mining is defined by
    shared folder `SHARED_TODO` and `SHARED_READY`"""

    with mp.context() as context:
        # Remove all environment vars
        context.setattr(
            os, 'environ', {
                'SHARED_SPACE': 'NO_PATH',
                'SHARED_TODO': 'NO_PATH',
                'SHARED_READY': 'NO_PATH',
            })

        with pytest.raises(SystemExit):
            configos.environment(check=True)
