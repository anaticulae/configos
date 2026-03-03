# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utilo

import configo.cli.plan
import configo.cli.result


def evaluate(
    create: list,
    run: str,
    show: str,
    reduce: int,
    cmd_test: str,
):  # pylint:disable=W0613
    if create:
        plan = configo.cli.plan.create(create)
        utilo.log(configo.cli.plan.dump(plan))
    if run:
        if cmd_test is None:
            cmd_test = 'baw test -n1'
        configo.cli.plan.run(
            run,
            reduce=reduce,
            cmd_test=cmd_test,
        )
    if show:
        configo.cli.result.show(show)


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
