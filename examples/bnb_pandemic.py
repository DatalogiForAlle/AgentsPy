#!/usr/bin/env python3
import math
import random
from agents import Agent, Model, run, AgentShape

"""
  Forklaring af model:
  En kombination af bread_n_butter og epidemic modellerne.
  Agenternes mængde af brød/smør aftager nu langsomt og konstant, men enkelte
  agenter får med tilfældige mellemrum uddelt ekstra brød/smør, sådan at der
  opretholdes et nogenlunde konsistent niveau af brød/smør.
  Handelen fungerer på samme måde som før, men der er nu mulighed for at smitte
  gennem handel.
  Raske agenter undgår syge agenter, med mindre at deres mængde af brød og smør
  er aftaget for meget.
  Syge agenter undgår altid andre syge agenter.
"""


class Person(Agent):
    def update_visual(self):
        self.size = self.utility() * 5

    def utility(self):
        return math.sqrt(self.bread) * math.sqrt(self.butter)

    def setup(self, model):
        self.shape = AgentShape.CIRCLE
        self.bread = random.randint(0, 9) + 1.0
        self.butter = random.randint(0, 9) + 1.0
        self.update_visual()
        self.trade_cooldown = 0
        self.infection = 0
        self.risk_threshold = self.utility() * 0.8
        self.color = (50, 150, 50)
        if random.randint(0, 100) < 10:
            self.infection = 2000
            self.color = (200, 200, 0)

    def step(self, model):
        if model.Decay:
            self.bread *= 0.9999
            self.butter *= 0.9999
            if random.randint(0, 10000) == 10000:
                self.bread += random.randint(0, 5)
                self.butter += random.randint(0, 5)
        self.direction += random.randint(0, 20) - 10
        self.speed = model.movespeed
        model.total_util += self.utility()
        if self.utility() > self.risk_threshold or self.infection > 0:
            nearby = self.agents_nearby(60)
            nearby_infected = 0
            new_dir = 0
            for other in nearby:
                if other.infection > 0:
                    nearby_infected += 1
                    self.point_towards(other.x, other.y)
                    new_dir += self.direction
            if nearby_infected > 0:
                new_dir /= nearby_infected
                self.direction = new_dir + 180
        self.forward()
        self.update_visual()

        if self.infection > 0:
            self.infection -= 1
            self.color = (200, 200, 0)
        else:
            self.color = (50, 150, 50)

        self.trade_cooldown -= 1
        if self.trade_cooldown > 0:
            return

        nearby = self.agents_nearby(self.size)
        if len(nearby) > 0:
            other = nearby.pop()
            if other.trade_cooldown > 0:
                return
            total_bread = self.bread + other.bread
            price_bread = (self.butter / total_bread
                           + other.butter / total_bread)

            self.bread = self.bread / 2 + self.butter / (2 * price_bread)
            self.butter = self.bread * price_bread

            other.bread = other.bread / 2 + other.butter / (2 * price_bread)
            other.butter = other.bread * price_bread

            self.trade_cooldown = 60  # 1 second
            other.trade_cooldown = 60
            self.update_visual()
            other.update_visual()
            self.risk_threshold = self.utility() * 0.8
            other.risk_threshold = other.utility() * 0.8

            if self.infection > 0 and other.infection == 0:
                other.infection = 2000
                other.color = (200, 200, 0)
            if other.infection > 0 and self.infection == 0:
                self.infection = 2000
                self.color = (200, 200, 0)


def setup(model):
    model.reset()
    model.clear_plots()
    model.total_util = 0
    model.BNP = 0
    people = set([Person() for i in range(20)])
    model.add_agents(people)


def step(model):
    model.BNP = 0
    for a in model.agents:
        a.step(model)
        model.BNP += a.utility()
    model.update_plots()
    model.remove_destroyed_agents()


bnb_model = Model("Bread & butter economy during pandemic", 50, 50)
bnb_model.add_button("Setup", setup)
bnb_model.add_button("Step", step)
bnb_model.add_toggle_button("Go", step)
bnb_model.add_controller_row()
bnb_model.add_slider("movespeed", 0.5, 0.1, 1)
bnb_model.add_checkbox("Decay")
bnb_model.line_chart(["BNP"], [(0, 0, 0)])
bnb_model.show_direction = False
run(bnb_model)
