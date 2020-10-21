import math
import random
import operator
import colorsys
from enum import Enum


class AgentShape(Enum):
    CIRCLE = 1
    ARROW = 2
    PERSON = 3
    HOUSE = 4


class Agent:
    """
    Agents are the units that make up the "active" portion of the model. They generally move around the model area, interacting with each other.
    """
    def __init__(self):
        """
        Creates an agent with a random position, direction and color. Has no initial model; this must be provided by ``Agent.set_model``.
        """
        # Destroyed agents are not drawn and are removed from their area.
        self.__destroyed = False

        # Number of edges in the regular polygon representing the agent.
        self.__resolution = 10

        # Generate agent color in HSL and convert to RGB, to avoid
        # dark colors, with low contrast to the default black
        # background
        hue = random.random()
        saturation = random.uniform(0.8, 1.0)
        lightness = random.uniform(0.25, 1.0)
        r, g, b = colorsys.hls_to_rgb(hue, lightness, saturation)
        self.__color = (int(r*255), int(g*255), int(b*255))

        self.x = 0
        """The x-coordinate of the agent."""
        self.y = 0
        """The y-coordinate of the agent."""
        self.size = 8
        """The size of the agent. If the agent is drawn as a circle, this is equivalent to its diameter."""
        self.__direction = random.randint(0, 359)
        self.speed = 1
        """The speed of the agent. This is the default distance it will move when calling forward or backward."""
        self.__current_tile = None
        self.selected = False
        self.shape = AgentShape.ARROW

        # Associated simulation area.
        get_quickstart_model().add_agent(self, setup=False)

    # Should be overwritten by a subclass
    def setup(self, model):
        """
        This method is run when the agent is added to a model. The method is empty by default, and is intented to be overwritten by a subclass.

        Parameters
        ----------
        model
            The model object that the agent has been added to.
        """
        pass

    # Update current tile
    def update_current_tile(self):
        """
        Updates the tile that the agent is currently standing on.

        Effectively, this removes the agent from the set of agents standing on the previous tile, and adds it to the set of agents standing on the current tile.
        """
        new_tile = self.current_tile()
        if not self.__current_tile:
            self.__current_tile = new_tile
            self.__current_tile.add_agent(self)
        elif not (self.__current_tile is new_tile):
            self.__current_tile.remove_agent(self)
            new_tile.add_agent(self)
            self.__current_tile = new_tile

    # To be called after each movement step
    def __post_move(self):
        if self.__model.wrapping():
            self.__wraparound()
        else:
            self.__stay_inside()
        self.update_current_tile()

    # Makes the agent wrap around the simulation area
    def __wraparound(self):
        self.x = self.x % self.__model.width
        self.y = self.y % self.__model.height

    # If the agent is outside the simulation area,
    # return it to the closest point inside
    def __stay_inside(self):
        self.x = min(max(self.x, 0), self.__model.width)
        self.y = min(max(self.y, 0), self.__model.height)

    def center_in_tile(self):
        """
        Move the agent to the center of the tile it is standing on.
        """
        w = self.__model.width
        h = self.__model.height
        tx = self.__model.x_tiles
        ty = self.__model.y_tiles
        self.x = math.floor(self.x * tx / w) * w / tx + (w / tx) / 2
        self.y = math.floor(self.y * ty / h) * h / ty + (h / ty) / 2
        self.__post_move()

    def jump_to(self, x, y):
        """
        Move the agent to a specified point.

        Parameters
        ----------
        x
            Destination x-coordinate.
        y
            Destination y-coordinate.
        """
        self.x = x
        self.y = y
        self.__post_move()

    def jump_to_tile(self, t):
        """
        Move the agent to the center of a specified tile.

        Parameters
        ----------
        t
            Destination tile.
        """
        w = self.__model.width
        h = self.__model.height
        x_tiles = self.__model.x_tiles
        y_tiles = self.__model.y_tiles
        self.x = t.x * w / x_tiles
        self.y = t.y * h / y_tiles
        self.center_in_tile()
        self.__post_move()

    def set_model(self, model):
        """
        Provides the Model object that the agents belongs to.

        The stored model is used in other methods such as ``Agent.agents_nearby`` and ``Agent.current_tile``, which rely on information about other objects in the model.

        Parameters
        ----------
        model
            The model to assign the agent to.
        """
        self.__model = model

    def direction_to(self, other_x, other_y):
        """
        Calculate the direction in degrees from the agent to a given point.

        Parameters
        ----------
        other_x
            The x-coordinate of the target point.
        other_y
            The y-coordinate of the target point.
        """
        direction = 0
        dist = self.distance_to(other_x, other_y)
        if dist > 0:
            direction = math.degrees(math.acos((other_x - self.x) / dist))
            if (self.y - other_y) > 0:
                direction = 360 - direction
        return direction

    def point_towards(self, other_x, other_y):
        """
        Make the agent orient itself towards a given point.

        Parameters
        ----------
        other_x
            The x-coordinate of the target point.
        other_y
            The y-coordinate of the target point.
        """
        dist = self.distance_to(other_x, other_y)
        if dist > 0:
            self.direction = math.degrees(math.acos((other_x - self.x) / dist))
            if (self.y - other_y) > 0:
                self.direction = 360 - self.direction

    def forward(self, distance=None):
        """
        Moves the agent forward in the direction it is currently facing.

        Parameters
        ----------
        Distance
            The distance to move the agent. If none is specified, it moves a distance equal to its speed-attribute.
        """
        if distance is None:
            distance = self.speed
        self.x += math.cos(math.radians(self.direction)) * distance
        self.y += math.sin(math.radians(self.direction)) * distance
        self.__post_move()

    def backward(self, distance=None):
        """
        Moves the agent in the opposite direction of its current orientation.

        Parameters
        ----------
        Distance
            The distance to move the agent. If none is specified, it moves a distance equal to its speed-attribute.
        """
        if distance is None:
            distance = self.speed
        self.x -= math.cos(math.radians(self.direction)) * distance
        self.y -= math.sin(math.radians(self.direction)) * distance
        self.__post_move()

    def left(self, degrees):
        """
        Make the agent turn left (counter clockwise) the given number of degrees.

        Parameters
        ----------
        degrees
            The amount of degrees to turn.
        """
        self.direction += degrees

    def right(self, degrees):
        """
        Make the agent turn right (clockwise) the given number of degrees.

        Parameters
        ----------
        degrees
            The amount of degrees to turn.
        """
        self.direction -= degrees

    def distance_to(self, other_x, other_y):
        """
        Returns the distance between the agent and another point.

        Parameters
        ----------
        other_x
            The x-coordinate of the target point.
        other_y
            The y-coordinate of the target point.
        """
        return ((self.x - other_x) ** 2 + (self.y - other_y) ** 2) ** 0.5

    def agents_nearby(self, distance, agent_type=None):
        """
        Returns a list of nearby agents.
        May take a type as argument and only return agents of that type.

        Parameters
        ----------
        distance
            The radius around the agent to search in.
        agent_type
            If provided, only returns agents of this type.
        """
        nearby = set()
        for a in self.__model.agents:
            if self.distance_to(a.x, a.y) <= distance and not (a is self):
                if agent_type is None or type(a) is agent_type:
                    nearby.add(a)
        return nearby

    def current_tile(self):
        """
        Returns the tile that the agent is currently standing on, based on its coordinates.

        The tile returned is the one that overlaps with the exact center of the agent, so even if the agent visually covers multiple tiles due to its size, only one tile is returned.
        """
        x = math.floor((self.__model.x_tiles * self.x) / self.__model.width)
        y = math.floor((self.__model.y_tiles * self.y) / self.__model.height)
        return self.__model.tile(x, y)

    def neighbor_tiles(self):
        """
        Returns the surrounding tiles as a 3x3 grid. Includes the current tile.
        """
        return self.nearby_tiles(-1, -1, 1, 1)

    def nearby_tiles(self, x1, y1, x2, y2):
        """
        Returns a rectangle of tiles relative to the agent's current position.

        Parameters
        ----------
        x1
            The x-coordinate of the top-left tile (relative to the current tile).
        y1
            The y-coordinate of the top-left tile (relative to the current tile).
        x2
            The x-coordinate of the bottom-right tile (relative to the current tile).
        y2
            The y-coordinate of the bottom-right tile (relative to the current tile).
        """
        tile = self.__current_tile
        tiles = []
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                tiles.append(self.__model.tile((tile.x + x), (tile.y + y)))
        return tiles

    def is_destroyed(self):
        """
        Returns True or False whether or not the agent is destroyed.
        """
        return self.__destroyed

    def destroy(self):
        """
        Marks the agent for destruction, removing it from the set of agents in the model.
        """
        if not self.__destroyed:
            self.__destroyed = True

    @property
    def color(self):
        """The color of the agent. Must be provided as an RGB 3-tuple, e.g. (255, 255, 255) to color the agent white."""
        return self.__color

    @color.setter
    def color(self, color):
        r, g, b = color
        self.__color = [r, g, b]

    @property
    def direction(self):
        """The direction of the agent, measured in degrees."""
        return self.__direction % 360

    @direction.setter
    def direction(self, direction):
        self.__direction = direction % 360


class Tile:
    """
    A square, of which many make up the "floor" of the model.
    """
    def __init__(self, x, y, model):
        self.x = x
        """The x-coordinate of the tile."""
        self.y = y
        """The y-coordinate of the tile."""
        self.info = {}
        """A dictionary, which may be used to store key-value pairs in the tile."""
        self.color = (0, 0, 0)
        """The color of the tile. Must be provided as an RGB 3-tuple, e.g. (255, 255, 255) to color the tile white."""
        self.__agents = set()
        self.__model = model

    def add_agent(self, agent):
        """
        Adds an Agent to the set of agents standing on the tile. Usually called by the method ``Agent.update_current_tile``.

        Parameters
        ----------
        agent
            The agent to add.
        """
        self.__agents.add(agent)

    def remove_agent(self, agent):
        """
        Removes an Agent ``agent`` from the set of agents standing on the tile. Usually called by the method ``Agent.update_current_tile``.

        Parameters
        ----------
        agent
            The agent to remove.
        """
        self.__agents.discard(agent)

    def get_agents(self):
        """
        Gets the set of agents currently on the tile.
        """
        return self.__agents


class Spec:
    pass


class ButtonSpec(Spec):
    def __init__(self, label, function):
        self.label = label
        self.function = function


class ToggleSpec(Spec):
    def __init__(self, label, function):
        self.label = label
        self.function = function


class SliderSpec(Spec):
    def __init__(self, variable, minval, maxval, initial):
        self.variable = variable
        self.minval = minval
        self.maxval = maxval
        self.initial = initial


class CheckboxSpec(Spec):
    def __init__(self, variable):
        self.variable = variable


class LineChartSpec(Spec):
    def __init__(self, variable, color):
        self.variable = variable
        self.color = color

class MultiLineChartSpec(Spec):
    def __init__(self, variables, colors):
        self.variables = variables
        self.colors = colors

class MonitorSpec(Spec):
    def __init__(self, variable):
        self.variable = variable


class BarChartSpec(Spec):
    def __init__(self, variables, color):
        self.variables = variables
        self.color = color


class HistogramSpec(Spec):
    def __init__(self, variable, minimum, maximum, intervals, color):
        self.variable = variable
        self.minimum = minimum
        self.maximum = maximum
        i_size = (maximum - minimum) / intervals
        self.bins = [
            (minimum + i_size * i, minimum + i_size * (i + 1))
            for i in range(intervals)
        ]
        self.color = color

class EllipseStruct():
    def __init__(self,x,y,w,h,color):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color

class RectStruct():
    def __init__(self,x,y,w,h,color):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color

class Model:
    """
    Models contain the agents and tiles that make up the simulation. They also provide some functionality for manipulating said simulation, such as buttons, and ways to visualize simulation data, such as graphs.

    To run a model, use
    ::

        agents.run(model)
    """
    def __init__(self, title, x_tiles=50, y_tiles=50, tile_size=8,
                 cell_data_file=None):
        # Title of model, shown in window title
        self.title = title

        if not cell_data_file:
            # Number of tiles on the x/y axis.
            self.x_tiles = x_tiles
            self.y_tiles = y_tiles

        else:
            cell_data = open(cell_data_file, "r")
            cell_data.readline()
            cell_data.readline()
            header_line = cell_data.readline()[:-1]
            self.header_info = header_line.split('\t')

            self.load_data = []
            for line in cell_data:
                cell = line[:-1].split('\t')
                x = int(cell[0])
                y = int(cell[1])
                self.x_tiles = max(x+1, x_tiles)
                self.y_tiles = max(y+1, y_tiles)
                self.load_data.append(cell)

            cell_data.close()

        # Initial tileset (empty).
        self.tiles = [Tile(x, y, self)
                      for y in range(y_tiles)
                      for x in range(x_tiles)]

        # Pixel sizes
        self.tile_size = tile_size
        self.width = x_tiles * tile_size
        self.height = y_tiles * tile_size

        self.__agents = []
        self.variables = {}
        self.plot_specs = []
        self.controller_rows = []
        self.add_controller_row()
        self.plots = set()  # Filled in during initialization
        self.show_direction = False
        self._paused = False
        self._wrapping = True
        self._close_func = None
        self._shapes = []

    def add_agent(self, agent, setup=True):
        agent.set_model(self)
        agent.x = random.randint(0, self.width)
        agent.y = random.randint(0, self.height)
        agent.update_current_tile()
        self.__agents.append(agent)
        if setup:
            agent.setup(self)

    def add_agents(self, agents):
        for a in agents:
            self.add_agent(a)

    def tile(self, x, y):
        row = y % self.y_tiles
        column = x % self.x_tiles
        return self.tiles[row * self.x_tiles + column]

    # Based on
    # kite.com
    # /python
    # /answers
    # /how-to-sort-a-list-of-objects-by-attribute-in-python
    def agents_ordered(self, variable, increasing=True):
        # Only returns the list of agents that actually have that attribute
        agent_list = filter(lambda a: hasattr(a, variable), self.__agents)
        ret_list = sorted(agent_list, key=operator.attrgetter(variable))
        if not increasing:
            ret_list.reverse()
        return iter(ret_list)

    # Destroys all agents, clears the agent set, and resets all tiles.
    def reset(self):
        for a in self.__agents:
            a.destroy()
        self.__agents = []
        self._shapes = []
        for x in range(self.x_tiles):
            for y in range(self.y_tiles):
                i = y * self.x_tiles + x
                self.tiles[i].color = (0, 0, 0)
                self.tiles[i].info = {}
        self.clear_plots()
        self.unpause()

    def reload(self):
        for tile_data in self.load_data:
            x = int(tile_data[0])
            y = int(tile_data[1])
            for i in range(2, len(tile_data)):
                variable = self.header_info[i]
                tile = self.tiles[y*self.x_tiles+x]
                tile.info[variable] = float(tile_data[i])

    def update_plots(self):
        for plot in self.plots:
            if type(plot.spec) is LineChartSpec:
                plot.add_data(self.variables[plot.spec.variable])
            elif type(plot.spec) is MultiLineChartSpec:
                dataset = []
                for d in plot.spec.variables:
                    dataset.append(self.variables[d])
                plot.add_data(dataset)
            elif type(plot.spec) is BarChartSpec:
                dataset = []
                for d in plot.spec.variables:
                    dataset.append(self.variables[d])
                plot.update_data(dataset)
            elif type(plot.spec) is HistogramSpec:
                dataset = []
                for b in plot.spec.bins:
                    bin_count = 0
                    for a in self.__agents:
                        if hasattr(a, plot.spec.variable):
                            val = getattr(a, plot.spec.variable)
                            if val >= b[0] and val <= b[1]:
                                bin_count += 1
                    dataset.append(bin_count)
                plot.update_data(dataset)

    def remove_destroyed_agents(self):
        new_agents = []
        for a in self.__agents:
            if not a.is_destroyed():
                new_agents.append(a)
            else:
                a.current_tile().remove_agent(a)
        self.__agents = new_agents

    def clear_plots(self):
        for plot in self.plots:
            plot.clear()

    def mouse_click(self, x, y):
        for a in self.__agents:
            a.selected = False
            if (
                a.x - a.size / 2 < x
                and a.x + a.size / 2 > x
                and a.y - a.size / 2 < y
                and a.y + a.size / 2 > y
            ):
                for b in self.__agents:
                    b.selected = False
                a.selected = True

    def add_controller_row(self):
        self.current_row = []
        self.controller_rows.append(self.current_row)

    def add_button(self, label, func):
        self.current_row.append(ButtonSpec(label, func))

    def add_toggle_button(self, label, func):
        self.current_row.append(ToggleSpec(label, func))

    def add_slider(self, variable, minval, maxval, initial):
        self.variables[variable] = initial
        self.current_row.append(SliderSpec(variable, minval, maxval, initial))

    def add_checkbox(self, variable):
        self.variables[variable] = False
        self.current_row.append(CheckboxSpec(variable))

    def line_chart(self, variable, color):
        self.plot_specs.append(LineChartSpec(variable, color))

    def multi_line_chart(self, variables, colors):
        self.plot_specs.append(MultiLineChartSpec(variables, colors))

    def bar_chart(self, variables, color):
        self.plot_specs.append(BarChartSpec(variables, color))

    def histogram(self, variable, minimum, maximum, bins, color):
        self.plot_specs.append(
            HistogramSpec(variable, minimum, maximum, bins, color)
        )

    def monitor(self, variable):
        self.current_row.append(MonitorSpec(variable))

    def add_ellipse(self,x,y,w,h,color):
        new_shape = EllipseStruct(x,y,w,h,color)
        self._shapes.append(new_shape)
        return new_shape

    def add_rect(self,x,y,w,h):
        new_shape = RectStruct(x,y,w,h,color)
        self._shapes.append(new_shape)
        return new_shape

    def get_shapes(self):
        return iter(self._shapes)

    def clear_shapes(self):
        self._shapes.clear()

    def is_paused(self):
        return self._paused

    def pause(self):
        self._paused = True

    def unpause(self):
        self._paused = False

    def on_close(self, func):
        self._close_func = func

    def close(self):
        self.pause()
        if self._close_func:
            self._close_func(self)

    def enable_wrapping(self):
        self._wrapping = True

    def disable_wrapping(self):
        self._wrapping = False

    def wrapping(self):
        return self._wrapping

    @property
    def agents(self):
        self.remove_destroyed_agents()
        return iter(self.__agents)

    @agents.setter
    def agents(self, agents):
        self.__agents = list(agents)

    def __setitem__(self, key, item):
        self.variables[key] = item

    def __getitem__(self, key):
        return self.variables[key]

    def __delitem__(self, key):
        del self.variables[key]


class SimpleModel(Model):
    def __init__(self, title,
                 x_tiles, y_tiles,
                 setup_func, step_func,
                 tile_size=8):
        super().__init__(title, x_tiles, y_tiles, tile_size)
        self.setup_first = False

        def setup_wrapper(model):
            model.setup_first = True
            setup_func(model)

        def step_wrapper(model):
            if model.setup_first:
                step_func(model)
            else:
                print("Remember to click 'Setup' first!")

        self.add_button("Setup", setup_wrapper)
        self.add_toggle_button("Go", step_wrapper)


def get_quickstart_model():
    global quickstart_model
    if 'quickstart_model' not in globals():
        quickstart_model = Model("AgentsPy model", 50, 50)
    return quickstart_model

def contains_agent_type(agents, agent_type):
    """
    Returns a boolean indicating whether an agent of agent_type is in agents.
    """
    for a in agents:
        if type(a) == agent_type:
            return True
    return False

def only_agents_type(agents, agent_type):
    """
    Returns agents where all agents of type agent_type are removed.
    """
    agents_t = []
    for a in agents:
        if type(a) == agent_type:
            agents_t.add(a)
    return agents_t

def remove_agents_type(agents, agent_type):
    """
    Returns agents where all agents not of type agent_type are removed.
    """
    agents_t = []
    for a in agents:
        if not (type(a) == agent_type):
            agents_t.add(a)
    return agents_t

# kite.com/python/answers/how-to-sort-a-list-of-objects-by-attribute-in-python
def agents_ordered(agents, variable, increasing=True):
    """
    Returns the agents list, sorted by variable in either increasing
    or decreasing order. Prints an error if not all agents in the list
    have the attribute.
    """
    try:
        sorted_agents = sorted(list(agents), key=operator.attrgetter(variable))
        if not increasing:
            sorted_agents.reverse()
        return iter(sorted_agents)
    except:
        print("Failed to sort agents. Do all agents have the attribute "+variable+" ?")
        return agents

def destroy_agents(agents):
    """
    Destroys all agents in agents.
    """
    for a in agents:
        a.destroy()
