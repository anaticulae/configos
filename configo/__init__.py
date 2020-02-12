#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import os

# Public API:
#
# Cache
from configo.cache import CACHE_LARGE
from configo.cache import CACHE_MEDIUM
from configo.cache import CACHE_SMALL
# directory
from configo.directory import check_startup
from configo.directory import environment
from configo.directory import export
from configo.directory import ready
from configo.directory import share
from configo.directory import tmp
from configo.directory import todo
# Document
from configo.document import OneSideDINA4
from configo.document import OneSideDINA5
# Exception
from configo.exception import InvalidHolyValue
from configo.exception import MissingHolyValue
# Holy
from configo.holyvalue import HV
from configo.holyvalue import HV_FLOAT
from configo.holyvalue import HV_FLOAT_PLUS
from configo.holyvalue import HV_INT
from configo.holyvalue import HV_INT_PLUS
from configo.holyvalue import HV_PERCENT
from configo.holyvalue import HV_PERCENT_PLUS
from configo.holyvalue import DataType
from configo.holyvalue import generate
from configo.holyvalue import init
from configo.holyvalue import load
# Server
from configo.server import package_address
from configo.server import package_configuration

__version__ = '0.5.0'

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
