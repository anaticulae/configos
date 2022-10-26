# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

import configo
import configo.holyvalue.collect


def create(todo: list) -> dict:
    result = {}
    for path in todo:
        program = utila.path_current(path)
        collected = configo.holyvalue.collect.collect(path)
        for groupname, group in collected.items():
            for key, value in group.items():
                hvgroup = value.get('hvgroup', f'{program}.{groupname}')
                if hvgroup == 'NO_GROUP':
                    hvgroup = f'{program}.{groupname}'
                hvgroup = hvgroup.upper()
                variable = f'{hvgroup}.{key}'
                todo = ranges(
                    default=value.get('default'),
                    limit=value.get('limit', None),
                    datatype=value.get('datatype', None),
                )
                if not todo:
                    continue
                result[variable] = todo
    return result


STEPS = (1.0, 0.1, 0.3, 0.5, 0.9, 1.2, 1.8, 2.2, 2.8, 3.5)


def ranges(
    default,
    limit=None,
    datatype: configo.DataType = None,
    steps=None,
) -> tuple:
    """\
    >>> ranges(50, 300, configo.DataType.INT_PLUS, steps=((1.0, 1.5, 2.0)))
    (50, 75, 100)
    >>> ranges(1.2, 3.0, configo.DataType.FLOAT, steps=((1.0, 1.5, 2.0)))
    (1.2, 1.8, 2.4)
    >>> ranges(True, datatype=configo.DataType.BOOL)
    (True, False)
    """
    if steps is None:
        steps = STEPS
    if default is None:
        return tuple()
    if datatype and datatype == configo.DataType.STR:
        return tuple()
    if datatype == configo.DataType.BOOL:
        return (True, False)
    data = tuple(utila.roundme(default * item) for item in steps)
    if 'INT' in str(datatype):
        data = tuple(int(item) for item in data)
    if limit is not None:
        data = tuple(item for item in data if item < limit)
    return data
