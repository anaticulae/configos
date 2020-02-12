Bugs
====

Open
----

HolyValue Definition
~~~~~~~~~~~~~~~~~~~~

This result that the HolyValue has the name `30`. But the intention of
the programmer is to say give me a holy value with default value 30.

.. code-block:: python

  LEFT_PERCENT = configo.HV_PERCENT_PLUS(30)

But the correct solution is:

.. code-block:: python

  LEFT_PERCENT = configo.HV_PERCENT_PLUS(default=30)

Solution: Raise ValueError if name of HolyValue is not a str.

Closed
------
