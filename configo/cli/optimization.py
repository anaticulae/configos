# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections
import csv
import os
import re

import utila

import configo
import configo.holyvalue.collect


def evaluate(create: list, run: str, show: str, reduce: int):  # pylint:disable=W0613
    if create:
        plan = create_plan(create)
        utila.log(dump_plan(plan))
    if run:
        run_plan(run, reduce=reduce)
    if show:
        show_result(show)


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


def run_plan(run, reduce=100, seed=None, test_before: bool = False):
    run = os.path.abspath(run[0])
    plan = utila.yaml_load(run)
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
        utila.run('baw test')
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
            run_test(key=keys, config=step, step=index, tmpdir=tmpdir)


def show_result(result):
    single = result[0]
    parsed, header, size = parse_result(single)
    rendered = render_table(list(parsed.values()), size, header=header)
    with utila.make_tmpdir(root=configo.ROOT) as output:
        outpath = os.path.join(output, 'index.html')
        utila.file_create(outpath, rendered)
        testrun = utila.testing()
        if not testrun:
            utila.run(f'start {outpath}')


def parse_result(path) -> dict:
    collected = collections.defaultdict(set)
    with open(path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        data = list(reader)
    width, height = 0, 0
    header = data[0][1:-1]
    for row in data[1:]:
        number, *content, failure = row  # pylint:disable=W0612
        failure = int(failure)
        for index, value in enumerate(content):
            # TODO: ADD BOOL CHECKUP
            if utila.isint(value):
                value = int(value)
            else:
                value = float(value)
            collected[index].add((value, failure))
        width = len(content)
        height += 1
    result = {key: prepare(value) for key, value in collected.items()}
    return result, header, (width, height)


def prepare(value):
    grouped = utila.groupby_x(value, selector=lambda x: x[0])
    result = []
    for group in grouped:
        result.append((group[0][0], min([item[1] for item in group])))
    return sorted(result, key=lambda x: x[0], reverse=True)


def render_table(data, size, header=None) -> str:
    width = 150 * size[0]
    result = f'<html><table width={width}>'
    if header:
        result += '<tr>'
        result += ''.join([
            f'<td style="min-width:150px;font-size:10px;overflow:hidden">{item.replace(".", " ")}</td>'
            for item in header
        ])
        result += '</tr>'
    for _ in range(size[1]):  # pylint:disable=W0612
        result += '<tr>'
        for pos in range(size[0]):
            current = data[pos]
            if current:
                value, failure = current.pop()
                color = 'green' if not failure else 'orange'
                result += f'<td style="background:{color};" height=50px><center>{value} [{failure}]</center></td>'
            else:
                result += '<td></td>'
        result += '</tr>'
    result += '</table></html>'
    return result


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
        action='append',
    )
    show.add_argument(
        '-r',
        default=100,
        type=int,
        help='number of optimization steps',
    )
