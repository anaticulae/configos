# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
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


def evaluate(create: list, run: str, show: str):  # pylint:disable=W0613
    if create:
        plan = create_plan(create)
        utila.log(dump_plan(plan))
    if run:
        run_plan(run)


def create_plan(todo: list) -> dict:
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


def run_plan(run, reduce=999, seed=None):
    run = os.path.abspath(run[0])
    plan = utila.yaml_load(run)
    todo = list(plan.values())
    keys = list(plan.keys())
    mapped = utila.minimal(todo)
    utila.log(f'different steps: {len(mapped)}')
    reduced = utila.choose_random(mapped, count=reduce, seed=seed)
    utila.log(f'reduce values: {reduce}')
    # verify code without hv-modification
    utila.log('test project')
    # utila.run('baw test')
    # utila.log(utila.from_tuple(keys, ';'))
    with utila.make_tmpdir(configo.ROOT) as tmpdir:
        utila.log(tmpdir)
        for index, step in enumerate(reduced):
            run_test(key=keys, config=step, step=index, tmpdir=tmpdir)


def run_test(key, config, step: int, tmpdir, hcvalue='RAWMAKER'):
    # write hv config
    cfg = create_config(key, config)
    step = str(step).zfill(4)
    cfgpath = os.path.join(tmpdir, f'{step}.hv')
    utila.file_create(cfgpath, cfg)
    configo.cloud_set(program=hcvalue, namepath=cfgpath)
    # run tests
    utila.log(f'run step: {step}')
    utila.log(utila.from_tuple(config, ';'))
    cmd = 'baw test'
    completed = utila.run(
        cmd,
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
    config = f'{step};' + utila.from_tuple(config, ';') + f';{tests}\n'
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


STEPS = (0.3, 0.5, 0.9, 1.0, 1.2, 1.8, 2.2)


def ranges(default, limit=None, datatype: configo.DataType = None) -> tuple:
    """\
    >>> ranges(50, 300, configo.DataType.INT_PLUS)
    (15, 25, 45, 50, 60, 90, 110)
    >>> ranges(1.2, 3.0, configo.DataType.FLOAT)
    (0.36, 0.6, 1.08, 1.2, 1.44, 2.16, 2.64)
    """
    if default is None:
        return tuple()
    if datatype and datatype == configo.DataType.STR:
        return tuple()
    if datatype == configo.DataType.BOOL:
        return (True, False)
    data = tuple(utila.roundme(default * item) for item in STEPS)
    if 'INT' in str(datatype):
        data = tuple(int(item) for item in data)
    if limit is not None:
        data = tuple(item for item in data if item < limit)
    return data


def dump_plan(plan: dict) -> str:
    dumped = utila.yaml_dump(plan)
    return dumped


def add_option(parser):
    # TODO: REPLACE WITH UTILA METHOD
    sub = parser.add_subparsers(help='run optimizer to determine holy values')
    show = sub.add_parser('optimize')
    show.add_argument(
        '--create',
        help='create optimization plan',
        action='append',
    )
    show.add_argument(
        '--run',
        help='run optimization',
        action='append',
    )
    show.add_argument(
        '--show',
        help='show optimization result',
        action='append_const',
        const=str,
    )
