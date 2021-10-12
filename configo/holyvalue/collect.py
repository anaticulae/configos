# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import glob
import io
import os
import re
import tokenize

import utila

import configo.holyvalue.access


def generate(path: str) -> str:
    """Iterate thrue python files and extract config with holyvalues
    constructs out of project structure.

    Args:
        path(str): project root path
    Returns:
        project configuration file
    """
    assert os.path.exists(path), f'path does not exists: {path}'
    result = {}
    with utila.chdir(path):
        files = list(glob.glob(os.path.join(path, '**/*.py'), recursive=True))
        for item in files:
            relative = utila.make_relative(item, path)
            relative = utila.make_package(relative)
            code = utila.file_read(item)
            parsed = holyvalue_from_file(code)
            if parsed:
                result[relative] = parsed
    signature = utila.attributes(configo.holyvalue.access.holyvalue)
    root = rootpackage(path)
    raw = []
    for package in sorted(result.keys()):
        raw.append(f'[{root}.{package}]')
        for variable, values in result[package].items():
            for item, value in values.items():
                raw.append(f'# {item}:{value}')
            assert 'name' in signature, 'require name'
            variable = values.get('name', variable)
            variable = variable.replace("'", '').upper()
            assert 'default' in signature, 'require default'
            default = values.get('default', 'None')
            raw.append(f"{variable} = {default}")
            raw.append('')
        raw.append('')
    return utila.NEWLINE.join(raw)


def rootpackage(root: str) -> str:
    package = os.path.split(root)[1]
    # rawmaker-2.26.6-py3.8.egg
    package = str(package).split('-')[0]
    return package


PATTERN = r"\b(?P<variable>[\w\d_]+) = configo\.HV[\w\d_]*\((?P<config>.*)\)"


def holyvalue_from_file(sourcecode: str) -> dict:
    """Parse holyvalues from `sourcecode`.

    Args:
        sourcecode(str): python source code file
    Returns:
        Dictionary with holyvalues and further configuration parameter,
        e.g. limit, variable, group etc.
    """
    lines = codelines(sourcecode)
    result = {}
    for line, comment in lines.items():
        # TODO: THINK ABOUT USING TOKEN
        matched = re.match(PATTERN, line, re.MULTILINE)
        if not matched:
            continue
        config = matched['config']
        if config:
            config = prepare_config(config, line)
        else:
            config = {}
        if comment.strip():
            config['comment'] = comment
        variable = matched['variable']
        result[variable] = config
    return result


def prepare_config(config, line):
    config = [item.split('=', 1) for item in config.split(', ')]
    for item in config:
        if len(item) == 1:
            # no variables, see 10
            # TABLE_MIN_LINE_COUNT = configo.HV_INT_PLUS(10)
            utila.error(f'could not determine args value: {line}')
    config = [item for item in config if len(item) > 1]
    config = {item[0]: item[1] for item in config}
    return config


def codelines(sourcecode: str):
    """Remove comments etc. out of `sourcecode`."""
    lines = {}
    tokenized = list(token(sourcecode))
    for index, item in enumerate(tokenized[1:], start=1):
        if item.type != tokenize.NAME:
            # skip comments etc.
            continue
        stripped = item.line.strip()
        holycomment = ''
        # TODO: SUPPORT MULTILINE COMMENT
        # look one line back to check if holy value has a holy comment
        if tokenized[index - 1].type in (tokenize.NL,):  # comment
            holycomment = tokenized[index - 1].line
            holycomment = holycomment.replace('#', '', 1)
            holycomment = holycomment.strip()
        if lines.get(stripped, None):
            # do not overwrite holy comments
            continue
        lines[stripped] = holycomment
    return lines


def token(code: str):
    buffer = io.BytesIO(code.encode(utila.UTF8)).readline
    source = tokenize.tokenize(buffer)
    return source
