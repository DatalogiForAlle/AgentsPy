Agent
=====

Description
-----------
Agents are the units that make up the "active" portion of the model. They generally move around the model area, interacting with each other.


Fields
------
* **x**
    The x-coordinate of the agent.

* **y**
    The y-coordinate of the agent.

* **size**
    The size of the agent. If the agent is drawn as a circle, this is equivalent to its diameter.

* **direction**
    The direction of the agent, measured in degrees.

* **speed**
    The speed of the agent. This is the distance it will move when calling **Agent.forward**.

* **selected**
    Whether or not the agent has been selected by clicking it. Generally, this should not be set manually, but it may be useful for debugging. For example, to print the coordinates of the selected agent, use something to the effect of:
    ::

        for a in model.agents:
            if a.selected:
                print(a.x,a.y)

* **color**
    The color of the agent. Must be provided as an RGB 3-tuple, e.g. (255, 255, 255) to color the agent white.

Methods
-------
* **__init__()**
    Creates an agent with a random position, direction and color. Has no initial model; this must be provided by **Agent.set_model**.

* **set_model(model)**
    Provides the Model **model** that the agents belongs to. The stored model is used in other methods such as **Agent.agents_nearby** and **Agent.current_tile**, which rely on information about other objects in the model.

* **setup(model)**
    This method is run when the agent is added to the Model **model**. It is empty by default, and is intented to be overwritten by a subclass.

* **update_current_tile()**
    Updates the tile that the agent is currently standing on.

    Effectively, this removes the agent from the set of agents standing on the previous tile, and adds it to the set of agents standing on the current tile.

* **current_tile()**
    Returns the tile that the agent is currently standing on, based on its coordinates.

    The tile returned is the one that overlaps with the exact center of the agent, so even if the agent visually covers multiple tiles due to its size, only one tile is returned.

* **align()**
    Moves the agent such that its center is the same as the center of its current tile.

* **distance_to(x,y)**
    Returns the euclidean distance from the agent's center to the point specified by (**x**, **y**).

* **direction_to(x,y)**
    Returns the direction, in degrees, from the agent's center to the point specified by (**x**, **y**).

* **point_towards(x,y)**
    Adjusts the direction of the agent, such that it points towards the point (**x**, **y**).

* **forward()**
    Moves the agent forward in the direction **self.direction** with a distance of **self.speed**. Updates the current tile of the agent.

* **jump_to(x,y)**
    Moves the center of the agent to the point specified by (**x**, **y**). Updates the current tile of the agent.

* **agents_nearby(distance, agent_type=None)**
    Returns the set of all agents whose center is within **distance** of the calling agent's center, excluding the agent itself.

    A subclass of **Agent** may be provided as a parameter **agent_type**, such that the set only contains agents of that subclass. If None is provided as the argument, agents of all types are included in the set.

* **nearby_tiles(x1,y1,x2,y2)**
    Returns the set of all tiles in a rectangular area around the agent. The upper-left point of the rectangle is (**self.x+x1**, **self.y+y1**), the lower-right point is (**self.x+x2**, **self.y+y2**).

    The agent's own tile is also included.

* **neighbor_tiles()**
    The same as calling **nearby_tiles(-1,-1,1,1)**.

* **destroy()**
    Marks the agent as destroyed, removing it from the set of agents in its stored model.

* **is_destroyed()**
    Returns True if **destroy()** has been called on this agent, False otherwise.

