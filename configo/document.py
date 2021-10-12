# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Document Constants
==================

This class provides information about the `expected` parameter of the
layout-checker-configuration.

For the first approach, DinA4 is enough, DinA5 is included to keep supporting
different page formats and pageconfiguration(oneside/twoside) in mind.
"""

import collections
import dataclasses

PageSize = collections.namedtuple('PageSize', 'width height')
PageBorder = collections.namedtuple('PageBorder', 'left right top bottom')

DINA4 = PageSize(210, 297)
DINA5 = PageSize(148, 210)

# Manuel Rene Theisen, Wissenschaftliches Arbeiten: Erfolgreich bei Bachelor-
# und Masterarbeit.
BORDER_DINA4 = PageBorder(40, 20, 40, 20)

# TODO: Make configuration readonly?


@dataclasses.dataclass
class DocumentConfiguration:
    """Base class of all document configuration"""
    pagesize: PageSize = None
    pageborder: PageBorder = None


class OneSideDINA4(DocumentConfiguration):
    pagesize = DINA4
    pageborder = BORDER_DINA4


class OneSideDINA5(DocumentConfiguration):
    pagesize = DINA5
    pageborder = BORDER_DINA4  # What is a good value for DINA5?
