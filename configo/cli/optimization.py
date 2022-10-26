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

import utila

import configo
import configo.cli.plan


def evaluate(
    create: list,
    run: str,
    show: str,
    reduce: int,
    cmd_test: str,
):  # pylint:disable=W0613
    if create:
        plan = configo.cli.plan.create(create)
        utila.log(configo.cli.plan.dump(plan))
    if run:
        if cmd_test is None:
            cmd_test = 'baw test -n1'
        configo.cli.plan.run(
            run,
            reduce=reduce,
            cmd_test=cmd_test,
        )
    if show:
        show_result(show)


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
    with open(path, newline='', encoding='utf8') as csvfile:
        reader = csv.reader(csvfile)
        data = list(reader)
    width, height = 0, 0
    header = data[0][1:-1]
    for row in data[1:]:
        number, *content, failure = row  # pylint:disable=W0612
        failure = int(failure)
        for index, value in enumerate(content):
            # TODO: ADD BOOL CHECKUP
            value = int(value) if utila.isint(value) else float(value)
            collected[index].add((value, failure))
        width = len(content)
        height += 1
    result = {key: prepare(value) for key, value in collected.items()}
    return result, header, (width, height)


def prepare(value):
    grouped = utila.groupby_x(value, selector=lambda x: x[0])
    result = []
    for group in grouped:
        result.append((group[0][0], min((item[1] for item in group))))
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
    show.add_argument(
        '-t',
        default=None,
        type=str,
        help='run test after each holy value update (baw test -n1)',
    )
