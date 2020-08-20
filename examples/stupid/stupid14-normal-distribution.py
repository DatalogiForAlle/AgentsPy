import random
import math
import numpy as np
from agents import Agent, Model, run


class Bug(Agent):
    def draw_color(self):
        gradient = max(0, 255-255*self.grow_size/10)
        self.color = (255, gradient, gradient)

    def setup(self, model):
        self.size = 8
        self.grow_size = max(0, np.random.normal(0.1, 0.03))
        self.survivalprobability = 95
        model["current_bugs"] += 1
        self.draw_color()
        self.align()
        self.update_current_tile()

    def step(self, model):
        # Eat from the current tile
        t = self.current_tile()
        self.grow_size += min(model["max_food_eat"], t.info["food"])
        t.info["food"] = max(0, t.info["food"]-model["max_food_eat"])

        # Split into new bugs
        if self.grow_size > 10:
            for _ in range(5):
                for _ in range(5):
                    newbug_x = 3-random.randint(0, 6)
                    newbug_y = 3-random.randint(0, 6)
                    newbug_t = model.tiles[((t.y+newbug_y) % model.y_tiles)
                                           * model.x_tiles
                                           + (t.x+newbug_x) % model.x_tiles]
                    if len(newbug_t.get_agents()) == 0:
                        newbug = Bug()
                        model.add_agent(newbug)
                        newbug.x = newbug_t.x * model.width / model.x_tiles
                        newbug.y = newbug_t.y * model.height / model.y_tiles
                        newbug.align()
                        break
            self.destroy()
            model["current_bugs"] -= 1
            return

        # Find all nearby valid tiles
        nearby_tiles = self.nearby_tiles(-4, -4, 4, 4)
        random.shuffle(nearby_tiles)

        def is_valid_tile(t):
            return len(t.get_agents()) == 0
        nearby_tiles = list(filter(is_valid_tile, nearby_tiles))

        # Move to the best tile
        best_t = None
        for new_t in nearby_tiles:
            if (not best_t or (best_t.info["food"] < new_t.info["food"])):
                if len(new_t.get_agents()) == 0:
                    best_t = new_t
        if best_t:
            self.jump_to((best_t.x)*model.width/model.x_tiles,
                         (best_t.y)*model.height/model.y_tiles)
            self.align()
        self.draw_color()

        if self.survivalprobability < random.randint(0, 100):
            model["current_bugs"] -= 1
            self.destroy()


def setup(model):
    global f
    f = open("stupid.data", "w")
    model.reset()
    people = set([Bug() for i in range(math.floor(model["initial_bugs"]))])
    model["current_bugs"] = model["initial_bugs"]
    model["stop"] = False
    model.add_agents(people)
    for t in model.tiles:
        t.info["food"] = 0.0
        t.color = (0, 0, 0)


def step(model):
    global f
    if not model["stop"]:
        bug_min = None
        bug_mean = 0
        bug_max = None
        for a in model.agents_ordered("grow_size"):
            a.step(model)
            if not bug_min or bug_min > a.grow_size:
                bug_min = a.grow_size
            if not bug_max or bug_max < a.grow_size:
                bug_max = a.grow_size
            bug_mean += a.grow_size
        bug_mean /= model["initial_bugs"]
        f.write(str(bug_min) + " " + str(bug_mean) + " " + str(bug_max) + "\n")
        # Flush is necessary as long as we can't call f.close()
        # when the user exits the program
        f.flush()

        for t in model.tiles:
            food_prod = random.random() * model["max_food_prod"]
            t.info["food"] += food_prod
            c = min(255, math.floor(t.info["food"] * 255))
            t.color = (c, c, c)
        model.update_plots()
        model.remove_destroyed_agents()


stupid_model = Model("StupidModel w. gauss distribution of sizes (stupid14)",
                     100, 100, tile_size=5)
stupid_model.add_button("setup", setup)
stupid_model.add_button("step", step)
stupid_model.add_toggle_button("go", step)
stupid_model.add_controller_row()
stupid_model.add_slider("initial_bugs", 10, 300, 100)
stupid_model.add_controller_row()
stupid_model.add_slider("max_food_eat", 0.1, 1.0, 1.0)
stupid_model.add_controller_row()
stupid_model.add_slider("max_food_prod", 0.01, 0.1, 0.01)
stupid_model.histogram("grow_size", 0, 10, 5, (0, 0, 0))
stupid_model.line_chart("current_bugs", (0, 0, 0))
run(stupid_model)
