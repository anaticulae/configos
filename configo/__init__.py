#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
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
# debug
from configo.debugs import debug
from configo.debugs import debug_set
from configo.debugs import debug_unset
# directory
from configo.directory import check_startup
from configo.directory import environment
from configo.directory import export
from configo.directory import ready
from configo.directory import share
from configo.directory import tmp
from configo.directory import todo
# docs
from configo.docs import docs_url
# Document
from configo.document import OneSideDINA4
from configo.document import OneSideDINA5
# env
from configo.env import dump as dump_env
from configo.env import env
from configo.env import env_del
from configo.env import env_set
from configo.env import load as load_env
from configo.env import unload as unload_env
# Exception
from configo.exception import HolyValueError
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
from configo.holyvalue.table import HolyTable
# Server
from configo.server import package_address
from configo.server import package_configuration

__version__ = '0.8.7'

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
