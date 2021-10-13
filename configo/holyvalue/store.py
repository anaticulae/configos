# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configparser
import os

import utila

import configo.exception
import configo.holyvalue
import configo.holyvalue.data

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
            current = configo.holyvalue.data.DataSet()
        self.path = path
        self.current = current

    def load(self, name: str):
        parsed = parse(self.path, name)
        self.current = parsed

    def get(self, group: str, variable: str, default=None):

        def default_warning():
            msg = f'not defined in database {group}:{variable}; use default: {default}'
            utila.info(msg)

        # determine hv-group
        _group = self.current.data.get(group, None)  # pylint:disable=E1101
        if not _group:
            if default is not None:
                default_warning()
                return default
            raise configo.exception.MissingHolyValue(f'invalid group: {group}')
        # determine hv-name
        variable = variable.upper()
        _var = _group.data.get(variable.upper(), None)
        if not _var:
            if default is not None:
                default_warning()
                return default
            msg = f'invalid variable: {group}:{variable}'
            raise configo.exception.MissingHolyValue(msg)
        return _var.value


def parse(path, name: str = None) -> 'DataSet':
    assert os.path.exists(path), f'path does not exists: {path}'
    datapath = os.path.join(path, f'{name}.{configo.holyvalue.EXT}')
    assert os.path.exists(datapath), f'dataset: {name} does not exists'

    dataset = configo.holyvalue.data.DataSet(name=name)

    parser = configparser.ConfigParser()
    parser.read(datapath, encoding='utf8')

    for groupname, groupdata in parser.items():
        if groupname == 'DEFAULT':
            continue
        group = configo.holyvalue.data.Group(name=groupname)
        for datakey, data in groupdata.items():
            datakey = datakey.upper()
            datum = configo.holyvalue.data.Datum(name=datakey, value=data)
            group.data[datakey] = datum  # pylint:disable=E1137
        dataset.data[groupname] = group  # pylint:disable=E1137
    return dataset


def init(path: str):
    """Init `DATABASE` with configuration `path`."""
    assert path is None or os.path.exists(path), f'path does not exists: {path}'
    global DATABASE  # pylint:disable=global-statement
    DATABASE = DataBase(path)


def load(name: str):
    """Load `DATABASE` with dataset of `name`."""
    database().load(name)


def database():
    """Access global variable `DATABASE`"""
    global DATABASE  # pylint:disable=global-statement
    return DATABASE
