# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import sys

import utila

import configo
import configo.cli.generate
import configo.cli.optimization


@utila.saveme
def main():
    current, data = evaluate()
    for action, method in runner():
        if current != action:
            continue
        if method.evaluate(*data):
            return utila.FAILURE
        return utila.SUCCESS
    return utila.INVALID_COMMAND


def runner():
    runme = (
        ('generate', configo.cli.generate),
        ('optimize', configo.cli.optimization),
    )
    return runme


def evaluate() -> tuple:
    parser = create_parser()
    args = utila.parse(parser)
    action, data = '', None
    gen = (args.get('input'), args.get('noskip', False))
    if args['generate']:
        action = 'generate'
        data = gen
    optimize = (args.get('create'), args.get('run'), args.get('show'))
    if any(optimize):
        action = 'optimize'
        data = optimize
    if not action:
        utila.error('nothing todo')
        sys.exit(utila.INVALID_COMMAND)
    return action, data


def create_parser():
    result = utila.cli.create_parser(
        todo=[
            utila.cli.Flag(
                longcut='--generate',
                message='create default config out of source',
            ),
            utila.cli.Flag(
                longcut='--noskip',
                message='do not skip any path',
            ),
        ],
        config=utila.ParserConfiguration(
            inputparameter=True,
            outputparameter=False,
            cacheflag=False,
            cprofile=False,
            multiprocessed=False,
            pages=False,
            prefix=False,
            verboseflag=True,
            waitingflag=False,
        ),
        prog=configo.PROCESS,
        version=configo.__version__,
    )
    configo.cli.optimization.add_option(result)
    return result
