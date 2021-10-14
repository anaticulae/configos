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
    action, data = evaluate()
    if action == 'generate':
        inpath, noskip = data
        for path in inpath:
            if not utila.exists(path):
                utila.error(f'input does not exists: {path}')
                return utila.FAILURE
        if generate(inpath, noskip):
            return utila.FAILURE
        return utila.SUCCESS
    if action == 'optimize':
        if optimization(*data):
            return utila.FAILURE
        return utila.SUCCESS
    return utila.INVALID_COMMAND


def generate(inpath: list, noskip=False) -> int:
    skip = None if noskip else skips
    done = False
    for item in inpath:
        collected = configo.generate(item, skips=skip)
        if not collected:
            continue
        utila.print_banner(text=item, symbol='#')
        utila.log(collected)
        done = True
    if not done:
        utila.error('could not locate any HolyValue')
        return utila.FAILURE
    return utila.SUCCESS


def optimization(create: list, run: str, show: str):
    print(create)
    print(run)
    print(show)
    pass


def skips(item: str) -> bool:
    item = str(item)
    return 'build' in item or 'tests' in item


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
            multiprocessed=False,
            pages=False,
            prefix=False,
            verboseflag=True,
            waitingflag=False,
            cacheflag=False,
        ),
        prog=configo.PROCESS,
        version=configo.__version__,
    )
    create_optimize_option(result)
    return result


def create_optimize_option(parser):
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
        action='append_const',
        const=str,
    )
    show.add_argument(
        '--show',
        help='show optimization result',
        action='append_const',
        const=str,
    )
