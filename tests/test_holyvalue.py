# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import inspect
import os

import pytest
import utilo
import utilotest

import configos
import configos.holyvalue
import configos.holyvalue.data
import configos.holyvalue.store
import tests

EXAMPLE = os.path.join(tests.TEST_DATA, 'examples')
FIRST_ONE = 'first_one'


@pytest.fixture
def default_one():
    """Init `DataBase` with `FIRST_ONE` example"""
    configos.init(EXAMPLE)
    configos.load(FIRST_ONE)


def test_holyvalue_load_databas():
    parsed = configos.holyvalue.store.parse(
        os.path.join(EXAMPLE, f'{FIRST_ONE}.hv'),
        FIRST_ONE,
    )
    assert parsed
    assert len(parsed.data) == 2


@pytest.mark.usefixtures('default_one')
def test_holyvalue_hv():
    distance = configos.HV(group='groupme.footer.header', name='DISTANCE')
    # No convertion is done, cause of not defining `datatype`
    assert distance == '50022', distance


@pytest.mark.usefixtures('default_one')
def test_holyvalue_hv_group_from_module(mp):
    """Test to determine variable out of module and variable assignment"""

    def getmodule(__=None, _=None):  # pylint:disable=W0613
        # patch object.__name__
        return type('groupme.footer.header', (tuple,), {})

    with mp.context() as context:
        context.setattr(inspect, 'getmodule', getmodule)
        distance = configos.HV(
            datatype=configos.holyvalue.data.DataType.INT_PLUS,
            limit=60000,
        )

    assert distance == 50022, distance


def test_holyvalue_hv_use_default(capsys):
    """Test returning `default` value for non defined variables and
    inform developer about this."""
    default = 'Helm'
    with utilo.level_tmp(utilo.Level.DEBUG):
        result = configos.HV(default=default).value
    assert result == default
    # ensure to log warning
    stdout = utilotest.stdout(capsys)
    assert 'not defined' in stdout, stdout


def test_holyvalue_hv_use_no_default():
    with pytest.raises(configos.MissingHolyValue):
        _ = configos.HV().value


def test_holyvalue_invalid_variable():
    """Test that variable not exists"""

    with pytest.raises(configos.MissingHolyValue):
        _ = configos.HV(
            group='groupme.footer.header',
            name='does_not_exists',
        ).value

    # use default value instead of throwing MissingHolyValue-Exception
    default = 100
    got = configos.HV(
        group='groupme.footer.header',
        name='does_not_exists',
        default=100,
    )
    assert got == default


@pytest.mark.usefixtures('default_one')
@pytest.mark.parametrize('datatype', sorted(configos.NOMATH, key=lambda x: x.name)) # yapf:disable
def test_holyvalue_invalid_limit(datatype):
    """Test to determine variable out of module and variable assignment"""
    with pytest.raises(configos.InvalidHolyValue):
        _ = configos.HV(
            group='groupme.footer.header',
            name='distance',
            datatype=datatype,
            limit=100,  # LIMIT IS HIGHER THAN DEFINED 50022 in first_one.hv
        ).value


def test_holyvalue_generate_configuration():
    """If this test fails, check holyvalue() signature and config generator"""
    config = configos.generate(tests.HVEXAMPLE)
    assert config is not None
    assert len(config) > 200, 'no enough content'

    keys = ['FIRST', 'SECOND', 'THIRD', 'LEVEL_UP', 'HELMUT']
    for key in keys:
        assert f'{key} = ' in config, utilo.log_raw(config)

    variables = ['default', 'limit', 'datatype', 'comment']
    for variable in variables:
        assert f'# {variable}:' in config, print(config)

    assert config.count('#') >= 5, utilo.log_raw(config)


def test_holyvalue_generate_and_load(td):
    path = td.tmpdir.join('config.hv')
    # create config
    config = configos.generate(tests.HVEXAMPLE)
    utilo.file_create(path, config)
    # parse config
    parsed = configos.holyvalue.store.parse(path, 'config')
    assert parsed


def test_holyvalue_evaluate_percent_plus():
    with pytest.raises(configos.InvalidHolyValue):
        _ = configos.HV(
            default=15,
            limit=10,
            datatype=configos.DataType.PERCENT_PLUS,
        )


def test_holyvalue_less_verbose_api():
    access = configos.HV_INT_PLUS(default=5)
    assert access == 5


def test_holyvalue_default_database():
    hello = configos.HV_INT_PLUS(default=5)
    assert hello == 5


def test_holyvalue_right_hand_evaluation_name_and_group():
    abc = configos.HV(
        name='alpha',
        default=15,
        limit=120,
        datatype=configos.DataType.PERCENT_PLUS,
    )
    assert abc.name == 'alpha'
    # TODO: ENABLE LATER
    # assert abc.group == 'tests.test_holyvalue'


def test_holyvalue_operation():
    smaller = configos.HV(
        default=5,
        name='smaller',
        datatype=configos.DataType.INT,
    )
    value = configos.HV(
        default=15,
        name='alpha',
        datatype=configos.DataType.INT,
    )
    string = configos.HV(
        default='string',
        name='alpha',
        datatype=configos.DataType.STR,
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


def test_hv_ranged():
    start = configos.HV_INT_PLUS(default=10)
    end = configos.HV_INT_PLUS(default=20)
    assert len(utilo.rtuple(start, end)) == end - start


def test_hv_slice():
    data = [1, 2, 3, 4, 5, 6, 7]
    start = configos.HV_INT_PLUS(default=2)
    selected = data[start:]
    assert selected == [3, 4, 5, 6, 7]
