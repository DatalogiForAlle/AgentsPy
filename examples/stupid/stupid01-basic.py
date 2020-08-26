import random
from agents import Agent, Model, run


class Bug(Agent):
    def setup(self, model):
        self.size = 8
        self.color = (255, 0, 0)

        # Align to center of tile
        self.center_in_tile()

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

    def step(self, model):
        self.move()


def setup(model):
    model.reset()
    model["initial_bugs"] = 100

    # Create and add agents
    for i in range(int(model["initial_bugs"])):
        model.add_agent(Bug())


def step(model):
    # Move all agents
    for agent in model.agents:
        agent.step(model)


stupid_model = Model("Basic StupidModel (stupid01)",
                     100, 100, tile_size=5)
stupid_model.add_button("setup", setup)
stupid_model.add_button("step", step)
stupid_model.add_toggle_button("go", step)
run(stupid_model)
