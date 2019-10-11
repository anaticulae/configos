# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import configparser
import dataclasses
import enum
import glob
import inspect
import io
import os
import re
import tokenize
import typing

import utila

import configo.utils

EXT = 'hv'

DATABASE = None


class InvalidHolyValue(ValueError):
    pass


class MissingHolyValue(ValueError):
    pass


def holyvalue(
        variable: str = None,
        group: str = None,
        default=None,
        limit=None,
        datatype: 'DataType' = None,
):
    """Access `holyvalue` via `variable` and `group`.

    Args:
        variable(str): variable name
        group(str): module where `var` is located
        default: define default variable for non defined variable to
                 avoid updating configration to often.
        limit: limit to validate configuration file
        datatype: convert str-based configuration file
    Returns:
        defined holyvalue in `config_name.hv` or `default` one
    Raises:
        InvalidHolyValue: if value of configuration file hits requirements
        MissingHolyValue: if value is not defined and no default one is defined

    TODO: MAKE method update able/facade/callable
    """
    frame = inspect.currentframe()
    if variable is None:
        # TODO: NOT VERY STABLE/ DIRTY
        # determine variable out of code
        levelup = inspect.stack(context=10)[1].code_context
        code = utila.NEWLINE.join(levelup)
        matched = re.search(r'(?P<variable>[\w\d_]+) = configo\.HV\(', code)
        variable = str(matched['variable']).strip().upper()

    if group is None:
        # determine call package
        group = inspect.getmodule(frame).__name__

    data = database().get(group=group, variable=variable, default=default)

    data = convert(data, datatype=datatype)

    if not validate(data, datatype=datatype, limit=limit):
        msg = f'invalid holyvalue {data}; limit: {limit}; datatype: {datatype}'
        raise InvalidHolyValue(msg)

    return data


def init(path: str):
    """Init `DATABASE` with configuration `path`."""
    assert os.path.exists(path), f'path does not exists: {path}'
    global DATABASE  # pylint:disable=global-statement
    DATABASE = DataBase(path)


def load(name: str):
    """Load `DATABASE` with dataset of `name`."""
    database().load(name)


def validate(data, datatype=None, limit=None):
    datatype = str(datatype)
    if 'PLUS' in datatype:
        if data < 0.0:
            return False
    if limit is not None:
        if data > limit:
            return False
    return True


def convert(data, datatype=None):
    if datatype is None:
        return data

    # convert value
    datatype = str(datatype)
    if 'INT' in datatype:
        data = int(data)
    if 'FLOAT' in datatype:
        data = float(data)
    if 'PERCENT' in datatype:
        data = float(data)
        data = data * 0.01
    return data


def database():
    """Access global variable `DATABASE`"""
    global DATABASE  # pylint:disable=global-statement
    return DATABASE


class DataBase:
    """Define facade to access variable via `group` and `variable` name."""

    def __init__(self, path: str, current: str = None):
        """Setup `DataBase` with no `current` DataSet. Use `load` or
        `current` to init `DataSet`.

        Args:
            path(str): folder with different `DataSet`s
            current(str): name of default dataset
        """
        self.path = path
        self.current = current

    def load(self, name: str):
        parsed = parse(self.path, name)
        self.current = parsed

    def get(self, group: str, variable: str, default=None):

        def default_warning():
            msg = f'invalid {group}:{variable}; use default: {default}'
            utila.info(msg)

        _group = self.current.data.get(group, None)  # pylint:disable=E1101
        if not _group:
            if default is not None:
                default_warning()
                return default
            raise MissingHolyValue(f'invalid group: {group}')

        variable = variable.upper()
        _var = _group.data.get(variable.upper(), None)
        if not _var:
            if default is not None:
                default_warning()
                return default
            raise MissingHolyValue(f'invalid variable: {group}:{variable}')

        return _var.value


def parse(path, name: str = None):
    assert os.path.exists(path), f'path does not exists: {path}'
    datapath = os.path.join(path, f'{name}.{EXT}')
    assert os.path.exists(datapath), f'dataset: {name} does not exists'

    dataset = DataSet(name=name)

    parser = configparser.ConfigParser()
    parser.read(datapath, encoding='utf8')

    for groupname, groupdata in parser.items():
        if groupname == 'DEFAULT':
            continue
        group = Group(name=groupname)
        for datakey, data in groupdata.items():
            datakey = datakey.upper()
            datum = Datum(name=datakey, value=data)
            group.data[datakey] = datum  # pylint:disable=E1137
        dataset.data[groupname] = group  # pylint:disable=E1137
    return dataset


class DataType(enum.Enum):
    INT = enum.auto()
    INT_PLUS = enum.auto()

    FLOAT = enum.auto()
    FLOAT_PLUS = enum.auto()

    PERCENT = enum.auto()
    PERCENT_PLUS = enum.auto()


@dataclasses.dataclass
class Datum:
    name: str = None
    value: object = None
    description: str = None
    datatype: DataType = None
    limit = None
    unit: str = None


@dataclasses.dataclass
class Group:

    name: str = None
    data: typing.Dict[str, Datum] = dataclasses.field(default_factory=dict)


@dataclasses.dataclass
class DataSet:

    name: str = None
    data: typing.Dict[str, Group] = dataclasses.field(default_factory=dict)


def generate(path: str) -> str:
    """Iterate thrue python files and extract config with holyvalues
    constructs out of project structure.

    Args:
        path(str): project root path
    Returns:
        project configuration file
    """
    assert os.path.exists(path), f'path does not exists: {path}'
    result = {}
    with configo.utils.chdir(path):
        files = list(glob.glob(os.path.join(path, '**/*.py'), recursive=True))
        for item in files:
            relative = utila.make_relative(item, path)
            # TODO: REPLACE WITH MAKE_PACKAGE
            relative = relative.replace('.py', '')
            relative = relative.replace('/', '.')
            code = utila.file_read(item)
            parsed = holyvalue_from_file(code)
            if parsed:
                result[relative] = parsed
    rootpackage = os.path.split(path)[1]

    raw = []
    for package in sorted(result.keys()):
        raw.append(f'[{rootpackage}.{package}]')
        for variable, values in result[package].items():
            for item, value in values.items():
                raw.append(f'# {item}:{value}')
            variable = values.get('variable', variable)
            variable = variable.replace("'", '').upper()
            default = values.get('default', 'None')
            raw.append(f"{variable} = {default}")
            raw.append('')
        raw.append('')
    return utila.NEWLINE.join(raw)


def holyvalue_from_file(sourcecode: str):
    """Parse holyvalues from `sourcecode`

    Args:
        sourcecode(str): python source code file
    Returns:
        dictonary with holyvalues and further configuration parameter,
        eg. limit, variable, group etc.
    """
    lines = codelines(sourcecode)
    result = {}
    lines = set()
    for item in token(code):
        if item.type != 1:
            # skip comments etc.
            continue
        lines.add(item.line.strip())
    for line in lines:
        # TODO: THINK ABOUT USING TOKEN
        pattern = r'\b(?P<variable>[\w\d_]+) = configo\.HV\((?P<config>.*)\)'
        matched = re.match(pattern, line, re.MULTILINE)
        if not matched:
            continue
        variable = matched['variable']
        config = matched['config']
        if config:
            config = [item.split('=', 1) for item in config.split(', ')]
            config = {item[0]: item[1] for item in config}
        else:
            config = {}
        result[variable] = config
    return result


def token(code: str):
    source = tokenize.tokenize(io.BytesIO(code.encode('utf-8')).readline)
    return source
