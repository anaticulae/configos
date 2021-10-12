# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import sys

import utila

import configo


@utila.saveme
def main():
    inpath, action = evaluate()
    for path in inpath:
        if not utila.exists(path):
            utila.error(f'input does not exists: {path}')
            return utila.FAILURE
    if action == 'generate':
        collected = [configo.generate(item) for item in inpath]
        # TODO: ADD FILE SOURCE?
        raw = utila.NEWLINE.join(collected)
        utila.log(raw)
        return utila.SUCCESS
    return utila.INVALID_COMMAND


def evaluate() -> tuple:
    parser = utila.cli.create_parser(
        todo=[
            utila.cli.Flag(
                longcut='--generate',
                message='create default config out of source',
            ),
        ],
        config=utila.ParserConfiguration(
            inputparameter=True,
            outputparameter=False,
            multiprocessed=False,
            pages=False,
            prefix=False,
            verboseflag=True,
            waitingflag=False,
            cacheflag=False,
        ),
        version=configo.__version__,
        prog='configo',
    )
    args = utila.parse(parser)
    action = ''
    if args['generate']:
        action = 'generate'
    if not action:
        utila.error('nothing todo')
        sys.exit(utila.INVALID_COMMAND)
    choice = (
        args['input'],
        action,
    )
    return choice
