.. _model-reference:

Model
=====

Models contain the agents and tiles that make up the simulation. They also provide some functionality for manipulating said simulation, such as buttons, and ways to visualize simulation data, such as graphs.

To run a model, use
::

   agents.run(model)

.. autoclass:: agents.Model
   :members:

Cell-data file format
---------------------
The two initial lines are skipped, and may be used to describe the cell-data or for other comments. The third line must contain a set of column names, seperated by tabs. The column names specify the names of variables stored by each tile. The first and second column cannot be used for variables, but must instead contain x and y coordinates, respectively.

The remaining lines of the file should then contain the coordinates and variable data. The start of a cell-data file might look like this:
::

   This file contains cell data for a model where each cell/tile has some resource.
   The data specifies the rate of resource production and max resource content for each cell.
   x	y	prod	max_res
   0	0	0.15	10.0
   1	0	0.20	20.0
   2	0	0.05	30.0
   3	0	0.35	5.0
   ...
