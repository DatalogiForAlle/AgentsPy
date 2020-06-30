import random
from agents import *

class Bug(Agent):
    def draw_color(self):
        gradient = max(0,255-255*self.grow_size/10)
        self.color = (255,gradient,gradient)

    def setup(self, model):
        self.size = 8
        self.grow_size = 0
        self.draw_color()
        self.align()

    def step(self, model):
        t = self.current_tile()
        new_x = (t.x + RNG(8) - 4) % model.x_tiles
        new_y = (t.y + RNG(8) - 4) % model.y_tiles
        new_t = model.tiles[new_y * model.x_tiles + new_x]
        while len(new_t.get_agents()) > 0:
            new_x = (t.x + RNG(8) - 4) % model.x_tiles
            new_y = (t.y + RNG(8) - 4) % model.y_tiles
            new_t = model.tiles[new_y * model.x_tiles + new_x]
        self.draw_color()
        self.jump_to(new_x*model.width/model.x_tiles,
                     new_y*model.height/model.y_tiles)
        self.grow_size += 1

def setup(model):
    model.reset()
    model["initial_bugs"] = 100
    people = set([Bug() for i in range(math.floor(model["initial_bugs"]))])
    model.add_agents(people)

def step(model):
    for a in model.agents:
        a.step(model)

stupid_model = Model("Dum-dum", 100,100)
stupid_model.add_button("setup", setup)
stupid_model.add_button("step", step)
stupid_model.add_toggle_button("go", step)
run(stupid_model)
