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
    Creates an agent with a random position, direction and color. Has no
    initial model; this must be provided by ``Agent.set_model``.
    """

    def __init__(self):
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
        self.__color = (int(r * 255), int(g * 255), int(b * 255))

        self.x = 0
        self.y = 0
        self.size = 8
        self.__direction = random.randint(0, 359)
        self.speed = 1
        self.__current_tile = None
        self.__draw_path = False
        self.__paths = []
        self.__prev_pos = (self.x, self.y)
        self.selected = False
        self.shape = AgentShape.ARROW

        # Associated simulation area.
        get_quickstart_model().add_agent(self, setup=False)

    # Should be overwritten by a subclass
    def setup(self, model):
        """
        This method is run when the agent is added to a model. The method is
        empty by default, and is intented to be overwritten by a subclass.

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

        Effectively, this removes the agent from the set of agents standing on
        the previous tile, and adds it to the set of agents standing on the
        current tile.
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
        skip_draw = False
        if self.__model.wrapping():
            skip_draw = self.__wraparound()
        else:
            self.__stay_inside()
        self.update_current_tile()
        new_pos = (self.x, self.y)
        if self.__draw_path and not skip_draw:
            self.__paths[-1].append((self.__prev_pos, new_pos))
        self.__prev_pos = new_pos

    # Makes the agent wrap around the simulation area
    def __wraparound(self):
        # We've found need to introduce this hack, where we do modulus
        # twice, as there's some problems with the built-in Python
        # modulus operator
        # Example where it's necessary:
        #   >>> -1.8369701987210297e-16 % 400
        #   400.0
        #
        # This should've returned 0.
        prev_x = self.x
        prev_y = self.y
        self.x = self.x % self.__model.width % self.__model.width
        self.y = self.y % self.__model.height % self.__model.height
        # Returns true if a wrap occurred
        return prev_x != self.x or prev_y != self.y

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

        The stored model is used in other methods such as
        ``Agent.agents_nearby`` and ``Agent.current_tile``, which rely on
        information about other objects in the model.

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
            The distance to move the agent. If none is specified, it moves a
            distance equal to its speed-attribute.
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
            The distance to move the agent. If none is specified, it moves a
            distance equal to its speed-attribute.
        """
        if distance is None:
            distance = self.speed
        self.x -= math.cos(math.radians(self.direction)) * distance
        self.y -= math.sin(math.radians(self.direction)) * distance
        self.__post_move()

    def rotate(self, degrees):
        """
        Make the agent turn the given number of degrees. Positive is
        counter-clockwise, negative is clockwise.

        Parameters
        ----------
        degrees
            The amount of degrees to turn.
        """
        self.direction += degrees

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
        Returns the tile that the agent is currently standing on, based on its
        coordinates.

        The tile returned is the one that overlaps with the exact center of the
        agent, so even if the agent visually covers multiple tiles due to its
        size, only one tile is returned.
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
            The x-coordinate of the top-left tile
            (relative to the current tile).
        y1
            The y-coordinate of the top-left tile
            (relative to the current tile).
        x2
            The x-coordinate of the bottom-right tile
            (relative to the current tile).
        y2
            The y-coordinate of the bottom-right tile
            (relative to the current tile).
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
        Marks the agent for destruction, removing it from the set of agents in
        the model.
        """
        if not self.__destroyed:
            self.__destroyed = True

    def pendown(self):
        self.__draw_path = True
        self.__paths.append([])

    def penup(self):
        self.__draw_path = False

    def get_paths(self):
        return self.__paths

    @property
    def color(self):
        """
        The color of the agent. Must be provided as an RGB 3-tuple, e.g. (255,
        255, 255) to color the agent white.
        """
        return self.__color

    @color.setter
    def color(self, color):
        r, g, b = color
        self.__color = [r, g, b]

    @property
    def direction(self):
        """
        The direction of the agent, measured in degrees.
        """
        return self.__direction % 360

    @direction.setter
    def direction(self, direction):
        self.__direction = direction % 360


class Tile:
    """
    Creates a tile. *x* and *y* is the tile's position in the *tile grid*, not
    absolute coordinates for the model.

    Parameters
    ----------
    x
        The tile's x-coordinate in the tile grid.
    y
        The tile's y-cooridnate in the tile grid.
    model
        The model that the tile is a part of.
    """

    def __init__(self, x, y, model):
        self.x = x
        self.y = y
        self.info = {}
        self.color = (0, 0, 0)
        self.__agents = set()
        self.__model = model

    def add_agent(self, agent):
        """
        Adds an Agent to the set of agents standing on the tile. Usually called
        by the method ``Agent.update_current_tile``.

        Parameters
        ----------
        agent
            The agent to add.
        """
        self.__agents.add(agent)

    def remove_agent(self, agent):
        """
        Removes an Agent ``agent`` from the set of agents standing on the tile.
        Usually called by the method ``Agent.update_current_tile``.

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
    def __init__(self, variable, initial, minval, maxval):
        self.variable = variable
        self.minval = minval
        self.maxval = maxval
        self.initial = initial


class CheckboxSpec(Spec):
    def __init__(self, variable):
        self.variable = variable


class LineChartSpec(Spec):
    def __init__(self, variables, colors, min_y, max_y):
        self.variables = variables
        self.colors = colors
        self.min_y = min_y
        self.max_y = max_y


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


class AgentGraphSpec(Spec):
    def __init__(self, agents, variable, min_y, max_y):
        self.agents = agents
        self.variable = variable
        self.min_y = min_y
        self.max_y = max_y


class EllipseStruct:
    def __init__(self, x, y, w, h, color):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color


class RectStruct:
    def __init__(self, x, y, w, h, color):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color


class Model:
    """
    Creates a model with the given title. There are two ways of creating a
    model; creating a blank model of size *x_tiles* times *y_tiles* with no
    predetermined data, or creating a model with predetermined data from a
    *cell_data_fille*.

    Parameters
    ----------
    title
        The title of the model (to show in the simulation window).
    x_tiles
        The number of tiles on the x-axis. Ignored if a *cell_data_file* is
        provided.
    y_tiles
        The number of tiles on the y-axis. Ignored if a *cell_data_file* is
        provided.
    tile_size
        The width/height of each tile in pixels.
    cell_data_file
        If provided, generates a model from the data file instead. The data is
        not immediately to the tiles, but must be applied with
        ``Model.reload()``.
    """

    def __init__(
        self, title, x_tiles=50, y_tiles=50, tile_size=8, cell_data_file=None
    ):
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
            self.header_info = header_line.split("\t")

            self.x_tiles = 0
            self.y_tiles = 0
            self.load_data = []
            for line in cell_data:
                cell = line[:-1].split("\t")
                x = int(cell[0])
                y = int(cell[1])
                self.x_tiles = max(x + 1, self.x_tiles)
                self.y_tiles = max(y + 1, self.y_tiles)
                self.load_data.append(cell)

            cell_data.close()

        # Initial tileset (empty).
        self.tiles = [
            Tile(x, y, self)
            for y in range(self.y_tiles)
            for x in range(self.x_tiles)
        ]

        # Pixel sizes
        self.tile_size = tile_size
        self.width = self.x_tiles * tile_size
        self.height = self.y_tiles * tile_size

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
        """
        Adds an agent to the model.

        Parameters
        ----------
        agent
            The agent to add to the model.
        setup
            Whether or not to run the agent's ``setup`` function (default
            ``True``).
        """
        agent.set_model(self)
        agent.jump_to(
            random.randint(0, self.width), random.randint(0, self.height)
        )
        agent.update_current_tile()
        self.__agents.append(agent)
        if setup:
            agent.setup(self)
        for plot in self.plots:
            if type(plot.spec) is AgentGraphSpec:
                plot.spec.agents.append(agent)

    def add_agents(self, agents):
        """
        Adds a collection of agents.

        Parameters
        ----------
        agents
            The agents to add.
        """
        for a in agents:
            self.add_agent(a)

    def tile(self, x, y):
        """
        Returns the tile at the (x,y) position in the tile-grid (*not* the
        (x,y) position of the simulation area).

        Parameters
        ----------
        x
            The x-coordinate of the tile.
        y
            The y-coordinate of the tile.
        """
        row = y % self.y_tiles
        column = x % self.x_tiles
        return self.tiles[row * self.x_tiles + column]

    # Based on
    # kite.com
    # /python
    # /answers
    # /how-to-sort-a-list-of-objects-by-attribute-in-python
    def agents_ordered(self, variable, increasing=True):
        """
        Returns a list of agents in the model, ordered based on one of their
        attributes. Agents who do not have the attribute are not included in
        the list.

        Parameters
        ----------
        variable
            The attribute to order by.
        increasing
            Whether or not to order the agents in increasing or decreasing
            order (default ``True``).
        """
        # Only returns the list of agents that actually have that attribute
        agent_list = filter(lambda a: hasattr(a, variable), self.__agents)
        ret_list = sorted(agent_list, key=operator.attrgetter(variable))
        if not increasing:
            ret_list.reverse()
        return iter(ret_list)

    # Destroys all agents, clears the agent set, and resets all tiles.
    def reset(self):
        """
        Resets the model by doing the following:

        * Destroys all agents.
        * Clears the set of agents.
        * Clears the set of shapes.
        * Clears all tiles (removes all of their ``info`` and colors them
          black).
        * Clears all plots.
        * Unpauses the model.
        """
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
        """
        Applies the data from the cell-data-file to the tiles in the model.
        Only usable if the model was created with a ``cell_data_file`` in the
        constructor.
        """
        for tile_data in self.load_data:
            x = int(tile_data[0])
            y = int(tile_data[1])
            for i in range(2, len(tile_data)):
                variable = self.header_info[i]
                tile = self.tiles[y * self.x_tiles + x]
                tile.info[variable] = float(tile_data[i])

    def update_plots(self):
        """
        Updates all plots with the relevant data. Usually called in each
        iteration of the simulation (i.e. in a ``step`` function or similar).
        """
        for plot in self.plots:
            if type(plot.spec) is LineChartSpec:
                dataset = []
                for d in plot.spec.variables:
                    dataset.append(getattr(self, d))
                plot.add_data(dataset)
            elif type(plot.spec) is BarChartSpec:
                dataset = []
                for d in plot.spec.variables:
                    dataset.append(getattr(self, d))
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
            elif type(plot.spec) is AgentGraphSpec:
                plot.update_data()

    def remove_destroyed_agents(self):
        new_agents = []
        for a in self.__agents:
            if not a.is_destroyed():
                new_agents.append(a)
            else:
                a.current_tile().remove_agent(a)
        self.__agents = new_agents

    def clear_plots(self):
        """
        Clears the data from all plots.
        """
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
        """
        Creates a new row to place controller widgets on (buttons, sliders,
        etc.).
        """
        self.current_row = []
        self.controller_rows.append(self.current_row)

    def add_button(self, label, func, toggle=False):
        """
        Adds a button that runs a provided function when pressed. Can be
        specified to be a toggled button, which will cause the button to
        continuously call the function while toggled on.

        Parameters
        ----------
        label
            The label on the button.
        func
            The function to run when the button is pressed.
        toggle
            Whether or not the button should be a toggled button.
        """
        if not toggle:
            self.current_row.append(ButtonSpec(label, func))
        else:
            self.current_row.append(ToggleSpec(label, func))

    def add_slider(self, variable, initial, minval=0, maxval=100):
        """
        Adds a slider that can be used to adjust the value of a variable in the
        model.

        Parameters
        ----------
        variable
            The name of the variable to adjust. Must be privded as a string.
        minval
            The minimum value of the variable.
        maxval
            The maximum value of the variable.
        initial
            The initial value of the variable.
        """
        if len(self.current_row) > 0:
            self.add_controller_row()
        setattr(self, variable, initial)
        self.variables[variable] = initial
        self.current_row.append(SliderSpec(variable, initial, minval, maxval))

    def add_checkbox(self, variable):
        """
        Adds a checkbox that can be used to change the value of a variable
        between true and false.

        Parameters
        ----------
        variable
            The name of the variable to adjust. Must be provided as a string.
        """
        if len(self.current_row) > 0:
            self.add_controller_row()
        setattr(self, variable, False)
        self.current_row.append(CheckboxSpec(variable))

    def line_chart(self, variables, colors, min_y=None, max_y=None):
        """
        Adds a line chart to the simulation window that shows the trend of
        multiple variables over time.

        Parameters
        ----------
        variables
            The names of the variables. Must be provided as a list of strings.
        colors
            The color of each line.
        min_y
            The minimum value on the y-axis.
        max_y
            The maximum value on the y-axis.
        """
        self.plot_specs.append(LineChartSpec(variables, colors, min_y, max_y))

    def bar_chart(self, variables, color):
        """
        Adds a bar chart to the simulation window that shows the relation
        between multiple variables.

        Parameters
        ----------
        variables
            The list of the variables. Must be provided as a list of strings.
        color
            The color of all the bars.
        """
        self.plot_specs.append(BarChartSpec(variables, color))

    def histogram(self, variable, minimum, maximum, bins, color):
        """
        Adds a histogram to the simulation window that shows how the agents in
        the model are distributed based on a specific attribute.

        Parameters
        ----------
        variable
            The name of the attribute to base the distribution on. Must be
            provided as a string.
        minimum
            The minimum value of the distribution.
        maximum
            The maximum value of the distribution.
        bins
            The number of bins in the histogram.
        color
            The color of all the bars.
        """
        self.plot_specs.append(
            HistogramSpec(variable, minimum, maximum, bins, color)
        )

    def agent_line_chart(self, variable, min_y=None, max_y=None):
        """
        Adds a line chart to the simulation window that shows the trend of
        multiple variables over time.

        Parameters
        ----------
        variables
            The names of the variables. Must be provided as a list of strings.
        colors
            The color of each line.
        min_y
            The minimum value on the y-axis.
        max_y
            The maximum value on the y-axis.
        """
        self.plot_specs.append(AgentGraphSpec([], variable, min_y, max_y))

    def monitor(self, variable):
        """
        Adds a single line that shows the value of the given variable.

        Parameters
        ----------
        variable
            The variable to monitor.
        """
        if len(self.current_row) > 0:
            self.add_controller_row()
        self.current_row.append(MonitorSpec(variable))

    def add_ellipse(self, x, y, w, h, color):
        """
        Draws an ellipse on the simulation area. Returns a shape object that
        can be used to refer to the ellipse.

        Parameters
        ----------
        x
            The top-left x-coordinate of the ellipse.
        y
            The top-left y-coordinate of the ellipse.
        w
            The width of the ellipse.
        h
            The height of the ellipse.
        color
            The color of the ellipse.
        """
        new_shape = EllipseStruct(x, y, w, h, color)
        self._shapes.append(new_shape)
        return new_shape

    def add_rect(self, x, y, w, h, color):
        """
        Draws a square on the simulation area. Returns a shape object that can
        be used to refer to the square.

        Parameters
        ----------
        x
            The top-left x-coordinate of the square.
        y
            The top-left y-coordinate of the square.
        w
            The width of the square.
        h
            The height of the square.
        color
            The color of the square.
        """
        new_shape = RectStruct(x, y, w, h, color)
        self._shapes.append(new_shape)
        return new_shape

    def get_shapes(self):
        """
        Returns an iterator containing all the shapes in the model.
        """
        return iter(self._shapes)

    def clear_shapes(self):
        """
        Clears all shapes in the model.
        """
        self._shapes.clear()

    def is_paused(self):
        """
        Returns whether the model is paused or not.
        """
        return self._paused

    def pause(self):
        """
        Pauses the model. The main effect of this is to ignore the "on" status
        of any toggled buttons, meaning that `step` functions and similar are
        not run.
        """
        self._paused = True

    def unpause(self):
        """
        Unpauses the model. See `Model.pause()`.
        """
        self._paused = False

    def on_close(self, func):
        """
        Defines a function to be run when the simulation window is closed. This
        is generally used to close any open file pointers.
        """
        self._on_close = func

    def close(self):
        self.pause()
        if self._close_func:
            self._close_func(self)

    def enable_wrapping(self):
        """
        Enables wrapping, i.e. turns the simulation area *toroidal*. Agents
        exiting the simulation area on one side will enter on the other side.
        """
        self._wrapping = True

    def disable_wrapping(self):
        """
        Disables wrapping. Agents attempting to move outside the simulation
        area will collide with the border and be moved back to the closest
        point inside.
        """
        self._wrapping = False

    def wrapping(self):
        """
        Returns whether wrapping is enabled or not.
        """
        return self._wrapping

    def agent_count(self):
        return len(self.__agents)

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
    def __init__(
        self, title, x_tiles, y_tiles, setup_func, step_func, tile_size=8
    ):
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
        self.add_button("Go", step_wrapper, toggle=True)


def get_quickstart_model():
    global quickstart_model
    if "quickstart_model" not in globals():
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
    Returns the agents list, sorted by variable in either increasing or
    decreasing order. Prints an error if not all agents in the list have the
    attribute.
    """
    try:
        sorted_agents = sorted(list(agents), key=operator.attrgetter(variable))
        if not increasing:
            sorted_agents.reverse()
        return iter(sorted_agents)
    except AttributeError:
        print(
            "Failed to sort agents. Do all agents have the attribute "
            + variable
            + " ?"
        )
        return agents


def agents_random(agents):
    l_agents = list(agents)
    random.shuffle(l_agents)
    return l_agents


def destroy_agents(agents):
    """
    Destroys all agents in agents.
    """
    for a in agents:
        a.destroy()
