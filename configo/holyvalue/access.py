# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""\
>>> STR = HV_STR('hello')
>>> f'{STR} hier'
'hello hier'
"""

import functools
import inspect

import utilo

import configo
import configo.holyvalue
import configo.holyvalue.collect
import configo.holyvalue.data

NO_GROUP = 'NO_GROUP'


def holyvalue(
    default=None,
    *,
    name: str = None,
    group: str = None,
    limit=None,
    datatype: 'DataType' = None,
) -> 'HolyValue':
    """Access `holyvalue` via `variable` and `group`.

    Args:
        default(DataType): define default variable for non defined
                           variable to avoid updating configration to
                           often.
        name(str): name of holy value
        group(str): module where `var` is located
        limit(DataType): limit to validate configuration file
        datatype(DataType): convert str-based configuration file
    Raises:
        InvalidHolyValue: if value of configuration file hits requirements
        MissingHolyValue: if value is not defined and no default one is defined
    Returns:
        Defined HolyValue in `config_name.hv` or `default` one.

    TODO: MAKE method update able/facade/callable
    """
    assert name is None or isinstance(name, str), f'invalid name {name}'
    assert group is None or isinstance(group, str), f'invalid group: {group}'
    if name is None:
        # TODO: REMOVE THIS HACK
        # TODO: NOT VERY STABLE/ DIRTY
        # determine variable out of code
        levelup = inspect.stack(context=1)[1].code_context
        code = utilo.NEWLINE.join(levelup)
        matched = utilo.search(configo.holyvalue.collect.PATTERN, code)
        name = str(matched['variable']).strip().upper()
    if group is None:
        # determine call package
        frame = inspect.currentframe()
        parent = frame.f_back  # get invoker
        inspected = inspect.getmodule(parent)
        if inspected:
            group = inspect.getmodule(inspected).__name__
        else:
            # is loaded later via dynamic code loader
            utilo.debug(f'could not determine holyvalue group: {parent}')
            group = NO_GROUP
    if not configo.holyvalue.data.validate(default, datatype, default, limit):
        msg = f'invalid default/limit/datatype; name: {name}; group:{group} '
        msg += f'default: {default}; limit: {limit}; type: {datatype}'
        raise configo.InvalidHolyValue(msg)
    result = configo.HolyValue(name, group, datatype, default, limit)
    return result


DataType = configo.holyvalue.data.DataType
init = lambda datatype: functools.partial(holyvalue, datatype=datatype)
HV = holyvalue  # pylint:disable=C0103

HV_BOOL = init(DataType.BOOL)  # pylint:disable=C0103
HV_STR = init(DataType.STR)  # pylint:disable=C0103

HV_INT = init(DataType.INT)  # pylint:disable=C0103
HV_INT_PLUS = init(DataType.INT_PLUS)  # pylint:disable=C0103
HV_INT_MINUS = init(DataType.INT_MINUS)  # pylint:disable=C0103

HV_FLOAT = init(DataType.FLOAT)  # pylint:disable=C0103
HV_FLOAT_PLUS = init(DataType.FLOAT_PLUS)  # pylint:disable=C0103
HV_FLOAT_MINUS = init(DataType.FLOAT_MINUS)  # pylint:disable=C0103

HV_PERCENT = init(DataType.PERCENT)  # pylint:disable=C0103
HV_PERCENT_PLUS = init(DataType.PERCENT_PLUS)  # pylint:disable=C0103
HV_PERCENT_MINUS = init(DataType.PERCENT_MINUS)  # pylint:disable=C0103

HV_SECOND = init(DataType.SECOND)  # pylint:disable=C0103
HV_MINUTE = init(DataType.MINUTE)  # pylint:disable=C0103
HV_HOUR = init(DataType.HOUR)  # pylint:disable=C0103

HV_API = init(DataType.API)  # pylint:disable=C0103
HV_SECRET = init(DataType.SECRET)  # pylint:disable=C0103

HV_KB = init(DataType.KB)  # pylint:disable=C0103
HV_MB = init(DataType.MB)  # pylint:disable=C0103
HV_GB = init(DataType.GB)  # pylint:disable=C0103
