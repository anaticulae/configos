#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# Tis file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import os

# Public API:
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

__version__ = '0.1.4'

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
