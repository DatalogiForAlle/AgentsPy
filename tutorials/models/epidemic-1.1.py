from agents import Model, Agent, run

epidemic_model = Model("Epidemimodel", 100, 100)

epidemic_model.add_agent(Agent())

if __name__ == "__main__":
    run(epidemic_model)
