import random
import math
from agents import Agent, Model, run, AgentShape

file_handle = None


class Bug(Agent):
    def size_to_color(self):
        gradient = max(0, 255-255*self.grow_size/10)
        self.color = (255, gradient, gradient)

    def setup(self, model):
        self.shape = AgentShape.CIRCLE
        self.size = 8
        self.grow_size = 1
        self.survivalProbability = 95
        self.size_to_color()
        self.center_in_tile()

    def move(self):
        """
        Jump to a random tile in the neighborhood of the agent, which is
        not occupied by other agents
        """
        # Find all nearby tiles within distance of 4 tiles
        nearby_tiles = self.nearby_tiles(-4, -4, 4, 4)
        random.shuffle(nearby_tiles)

        # Find all unoccipied tiles
        unoccupied_tiles = []
        for tile in nearby_tiles:
            if len(tile.get_agents()) == 0:
                unoccupied_tiles.append(tile)

        # Do nothing if all tiles are occupied
        if len(unoccupied_tiles) == 0:
            return
        else:
            # Remove last element, use as current best
            best = unoccupied_tiles.pop()

            # Find the best tile
            for tile in unoccupied_tiles:
                if best.info["food"] < tile.info["food"]:
                    best = tile

            # Jump to best
            self.jump_to_tile(best)

    def eat(self, model):
        # Eat from the current tile
        tile = self.current_tile()
        self.grow_size += min(model.max_food_eat, tile.info["food"])
        tile.info["food"] = max(0, tile.info["food"]-model.max_food_eat)
        self.size_to_color()

    def reproduce(self, model):
        # Split into new bugs
        if self.grow_size > 10:
            tile = self.current_tile()

            # Reproduce to 5 new bugs
            for i in range(5):
                # Try 5 times
                for j in range(5):
                    newbug_x = 3-random.randint(0, 6)
                    newbug_y = 3-random.randint(0, 6)

                    tile = model.tile(tile.x+newbug_x, tile.y+newbug_y)
                    if len(tile.get_agents()) == 0:
                        newbug = Bug()
                        model.add_agent(newbug)
                        newbug.jump_to_tile(tile)
                        break
            self.destroy()

    def step(self, model):
        self.eat(model)
        self.move()
        if self.survivalProbability < random.randint(0, 100):
            self.destroy()
        else:
            self.reproduce(model)


def setup(model):
    # Open data file for writing
    global file_handle
    file_handle = open("stupid.data", "w")

    model.reset()

    # Add agents
    for i in range(int(model.initial_bugs)):
        model.add_agent(Bug())

    # Initialize tiles
    for tile in model.tiles:
        tile.info["food"] = 0.0
        tile.color = (0, 0, 0)


def step(model):
    # Food production
    for tile in model.tiles:
        food_prod = random.uniform(0, model.max_food_prod)
        tile.info["food"] += food_prod
        c = min(255, math.floor(tile.info["food"] * 255))
        tile.color = (c, c, c)

    # Move all agents
    for agent in model.agents_ordered("grow_size"):
        agent.step(model)

    # Calculate min, average and max bug size
    bug_min = 100
    bug_sum = 0
    bug_max = 0
    for agent in model.agents:
        bug_min = min(bug_min, agent.grow_size)
        bug_max = max(bug_max, agent.grow_size)
        bug_sum += agent.grow_size
    bug_mean = bug_sum / model.agent_count()

    # Write min, average and max bug size to file
    file_handle.write(str(bug_min) + " " + str(bug_mean) + " " + str(bug_max) + "\n")

    # Update plots
    model.update_plots()
    model.remove_destroyed_agents()

    # TODO: Stop after 1000 iterations
    if model.agent_count() == 0:
        model.pause()


def close(model):
    if file_handle:
        file_handle.close()


stupid_model = Model("StupidModel w. mortality and reproduction (stupid12)",
                     100, 100, tile_size=5)
stupid_model.add_button("setup", setup)
stupid_model.add_button("step", step)
stupid_model.add_toggle_button("go", step)
stupid_model.add_controller_row()
stupid_model.add_slider("initial_bugs", 100, 10, 300)
stupid_model.add_controller_row()
stupid_model.add_slider("max_food_eat", 1.0, 0.1, 1.0)
stupid_model.add_controller_row()
stupid_model.add_slider("max_food_prod", 0.01, 0.01, 0.1)
stupid_model.histogram("grow_size", 0, 10, 5, (0, 0, 0))
stupid_model.on_close(close)
run(stupid_model)
