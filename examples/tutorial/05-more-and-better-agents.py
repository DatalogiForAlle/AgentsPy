from random import randint
from agents import Model, Agent, run

miner_model = Model("MinerBots", 100, 100)


def setup(model):
    model.reset()
    for x in range(10):
        model.add_agent(Agent())


def step(model):
    for ag in model.agents:
        ag.forward()
        ag.direction += randint(0, 20) - 10


miner_model.add_button("Setup", setup)

miner_model.add_toggle_button("Go", step)

run(miner_model)
