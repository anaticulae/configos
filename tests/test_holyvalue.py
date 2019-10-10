# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import inspect
import os

import pytest
import utila

import configo
import configo.holyvalue
import tests

EXAMPLE = os.path.join(tests.TEST_DATA, 'examples')
FIRST_ONE = 'first_one'


@pytest.fixture
def default_one():
    """Init `DataBase` with `FIRST_ONE` example"""
    configo.init(EXAMPLE)
    configo.load(FIRST_ONE)


def test_holyvalue_load_databas():
    parsed = configo.holyvalue.parse(EXAMPLE, FIRST_ONE)
    assert parsed
    assert len(parsed.data) == 2


@pytest.mark.usefixtures('default_one')
def test_holyvalue_hv():
    distance = configo.HV(group='groupme.footer.header', variable='DISTANCE')
    # No convertion is done, cause of not defining `datatype`
    assert distance == '50022', distance


@pytest.mark.usefixtures('default_one')
def test_holyvalue_hv_group_from_module(monkeypatch):
    """Test to determine variable out of module and variable assignment"""

    def getmodule(__=None, _=None):  # pylint:disable=W0613
        # TODO: realy bad mock
        class Back:  # pylint:disable=R0903
            __name__ = 'groupme.footer.header'

        return Back()

    with monkeypatch.context() as context:
        context.setattr(inspect, 'getmodule', getmodule)
        distance = configo.HV(
            datatype=configo.holyvalue.DataType.INT_PLUS,
            limit=60000,
        )

    assert distance == 50022, distance


@pytest.mark.usefixtures('default_one')
def test_holyvalue_hv_use_default(monkeypatch, capsys):
    """Test returning `default` value for non defined variables and
    inform developer about this."""
    default = 'Helm'

    with monkeypatch.context() as context:
        context.setattr(utila.logger, 'LEVEL', utila.Level.DEBUG)
        result = configo.HV(default=default)
    assert result == default

    # ensure to log warning
    out = capsys.readouterr().out
    assert 'invalid' in out, out


@pytest.mark.usefixtures('default_one')
def test_holyvalue_hv_use_no_default():
    with pytest.raises(ValueError):
        _ = configo.HV()


@pytest.mark.usefixtures('default_one')
def test_holyvalue_invalid_variable():
    """Test that variable not exists"""

    with pytest.raises(configo.MissingHolyValue):
        configo.HV(
            group='groupme.footer.header',
            variable='does_not_exists',
        )

    # use default value instead of throwing MissingHolyValue-Exception
    default = 100
    got = configo.HV(
        group='groupme.footer.header',
        variable='does_not_exists',
        default=100,
    )
    assert got == default


@pytest.mark.usefixtures('default_one')
@pytest.mark.parametrize('datatype', list(configo.DataType))
def test_holyvalue_invalid_limit(datatype):
    """Test to determine variable out of module and variable assignment"""

    with pytest.raises(configo.InvalidHolyValue):
        configo.HV(
            group='groupme.footer.header',
            variable='distance',
            datatype=datatype,
            limit=100,
        )
