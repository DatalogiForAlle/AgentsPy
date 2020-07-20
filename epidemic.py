#!/usr/bin/env python3
import random
import math
from agents import *

class Person(Agent):
    def infect(self, model):
        self.infection = 1000
        model["infected"] += 1
        model["normal"] -= 1
        self.color = (200,200,0)

    def immunize(self, model):
        self.infection = 0
        model["infected"] -= 1
        model["immune"] += 1
        self.immune = True

    def setup(self, model):
        self.color = (50,150,50)
        self.immune = False
        self.size = 10
        self.infection = 0
        model["normal"] += 1
        if (RNG(100) < 5):
            self.infect(model)

    def step(self, model):
        self.direction += RNG(20)-10
        self.speed = model["movespeed"]
        nearby = self.agents_nearby(30)
        nearby = self.agents_nearby(60)
        nearby_infected = 0
        new_dir = 0
        for other in nearby:
            if other.infection > 0:
                nearby_infected += 1
                self.point_towards(other.x,other.y)
                new_dir += self.direction
        if nearby_infected > 0:
            new_dir /= nearby_infected
            self.direction = new_dir + 180
        self.forward()

        if self.infection > 1:
            t = self.current_tile()
            t.info["infection"] = model["decay"] * 60
            for b in self.agents_nearby(15):
                if (not b.immune) and (b.infection == 0):
                    b.infect(model)
            self.infection -= 1
        elif self.infection == 1:
            self.immunize(model)
        elif not self.immune:
            if self.current_tile().info["infection"] > 0:
                self.infect(model)

        if self.infection > 0:
            self.color = (200,200,0)
        elif self.immune:
            self.color = (0,0,250)
        else:
            self.color = (50,150,50)

def setup(model):
    model.reset()
    model["movespeed"] = 0.2
    model["normal"] = 0
    model["infected"] = 0
    model["immune"] = 0
    model["decay"] = 2
    people = set([Person() for i in range(100)])
    model.add_agents(people)
    for t in model.tiles:
        t.color = (0,50,0)
        t.info["infection"] = 0
    model.clear_plots()

def step(model):
    for a in model.agents:
        a.step(model)
    for t in model.tiles:
        if t.info["infection"] > 0:
            t.color = (100,100,0)
            t.info["infection"] -= 1
        else:
            t.color = (0,50,0)
    model.update_plots()

def direction(model):
    for a in model.agents:
        a.show_direction = not a.show_direction

epidemic_model = SimpleModel("Epidemic",100,100,setup,step)
epidemic_model.add_toggle_button("Go", step)
epidemic_model.add_slider("movespeed", 0.1, 1, .1)
epidemic_model.add_slider("decay", 0, 3, 2)
epidemic_model.graph("immune", (100, 100, 255))
epidemic_model.graph("infected", (255, 255, 0))
epidemic_model.histogram(["normal","infected","immune"], (255, 255, 0))
epidemic_model.monitor("immune")
run(epidemic_model)

