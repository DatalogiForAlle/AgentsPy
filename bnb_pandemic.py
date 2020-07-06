#!/usr/bin/env python3
import random
import math
from agents import *

"""
  Forklaring af model:
  Modellen viser et sæt agenter der foretager handel med hinanden med resourcerne brød og smør.
  Grafen til højre viser summen af agenternes nyttefunktioner (som er brød^0.5 * smør^0.5).
  Agenterne farves blå, jo mere brød de har, og gule, jo mere smør de har. Hvide/grå agenter har
  god balance i deres to resourcer.
  Agenternes størrelse er en funktion af deres nyttefunktion.
"""

class Person(Agent):
    def update_visual(self):
        self.size = self.utility()*5

    def utility(self):
        return (self.bread**0.5) * (self.butter**0.5)

    def setup(self, model):
        self.bread = RNG(9)+1.0
        self.butter = RNG(9)+1.0
        self.update_visual()
        self.trade_cooldown = 0
        self.infection = 0
        self.risk = 100.0
        self.risk_threshold = 10
        self.color = (50,150,50)
        if (RNG(100) < 5):
            self.infection = 1000
            self.color = (200,200,0)

    def step(self, model):
        self.direction += RNG(20)-10
        self.speed = model["movespeed"]
        model["total_util"] += self.utility()
        if self.infection == 0:
            self.risk *= 0.99
        if self.risk > self.risk_threshold:
            nearby = self.agents_nearby(60)
            for other in nearby:
                if other.infection > 0:
                    self.point_towards(other.x,other.y)
                    self.direction += 180
        self.forward()

        if self.infection > 0:
            self.infection -= 1

        if self.infection > 0:
            self.color = (200,200,0)
        else:
            self.color = (50,150,50)

        self.trade_cooldown -= 1
        if self.trade_cooldown > 0:
            return

        nearby = self.agents_nearby(self.size)
        if len(nearby) > 0:
            other = nearby.pop()
            if other.trade_cooldown > 0:
                return
            total_bread = self.bread + other.bread
            price_bread = self.butter / total_bread + other.butter / total_bread
            self.bread = self.bread / 2 + self.butter / (2*price_bread)
            self.butter = self.bread * price_bread
            other.bread = other.bread / 2 + other.butter / (2*price_bread)
            other.butter = other.bread * price_bread
            self.trade_cooldown = 60 # 1 second
            other.trade_cooldown = 60
            self.update_visual()
            other.update_visual()

            if self.infection > 0 and other.infection == 0:
                other.infection = 1000
                other.risk = 100.0
                other.risk_threshold = 10
            if other.infection > 0 and self.infection == 0:
                self.infection = 1000
                self.risk = 100.0
                self.risk_threshold = 10

def setup(model):
    model.reset()
    model.clear_plots()
    model["total_util"] = 0
    model["movespeed"] = 0.2
    people = set([Person() for i in range(20)])
    model.add_agents(people)

def step(model):
    model["total_util"] = 0
    for a in model.agents:
        a.step(model)
    model.update_plots()
    model.remove_destroyed_agents()

bnb_model = Model("Epidemic",50,50)
bnb_model.add_button("Setup", setup)
bnb_model.add_button("Step", step)
bnb_model.add_toggle_button("Go", step)
bnb_model.add_slider("movespeed", 0.1, 1, .1)
bnb_model.graph("total_util",(0,0,0))
run(bnb_model)

