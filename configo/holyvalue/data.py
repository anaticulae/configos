# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib
import dataclasses
import enum
import typing

import utila

import configo


class HolyMixin:
    pass


class DataType(enum.Enum):

    INT = enum.auto()
    INT_PLUS = enum.auto()

    FLOAT = enum.auto()
    FLOAT_PLUS = enum.auto()

    PERCENT = enum.auto()
    PERCENT_PLUS = enum.auto()

    BOOL = enum.auto()
    STR = enum.auto()


NOMATH = {
    item for item in DataType if item not in (
        DataType.BOOL,
        DataType.STR,
    )
}


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


def convert(data, datatype=None):
    """\
    >>> convert(1, DataType.BOOL)
    True
    """
    if datatype is None:
        return data
    # convert value
    datatype = str(datatype)
    if 'INT' in datatype:
        data = int(data)
    elif 'FLOAT' in datatype:
        data = float(data)
    elif 'PERCENT' in datatype:
        data = float(data)
        data = data * 0.01
    elif 'BOOL' in datatype:
        data = utila.str2bool(data)
    return data


class HolyValue(HolyMixin):
    """\
    >>> 10.0 + HolyValue(default=5.0)
    15.0
    >>> 10.0 - HolyValue(default=5.0)
    5.0
    >>> 10 / HolyValue(default=5.0)
    2.0
    >>> HolyValue(default=5.0) / 10
    0.5
    """

    def __init__(self, name=None, group=None, datatype=None, default=None, limit=None):  # yapf:disable
        self.hvname = name
        self.hvgroup = group
        self.datatype = datatype
        self.default = default
        self.limit = limit

    @property
    def value(self):
        assert configo.database(), 'could not access database'
        if not self.valid:
            msg = (f'invalid holyvalue: {self.group}:{self.name};\n'
                   f'value:{self.data}; default:{self.default};\n'
                   f'limit:{self.limit}; datatype:{self.datatype}')
            raise configo.exception.InvalidHolyValue(msg)
        return self.data

    @property
    def valid(self):
        return validate(
            self.data,
            datatype=self.datatype,
            default=self.default,
            limit=self.limit,
        )

    @property
    def name(self):
        return self.hvname

    @property
    def group(self):
        return self.hvgroup

    @property
    def data(self):
        result = configo.database().get(
            group=self.group,
            variable=self.name,
            default=self.default,
        )
        result = convert(result, datatype=self.datatype)
        return result

    def __add__(self, other):
        with contextlib.suppress(TypeError):
            return self.value + other
        return self.value + other.value

    __radd__ = __add__

    def __sub__(self, other):
        with contextlib.suppress(TypeError):
            return self.value - other
        return self.value - other.value

    def __rsub__(self, other):
        return other - self.value

    def __mul__(self, other):
        with contextlib.suppress(TypeError):
            return self.value * other
        return self.value * other.value

    __rmul__ = __mul__

    def __truediv__(self, other):
        with contextlib.suppress(TypeError):
            return self.value / other
        return self.value / other.value

    def __rtruediv__(self, other):
        return other / self.value

    def __mod__(self, other):
        with contextlib.suppress(TypeError):
            return self.value % other
        return self.value % other.value

    def __lt__(self, other):
        return self.value < other

    def __le__(self, other):
        return self.value <= other

    def __gt__(self, other):
        return self.value > other

    def __ge__(self, other):
        return self.value >= other

    def __eq__(self, other):
        return self.value == other


def validate(data, datatype=None, default=None, limit=None) -> bool:
    """\
    >>> validate(True, DataType.BOOL, True)
    True
    >>> validate(51, DataType.INT, limit=50)
    False
    >>> validate(-10, DataType.INT_PLUS)
    False
    >>> validate(10.0, DataType.INT_PLUS)
    False
    """
    with contextlib.suppress(TypeError):
        # avoid that default is higher than limit
        if default > limit:
            return False
    if data is None:
        return True
    if 'INT' in str(datatype):
        if not utila.isint(data):
            return False
    if 'PLUS' in str(datatype):
        if data < 0.0:
            return False
    if limit is not None and datatype != DataType.BOOL:
        if data > limit:
            return False
    return True
