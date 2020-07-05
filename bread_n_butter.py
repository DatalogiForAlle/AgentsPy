#!/usr/bin/env python3
import random
import math
from agents import *
"""
# Utility function
# to varer / to agenter der har hver deres slags varer
# ex. man kan have 0-10 brod og 0-10 smor
# random mængder
# Agenterne har ens "AI" men forskellige mængder af brød
# Alle agenterne har en nyttefunktion (eks brød^a * smør^b)
# Når man møder en anden agent, hvor meget vil man så bytte?
# Der vil som udgangspunkt altid være en optimal bytte-fordeling
# Der kan også være ulighed: nogle der startet med meget brød/smør, nogen der starter med lidt
# Der skal også være en model/graf der viser hvor "tilfredse" folk er
"""

"""
 Udregninger:

 U = bread^0.5 * butter^0.5
 Endowed with bread_1, butter_1, bread_2 and butter_2
 MU_br_1 = 0.5*bread_1^-0.5 * butter_1^0.5
 MU_bu_1 = 0.5*butter_1^-0.5 * bread_1^0.5
 MU_br_2 = 0.5*bread_2^-0.5 * butter_2^0.5
 MU_bu_2 = 0.5*butter_2^-0.5 * bread_2^0.5
 butter_1 / bread_1 = butter_2 / bread_2
 butter_2 / bread_2 = (total_butter - butter_2) / (total_bread - bread_2)
 butter_2 = (total_butter - butter_2) / (total_bread - bread_2) * bread_2
 butter_2 * (total_bread - bread_2) = (total_butter - butter_2) * bread_2
 butter_2 * total_bread - butter_2 * bread_2 = total_butter * bread_2 - butter_2 * bread_2
 butter_2 * total_bread = total_butter * bread_2
 butter_2 = total_butter * bread_2 / total_bread

 butter_1 = bread_1*P_bread
 butter_2 = bread_2*P_bread

 P_bread*1.bread+P_butter*1.butter = P_bread*bread_1+P_butter*bread_1*P_bread
 P_bread*1.bread+1.butter = P_bread*bread_1+bread_1*P_bread
 P_bread*1.bread+1.butter = 2*P_bread*bread_1
 P_bread*1.bread / 2*P_bread + 1.butter / 2*P_bread = bread_1

 P_bread*2.bread+P_butter*2.butter = P_bread*bread_2+P_butter*bread_2*P_bread
 P_bread*2.bread+2.butter = P_bread*bread_2+bread_2*P_bread
 P_bread*2.bread / 2*P_bread + 2.butter / 2*P_bread = bread_2

 total_bread =
     P_bread*1.bread / 2*P_bread
   + 1.butter / 2*P_bread
   + P_bread*2.bread / 2*P_bread
   + 2.butter / 2*P_bread

 total_bread*P_bread =
     P_bread*1.bread
   + 1.butter
   + P_bread*2.bread
   + 2.butter
   - total_bread*P_bread

  total_bread*P_bread =
     1.butter
   + 2.butter
"""

class Person(Agent):
    def update_visual(self):
        self.color = (int(self.butter*20),int(self.butter*20),int(self.bread*20))
        self.size = (self.bread+self.butter)*2

    def utility(self):
        return (self.bread**0.5) * (self.butter**0.5)

    def setup(self, model):
        self.bread = RNG(9)+1.0
        self.butter = RNG(9)+1.0
        self.update_visual()
        self.trade_cooldown = 0

    def step(self, model):
        self.direction += RNG(20)-10
        self.speed = model["movespeed"]
        self.forward()
        model["total_util"] += self.utility()

        self.trade_cooldown -= 1
        if self.trade_cooldown > 0:
            return

        nearby = self.agents_nearby(15)
        if len(nearby) > 0:
            other = nearby.pop()
            """
            P_bread =
              1.butter / total_bread
              + 2.butter / total_bread

            bread_1 = 1.bread / 2 + 1.butter / 2*P_bread
            butter_1 = bread_1*P_bread
            bread_2 = 2.bread / 2 + 2.butter / 2*P_bread
            butter_2 = bread_2*P_bread
            """
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

def setup(model):
    model.reset()
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

