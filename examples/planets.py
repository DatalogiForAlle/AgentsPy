from agents import *
from random import randint

class Planet(Agent):
    def setup(self, model):
        self.size = randint(5,20)
        self.shape = AgentShape.CIRCLE
        self.ax = 0
        self.ay = 0

    def step(self, model):
        G = 6.674 * (10**(-3))
        for other in model.agents:
            if other is not self:
                M = self.size * other.size
                dst = self.distance_to(other.x,other.y)
                if dst != 0:
                    F = G*M/(dst*self.size)
                    dx = other.x - self.x
                    if dx != 0:
                        self.ax += dx*F/dst
                    dy = other.y - self.y
                    if dy != 0:
                        self.ay += dy*F/dst
        self.jump_to(self.x+self.ax,
                     self.y+self.ay)


galaxy = Model("Planet simulation", 100, 100)

def model_setup(model):
    model.reset()
    #model.disable_wrapping()
    for i in range(100):
        planet = Planet()
        planet.name = "Planet "+str(i)
        model.add_agent(planet)

def model_step(model):
    for agent in model.agents:
        agent.step(model)

galaxy.add_button("Setup", model_setup)
galaxy.add_button("Go", model_step, toggle=True)
run(galaxy)
