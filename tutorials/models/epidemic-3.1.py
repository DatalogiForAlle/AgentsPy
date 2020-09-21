from agents import *
from random import randint

class Person(Agent):
    def setup(self,model):
        model["S"] += 1
        self.category = 0
        self.color = (0,200,0)
        if randint(1,50) == 1:
            self.infect(model)

    def step(self, model):
        avg_direction = 0
        nearby_agents = 0
        for agent in self.agents_nearby(20):
            if agent.category == 1:
                avg_direction += self.direction_to(agent.x,agent.y)
                nearby_agents += 1
        if nearby_agents > 0:
            self.direction = (avg_direction / nearby_agents) + 180
        else:
            self.direction += randint(-10,10)
        self.forward()
        if self.category == 1:
            for agent in self.agents_nearby(12):
                if agent.category == 0:
                    agent.infect(model)
            self.infection_level -= 1
            if self.infection_level == 0:
                self.turn_immune(model)

    def infect(self, model):
        model["S"] -= 1
        model["I"] += 1
        self.color = (200,0,0)
        self.category = 1
        self.infection_level = 600

    def turn_immune(self, model):
        model["I"] -= 1
        model["R"] += 1
        self.color = (0,0,200)
        self.category = 2

def setup(model):
    model.reset()
    model["S"] = 0
    model["I"] = 0
    model["R"] = 0
    for person in range(100):
        model.add_agent(Person())

def step(model):
    for person in model.agents:
        person.step(model)
    model.update_plots()

epidemic_model = Model("Epidemimodel", 100, 100)

epidemic_model.add_button("Setup", setup)
epidemic_model.add_toggle_button("Go", step)
epidemic_model.multi_line_chart(["S","I","R"],[(0, 200, 0),(200, 0, 0),(0, 0, 200)])

run(epidemic_model)
