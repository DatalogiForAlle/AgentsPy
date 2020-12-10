from agents import Model, Agent, run


def setup(model):
    model.reset()
    print("hello\n")
    model.add_agent(Agent())


epidemic_model = Model("Epidemimodel", 100, 100)

epidemic_model.add_button("Setup", setup)
print("hello 1")
# run(epidemic_model)
