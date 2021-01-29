from agents import Model, Agent, run

miner_model = Model("MinerBots", 100, 100)

miner_model.add_agent(Agent())

run(miner_model)
