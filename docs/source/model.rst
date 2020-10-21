.. _model-reference:

Model
=====

.. autoclass:: agents.Model
   :members:

Fields
------
* ``title``
    The title of the model. This will be shown in the top of the window when running the simulation.

* ``width``
    The width of the model.

* ``height``
    The height of the model.

* ``x_tiles``
    The number of tiles on the x-axis.

* ``y_tiles``
    The number of tiles on the y-axis.

* ``tile_size``
    The length of the side of a single tile.

* ``tiles``
    The array containing all tiles in the model. The tiles are ordered by row, so ``self.tiles[0]`` is the tile in position (0,0), ``self.tiles[1]`` is the tile in position (1,0), and so on.

    To find the Tile ``tile`` in *position* (x,y), use the formula:
    ::

        tile = self.tiles[y * self.x_tiles + x]

    Note that x and y represent the "x'th tile from the left" and "y'th tile from the top", and not absolute coordinates. To find the tile at *coordinates* (x,y), use the formula:
    ::

        x = math.floor(self.x_tiles * x / self.width)
        y = math.floor(self.y_tiles * y / self.height)
        tile = self.tiles[y * self.x_tiles + x]

* ``agents``
    A set containing all agents in the model. Accessing this property will automatically clear destroyed agents from the set.

    Accessing this property, agents are always returned in the same order.

Methods
-------
* ``__init__(title, x_tiles=50, y_tiles=50, tile_size=8, cell_data_file=None)``
    If no ``cell_data_file`` is specified, creates a model with the given title, number of tiles on the x and y axis, and size of each tile may also be defined.

    If a string is given for ``cell_data_file``, tile-data is stored in the model based on the specifications in the file.

    *Cell-data file format:*

    The two initial are not parsed, and may contain information about the cell-data or other comments. The third line must contain a set of column names, seperated by tabs. The column names specify the names of variables stored by each tile. The first and second column cannot be used for variables, but must instead contain x and y coordinates, respectively.

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

    Note that the values specified in the file are not immediately applied to the tiles, but must
    be loaded in using the ``Model.reload`` method.

* ``add_agent(agent)``
    Adds the Agent ``agent`` to the model's internal set. The agent is then placed on a random coordinate within the model, and ``agent.setup`` is called, with the argument being the model itself.

* ``add_agents(agents)``
    Adds each agent in the set ``agents`` using ``self.add_agent``.

* ``agents_random()``
    Returns a list of all agents, shuffled randomly. Also clears destroyed agents.

* ``agents_ordered(variable, increasing=True)``
    Returns a list of all agents, ordered either in increasing or decreasing order based on the attribute ``variable``.

* ``reset()``
    Destroys all agents, clears the set of ``self.agents``, then resets all tiles by coloring them black and clearing their ``info``.

* ``reload()``
    Only relevant if generating a model from file data. This applies all the data from the file to the tiles in the model.

* ``update_plots()``
    Updates all existing plots. This either adds a new data point to a graph plot, or refreshes a histogram plot. This method should only be called once each simulation step.

* ``remove_destroyed_agents()``
    Immediately removed all destroyed agents from the ``self.agents`` set.

* ``clear_plots()``
    Clears all plots. Graphs have all their data points removed, while the bars of all histograms are set to 0.

* ``add_button(label, func)``
    Adds a button to the simulation with the label ``label``. When the button is pressed, ``func`` is called once with the model itself as the only argument.

* ``add_toggle_button(label, func)``
    Adds a toggleable button to the simulation with the label ``label``. When the button is pressed, ``func`` is called continuously with the model itself as the only argument.

* ``add_slider(variable, minval, maxval, initial)``
    Adds a slider to the simulation, which can then be used to adjust the value of ``self[variable]``. ``minval`` and ``maxval`` determine the minimum and maximum, respectively, while ``initial`` sets the initial value of ``self[variable]``.

* ``add_checkbox(variable)``
    Adds a checkbox to the simulation, which can then toggle ``self[variable]`` between True and False.

* ``line_chart(variable, color)``
    Adds a line graph to the simulation, which shows the trend of ``self[variable]`` over time. The color of the line can be specified with ``color``, an RGB 3-tuple.

* ``bar_chart(variables, color)``
    Adds a bar chart to the simulation, which shows the relation between all variables given in the list ``variables``. The color of the bars can be specified with ``color``, an RGB 3-tuple.

* ``histogram(variable, minimum, maximum, bins, color)``
    Adds a histogram to the simulation, which takes the value of ``variable`` for each *agent* in the model, then shows the distribution of those values as a histogram. A total of ``bins`` bars are shown in the histogram, covering the interval between ``minimum`` and ``maximum``.

    Thus, each bar represents an interval of size:
    ::

        (maximum - minimum) / bins

* ``monitor(variable)``
    Adds a monitor to the simulation, which constantly shows the value of ``self[variable]``.

* ``on_close(func)``
    Defines a function that should be run when the simulation window closes. This could, for example, be an ``f.close()`` call to close a data file that is being written to.

* ``pause()``
    Pauses the model by disabling all toggleable buttons.

* ``unpause()``
    Unpauses the model by re-enabling all toggleable buttons.

* ``is_paused()``
    Returns a bool signaling whether or not the model is paused.

* ``enable_wrapping()``
    Enables the wrapping of the simulation area, meaning that agents who move outside the border of the area will appear on the opposite side.

* ``disable_wrapping()``
    Disables the wrapping of the simulation area, causing agents that move outside the border of the area to be moved to the closest point inside the area.

* ``wrapping()``
    Returns a bool signaling whether or not the model has wrapping enabled.
