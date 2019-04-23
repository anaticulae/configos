# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# Tis file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

from configo import package_address
from configo import package_configuration
from configo.server import HELPY_EXT_DIRECT
from configo.server import HELPY_EXT_PORT
from configo.server import HELPY_INT_DIRECT
from configo.server import HELPY_INT_PORT
from configo.server import HELPY_URL
from pytest import raises


def test_missing_environment(monkeypatch):
    with monkeypatch.context() as context:
        # Remove all environment vars
        context.setattr(os, 'environ', {})

        with raises(SystemExit):
            package_address()

        with raises(SystemExit):
            package_configuration()


def test_package_adress_and_configuration(monkeypatch):
    with monkeypatch.context() as context:
        # Remove all environment vars
        context.setattr(
            os, 'environ', {
                HELPY_URL: 'http://packages.checkitweg.de',
                HELPY_INT_PORT: 8081,
                HELPY_EXT_PORT: 8082,
                HELPY_INT_DIRECT: HELPY_URL + ':' + HELPY_INT_PORT,
                HELPY_EXT_DIRECT: HELPY_URL + ':' + HELPY_EXT_PORT,
            })

        config = package_configuration()
        assert len(config) == 3

        adress = package_address()
        assert len(adress) == 2
