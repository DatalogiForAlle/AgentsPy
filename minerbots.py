#!/usr/bin/env python3
import random
import math
from agents import *

class Homebase(Agent):
    def setup(self, model):
        self.size = 20
        self.color = (200,200,200)
        self.x = model.width/2
        self.y = model.height/2

    def step(self,model):
        for a in self.agents_nearby(self.size/2+5):
            if type(a) == Minerbot and a.loaded:
                a.loaded = False
                a.color = (100,100,100)
                self.size += 1
                model["minerals_collected"] += 1

class Minerbot(Agent):
    def setup(self, model):
        self.size = 10
        self.color = (100, 100, 100)
        self.direction = RNG(360)
        self.loaded = False
        self.x = model.width/2
        self.y = model.height/2

    def step(self, model):
        self.speed = model["robot_speed"]
        if self.loaded:
            self.point_towards(model.width/2,model.height/2)
        else:
            self.direction += RNG(20)-10
        self.forward()
        t = self.current_tile()
        if t.info["has_mineral"] and not self.loaded:
            t.info["has_mineral"] = False
            t.color = (200,100,0)
            self.color = (100,100,255)
            self.loaded = True

class Alien(Agent):
    def setup(self, model):
        self.size = 15
        self.color = (0,255,0)
        self.direction = RNG(360)

    def destroy_robot(self):
        t = self.current_tile()
        for other in t.get_agents():
            if type(other) == Minerbot:
                other.destroy()

    def step(self, model):
        self.destroy_robot()
        self.forward()

miner_model = Model("MinerBots",100,100)

def setup(model):
    model.reset()
    model.clear_plots()
    for t in model.tiles:
        if RNG(50) == 50:
            t.color = (0,255,255)
            t.info["has_mineral"] = True
        else:
            t.color = (200,100,0)
            t.info["has_mineral"] = False
    bots = set([Minerbot() for _ in range(10)])
    model.add_agents(bots)
    model["Homebase"] = Homebase()
    model.add_agent(model["Homebase"])
    aliens = set([Alien() for _ in range(3)])
    model.add_agents(aliens)
    model["minerals_collected"] = 0
    model["robot_speed"] = 1

def step(model):
    for a in model.agents:
        a.step(model)
    model.update_plots()

def build_bot(model):
    if model["Homebase"].size > 30:
        model["Homebase"].size -= 10
        model.add_agent(Minerbot())

miner_model.add_button("Setup", setup)
miner_model.add_toggle_button("Go", step)
miner_model.graph("minerals_collected",(0,0,255))
miner_model.add_button("Build new bot", build_bot)
miner_model.add_slider("robot_speed", 1, 5, 2)
run(miner_model)

