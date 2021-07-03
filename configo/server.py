#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import os
import sys

import utila

HELPY_URL = 'HELPY_URL'

HELPY_INT_PORT = 'HELPY_INT_PORT'
HELPY_EXT_PORT = 'HELPY_EXT_PORT'

HELPY_INT_DIRECT = 'HELPY_INT_DIRECT'
HELPY_EXT_DIRECT = 'HELPY_EXT_DIRECT'


def package_configuration():
    """Return tuple with adress, internal package port and external package
    port of the package repository"""

    try:
        adress = os.environ[HELPY_URL]
        internal = os.environ[HELPY_INT_PORT]
        external = os.environ[HELPY_EXT_PORT]
        internal, external = int(internal), int(external)
        return (adress, internal, external)
    except KeyError as msg:
        handle_error(msg)
    return None


def package_address():
    """Return tuple of direct addresses to internal and external package
    repository"""

    try:
        internal = os.environ[HELPY_INT_DIRECT]
        external = os.environ[HELPY_EXT_DIRECT]
        return (internal, external)
    except KeyError as msg:
        handle_error(msg)
    return None


def handle_error(msg: KeyError):
    utila.error('Missing global var: %s' % msg)
    sys.exit(utila.FAILURE)
