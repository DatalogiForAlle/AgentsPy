from agents import Model, Agent, run
from random import randint


def model_setup(model):
    model.reset()
    for agent in range(100):
        model.add_agent(Agent())


def model_step(model):
    for agent in model.agents:
        agent.direction += randint(-10, 10)
        agent.forward()


epidemic_model = Model("Epidemimodel", 100, 100)

epidemic_model.add_button("Setup", model_setup)

epidemic_model.add_toggle_button("Go", model_step)

if __name__ == "__main__":
    run(epidemic_model)
