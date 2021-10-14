# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import inspect
import os

import pytest
import utila
import utilatest

import configo
import configo.holyvalue
import configo.holyvalue.data
import configo.holyvalue.store
import tests

EXAMPLE = os.path.join(tests.TEST_DATA, 'examples')
FIRST_ONE = 'first_one'


@pytest.fixture
def default_one():
    """Init `DataBase` with `FIRST_ONE` example"""
    configo.init(EXAMPLE)
    configo.load(FIRST_ONE)


def test_holyvalue_load_databas():
    parsed = configo.holyvalue.store.parse(EXAMPLE, FIRST_ONE)
    assert parsed
    assert len(parsed.data) == 2


@pytest.mark.usefixtures('default_one')
def test_holyvalue_hv():
    distance = configo.HV(group='groupme.footer.header', name='DISTANCE')
    # No convertion is done, cause of not defining `datatype`
    assert distance == '50022', distance


@pytest.mark.usefixtures('default_one')
def test_holyvalue_hv_group_from_module(monkeypatch):
    """Test to determine variable out of module and variable assignment"""

    def getmodule(__=None, _=None):  # pylint:disable=W0613
        # patch object.__name__
        return type('groupme.footer.header', (tuple,), {})

    with monkeypatch.context() as context:
        context.setattr(inspect, 'getmodule', getmodule)
        distance = configo.HV(
            datatype=configo.holyvalue.data.DataType.INT_PLUS,
            limit=60000,
        )

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
    stdout = utilatest.stdout(capsys)
    assert 'not defined' in stdout, stdout


def test_holyvalue_hv_use_no_default():
    with pytest.raises(configo.MissingHolyValue):
        _ = configo.HV().value


def test_holyvalue_invalid_variable():
    """Test that variable not exists"""

    with pytest.raises(configo.MissingHolyValue):
        _ = configo.HV(
            group='groupme.footer.header',
            name='does_not_exists',
        ).value

    # use default value instead of throwing MissingHolyValue-Exception
    default = 100
    got = configo.HV(
        group='groupme.footer.header',
        name='does_not_exists',
        default=100,
    )
    assert got == default


@pytest.mark.usefixtures('default_one')
@pytest.mark.parametrize('datatype', configo.NOMATH)
def test_holyvalue_invalid_limit(datatype):
    """Test to determine variable out of module and variable assignment"""
    with pytest.raises(configo.InvalidHolyValue):
        _ = configo.HV(
            group='groupme.footer.header',
            name='distance',
            datatype=datatype,
            limit=100,  # LIMIT IS HIGHER THAN DEFINED 50022 in first_one.hv
        ).value


def test_holyvalue_generate_configuration():
    """If this test fails, check holyvalue() signature and config generator"""
    config = configo.generate(tests.HVEXAMPLE)
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
    path = testdir.tmpdir.join('config.hv')
    # create config
    config = configo.generate(tests.HVEXAMPLE)
    utila.file_create(path, config)
    # parse config
    parsed = configo.holyvalue.store.parse(testdir.tmpdir, 'config')
    assert parsed


def test_holyvalue_evaluate_percent_plus():
    with pytest.raises(configo.InvalidHolyValue):
        hello = configo.HV(  # pylint:disable=unused-variable
            default=15,
            limit=10,
            datatype=configo.DataType.PERCENT_PLUS,
        )


def test_holyvalue_less_verbose_api():
    access = configo.HV_INT_PLUS(default=5)
    assert access == 5


def test_holyvalue_default_database():
    hello = configo.HV_INT_PLUS(default=5)
    assert hello == 5


def test_holyvalue_right_hand_evaluation_name_and_group():
    abc = configo.HV(
        name='alpha',
        default=15,
        limit=120,
        datatype=configo.DataType.PERCENT_PLUS,
    )
    assert abc.name == 'alpha'
    assert abc.group == 'tests.test_holyvalue'


def test_holyvalue_operation():
    smaller = configo.HV(
        default=5,
        name='smaller',
        datatype=configo.DataType.INT,
    )
    value = configo.HV(
        default=15,
        name='alpha',
        datatype=configo.DataType.INT,
    )
    string = configo.HV(
        default='string',
        name='alpha',
        datatype='string',
    )
    assert value + 15 == 30
    assert value + value == 30

    assert value - 15 == 0  # pylint:disable=C2001
    assert value - value == 0  # pylint:disable=C2001

    assert value * 15 == 15 * 15
    assert value * value == 15 * 15

    assert value / 15 == 1
    assert value / value == 1

    assert value % 2 == 1
    assert value % value == 0  # pylint:disable=C2001

    assert value >= (value * 0.5)
    assert smaller <= value  # pylint:disable=comparison-with-itself

    assert value == value  # pylint:disable=comparison-with-itself

    assert value > (value * 0.5)
    assert smaller < (value * 2)

    assert (value * 2) > value
    assert (value * 2) >= value

    assert value != (value * 2)
    assert value
    assert value is value  # pylint:disable=comparison-with-itself

    assert string == string  # pylint:disable=comparison-with-itself
