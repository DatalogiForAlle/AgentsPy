from agents import *

def setup():
    size(50, 50)
    title("My model")
    add_agent(Agent())

def step():
    a = agents()[0]
    a.forward()

run(setup, step) # this always sets up Setup, Step, Go buttons
