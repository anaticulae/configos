# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections
import csv
import os

import utilo

import configos


def show(result):
    single = result[0]
    parsed, header, size = parse_result(single)
    rendered = render_table(list(parsed.values()), size, header=header)
    with utilo.make_tmpdir(root=configos.ROOT) as output:
        outpath = os.path.join(output, 'index.html')
        utilo.file_create(outpath, rendered)
        testrun = utilo.testing()
        if not testrun:
            utilo.run(f'start {outpath}')


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
            value = int(value) if utilo.isint(value) else float(value)
            collected[index].add((value, failure))
        width = len(content)
        height += 1
    result = {key: prepare(value) for key, value in collected.items()}
    return result, header, (width, height)


def prepare(value):
    grouped = utilo.groupby_x(value, selector=lambda x: x[0])
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
