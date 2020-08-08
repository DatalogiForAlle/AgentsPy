from agents import *
from random import randint


class Homebase(Agent):

    def setup(self, model):
        self.size = 20
        self.color = (200, 200, 200)
        self.x = model.width/2
        self.y = model.height/2

    def step(self,model):
       for a in self.agents_nearby(self.size/2+5):
           if type(a) == Minerbot and a.loaded:
               a.loaded = False
               a.color = (100, 100, 100)
               self.size += 1
               model["minerals_collected"] += 1


class Minerbot(Agent):

    def setup(self, model):
        self.size = 10
        self.color = (100, 100, 100)
        self.direction = randint(0, 359)
        self.loaded = False
        self.x = model.width/2
        self.y = model.height/2

    def step(self, model):
        if self.loaded:
            self.point_towards(model.width/2, model.height/2)
        else:
            self.direction += randint(0, 20)-10
        self.forward()
        t = self.current_tile()
        if t.info["has_mineral"] and not self.loaded:
            t.info["has_mineral"] = False
            t.color = (200, 100, 0)
            self.color = (100, 100, 255)
            self.loaded = True


def setup(model):
    model.reset()
    for t in model.tiles:
        if randint(0, 50) == 50:
            t.color = (0, 255, 255)
            t.info["has_mineral"] = True
        else:
            t.color = (200, 100, 0)
            t.info["has_mineral"] = False
    bots = set([Minerbot() for _ in range(10)])
    miner_model.add_agents(bots)
    model.add_agent(Homebase())
    model.clear_plots()
    model["minerals_collected"] = 0


def step(model):
    for a in model.agents:
        a.step(model)
    model.update_plots()


miner_model = Model("MinerBots", 100, 100)

miner_model.add_button("Setup", setup)
miner_model.add_toggle_button("Go", step)
miner_model.line_chart("minerals_collected",(0,255,255))

run(miner_model)
