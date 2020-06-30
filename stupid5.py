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
        self.grow_size += min(model["max_food_eat"],t.info["food"])
        t.info["food"] = max(0,t.info["food"]-model["max_food_eat"])
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

def setup(model):
    model.reset()
    people = set([Bug() for i in range(math.floor(model["initial_bugs"]))])
    model.add_agents(people)
    for t in model.tiles:
        t.info["food"] = 0.0
        t.color = (0,0,0)

def step(model):
    for a in model.agents:
        a.step(model)
        if a.grow_size > 100:
            model["stop"] = True
    for t in model.tiles:
        food_prod = random.random() * model["max_food_prod"]
        t.info["food"] += food_prod
        c = min(255,math.floor(t.info["food"]/10 * 255))
        t.color = (c,c,c)

stupid_model = Model("Dum-dum", 100,100)
stupid_model.add_button("setup", setup)
stupid_model.add_button("step", step)
stupid_model.add_toggle_button("go", step)
stupid_model.add_slider("initial_bugs",10,300,100)
stupid_model.add_slider("max_food_eat",0.1,1.0,1.0)
stupid_model.add_slider("max_food_prod",0.01,0.1,0.01)
run(stupid_model)
