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

HVEXAMPLE = os.path.join(tests.TEST_DATA, 'hvexample')


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
    distance = configo.HV(group='groupme.footer.header', name='DISTANCE').value
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
        ).value

    assert distance == 50022, distance


def test_holyvalue_hv_use_default(monkeypatch, capsys):
    """Test returning `default` value for non defined variables and
    inform developer about this."""
    default = 'Helm'
    with monkeypatch.context() as context:
        context.setattr(utila.logger, 'LEVEL', utila.Level.DEBUG)
        result = configo.HV(default=default).value
    assert result == default

    # ensure to log warning
    out = capsys.readouterr().out
    assert 'invalid' in out, out


def test_holyvalue_hv_use_no_default():
    with pytest.raises(configo.MissingHolyValue):
        _ = configo.HV().value


def test_holyvalue_invalid_variable():
    """Test that variable not exists"""

    with pytest.raises(configo.MissingHolyValue):
        configo.HV(
            group='groupme.footer.header',
            name='does_not_exists',
        ).value

    # use default value instead of throwing MissingHolyValue-Exception
    default = 100
    got = configo.HV(
        group='groupme.footer.header',
        name='does_not_exists',
        default=100,
    ).value
    assert got == default


@pytest.mark.usefixtures('default_one')
@pytest.mark.parametrize('datatype', list(configo.DataType))
def test_holyvalue_invalid_limit(datatype):
    """Test to determine variable out of module and variable assignment"""

    with pytest.raises(configo.InvalidHolyValue):
        configo.HV(
            group='groupme.footer.header',
            name='distance',
            datatype=datatype,
            limit=100,  # LIMIT IS HIGHER THAN DEFINED 50022 in first_one.hv
        ).value


def test_holyvalue_generate_configuration():
    """If this test fails, check holyvalue() signature and config generator"""
    config = configo.generate(HVEXAMPLE)
    assert config is not None
    assert len(config) > 200, 'no enough content'

    keys = ['FIRST', 'SECOND', 'THIRD', 'LEVEL_UP', 'HELMUT']
    for key in keys:
        assert f'{key} = ' in config, utila.log_raw(config)

    variables = ['default', 'limit', 'datatype', 'comment']
    for variable in variables:
        assert f'# {variable}:' in config, print(config)

    assert config.count('#') >= 5, utila.log_raw(config)


def test_holyvalue_generate_and_load(testdir):
    root = str(testdir)
    path = os.path.join(root, 'config.hv')

    config = configo.generate(HVEXAMPLE)
    utila.file_create(path, config)

    parsed = configo.holyvalue.parse(root, 'config')
    assert parsed


def test_holyvalue_evaluate_percent_plus():
    with pytest.raises(configo.InvalidHolyValue):
        hello = configo.HV(  # pylint:disable=unused-variable
            default=15,
            limit=10,
            datatype=configo.DataType.PERCENT_PLUS,
        ).value


def test_holyvalue_less_verbose_api():
    access = configo.HV_INT_PLUS(default=5).value  # pylint:disable=W0612


def test_holyvalue_default_database():
    hello = configo.HV_INT_PLUS(default=5).value  # pylint:disable=W0612


def test_holyvalue_right_hand_evaluation_name_and_group():
    abc = configo.HV(
        name='alpha',
        default=15,
        limit=120,
        datatype=configo.DataType.PERCENT_PLUS,
    )
    assert abc.name == 'alpha'
    assert abc.group == 'tests.test_holyvalue'
