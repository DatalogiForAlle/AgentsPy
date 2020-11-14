#!/usr/bin/env python3
import random
import math
from agents import Agent, Model, run, AgentShape

"""
  Forklaring af model:
  Modellen viser et sæt agenter der foretager handel med hinanden
   med resourcerne brød og smør.
  Grafen til højre viser summen af agenternes nyttefunktioner
   (som er brød^0.5 * smør^0.5).
  Agenterne farves blå, jo mere brød de har, og gule, jo mere smør de har.
   Hvide/grå agenter har god balance i deres to resourcer.
  Agenternes størrelse er en funktion af deres nyttefunktion.
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
 butter_2 * total_bread - butter_2 * bread_2 =
  total_butter * bread_2 - butter_2 * bread_2
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
        self.color = (
            min(255, int(self.butter * 20)),
            min(255, int(self.butter * 20)),
            min(255, int(self.bread * 20)),
        )
        self.size = self.utility() * 5

    def utility(self):
        return math.sqrt(self.bread) * math.sqrt(self.butter)

    def setup(self, model):
        self.bread = random.randint(0, 9) + 1.0
        self.butter = random.randint(0, 9) + 1.0
        self.update_visual()
        self.trade_cooldown = 0
        self.util = self.utility()
        self.shape = AgentShape.CIRCLE

    def step(self, model):
        self.direction += random.randint(0, 20) - 10
        self.speed = model.movespeed
        self.forward()
        model.total_util += self.utility()

        self.trade_cooldown -= 1
        if self.trade_cooldown > 0:
            return

        nearby = self.agents_nearby(self.size)
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
        self.util = self.utility()


def setup(model):
    model.reset()
    model.clear_plots()
    model.total_util = 0
    model.movespeed = 0.2
    people = set([Person() for i in range(20)])
    model.add_agents(people)


def step(model):
    model.total_util = 0
    for a in model.agents:
        a.step(model)
    model.update_plots()
    model.remove_destroyed_agents()


bnb_model = Model("Bread & butter economy", 50, 50)
bnb_model.add_button("Setup", setup)
bnb_model.add_button("Step", step)
bnb_model.add_toggle_button("Go", step)
bnb_model.add_controller_row()
bnb_model.add_slider("movespeed", 0.1, 0.1, 1)
bnb_model.line_chart(["total_util"], [(0, 0, 0)])
bnb_model.agent_line_chart("util")
run(bnb_model)
