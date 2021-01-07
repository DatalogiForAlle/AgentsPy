from time import sleep
from random import randint
from agents import Agent, Model, run

modello = Model("Zepto", 100, 100)

"""
epidemic_model.add_slider("decay", 2, 0, 3)
epidemic_model.monitor("immune")

epidemic_model.line_chart(
    ["normal", "infected", "immune"],
    [(0, 200, 0), (200, 200, 0), (100, 100, 255)],
)
epidemic_model.bar_chart(["normal", "infected", "immune"], (100, 200, 100))
epidemic_model.agent_line_chart("infection", 0, 1000)
epidemic_model.on_close(print_infections)
"""

for i in range(100):
    modello.add_agent(Agent())

def step(model):
    for ag in model.agents:
        ag.forward()
        ag.direction += randint(-5,5)

modello.add_button("Go", step, toggle=True)

run(modello)
