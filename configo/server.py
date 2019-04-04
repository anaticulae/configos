#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# Tis file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

from utila import FAILURE
from utila import logging_error


def package_configuration():
    try:
        adress = environ['HELPY_URL']
        internal = int(environ['HELPY_INT_PORT'])
        external = int(environ['HELPY_EXT_PORT'])
        return (adress, internal, external)
    except KeyError as error:
        handle_error(error)


def package_address():
    try:
        internal = environ['HELPY_INT_DIRECT']
        external = environ['HELPY_EXT_DIRECT']
        return (internal, external)
    except KeyError as error:
        handle_error(error)


def handle_error(error: Exception):
    logging_error('Missing global var: %s' % error)
    exit(FAILURE)
