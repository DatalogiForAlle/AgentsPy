from agents import *

miner_model = Model("MinerBots", 100, 100)

def setup(model):
    model.reset()
    model.add_agent(Agent())

def step(model):
    for ag in model.agents:
        ag.forward()

miner_model.add_button("Setup", setup)

miner_model.add_toggle_button("Go", step)

run(miner_model)
