import random
import numpy as np
from agents import *

class Bug(Agent):
    def draw_color(self):
        gradient = max(0,255-255*self.grow_size/10)
        self.color = (255,gradient,gradient)

    def setup(self, model):
        self.size = 8
        self.grow_size = max(0,np.random.normal(0.1,0.03))
        self.state = "B0"
        self.survivalprobability = 95
        model["current_bugs"] += 1
        self.draw_color()
        self.align()

    def step(self, model):
        t = self.current_tile()
        self.grow_size += min(model["max_food_eat"],t.info["food"])
        t.info["food"] = max(0,t.info["food"]-model["max_food_eat"])
        if self.grow_size < 2.5:
            self.state = "B0"
        elif self.grow_size < 5:
            self.state = "B1"
        elif self.grow_size < 7.5:
            self.state = "B2"
        elif self.grow_size < 10:
            self.state = "B3"
        else:
            for _ in range(5):
                for _ in range(5):
                    newbug_x = 3-RNG(6)
                    newbug_y = 3-RNG(6)
                    newbug_t = model.tiles[((t.y+newbug_y) % model.y_tiles) * model.x_tiles
                                           + (t.x+newbug_x) % model.x_tiles]
                    if len(newbug_t.get_agents()) == 0:
                        newbug = Bug()
                        model.add_agent(newbug)
                        newbug.x = newbug_t.x * model.width / model.x_tiles
                        newbug.y = newbug_t.y * model.height / model.y_tiles
                        newbug.grow_size = 0
                        newbug.align()
                        break
            model["current_bugs"] -= 1
            self.destroy()
            return
        if self.grow_size > 100:
            model["stop"] = True
        new_x = -4
        new_y = -4
        best_t = None
        for y in range(-4,5):
            for x in range(-4,5):
                new_t = model.tiles[((t.y+y) % model.y_tiles) * model.x_tiles
                                    + (t.x+x) % model.x_tiles]
                if (not best_t
                    or (best_t.info["food"] < new_t.info["food"])):
                    if (len(new_t.get_agents()) == 0 or (x == 0 and y == 0)):
                        new_x = x
                        new_y = y
                        best_t = new_t
        self.draw_color()
        self.jump_to((best_t.x)*model.width/model.x_tiles,
                     (best_t.y)*model.height/model.y_tiles)
        self.align()
        if self.survivalprobability < RNG(100):
            model["current_bugs"] -= 1
            self.destroy()

class Predator(Agent):
    def setup(self, model):
        self.size = 8
        self.color = (0,0,255)
        self.align()
        self.update_current_tile()

    def step(self, model):
        t = self.current_tile()
        for y in range(-1,2):
            for x in range(-1,2):
                new_t = model.tiles[((t.y+y) % model.y_tiles) * model.x_tiles
                                    + (t.x+x) % model.x_tiles]
                if len(new_t.get_agents()) == 1:
                    ag = new_t.get_agents().pop()
                    if type(ag) == Bug:
                        new_t.get_agents().add(ag)
                        self.jump_to((new_t.x)*model.width/model.x_tiles,
                                     (new_t.y)*model.height/model.y_tiles)
                        self.align()
                        ag.destroy()
        rand_x = -1 + RNG(3)
        rand_y = -1 + RNG(3)
        new_t = model.tiles[((t.y+rand_y) % model.y_tiles) * model.x_tiles
                            + (t.x+rand_x) % model.x_tiles]
        self.jump_to((new_t.x)*model.width/model.x_tiles,
                                     (new_t.y)*model.height/model.y_tiles)
        self.align()

def setup(model):
    global f
    f = open("stupid.data", "w")
    model.reset()
    bugs = set([Bug() for i in range(math.floor(model["initial_bugs"]))])
    predators = set([Predator() for i in range(50)])
    model["current_bugs"] = model["initial_bugs"]
    model["B0"] = len(bugs)
    model["B1"] = 0
    model["B2"] = 0
    model["B3"] = 0
    model["B4"] = 0
    model["stop"] = False
    model.add_agents(bugs)
    model.add_agents(predators)
    cell_data = open("stupid.cell","r")
    for l in cell_data:
        cell = l.split()
        x = int(cell[0])
        y = int(cell[1])
        prod_rate = float(cell[2])
        t = model.tiles[y*model.x_tiles+x]
        t.info["prod"] = prod_rate
        t.info["food"] = 0.0
        t.color = (0,0,0)

def step(model):
    global f
    if not model["stop"]:
        model["B0"] = 0
        model["B1"] = 0
        model["B2"] = 0
        model["B3"] = 0
        model["B4"] = 0
        bug_min = None
        bug_mean = 0
        bug_max = None
        for a in model.agents_ordered("grow_size"):
            if type(a) == Bug:
                a.step(model)
                model[a.state] += 1
                if not bug_min or bug_min > a.grow_size:
                    bug_min = a.grow_size
                if not bug_max or bug_max < a.grow_size:
                    bug_max = a.grow_size
                bug_mean += a.grow_size
        for a in model.agents:
            if type(a) == Predator:
                a.step(model)
        bug_mean /= model["initial_bugs"]
        f.write(str(bug_min) + " " + str(bug_mean) + " " + str(bug_max) + "\n")

        for t in model.tiles:
            t.info["food"] += t.info["prod"]
            c = min(255,math.floor(t.info["food"] * 255))
            t.color = (c,c,c)
        model.update_plots()
        model.remove_destroyed_agents()

stupid_model = Model("Dum-dum", 250,112)
stupid_model.add_button("setup", setup)
stupid_model.add_button("step", step)
stupid_model.add_toggle_button("go", step)
stupid_model.add_slider("initial_bugs",10,300,100)
stupid_model.add_slider("max_food_eat",0.1,1.0,1.0)
stupid_model.add_slider("max_food_prod",0.01,0.1,0.01)
stupid_model.histogram(["B0","B1","B2","B3","B4"],[(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0)])
stupid_model.graph("current_bugs",(0,0,0))
run(stupid_model)
