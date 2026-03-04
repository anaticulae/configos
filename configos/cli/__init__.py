# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import sys

import utilo

import configos
import configos.cli.generate
import configos.cli.optimization


@utilo.saveme
def main():
    current, data = evaluate()
    for action, method in runner():
        if current != action:
            continue
        if method.evaluate(*data):
            return utilo.FAILURE
        return utilo.SUCCESS
    return utilo.INVALID_COMMAND


def runner():
    runme = (
        ('generate', configos.cli.generate),
        ('optimize', configos.cli.optimization),
    )
    return runme


def evaluate() -> tuple:
    parser = create_parser()
    args = utilo.parse(parser)
    action, data = '', None
    gen = (args.get('input'), args.get('noskip', False))
    if args['generate']:
        action = 'generate'
        data = gen
    optimize = (
        args.get('create'),
        args.get('run'),
        args.get('show'),
        args.get('r'),
        args.get('t'),
    )
    if any(optimize):
        action = 'optimize'
        data = optimize
    if not action:
        utilo.error('nothing todo')
        sys.exit(utilo.INVALID_COMMAND)
    return action, data


def create_parser():
    result = utilo.cli.create_parser(
        todo=[
            utilo.cli.Flag(
                longcut='--generate',
                message='create default config out of source',
            ),
            utilo.cli.Flag(
                longcut='--noskip',
                message='do not skip any path',
            ),
        ],
        config=utilo.ParserConfiguration(
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
        prog=configos.PROCESS,
        version=configos.__version__,
    )
    configos.cli.optimization.add_option(result)
    return result
