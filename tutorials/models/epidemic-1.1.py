from agents import *

epidemic_model = Model("Epidemimodel", 100, 100)

epidemic_model.add_agent(Agent())

run(epidemic_model)
