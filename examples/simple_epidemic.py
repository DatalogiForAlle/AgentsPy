#!/usr/bin/env python3
import random
from agents import Agent, SimpleModel, run


class Person(Agent):

    # Inficer agenten
    def infect(self, model):
        self.infection = 1000
        self.color = (200, 200, 0)

    # Gør agenten immun
    def immunize(self, model):
        self.infection = 0
        self.immune = True
        self.color = (0, 0, 250)

    def setup(self, model):
        self.color = (50, 150, 50)
        self.immune = False
        self.size = 10
        self.infection = 0
        if random.randint(0, 100) < 5:
            self.infect(model)

    def step(self, model):
        self.direction += random.randint(0, 20) - 10
        self.speed = model.movespeed
        self.forward()

        if self.infection > 1:
            for b in self.agents_nearby(15):
                if (not b.immune) and (b.infection == 0):
                    b.infect(model)
            self.infection -= 1
        elif self.infection == 1:
            self.immunize(model)


def setup(model):
    model.reset()
    model.movespeed = 0.5
    people = set([Person() for i in range(100)])
    model.add_agents(people)
    for t in model.tiles:
        t.color = (0, 50, 0)
    model.clear_plots()


def step(model):
    for a in model.agents:
        a.step(model)


epidemic_model = SimpleModel("Epidemic", 100, 100, setup, step)
run(epidemic_model)
