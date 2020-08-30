import random
import math
from agents import Agent, Model, run, AgentShape

file_handle = None


def find_tile_with_bug(tiles):
    for tile in tiles:
        agents = tile.get_agents()
        for agent in agents:
            if type(agent) == Bug:
                return tile
    return None


class Bug(Agent):
    def size_to_color(self):
        gradient = max(0, 255-255*self.grow_size/10)
        self.color = (255, gradient, gradient)

    def setup(self, model):
        self.size = 8
        self.grow_size = max(0, random.gauss(model["initialBugSizeMean"],
                                             model["initialBugSizeSD"]))
        self.survivalProbability = 95
        self.size_to_color()
        self.center_in_tile()
        model["current_bugs"] += 1

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
            # TODO: bugs can now move to a tile with a predator
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
        self.grow_size += min(model["max_food_eat"], tile.info["food"])
        tile.info["food"] = max(0, tile.info["food"]-model["max_food_eat"])
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

                    # TODO: the indexing here could perhaps be made simpler
                    tile = model.tiles[((tile.y+newbug_y) % model.y_tiles)
                                       * model.x_tiles
                                       + (tile.x+newbug_x) % model.x_tiles]
                    # TODO: we should still add the bug if the tile
                    # contains a predator, as a cell can contain both
                    if len(tile.get_agents()) == 0:
                        newbug = Bug()
                        newbug.grow_size = 0.0
                        model.add_agent(newbug)
                        newbug.jump_to_tile(tile)
                        break
            self.destroy()
            model["current_bugs"] -= 1

    def step(self, model):
        self.eat(model)
        self.move()
        if self.survivalProbability < random.randint(0, 100):
            self.destroy()
            model["current_bugs"] -= 1
        else:
            self.reproduce(model)


class Predator(Agent):
    def setup(self, model):
        self.size = 8
        self.color = (0, 0, 255)
        self.center_in_tile()
        self.shape = AgentShape.CIRCLE

    def hunt(self, model):
        # Shuffle neighbouring tiles
        nearby_tiles = self.neighbor_tiles()
        random.shuffle(nearby_tiles)

        # Find the first tile with a bug
        new_tile = find_tile_with_bug(nearby_tiles)

        # If no tile has bugs, jump to random cell
        if new_tile is None:
            current_tile = self.current_tile()
            rand_x = current_tile.x + random.randrange(-1, 2)
            rand_y = current_tile.y + random.randrange(-1, 2)
            random_tile = model.tiles[(rand_y % model.y_tiles) * model.x_tiles
                                      + rand_x % model.x_tiles]
            self.jump_to_tile(random_tile)
        else:
            # Kill the bug
            has_predator = False
            for agent in new_tile.get_agents():
                if type(agent) == Bug:
                    agent.destroy()
                elif type(agent) == Predator:
                    has_predator = True

            # If no predator, jump to tile
            if not has_predator:
                self.jump_to_tile(new_tile)

    def step(self, model):
        self.hunt(model)


def setup(model):
    # Open data file for writing
    global file_handle
    file_handle = open("stupid.data", "w")

    model.reset()
    model.reload()
    model["current_bugs"] = model["initial_bugs"]

    # Add agents
    for i in range(int(model["initial_bugs"])):
        model.add_agent(Bug())
        # TODO: only add agent if tile is empty?
    for i in range(200):
        model.add_agent(Predator())

    # Initialize tiles
    for tile in model.tiles:
        tile.info["food"] = 0.0
        tile.color = (0, 0, 0)


def step(model):
    # Food production
    for tile in model.tiles:
        tile.info["food"] += tile.info["prod"]
        c = min(255, math.floor(tile.info["food"] * 255))
        tile.color = (c, c, c)

    # Move all agents
    for agent in model.agents_ordered("grow_size"):
        if type(agent) == Bug:
            agent.step(model)

    for agent in model.agents:
        if type(agent) == Predator:
            agent.step(model)

    # Calculate min, average and max bug size
    bug_min = 100
    bug_sum = 0
    bug_max = 0
    for agent in model.agents:
        if type(agent) == Bug:
            bug_min = min(bug_min, agent.grow_size)
            bug_max = max(bug_max, agent.grow_size)
            bug_sum += agent.grow_size
    bug_mean = bug_sum / len(model.agents)

    # Write min, average and max bug size to file
    file_handle.write("{} {} {}\n".format(bug_min, bug_mean, bug_max))

    # Update plots
    model.update_plots()
    model.remove_destroyed_agents()

    # TODO: Stop after 1000 iterations
    if len(model.agents) == 0:
        model.pause()


def close(model):
    if file_handle:
        file_handle.close()


stupid_model = Model("StupidModel w. multiple agent types (stupid16)",
                     100, 100, tile_size=3,
                     cell_data_file="stupid.cell")
stupid_model.add_button("setup", setup)
stupid_model.add_button("step", step)
stupid_model.add_toggle_button("go", step)
stupid_model.add_controller_row()
stupid_model.add_slider("initial_bugs", 10, 300, 100)
stupid_model.add_controller_row()
stupid_model.add_slider("max_food_eat", 0.1, 1.0, 1.0)
stupid_model.add_controller_row()
stupid_model.add_slider("initialBugSizeMean", 0, 10, 1)
stupid_model.add_slider("initialBugSizeSD", 0, 10, 5)
stupid_model.histogram("grow_size", 0, 10, 5, (0, 0, 0))
stupid_model.line_chart("current_bugs", (0, 0, 0))
stupid_model.on_close(close)
run(stupid_model)
