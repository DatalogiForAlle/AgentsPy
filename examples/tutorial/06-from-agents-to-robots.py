from random import randint
from agents import *

miner_model = Model("MinerBots", 100, 100)

class Robot(Agent):
    def setup(self, model):
        self.color = (100, 100, 100)
        self.direction = random.randint(0, 359)

    def step(self, model):
        self.direction += randint(0, 20) - 10
        self.forward()

def setup(model):
    model.reset()
    for x in range(10):
        model.add_agent(Robot())

def step(model):
    for ag in model.agents:
        ag.step(model)

miner_model.add_button("Setup", setup)

miner_model.add_toggle_button("Go", step)

run(miner_model)
