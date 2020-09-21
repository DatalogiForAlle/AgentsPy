from agents import *
from random import randint

def setup(model):
    model.reset()
    for agent in range(100):
        model.add_agent(Agent())

def step(model):
    for agent in model.agents:
        agent.direction += randint(-10,10)
        agent.forward()

epidemic_model = Model("Epidemimodel", 100, 100)

epidemic_model.add_button("Setup", setup)

epidemic_model.add_toggle_button("Go", step)

run(epidemic_model)
