from agents import Model, Agent, run


def model_setup(model):
    model.reset()
    print("hello\n")
    model.add_agent(Agent())


epidemic_model = Model("Epidemimodel", 100, 100)

epidemic_model.add_button("Setup", model_setup)

run(epidemic_model)
