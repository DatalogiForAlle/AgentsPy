from agents import Model, Agent, run
from random import randint


class Person(Agent):
    def setup(self, model):
        self.category = 0
        self.color = (0, 200, 0)
        if randint(1, 50) == 1:
            self.infect(model)

    def step(self, model):
        self.direction += randint(-10, 10)
        self.forward()

    def infect(self, model):
        self.color = (200, 0, 0)
        self.category = 1


def model_setup(model):
    model.reset()
    for person in range(100):
        model.add_agent(Person())


def model_step(model):
    for person in model.agents:
        person.step(model)


epidemic_model = Model("Epidemimodel", 100, 100)

epidemic_model.add_button("Setup", model_setup)

epidemic_model.add_button("Go", model_step, toggle=True)

run(epidemic_model)
