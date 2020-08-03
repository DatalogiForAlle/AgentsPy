import random
from agents import Agent, Model, run


class Electron(Agent):
    def setup(self, model):
        self.size = 5
        self.color = (0, 0, 255)
        self.speed = model["speed"]
        self.direction = 180
        self.charged = False

    def step(self, model):
        self.speed = model["speed"]
        self.direction = 180
        if self.x < self.speed + self.size:
            model["charge_flow"] += 1
        # If hitting a nucleus, point in the opposite direction of it
        for b in self.agents_nearby(distance=10, agent_type=Nucleon):
            self.point_towards(b.x, b.y)
            self.direction -= 180
            self.direction += random.randrange(-1, 2)
        self.forward()


class Nucleon(Agent):
    def setup(self, model):
        self.size = 10
        self.color = (255, 0, 0)

    def step(self, model):
        pass


def setup(model):
    model.reset()  # can this be made implicit?
    model["speed"] = 2
    model["charge_flow"] = 0

    # Add agents
    for i in range(200):
        model.add_agent(Electron())
    for i in range(50):
        model.add_agent(Nucleon())

    # Setup tiles
    for tile in model.tiles:
        tile.color = (100, 100, 100)


def step(model):
    old_charge_flow = model["charge_flow"]
    model["charge_flow"] = 0
    for agent in model.agents:
        agent.step(model)
    model["charge_flow"] = model["charge_flow"] * 0.01 + old_charge_flow * 0.99
    model.update_plots()


modello = Model("Electricity", 50, 25)
modello.add_button("Setup", setup)
modello.add_button("Step", step)
modello.add_toggle_button("Go", step)
modello.add_controller_row()
modello.add_slider("speed", 0.1, 3, 2)
modello.line_chart("charge_flow", (100, 100, 250))
run(modello)
