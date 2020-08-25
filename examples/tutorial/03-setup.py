from agents import *

miner_model = Model("MinerBots", 100, 100)

def setup(model):
    model.reset()
    model.add_agent(Agent())

miner_model.add_button("Setup", setup)

run(miner_model)
