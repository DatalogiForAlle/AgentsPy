from time import sleep
from random import randint
from agents import Agent, Model, run

modello = Model("Zepto", 100, 100)
modello.x = 42

"""
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
    print(model.x)
    for ag in model.agents:
        ag.forward()
        ag.direction += randint(-5,5)
    model.update_plots()

modello.add_button("Go", step, toggle=True)

modello.add_slider("x", 42, 0, 100)

modello.line_chart( ["x"], [(0, 200, 0)] )

run(modello)
