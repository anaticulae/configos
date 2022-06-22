# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""HolyTable lookup
================

>>> table = HolyTable(strategy=utila.Strategy.LINEARISE)
>>> table.add(0,0)
>>> table.add(10,10)
>>> assert table(5.0) == 5.0, table(5.0)

>>> rate = HolyRate(((1, 1), (2, 2), (5, 1), (10, 5)))
>>> assert rate(2) == 1.0
>>> assert rate(6) == 0.2
>>> assert rate(10) == 0.2

"""

import utila

import configo.holyvalue.data


class HolyTable(configo.holyvalue.data.HolyMixin):

    def __init__(
        self,
        items: list = None,
        strategy: utila.Strategy = None,
        right_outranges_none: bool = False,
        left_outranges_none: bool = False,
    ):
        """HolyTable Looup

        Args:
            items: data points to construct lookup values
            strategy: strategy to construct lookup values
            left_outranges_none: return None if request value is out of
                                 defined range
            right_outranges_none: return None if request value is out of
                                 defined range
        """
        self.table = []
        self.strategy = strategy
        self.right_outranges_none = right_outranges_none
        self.left_outranges_none = left_outranges_none
        if items:
            for item in items:
                self.add(*item)

    def add(self, position, value):
        self.table.append((position, value))
        self.table = sorted(self.table, key=lambda x: x[0])
        assert utila.isascending([item[0] for item in self.table]), str(self.table) # yapf:disable

    def __call__(self, position):
        """Return lookup value or None.

        None: If request point is out of defined area and no fallback is
              activated.
        """
        assert self.table, 'empty table, use add to configure'
        value = utila.lookup(
            position,
            self.table,
            self.strategy,
            self.right_outranges_none,
            self.left_outranges_none,
        )
        return value


class HolyRate(HolyTable):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.table = [
            (pos, value / pos if pos else 0.0) for pos, value in self.table
        ]


class HolyList(configo.holyvalue.data.HolyMixin):
    """A HolyList is a list which can be configured by HolyValue-Mechanism.

    Therefore a live-configuration is possible.

    >>> data = HolyList((1, 3, 5))
    >>> assert list(data) == [1, 3, 5]
    """

    def __init__(self, items):
        self.items = items

    def __getitem__(self, index):
        return self.items[index]
