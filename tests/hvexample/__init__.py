# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configos

# first docstring
FIRST = configos.HV()

# backward
SECOND = configos.HV(default=100,
                     limit=1000,
                     datatype=configos.DataType.INT_PLUS)

THIRD = configos.HV()
