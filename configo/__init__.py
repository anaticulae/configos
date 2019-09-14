#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
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
# Document
from configo.document import OneSideDINA4
from configo.document import OneSideDINA5
# Server
from configo.server import package_address
from configo.server import package_configuration
# Share
from configo.share import check_startup
from configo.share import environment
from configo.share import export
from configo.share import ready
from configo.share import share
from configo.share import todo

__version__ = '0.1.29'

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
