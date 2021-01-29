from agents import *
from random import randint

class Prey(Agent):
    def setup(self, model):
        self.food = 0
        self.time_since_eating = 0

    def step(self, model):
        self.direction += randint(-10,10)
        self.forward()
        tile = self.current_tile()
        if tile.info["grass"]:
            self.food += 1
            self.time_since_eating = 0
            tile.info["grass"] = False
        if self.food > model.reproduce_food_count:
            new_prey = Prey()
            new_prey.x = self.x
            new_prey.y = self.y
            model.add_agent(new_prey)
            self.food = 0
        self.time_since_eating += 1
        if self.time_since_eating > model.max_time_since_eating:
            self.destroy()

def model_setup(model):
    model.reset()
    for a in range(100):
        model.add_agent(Prey())
    for t in model.tiles:
        t.info["grass"] = True
        t.color = (0,150,0)
    model.reproduce_food_count = 10
    model.max_time_since_eating = 60

def model_step(model):
    for a in model.agents:
        a.step(model)
    for t in model.tiles:
        if t.info["grass"]:
            t.color = (0,150,0)
        else:
            t.color = (80,80,0)
            if randint(1,500) == 500:
                t.info["grass"] = True


model = Model("Predator-prey-model", 50, 50)

model.add_button("Setup", model_setup)
model.add_toggle_button("Go", model_step)
model.add_slider("reproduce_food_count", 10, 1, 30)
model.add_slider("max_time_since_eating", 60, 10, 120)

run(model)
