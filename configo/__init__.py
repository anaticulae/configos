#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import os

# Public API:
# Cache
from configo.cache import CACHE_LARGE
from configo.cache import CACHE_MEDIUM
from configo.cache import CACHE_SMALL
from configo.cache import cache_large
from configo.cache import cache_medium
from configo.cache import cache_small
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
from configo.env import env
from configo.env import env_del
from configo.env import env_dump
from configo.env import env_load
from configo.env import env_path_append
from configo.env import env_path_remove
from configo.env import env_set
from configo.env import env_unload
# Exception
from configo.exception import HolyValueError
from configo.exception import InvalidHolyValue
from configo.exception import MissingHolyValue
# Holy
from configo.holyvalue.access import HV
from configo.holyvalue.access import HV_BOOL
from configo.holyvalue.access import HV_FLOAT
from configo.holyvalue.access import HV_FLOAT_PLUS
from configo.holyvalue.access import HV_INT
from configo.holyvalue.access import HV_INT_PLUS
from configo.holyvalue.access import HV_PERCENT
from configo.holyvalue.access import HV_PERCENT_PLUS
from configo.holyvalue.access import HV_STR
from configo.holyvalue.cloud import cloud_base
from configo.holyvalue.cloud import cloud_base_set
from configo.holyvalue.cloud import cloud_lookup
from configo.holyvalue.cloud import cloud_set
from configo.holyvalue.cloud import cloud_unset
from configo.holyvalue.cloud import holyname
from configo.holyvalue.collect import generate
from configo.holyvalue.data import NOMATH
from configo.holyvalue.data import DataType
from configo.holyvalue.data import HolyValue
from configo.holyvalue.store import database
from configo.holyvalue.store import init
from configo.holyvalue.store import load
from configo.holyvalue.store import parse
from configo.holyvalue.table import HolyList
from configo.holyvalue.table import HolyRate
from configo.holyvalue.table import HolyTable
# Server
from configo.server import package_address
from configo.server import package_configuration

__version__ = '0.20.0'

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
PROCESS = 'configo'

init(cloud_base())

# TODO: REMOVE LATER AND INCREASE MAJOR VERSION NUMBER
load_env = env_load
unload_env = env_unload
dump_env = env_dump
