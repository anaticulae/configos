# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools
import inspect
import re

import utila

import configo
import configo.holyvalue
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
    assert group is None or isinstance(group, str), f'invalid name: {group}'

    if name is None:
        # TODO: NOT VERY STABLE/ DIRTY
        # determine variable out of code
        levelup = inspect.stack(context=10)[1].code_context
        code = utila.NEWLINE.join(levelup)
        pattern = r'(?P<variable>[\w\d_]+) = configo\.HV[\w\d_]*\('
        matched = re.search(pattern, code)
        name = str(matched['variable']).strip().upper()

    if group is None:
        # determine call package
        frame = inspect.currentframe()
        parent = frame.f_back  # get invoker
        inspected = inspect.getmodule(parent)
        if inspected:
            group = inspect.getmodule(inspected).__name__
        else:
            # TODO: ENSURE THAT CODE IS LOADED WHEN USING DYNAMIC CODE LOADING
            utila.error(f'could not determine holyvalue group: {parent}')
            group = NO_GROUP

    result = configo.HolyValue(name, group, datatype, default, limit)
    return result


DataType = configo.holyvalue.data.DataType
HV = holyvalue

HV_BOOL = functools.partial(holyvalue, datatype=DataType.BOOL)

HV_INT = functools.partial(holyvalue, datatype=DataType.INT)
HV_INT_PLUS = functools.partial(holyvalue, datatype=DataType.INT_PLUS)

HV_FLOAT = functools.partial(holyvalue, datatype=DataType.FLOAT)
HV_FLOAT_PLUS = functools.partial(holyvalue, datatype=DataType.FLOAT_PLUS)

HV_PERCENT = functools.partial(holyvalue, datatype=DataType.PERCENT)
HV_PERCENT_PLUS = functools.partial(holyvalue, datatype=DataType.PERCENT_PLUS)
