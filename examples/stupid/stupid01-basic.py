import random
import math
from agents import Agent, Model, run


class Bug(Agent):
    def setup(self, model):
        self.size = 8
        self.color = (255, 0, 0)
        self.align()
        self.update_current_tile()

    def step(self, model):
        # Find all nearby valid tiles
        nearby_tiles = self.nearby_tiles(-4, -4, 4, 4)
        random.shuffle(nearby_tiles)

        def is_valid_tile(t):
            return len(t.get_agents()) == 0
        nearby_tiles = list(filter(is_valid_tile, nearby_tiles))

        # If there is a valid tile, pick the "first" one and jump to it
        if len(nearby_tiles) > 0:
            # Just use the first one in the list, it is shuffled anyways
            new_t = nearby_tiles[0]
            self.jump_to(new_t.x*model.width/model.x_tiles,
                         new_t.y*model.height/model.y_tiles)
            self.align()


def setup(model):
    model.reset()
    model["initial_bugs"] = 100
    people = set([Bug() for i in range(math.floor(model["initial_bugs"]))])
    model.add_agents(people)


def step(model):
    for a in model.agents:
        a.step(model)


stupid_model = Model("Basic StupidModel (stupid01)",
                     100, 100, tile_size=5)
stupid_model.add_button("setup", setup)
stupid_model.add_button("step", step)
stupid_model.add_toggle_button("go", step)
run(stupid_model)
