from agents import *
from random import randint

class Virus():
    def __init__(self, infection_level, mutation):
        self.infection_level = infection_level
        self.mutation = mutation

class Person(Agent):
    def setup(self,model):
        model["S"] += 1
        self.category = 0
        self.color = (200,200,200)

        self.immunities = []
        self.virus = None

        if randint(1,50) == 1:
            self.infect(model, Virus(600,5))

        if model["enable_groups"]:
            self.group = randint(1,5)
            self.group_indicator = model.add_ellipse(self.x-10,self.y-10,20,20,(0,0,0))
            if self.group == 1:
                self.group_indicator.color = (200,200,0)
            elif self.group == 2:
                self.group_indicator.color = (0,200,200)
            elif self.group == 3:
                self.group_indicator.color = (200,0,200)
            elif self.group == 4:
                self.group_indicator.color = (100,100,100)
            elif self.group == 5:
                self.group_indicator.color = (250,150,0)

    def step(self, model):
        if model["enable_groups"]:
            self.group_indicator.x = self.x-10
            self.group_indicator.y = self.y-10
        new_direction = 0
        nearby_agents = 0
        for agent in self.agents_nearby(model["social_distance"]):
            if model["enable_groups"] and agent.group != self.group:
                new_direction += self.direction_to(agent.x,agent.y)
                nearby_agents += 1
        if nearby_agents > 0:
            self.direction = (new_direction / nearby_agents) + 180
        else:
            self.direction += randint(-10,10)
        self.forward()
        if self.category == 1:
            for agent in self.agents_nearby(model["infection_distance"]):
                if agent.category == 0 and self.virus.mutation > 0:
                    agent.infect(model, Virus(600,self.virus.mutation-randint(0,1)))
            self.virus.infection_level -= 1
            if self.virus.infection_level == 0:
                self.turn_immune(model)

    def infect(self, model, virus):
        if not virus.mutation in self.immunities:
            model["S"] -= 1
            model["I"] += 1
            self.color = (200,150-30*virus.mutation,150-30*virus.mutation)
            self.category = 1
            self.virus = virus

    def turn_immune(self, model):
        model["I"] -= 1
        model["S"] += 1
        self.color = (200-30*len(self.immunities),200,200-30*len(self.immunities))
        self.category = 0
        self.immunities.append(self.virus.mutation)
        self.virus = None

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
#epidemic_model.multi_line_chart(["S","I","R"],[(0, 200, 0),(200, 0, 0),(0, 0, 200)])
epidemic_model.multi_line_chart(["S","I"],[(0, 200, 0),(200, 0, 0)])
epidemic_model.add_checkbox("enable_groups")
epidemic_model.add_controller_row()
epidemic_model.add_slider("social_distance", 0, 80, 50)
epidemic_model.add_controller_row()
epidemic_model.add_slider("infection_distance", 0, 40, 15)

run(epidemic_model)
