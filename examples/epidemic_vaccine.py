from agents import Model, Agent, run
from random import randint


class Person(Agent):
    def setup(self, model):
        model.Susceptible += 1
        self.category = 0
        self.color = (0, 200, 0)
        if randint(1, 50) == 1:
            self.infect(model)

    def step(self, model):
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

    def vaccinate(self, model):
        if self.category == 0:
            model.Susceptible -= 1
        elif self.category == 1:
            model.Infectious -= 1
        else:
            model.Recovered -= 1
        model.Vaccinated += 1
        self.color = (100, 100, 200)
        self.category = 3

counter = 0
file_handle = None

def model_setup(model):
    global counter, file_handle
    counter = 0
    if file_handle is not None:
        file_handle.close()
    file_handle = open("vaccine.csv", "w")
    file_handle.close()

    model.reset()
    model.Susceptible = 0
    model.Infectious = 0
    model.Recovered = 0
    model.Vaccinated = 0
    model.Vaccine_timer = 0
    model.Vaccine_rate = 0.2
    for person in range(100):
        model.add_agent(Person())


def model_step(model):
    global counter, file_handle
    for person in model.agents:
        person.step(model)

    model.Vaccine_timer += 1
    if model.Vaccine_timer > 30 / model.Vaccine_rate:
        model.Vaccine_timer = 0
        for person in model.agents:
            # If not infected or already vaccinated
            if person.category != 1 and person.category != 3:
                person.vaccinate(model)
                break

    file_handle = open("vaccine.csv", "a")
    file_handle.write(str(counter)+","
                      +str(model.Susceptible)+","
                      +str(model.Infectious)+","
                      +str(model.Recovered)+","
                      +str(model.Vaccinated)+"\n")
    file_handle.close()

    counter += 1
    model.update_plots()

def close(model):
    print("yo")
    if file_handle is not None:
        file_handle.close()

epidemic_model = Model("Epidemimodel", 100, 100)

epidemic_model.add_button("Setup", model_setup)
epidemic_model.add_button("Go", model_step, toggle=True)
epidemic_model.add_slider("Vaccine_rate", 0.2, 0.1, 1.0)

epidemic_model.line_chart(
    ["Susceptible", "Infectious", "Recovered", "Vaccinated"], [(0, 200, 0), (200, 0, 0), (0, 0, 200), (100, 100, 200)]
)
epidemic_model.bar_chart(["Susceptible", "Infectious", "Recovered", "Vaccinated"], (200, 200, 200))

epidemic_model.monitor("Susceptible")
epidemic_model.monitor("Infectious")
epidemic_model.monitor("Recovered")
epidemic_model.monitor("Vaccinated")
epidemic_model.on_close(close)

run(epidemic_model)
