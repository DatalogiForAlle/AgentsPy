from agents import *
from random import randint

class Person(Agent):
    def setup(self,model):
        self.category = 0

    def step(self,model):
        self.direction += randint(-10,10)
        self.forward()

def setup(model):
    model.reset()
    for person in range(100):
        model.add_agent(Person())

def step(model):
    for person in model.agents:
        person.step()

epidemic_model = Model("Epidemimodel", 100, 100)

epidemic_model.add_button("Setup", setup)

epidemic_model.add_toggle_button("Go", step)

run(epidemic_model)
