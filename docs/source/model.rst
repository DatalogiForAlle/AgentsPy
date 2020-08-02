Model
=====

Description
-----------
Models contain the agents and tiles that make up the simulation. They also provide some functionality for manipulating said simulation, such as buttons, and ways to visualize simulation data, such as graphs.

To run a model, use
::

    agentspy.run(model)

where **model** is a reference to your model.

The model class itself also acts as a dictionary, so key-value pairs may be stored in a specific model. For example:
::

    model["foo"] = 42

Fields
------
* **title**
    The title of the model. This will be shown in the top of the window when running the simulation.

* **width**
    The width of the model.

* **height**
    The height of the model.

* **x_tiles**
    The number of tiles on the x-axis.

* **y_tiles**
    The number of tiles on the y-axis.

* **tile_size**
    The length of the side of a single tile.

* **tiles**
    The array containing all tiles in the model. The tiles are ordered by row, so **self.tiles[0]** is the tile in position (0,0), **self.tiles[1]** is the tile in position (1,0), and so on.

    To find the Tile **tile** in *position* (x,y), use the formula:
    ::

        tile = self.tiles[y * self.x_tiles + x]

    Note that x and y represent the "x'th tile from the left" and "y'th tile from the top", and not absolute coordinates. To find the tile at *coordinates* (x,y), use the formula:
    ::

        x = math.floor(self.x_tiles * x / self.width)
        y = math.floor(self.y_tiles * y / self.height)
        tile = self.tiles[y * self.x_tiles + x]

* **agents**
    A set containing all agents in the model. Accessing this property will automatically clear destroyed agents from the set.

    Accessing this property, agents are always returned in the same order.

Methods
-------
* **__init__(title, x_tiles, y_tiles, tile_size)**
    Creates a model with the given title and number of tiles on the x and y axis. The size of each tile may also be defined.

* **add_agent(agent)**
    Adds the Agent **agent** to the model's internal set. The agent is then placed on a random coordinate within the model, and **agent.setup** is called, with the argument being the model itself.

* **add_agents(agents)**
    Adds each agent in the set **agents** using **self.add_agent**.

* **agents_random()**
    Returns a list of all agents, shuffled randomly. Also clears destroyed agents.

* **agents_ordered(variable, increasing=True)**
    Returns a list of all agents, ordered either in increasing or decreasing order based on the attribute **variable**.

* **reset()**
    Destroys all agents, clears the set of **self.agents**, then resets all tiles by coloring them black and clearing their **info**.

* **update_plots()**
    Updates all existing plots. This either adds a new data point to a graph plot, or refreshes a histogram plot. This method should only be called once each simulation step.

* **remove_destroyed_agents()**
    Immediately removed all destroyed agents from the **self.agents** set.

* **clear_plots()**
    Clears all plots. Graphs have all their data points removed, while the bars of all histograms are set to 0.

* **add_button(label, func)**
    Adds a button to the simulation with the label **label**. When the button is pressed, **func** is called once with the model itself as the only argument.

* **add_toggle_button(label, func)**
    Adds a toggleable button to the simulation with the label **label**. When the button is pressed, **func** is called continuously with the model itself as the only argument.

* **add_slider(variable, minval, maxval, initial)**
    Adds a slider to the simulation, which can then be used to adjust the value of **self[variable]**. **minval** and **maxval** determine the minimum and maximum, respectively, while **initial** sets the initial value of **self[variable]**.

* **add_checkbox(variable)**
    Adds a checkbox to the simulation, which can then toggle **self[variable]** between True and False.

* **graph(variable, color)**
    Adds a line graph to the simulation, which shows the trend of **self[variable]** over time. The color of the line can be specified with **color**, an RGB 3-tuple.

* **histogram(variables, color)**
    Adds a histogram to the simulation, which shows the relation between all variables given in the list **variables**. The color of the bars can be specified with **color**, an RGB 3-tuple.

* **histogram_bins(variable, minimum, maximum, bins, color)**
    Adds a histogram to the simulation, which takes the value of **variable** for each *agent* in the model, then shows the distribution of those values as a histogram. A total of **bins** bars are shown in the histogram, covering the interval between **minimum** and **maximum**.

    Thus, each bar represents an interval of size:
    ::

        (maximum - minimum) / bins

* **monitor(variable)**
    Adds a monitor to the simulation, which constantly shows the value of **self[variable]**.
