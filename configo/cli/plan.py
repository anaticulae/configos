# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections
import os
import re

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


def run(
    path,
    reduce=100,
    seed=None,
    test_before: bool = False,
    cmd_test=None,
):
    path = os.path.abspath(path[0])
    plan = utila.yaml_load(path)
    todo = list(plan.values())
    keys = list(plan.keys())
    mapped = first_one(todo)
    utila.log(f'different steps: {len(mapped)}')
    if len(mapped) > reduce:
        utila.log(f'reduce values: {reduce}')
        mapped = utila.choose_random(mapped, count=reduce, seed=seed)
    # verify code without hv-modification
    if test_before:
        utila.log('test project')
        utila.run(cmd_test)  # utila.run('baw test')
    # utila.log(utila.from_tuple(keys, ';'))
    with utila.make_tmpdir(configo.ROOT) as tmpdir:
        utila.log(f'outdir: {tmpdir}')
        header = f"number,{utila.from_tuple(keys, separator=',')},failure\n"
        utila.file_append(
            os.path.join(tmpdir, 'result'),
            header,
            create=True,
        )
        for index, step in enumerate(mapped):
            run_test(
                key=keys,
                config=step,
                step=index,
                tmpdir=tmpdir,
                cmd_test=cmd_test,
            )


def run_test(
    key,
    config,
    step: int,
    tmpdir,
    cmd_test,
    hcvalue='RAWMAKER',
):
    # write hv config
    cfg = create_config(key, config)
    step = str(step).zfill(4)
    cfgpath = os.path.join(tmpdir, f'{step}.hv')
    utila.file_create(cfgpath, cfg)
    configo.cloud_set(program=hcvalue, namepath=cfgpath)
    # run tests
    utila.log(f'run step: {step}')
    utila.log(utila.from_tuple(config, ';'))
    completed = utila.run(
        cmd_test,
        expect=None,
        env=dict(os.environ),
    )
    # cfgpath
    logpath = os.path.join(tmpdir, f'{step}.log')
    utila.file_create(logpath, completed.stderr)
    utila.file_append(logpath, completed.stdout)
    tests = 0
    if completed.returncode:
        stdout = completed.stdout
        tests = FAILED.search(stdout)['failed']
    config = f'{step},' + utila.from_tuple(config, ',') + f',{tests}\n'
    if completed.returncode:
        utila.error(config)
    # append result
    utila.file_append(
        os.path.join(tmpdir, 'result'),
        config,
        create=True,
    )


# === 5 failed, 178 passed, 168 skipped,
FAILED = re.compile(r'===\ (?P<failed>\d+)\ fail')

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


def create_config(keys, configs) -> str:
    grouped = collections.defaultdict(list)
    for key, config in zip(keys, configs):
        group, key = key.rsplit('.', 1)
        grouped[group].append(f'{key} = {config}')
    collected = []
    for key, value in grouped.items():
        collected.append('[' + key + ']')
        collected.extend(value)
    result = utila.NEWLINE.join(collected)
    return result


def first_one(items) -> list:
    """\
    >>> first_one(([1,], [2,]))
    [[1, 2]]
    >>> first_one([[1, 2], [3,]])
    [[1, 3], [2, 3]]
    >>> first_one([(4, ), (1, 2, 3), (5, 6)])
    [[4, 1, 5], [4, 2, 5], [4, 3, 5], [4, 1, 6]]
    """
    # TODO: MOVE TO UTILA
    items = [list(item) for item in items]
    result = []
    for index, _ in enumerate(items):
        base = [item[0] for item in items]
        for current in items[index]:
            copy = list(base)
            copy[index] = current
            result.append(copy)
    result = utila.make_unique(result)
    return result


def dump(plan: dict) -> str:
    dumped = utila.yaml_dump(plan)
    return dumped
