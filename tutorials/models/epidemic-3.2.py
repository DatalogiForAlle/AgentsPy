from agents import Model, Agent, run
from random import randint


class Person(Agent):
    def setup(self, model):
        model.Susceptible += 1
        self.category = 0
        self.color = (0, 200, 0)
        if randint(1, 50) == 1:
            self.infect(model)

        if model.enable_groups:
            self.group = randint(1, 5)
            self.group_indicator = model.add_ellipse(
                self.x - 10, self.y - 10, 20, 20, (0, 0, 0)
            )
            if self.group == 1:
                self.group_indicator.color = (200, 200, 0)
            elif self.group == 2:
                self.group_indicator.color = (0, 200, 200)
            elif self.group == 3:
                self.group_indicator.color = (200, 0, 200)
            elif self.group == 4:
                self.group_indicator.color = (100, 100, 100)
            elif self.group == 5:
                self.group_indicator.color = (250, 150, 0)

    def step(self, model):
        if model.enable_groups:
            self.group_indicator.x = self.x - 10
            self.group_indicator.y = self.y - 10
        new_direction = 0
        nearby_agents = 0
        for agent in self.agents_nearby(50):
            if model.enable_groups and agent.group != self.group:
                new_direction += self.direction_to(agent.x, agent.y)
                nearby_agents += 1
        if nearby_agents > 0:
            self.direction = (new_direction / nearby_agents) + 180
        else:
            self.direction += randint(-10, 10)
        self.forward()
        if self.category == 1:
            for agent in self.agents_nearby(12):
                if agent.category == 0:
                    agent.infect(model)
            self.infection_level -= 1
            if self.infection_level == 0:
                self.turn_immune(model)

    def infect(self, model):
        model.Susceptible -= 1
        model.Infectious += 1
        self.color = (200, 0, 0)
        self.category = 1
        self.infection_level = 600

    def turn_immune(self, model):
        model.Infectious -= 1
        model.Recovered += 1
        self.color = (0, 0, 200)
        self.category = 2


def model_setup(model):
    model.reset()
    model.Susceptible = 0
    model.Infectious = 0
    model.Recovered = 0
    for person in range(100):
        model.add_agent(Person())


def model_step(model):
    for person in model.agents:
        person.step(model)
    model.update_plots()


epidemic_model = Model("Epidemimodel", 100, 100)

epidemic_model.add_button("Setup", model_setup)
epidemic_model.add_button("Go", model_step, toggle=True)
epidemic_model.line_chart(
    ["Susceptible", "Infectious", "Recovered"], [(0, 200, 0), (200, 0, 0), (0, 0, 200)]
)
epidemic_model.add_checkbox("enable_groups")

run(epidemic_model)
