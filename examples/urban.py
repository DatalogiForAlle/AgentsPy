#!/usr/bin/env python3
import random
import math
from agents import Agent, Model, run


class Seeker(Agent):
    def setup(self, model):
        self.x = model.width // 2
        self.y = model.height // 2
        self.size = 4
        self.speed = 1
        self.direction = random.randint(0, 360)
        self.search_angle = 45
        self.color = (0, 0, 255)
        self.settled = False
        self.wait = 0
        self.max_wait = 180

    def get_next_tile(self, model, d):
        next_x = self.x + math.cos(math.radians(d)) * self.speed
        next_x = round(next_x * model.x_tiles / model.width)
        next_y = self.y + math.sin(math.radians(d)) * self.speed
        next_y = round(next_x * model.x_tiles / model.width)
        return model.tile(next_x, next_y)

    def step(self, model):
        if not self.settled:
            t = self.current_tile()
            t.info["value"] += 0.1
            fwd_tile = self.get_next_tile(model, self.direction)
            l_tile = self.get_next_tile(model,
                                        self.direction + self.search_angle)
            r_tile = self.get_next_tile(model,
                                        self.direction - self.search_angle)
            best_tile = max(
                fwd_tile.info["value"],
                l_tile.info["value"],
                r_tile.info["value"]
            )
            if best_tile == l_tile.info["value"]:
                self.direction += random.randint(0, self.search_angle)
            if best_tile == r_tile.info["value"]:
                self.direction -= random.randint(0, self.search_angle)
            self.forward()

            max_attraction_value = 255
            settle_value = random.randint(0, int(t.info["value"]))
            if settle_value > max_attraction_value / 2:
                self.settled = True
                self.wait = 0
                self.color = (150, 150, 255)
        else:
            t = self.current_tile()
            t.info["value"] += 0.1
            self.wait += 1
            if self.wait > self.max_wait:
                self.settled = False
                self.color = (0, 0, 255)


def setup(model):
    model.reset()
    model.invisible = False
    tx = model.x_tiles
    ty = model.y_tiles

    # Generate the "terrain"
    model.tiles[0].info["value"] = 100 + random.randint(0, 100)
    for x in range(tx):
        for y in range(ty):
            avg_value = 0
            neighbors = 0
            if y > 0:
                i = (y - 1) * tx + x
                avg_value += model.tiles[i].info["value"]
                neighbors += 1
            if x > 0:
                i = y * tx + (x - 1)
                avg_value += model.tiles[i].info["value"]
                neighbors += 1
            if neighbors > 0:
                model.tile(x,y).info["value"] = max(
                    0, min(255,
                           avg_value // neighbors - 20 + random.randint(0, 40))
                )

    for tile in model.tiles:
        tile.color = (tile.info["value"], tile.info["value"], 0)
    seekers = set([Seeker() for i in range(200)])
    model.add_agents(seekers)


def step(model):
    for tile in model.tiles:
        if tile.info["value"] > 255:
            tile.info["value"] = 0
        tile.color = (tile.info["value"], tile.info["value"], 0)
    for agent in model.agents:
        agent.step(model)


def invisible(model):
    model.invisible = not model.invisible
    if model.invisible:
        for a in model.agents:
            a.size = 0
    else:
        for a in model.agents:
            a.size = 4


urban_model = Model("urban", 50, 50)
urban_model.add_button("Setup", setup)
urban_model.add_toggle_button("Go", step)
urban_model.add_button("Invisible", invisible)
run(urban_model)
