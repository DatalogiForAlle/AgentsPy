#!/usr/bin/env python3
import random
from agents import Agent, SimpleModel, run


class Person(Agent):

    # Inficer agenten
    def infect(self, model):
        self.infection = 1000
        model.infected += 1
        model.normal -= 1
        self.color = (200, 200, 0)

    # Gør agenten immun
    def immunize(self, model):
        self.infection = 0
        model.infected -= 1
        model.immune += 1
        self.immune = True

    def setup(self, model):
        self.color = (50, 150, 50)
        self.immune = False
        self.size = 10
        self.infection = 0
        model.normal += 1
        if random.randint(0, 100) < 5:
            self.infect(model)

    def step(self, model):
        nearby = self.agents_nearby(30)
        nearby_infected = 0
        self.size = model.agentsize
        # Find the average angle of nearby infected agents
        average_angle = 0
        for other in nearby:
            if other.infection > 0:
                nearby_infected += 1
                average_angle += self.direction_to(other.x, other.y)
        # If any nearby infected, move away from them
        if nearby_infected > 0:
            average_angle /= nearby_infected
            self.direction = average_angle + 180
        else:
            self.direction += random.randint(0, 20) - 10
        self.speed = model.movespeed
        self.forward()

        if self.infection > 1:
            t = self.current_tile()
            t.info["infection"] = model.decay * 60
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
            self.color = (200, 200, 0)
        elif self.immune:
            self.color = (0, 0, 250)
        else:
            self.color = (50, 150, 50)


def setup(model):
    model.reset()
    model.unpause()
    model.movespeed = 0.5
    model.normal = 0
    model.infected = 0
    model.immune = 0
    model.decay = 2
    model.agentsize = 5
    people = set([Person() for i in range(100)])
    model.add_agents(people)
    for t in model.tiles:
        t.color = (0, 50, 0)
        t.info["infection"] = 0
    model.clear_plots()


def step(model):
    if model.immune == 100:
        model.pause()
    for a in model.agents:
        a.step(model)
    for t in model.tiles:
        if t.info["infection"] > 0:
            t.color = (100, 100, 0)
            t.info["infection"] -= 1
        else:
            t.color = (0, 50, 0)
    model.update_plots()


def direction(model):
    for a in model.agents:
        a.show_direction = not a.show_direction


def print_infections(model):
    print("Total infections are " + str(model["infected"]))


epidemic_model = SimpleModel("Epidemic", 100, 100, setup, step, tile_size=5)
epidemic_model.add_button("Step", step, toggle=True)
epidemic_model.add_slider("decay", 2, 0, 3)
epidemic_model.add_slider("movespeed", 0.5, 0.1, 2)
epidemic_model.monitor("immune")

epidemic_model.line_chart(
    ["normal", "infected", "immune"],
    [(0, 200, 0), (200, 200, 0), (100, 100, 255)],
)
epidemic_model.bar_chart(["normal", "infected", "immune"], (100, 200, 100))
epidemic_model.agent_line_chart("infection", 0, 1000)
epidemic_model.on_close(print_infections)

run(epidemic_model)
