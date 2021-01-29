import unittest
import pathlib
import agents

MODEL_FILENAME = pathlib.Path(__file__).parent.joinpath("test_model.cell")


class TestAgent(agents.Agent):
    def setup(self, model):
        self.test_variable = 42


class OtherAgent(agents.Agent):
    def setup(self, model):
        self.test_variable = 1337


class ModelTests(unittest.TestCase):
    def setUp(self):
        self.model = agents.Model("Test Model", 20, 20, tile_size=20)
        self.model_datafile = agents.Model(
            "Test Model 2", cell_data_file=MODEL_FILENAME
        )
        self.test_agent = TestAgent()
        self.other_agent = OtherAgent()

    def test_model_wrapping_enabled_by_default(self):
        """
        Test that wrapping is enabled by default when creating models
        """
        self.assertTrue(self.model.wrapping())

    def test_model_add_agent(self):
        """
        Test that the agent is actually added on model.add_agent()
        """
        self.model.add_agent(self.test_agent)
        for agent in self.model.agents:
            self.assertEqual(agent, self.test_agent)

    def test_model_add_agents(self):
        """
        Test that when adding a list of agents, all agents are added
        and only those agents are added
        """
        agent_list = [self.test_agent, self.other_agent]
        self.model.add_agents(agent_list)

        # Check all agents are added
        self.assertTrue(all([a in self.model.agents for a in agent_list]))

        # Check all only those agents are added
        self.assertTrue(all([a in agent_list for a in self.model.agents]))

    def test_model_reset(self):
        """
        Check that agents are removed on model.reset()
        """
        agent_list = [self.test_agent, self.other_agent]
        self.model.add_agents(agent_list)
        self.model.reset()
        self.assertEqual(len(list(self.model.agents)), 0)

    def test_model_reload(self):
        """
        Check that reload() after a reset() actually reloads the model file
        """
        self.model_datafile.reset()
        # Check that tiles were reset
        for tile in self.model_datafile.tiles:
            self.assertEqual(len(tile.info), 0)

        self.model_datafile.reload()
        # Check that values are reloaded
        for x in range(3):
            for y in range(3):
                tile = self.model_datafile.tile(x, y)
                self.assertTrue("data" in tile.info)
                self.assertEqual(tile.info["data"], y * 3 + x)

    def test_model_remove_destroyed_agents(self):
        """
        Check that remove_destroyed_agents() removes any agents
        which have been destroyed
        """
        agent_list = [self.test_agent, self.other_agent]
        self.model.add_agents(agent_list)
        self.test_agent.destroy()
        self.model.remove_destroyed_agents()

        # Check that test_agent is removed
        self.assertNotIn(self.test_agent, self.model.agents)

        # Check that other_agent is not removed
        self.assertIn(self.other_agent, self.model.agents)
