import unittest
from agents import *

class TestAgent(Agent):
    def setup(self, model):
        self.test_variable = 42

class OtherAgent(Agent):
    def setup(self, model):
        self.test_variable = 1337

class ModelTests(unittest.TestCase):
    def setUp(self):
        self.model = Model('Test Model', 20, 20, tile_size=20)
        self.model_datafile = Model('Test Model 2', cell_data_file='model_data')
        self.test_agent = TestAgent()
        self.other_agent = OtherAgent()

    def test_model_add_agent(self):
        self.model.add_agent(self.test_agent)
        for agent in self.model.agents:
            self.assertEqual(agent, self.test_agent,
                         'Model.add_agent() did not add the agent to the model')

    # Ideally this should also be checked the other way around,
    # but I'm not sure of the best way to do it.
    def test_model_add_agents(self):
        agent_list = [self.test_agent, self.other_agent]
        self.model.add_agents(agent_list)
        for a1 in agent_list:
            isIn = False
            for a2 in self.model.agents:
                if a1 is a2:
                    isIn = True
            self.assertTrue(isIn,
                            'Model.add_agents() did not add the agent to the model')

    def test_model_reset(self):
        agent_list = [self.test_agent, self.other_agent]
        self.model.add_agents(agent_list)
        self.model.reset()
        agents = 0
        for agent in self.model.agents:
            agents += 1
        self.assertEqual(agents, 0,
                         'Model.reset() did not remove all agents')

    def test_model_reload(self):
        self.model_datafile.reset()
        self.model_datafile.reload()
        for x in range(3):
            for y in range(3):
                self.assertEqual(self.model_datafile.tiles[y*3+x].info["data"], y*3+x,
                                 'Model.reload() did not apply the expected values to tiles')

    def test_model_remove_destroyed_agents(self):
        agent_list = [self.test_agent, self.other_agent]
        self.model.add_agents(agent_list)
        self.test_agent.destroy()
        self.model.remove_destroyed_agents()
        isIn = False
        for agent in self.model.agents:
            self.assertIsNot(agent, self.test_agent,
                             'Model.remove_destroyed_agents() did not remove a destroyed agent')
            if agent is self.other_agent:
                isIn = True
        self.assertTrue(isIn,
                        'Model.remove_destroyed_agents() removed the wrong agent')

if __name__ == '__main__':
    unittest.main()
