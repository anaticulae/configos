Bugs
====

Open
----

Direct Holy Value access produces:

.. code-block::none

    invalid rawmaker.features.boxes:HORIZONTAL_MAX_DIFF; use default: 50

.. code-block::python

    HORIZONTAL_MIN_WIDTH = configos.HV_FLOAT(0.2).value

Check: The direct accesses the database before the value is created.

Closed
------
