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
                model["minerals_collected"] += 1

class Alien(Agent):
    def setup(self, model):
        self.size = 15
        self.direction = randint(0,359)
        self.color = (0,255,0)

    def destroy_robots(self):
        for t in self.neighbor_tiles():
            for other in t.get_agents():
                if type(other) == Robot:
                    other.destroy()

    def step(self, model):
        self.speed = 1.5 * model["speed_factor"]
        self.direction += randint(0, 20) - 10
        self.forward()
        self.destroy_robots()

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
    model["Homebase"] = Homebase()
    model.add_agent(model["Homebase"])
    model.clear_plots()
    model["minerals_collected"] = 0
    for x in range(3):
        miner_model.add_agent(Alien())

def step(model):
    for ag in model.agents:
        ag.step(model)
    model.update_plots()

def build_bot(model):
    if model["Homebase"].size > 22:
        model["Homebase"].size -= 2
        model["minerals_collected"] -= 2
        model.add_agent(Robot())

miner_model.add_button("Setup", setup)

miner_model.add_toggle_button("Go", step)

miner_model.add_button("Build new bot", build_bot)

miner_model.add_slider("speed_factor", 1, 5, 1)

miner_model.line_chart("minerals_collected",(0,200,200))

run(miner_model)
