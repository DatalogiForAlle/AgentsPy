from random import randint
from agents import *

miner_model = Model("MinerBots", 100, 100)

class Robot(Agent):
    def setup(self, model):
        self.color = (100, 100, 100)
        self.direction = random.randint(0, 359)
        self.loaded = False
        self.x = model.width/2
        self.y = model.height/2

    def step(self, model):
        if self.loaded:
            self.point_towards(model.width/2, model.height/2)
        else:
            self.direction += randint(0, 20)-10
        self.forward()
        self.speed = model["speed_factor"]
        t = self.current_tile()
        if t.info["has_mineral"] and not self.loaded:
            t.info["has_mineral"] = False
            t.color = (200, 100, 0)
            self.color = (100, 100, 255)
            self.loaded = True

class Homebase(Agent):
    def setup(self, model):
        self.size = 20
        self.shape = AgentShape.HOUSE
        self.color = (200, 200, 200)
        self.x = model.width/2
        self.y = model.height/2

    def step(self, model):
        for a in self.agents_nearby(self.size/2+5):
            if type(a) == Robot and a.loaded:
                a.loaded = False
                a.color = (100, 100, 100)
                self.size += 1

def setup(model):
    model.reset()
    for x in range(10):
        model.add_agent(Robot())
    model["speed_factor"] = 1
    for t in model.tiles:
        if randint(0, 50) == 50:
            t.color = (0, 255, 255)
            t.info["has_mineral"] = True
        else:
            t.color = (200, 100, 0)
            t.info["has_mineral"] = False
    model.add_agent(Homebase())

def step(model):
    for ag in model.agents:
        ag.step(model)

miner_model.add_button("Setup", setup)

miner_model.add_toggle_button("Go", step)

miner_model.add_slider("speed_factor", 1, 5, 1)

run(miner_model)
