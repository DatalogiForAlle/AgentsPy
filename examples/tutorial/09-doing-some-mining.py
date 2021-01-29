from random import randint
from agents import Model, Agent, run

miner_model = Model("MinerBots", 100, 100)


class Robot(Agent):
    def setup(self, model):
        self.color = (100, 100, 100)
        self.direction = randint(0, 359)
        self.loaded = False

    def step(self, model):
        self.direction += randint(0, 20) - 10
        self.forward()
        self.speed = model.speed_factor
        t = self.current_tile()
        if t.info["has_mineral"] and not self.loaded:
            t.info["has_mineral"] = False
            t.color = (200, 100, 0)
            self.color = (100, 100, 255)
            self.loaded = True


def setup(model):
    model.reset()
    for x in range(10):
        model.add_agent(Robot())
    model.speed_factor = 1
    for t in model.tiles:
        if randint(0, 50) == 50:
            t.color = (0, 255, 255)
            t.info["has_mineral"] = True
        else:
            t.color = (200, 100, 0)
            t.info["has_mineral"] = False


def step(model):
    for ag in model.agents:
        ag.step(model)


miner_model.add_button("Setup", setup)

miner_model.add_toggle_button("Go", step)

miner_model.add_slider("speed_factor", 1, 1, 5)

run(miner_model)
