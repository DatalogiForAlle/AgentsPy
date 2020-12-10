from agents import Model, Agent, run
from random import randint


class Person(Agent):
    def setup(self, model):
        self.category = 0

    def step(self, model):
        self.direction += randint(-10, 10)
        self.forward()


def model_setup(model):
    model.reset()
    for person in range(100):
        model.add_agent(Person())


def model_step(model):
    for person in model.agents:
        person.step(model)


epidemic_model = Model("Epidemimodel", 100, 100)

epidemic_model.add_button("Setup", model_setup)

epidemic_model.add_toggle_button("Go", model_step)

if __name__ == "__main__":
    run(epidemic_model)
