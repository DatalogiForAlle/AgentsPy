Tile
=====

Description
-----------
A square, of which many make up the "floor" of the model.

Fields
------
* **x**
    The x-coordinate of the tile.

* **y**
    The y-coordinate of the tile.

* **info**
    A dictionary, which may be used to store key-value pairs in the tile.

* **color**
  The color of the tile. Must be provided as an RGB 3-tuple, e.g. (255, 255, 255) to color the tile white.


    Whether or not the agent has been selected by clicking it. Generally, this should not be set manually, but it may be useful for debugging. For example, to print the coordinates of the selected agent, use something to the effect of:
    ::

        for a in model.agents:
            if a.selected:
                print(a.x,a.y)


Methods
-------
* **__init__(x, y, model)**
    Creates a tile with the given x and y-coordinate, as well as defining the model it belongs to.

* **add_agent(agent)**
    Adds an Agent **agent** to the set of agents standing on the tile. Usually called by the method **Agent.update_current_tile**.

* **remove_agent(agent)**
    Removes an Agent **agent** from the set of agents standing on the tile. Usually called by the method **Agent.update_current_tile**.

* **get_agents()**
    Returns the set of agents currently standing on the tile.
