# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import io
import os
import re
import tokenize

import utila

import configo.holyvalue.access
import configo.holyvalue.data
import configo.utils


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
    path = os.path.abspath(path)
    files = utila.file_list(
        path,
        include='py',
        absolute=True,
        recursive=True,
    )
    for item in files:
        relative = utila.make_relative(item, path)
        relative = utila.make_package(relative)
        parsed = holyvalue_from_file(item)
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
            variable = values.get('hvname', variable)
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


def holyvalue_from_file(path: str) -> dict:
    """Parse holyvalues from `sourcecode`.

    Args:
        path(str): python source code file
    Returns:
        Dictionary with holyvalues and further configuration parameter,
        e.g. limit, variable, group etc.
    """
    commento = comments(utila.file_read(path))
    module = configo.utils.load_module(path)
    result = {}
    for key, value in vars(module).items():
        if not isinstance(value, configo.holyvalue.data.HolyMixin):
            continue
        result[key] = dict(comment=commento[key], **vars(value))
    return result


PATTERN = r"""
    \b
    (?P<variable>[\w\d_]+)[ ]=[ ]
    (
        configo\.HV[\w\d_]*?|
        configo\.HolyTable|
    )
"""


def comments(sourcecode: str) -> dict:
    lines = codelines(sourcecode)
    result = {}
    for line, comment in lines.items():
        matched = re.match(PATTERN, line, re.MULTILINE | re.VERBOSE)
        if not matched:
            continue
        variable = matched['variable']
        result[variable] = comment
    return result


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
