import math
import random
import operator

def RNG(maximum):
    return random.randint(0,maximum)

class Agent():
    def __init__(self):
        # Associated simulation area.
        self.__model = None

        # Destroyed agents are not drawn and are removed from their area.
        self.__destroyed = False

        # Number of edges in the regular polygon representing the agent.
        self.__resolution = 10

        # Color of the agent in RGB.
        self.__color = [RNG(255), RNG(255), RNG(255)]

        self.x = 0
        self.y = 0
        self.size = 1
        self.direction = RNG(359)
        self.speed = 1
        self.__current_tile = None
        self.selected = False

    # Update current tile
    def update_current_tile(self):
        new_tile = self.current_tile()
        if not self.__current_tile:
            self.__current_tile = self.current_tile()
            self.__current_tile.add_agent(self)
        elif not (self.__current_tile is new_tile):
            self.__current_tile.remove_agent(self)
            new_tile.add_agent(self)
            self.__current_tile = new_tile

    # To be called after each movement step
    def __post_move(self):
        self.__wraparound()
        self.update_current_tile()

    # Ensures that the agent stays inside the simulation area.
    def __wraparound(self):
        self.x = self.x % self.__model.width
        self.y = self.y % self.__model.height

    def align(self):
        w = self.__model.width
        h = self.__model.height
        tx = self.__model.x_tiles
        ty = self.__model.y_tiles
        self.x = math.floor(self.x * tx / w) * w / tx + (w/tx)/2
        self.y = math.floor(self.y * ty / h) * w / ty + (h/ty)/2

    def jump_to(self, x, y):
        self.x = x
        self.y = y
        self.__post_move()

    def set_model(self, model):
        self.__model = model

    def point_towards(self, other_x, other_y):
        dist = self.distance_to(other_x,other_y)
        if dist > 0:
            self.direction = math.degrees(math.acos((other_x - self.x) / dist))
            if (self.y - other_y) > 0:
                self.direction = 360 - self.direction

    def forward(self):
        self.x += math.cos(math.radians(self.direction)) * self.speed
        self.y += math.sin(math.radians(self.direction)) * self.speed
        self.__post_move()

    def distance_to(self, other_x, other_y):
        return ((self.x-other_x)**2 + (self.y-other_y)**2)**0.5

    # Returns a list of nearby agents.
    # May take a type as argument and only return agents of that type.
    def agents_nearby(self, distance, agent_type=None):
        nearby = set()
        for a in self.__model.agents:
            if self.distance_to(a.x,a.y) <= distance and not (a is self):
                if agent_type == None or type(a) is agent_type:
                    nearby.add(a)
        return nearby

    def current_tile(self):
        x = math.floor(self.__model.x_tiles * self.x / self.__model.width) % self.__model.x_tiles
        y = math.floor(self.__model.y_tiles * self.y / self.__model.height) % self.__model.y_tiles
        try:
            i = y*self.__model.x_tiles + x
            return self.__model.tiles[i]
        except:
            print(self.x, self.y, x, y)

    # Returns the surrounding tiles as a 3x3 grid. Includes the current tile.
    def neighbor_tiles(self):
        tileset = [[None for y in range(3)] for x in range(3)]
        (tx,ty) = self.model.get_tiles_xy()
        for y in range(3):
            for x in range(3):
                x = (floor(tx * self.x / self.__model.width)+x-1) % tx
                y = (floor(ty * self.y / self.__model.height)+y-1) % ty
                tileset[x][y] = self.__model.tiles[x][y]
        return tileset

    def is_destroyed(self):
        return self.__destroyed

    def destroy(self):
        if not self.__destroyed:
            self.__destroyed = True

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, color):
        r, g, b = color
        self.__color = [r, g, b]


class Tile():
    def __init__(self,x, y, model):
        self.x = x
        self.y = y
        self.info = {}
        self.color = (0, 0, 0)
        self.__agents = set()

    def add_agent(self,agent):
        self.__agents.add(agent)

    def remove_agent(self,agent):
        self.__agents.discard(agent)

    def get_agents(self):
        return self.__agents

        # Associated model.
        self.__model = model

class Spec():
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

class GraphSpec(Spec):
    def __init__(self, variable, color):
        self.variable = variable
        self.color = color

class HistogramSpec(Spec):
    def __init__(self, variables, colors):
        self.variables = variables
        self.colors = colors

class Model:
    def __init__(self, title, x_tiles, y_tiles, tile_size=8):
        # Title of model, shown in window title
        self.title = title

        # Number of tiles on the x/y axis.
        self.x_tiles = x_tiles
        self.y_tiles = y_tiles

        # Pixel sizes
        self.tile_size = tile_size
        self.width = x_tiles * tile_size
        self.height = y_tiles * tile_size

        # Internal set of agents.
        self.agents = set()

        # Initial tileset (empty).
        self.tiles = [Tile(x, y, self)
                      for y in range(y_tiles)
                      for x in range(x_tiles)]

        self.variables = {}
        self.plot_specs = []
        self.controller_rows = []
        self.add_controller_row()
        self.plots = set() # Filled in during initialization
        self.show_direction = False

    def add_agent(self, agent):
        agent.set_model(self)
        agent.x = RNG(self.width)
        agent.y = RNG(self.height)
        self.agents.add(agent)
        agent.setup(self)

    def add_agents(self, agents):
        for a in agents:
            self.add_agent(a)

    # Returns a list of all agents with random order
    def agents_random(self):
        agent_list = list(self.agents)
        random.shuffle(agent_list)
        return agent_list

    # Based on kite.com/python/answers/how-to-sort-a-list-of-objects-by-attribute-in-python
    def agents_ordered(self, variable, increasing=True):
        agent_list = list(self.agents)
        ret_list = sorted(agent_list, key=operator.attrgetter(variable))
        if not increasing:
            ret_list.reverse()
        return ret_list

    # Destroys all agents, clears the agent set, and resets all tiles.
    def reset(self):
        for a in self.agents:
            a.destroy()
        self.agents.clear()
        for x in range(self.x_tiles):
            for y in range(self.y_tiles):
                i = y*self.x_tiles + x
                self.tiles[i].color = (0,0,0)
                self.tiles[i].info = {}

    def update_plots(self):
        for plot in self.plots:
            if type(plot.spec) is GraphSpec:
                plot.add_data(self.variables[plot.spec.variable])
            elif type(plot.spec) is HistogramSpec:
                dataset = []
                for d in plot.spec.variables:
                    dataset.append(self.variables[d])
                plot.update_data(dataset)

    def remove_destroyed_agents(self):
        new_agents = set()
        for a in self.agents:
            if not a.is_destroyed():
                new_agents.add(a)
            else:
                a.current_tile().remove_agent(a)
        self.agents = new_agents

    def clear_plots(self):
        for plot in self.plots:
            plot.clear()


    def mouse_click(self,x,y):
        for a in self.agents:
            a.selected = False
            if (a.x-a.size/2 < x
                and a.x+a.size/2 > x
                and a.y-a.size/2 < y
                and a.y+a.size/2 > y):
                for b in self.agents:
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

    def graph(self, variable, color):
        self.plot_specs.append(GraphSpec(variable, color))

    def histogram(self, variables, colors):
        self.plot_specs.append(HistogramSpec(variables,colors))

    def __setitem__(self, key, item):
        self.variables[key] = item

    def __getitem__(self, key):
        return self.variables[key]

    def __delitem__(self, key):
        del self.variables[key]

class SimpleModel(Model):
    def __init__(self, title, x_tiles, y_tiles, setup_func, step_func, tile_size=8):
        super().__init__(title,x_tiles,y_tiles,tile_size)
        self.add_button("Setup",setup_func)
        self.add_toggle_button("Step",step_func)

