import random
import math
from agents import Agent, Model, run


class Bug(Agent):
    def size_to_color(self):
        gradient = max(0, 255-255*self.grow_size/10)
        self.color = (255, gradient, gradient)

    def setup(self, model):
        self.size = 8
        self.grow_size = 1
        self.size_to_color()
        self.align()

    def move(self):
        """
        Jump to a random tile in the neighborhood of the agent, which is
        not occupied by other agents
        """
        # Find all nearby tiles within distance of 4 tiles
        nearby_tiles = self.nearby_tiles(-4, -4, 4, 4)
        random.shuffle(nearby_tiles)

        # Find first unoccipied tile
        new_tile = None
        for tile in nearby_tiles:
            if len(tile.get_agents()) == 0:
                new_tile = tile

        # Jump there
        if new_tile is not None:
            self.jump_to_tile(new_tile)

        # Does nothing, if all tiles are occupied

    def eat(self, model):
        # Eat from the current tile
        tile = self.current_tile()
        self.grow_size += min(model["max_food_eat"], tile.info["food"])
        tile.info["food"] = max(0, tile.info["food"]-model["max_food_eat"])
        self.size_to_color()

    def step(self, model):
        self.eat(model)
        self.move()
        if self.grow_size > 100:
            model.pause()


def setup(model):
    # Open data file for writing
    global f
    f = open("stupid.data", "w")

    model.reset()

    # Add agents
    for i in range(int(model["initial_bugs"])):
        model.add_agent(Bug())

    # Initialize tiles
    for tile in model.tiles:
        tile.info["food"] = 0.0
        tile.color = (0, 0, 0)


def step(model):
    global f

    # Food production
    for tile in model.tiles:
        food_prod = random.uniform(0, model["max_food_prod"])
        tile.info["food"] += food_prod
        c = min(255, math.floor(tile.info["food"] * 255))
        tile.color = (c, c, c)

    # Move all agents
    for agent in model.agents_random():
        agent.step(model)

    # Calculate min, average and max bug size
    bug_min = 100
    bug_sum = 0
    bug_max = 0
    for agent in model.agents:
        bug_min = min(bug_min, agent.grow_size)
        bug_max = max(bug_max, agent.grow_size)
        bug_sum += agent.grow_size
    bug_mean = bug_sum / len(model.agents)

    # Write min, average and max bug size to file
    f.write(str(bug_min) + " " + str(bug_mean) + " " + str(bug_max) + "\n")

    # Update plots
    model.update_plots()

def close(model):
    global f
    f.close()

stupid_model = Model("StupidModel w. file output (stupid08)",
                     100, 100, tile_size=5)
stupid_model.add_button("setup", setup)
stupid_model.add_button("step", step)
stupid_model.add_toggle_button("go", step)
stupid_model.add_controller_row()
stupid_model.add_slider("initial_bugs", 10, 300, 100)
stupid_model.add_controller_row()
stupid_model.add_slider("max_food_eat", 0.1, 1.0, 1.0)
stupid_model.add_controller_row()
stupid_model.add_slider("max_food_prod", 0.01, 0.1, 0.01)
stupid_model.histogram("grow_size", 0, 10, 5, (0, 0, 0))
stupid_model.on_close(close)
run(stupid_model)
