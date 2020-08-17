SimpleModel
===========

Description
-----------
To simplify the generation of a model, one may use a ``SimpleModel`` object instead of a ``Model``. The main difference is that the ``SimpleModel`` constructor also takes a ``setup`` and ``step`` function as arguments, and then generates the appropriate **Setup** and **Go** buttons automatically, rather than having the user do it manually.

The ``SimpleModel`` also provides an error message if the **Go** button is pressed before the **Setup** button.

Fields
------
See :ref:`model-reference`.

Methods
-------
* ``__init__(title, x_tiles, y_tiles, setup_func, step_func, tile_size=8)``
    Creates a model with the given title and number of tiles on the x and y axis, as well as tile size. Also adds **Setup** and **Go** buttons to the simulation area.

For the remaining methods, see :ref:`model-reference`.
