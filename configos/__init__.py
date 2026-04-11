#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import importlib.metadata
import os

__version__ = importlib.metadata.version('configos')

# Public API:
# Cache
from configos.cache import CACHE_LARGE
from configos.cache import CACHE_MEDIUM
from configos.cache import CACHE_SMALL
from configos.cache import cache_large
from configos.cache import cache_medium
from configos.cache import cache_small
# debug
from configos.debugs import debug
from configos.debugs import debug_set
from configos.debugs import debug_unset
# directory
from configos.directory import check_startup
from configos.directory import environment
from configos.directory import export
from configos.directory import makedirs
from configos.directory import ready
from configos.directory import share
from configos.directory import tmp
from configos.directory import todo
# docs
from configos.docs import docs_url
# Document
from configos.document import OneSideDINA4
from configos.document import OneSideDINA5
# env
from configos.env import env
from configos.env import env_del
from configos.env import env_dump
from configos.env import env_load
from configos.env import env_path_append
from configos.env import env_path_remove
from configos.env import env_set
from configos.env import env_unload
# Exception
from configos.exception import HolyValueError
from configos.exception import InvalidHolyValue
from configos.exception import MissingHolyValue
# Holy
from configos.holyvalue.access import HV
from configos.holyvalue.access import HV_API
from configos.holyvalue.access import HV_BOOL
from configos.holyvalue.access import HV_FLOAT
from configos.holyvalue.access import HV_FLOAT_MINUS
from configos.holyvalue.access import HV_FLOAT_PLUS
from configos.holyvalue.access import HV_GB
from configos.holyvalue.access import HV_HOUR
from configos.holyvalue.access import HV_INT
from configos.holyvalue.access import HV_INT_MINUS
from configos.holyvalue.access import HV_INT_PLUS
from configos.holyvalue.access import HV_KB
from configos.holyvalue.access import HV_MB
from configos.holyvalue.access import HV_MINUTE
from configos.holyvalue.access import HV_PERCENT
from configos.holyvalue.access import HV_PERCENT_MINUS
from configos.holyvalue.access import HV_PERCENT_PLUS
from configos.holyvalue.access import HV_SECOND
from configos.holyvalue.access import HV_SECRET
from configos.holyvalue.access import HV_STR
from configos.holyvalue.cloud import cloud_base
from configos.holyvalue.cloud import cloud_base_set
from configos.holyvalue.cloud import cloud_lookup
from configos.holyvalue.cloud import cloud_set
from configos.holyvalue.cloud import cloud_unset
from configos.holyvalue.cloud import holyname
from configos.holyvalue.collect import generate
from configos.holyvalue.data import NOMATH
from configos.holyvalue.data import DataType
from configos.holyvalue.data import HolyValue
from configos.holyvalue.store import database
from configos.holyvalue.store import init
from configos.holyvalue.store import load
from configos.holyvalue.store import parse
from configos.holyvalue.table import HolyList
from configos.holyvalue.table import HolyRate
from configos.holyvalue.table import HolyTable
# Server
from configos.server import package_address
from configos.server import package_configuration

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
PROCESS = 'configos'

init(cloud_base())

# TODO: REMOVE LATER AND INCREASE MAJOR VERSION NUMBER
load_env = env_load
unload_env = env_unload
dump_env = env_dump
