# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configparser
import functools
import os

import utilo

import configos.exception
import configos.holyvalue
import configos.holyvalue.data

DATABASE = None


class DataBase:
    """Define facade to access variable via `group` and `variable` name."""

    def __init__(self, path: str, current: str = None):
        """Setup `DataBase` with no `current` DataSet. Use `load` or
        `current` to init `DataSet`.

        Args:
            path(str): folder with different `DataSet`s
            current(str): name of default dataset
        """
        if not current:
            current = configos.holyvalue.data.DataSet()
        self.path = path
        self.current = current

    def load(self, name: str, path: str = None):
        path = path if path else self.path
        path = os.path.join(path, f'{name}.hv')
        utilo.info(f'load path: {path}')
        parsed = parse(path, name)
        self.current = parsed

    @functools.lru_cache(maxsize=1024)
    def get(self, group: str, variable: str, default=None):
        if group:
            group = group.lower()
        if variable:
            variable = variable.upper()

        def default_warning():
            msg = f'not defined in database {group}:{variable}; use default: {default}'
            utilo.info(msg)

        # determine hv-group
        _group = self.current.data.get(group, None)  # pylint:disable=E1101
        if not _group:
            if default is not None:
                default_warning()
                return default
            raise configos.exception.MissingHolyValue(f'invalid group: {group}')
        # determine hv-name
        variable = variable.upper()
        _var = _group.data.get(variable.upper(), None)
        if not _var:
            if default is not None:
                default_warning()
                return default
            msg = f'invalid variable: {group}:{variable}'
            raise configos.exception.MissingHolyValue(msg)
        return _var.value


def parse(path, name: str = None) -> 'DataSet':
    # load config
    raw = utilo.from_raw_or_path(path, ftype='ini')
    parser = configparser.ConfigParser()
    parser.read_string(raw)
    # prepare data
    dataset = configos.holyvalue.data.DataSet(name=name)
    for groupname, groupdata in parser.items():
        if groupname == 'DEFAULT':
            continue
        groupname = groupname.lower()
        group = configos.holyvalue.data.Group(name=groupname)
        for datakey, data in groupdata.items():
            datakey = datakey.upper()
            datum = configos.holyvalue.data.Datum(name=datakey, value=data)
            group.data[datakey] = datum  # pylint:disable=E1137
        dataset.data[groupname] = group  # pylint:disable=E1137
    return dataset


def init(path: str):
    """Init `DATABASE` with configuration `path`."""
    assert path is None or os.path.exists(path), f'path does not exists: {path}'
    global DATABASE  # pylint:disable=global-statement
    DATABASE = DataBase(path)


def load(name: str, base: str = None):
    """Load `DATABASE` with dataset of `name`."""
    database().load(name=name, path=base)


def database():
    """Access global variable `DATABASE`"""
    return DATABASE
