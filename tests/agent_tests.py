import unittest
from agents import *

class TestAgent(Agent):
    def setup(self, model):
        self.test_variable = 42


class AgentTests(unittest.TestCase):
    def setUp(self):
        self.model = Model('Test Model', 20, 20, tile_size=20)
        self.test_agent = TestAgent()

    def test_agent_setup_on_add(self):
        self.model.add_agent(self.test_agent)
        self.assertEqual(self.test_agent.test_variable, 42,
                         'Agent.setup() not called in Model.add_agent()')

    def test_agent_center_in_tile(self):
        self.model.add_agent(self.test_agent)
        self.test_agent.jump_to(1,1)
        self.test_agent.center_in_tile()
        self.assertEqual((self.test_agent.x,self.test_agent.y), (10,10),
                         'Agent.center_in_tile() did not center agent properly')

    def test_agent_jump_to(self):
        self.model.add_agent(self.test_agent)
        self.test_agent.jump_to(42,43)
        self.assertEqual((self.test_agent.x,self.test_agent.y), (42,43),
                         'Agent.jump_to() did not place agent correctly')
        self.test_agent.jump_to(0,0)
        self.assertEqual((self.test_agent.x,self.test_agent.y), (0,0),
                         'Agent.jump_to() did not place agent correctly')
        self.test_agent.jump_to(399,399)
        self.assertEqual((self.test_agent.x,self.test_agent.y), (399,399),
                         'Agent.jump_to() did not place agent correctly')
        self.test_agent.jump_to(13,37)
        self.assertEqual((self.test_agent.x,self.test_agent.y), (13,37),
                         'Agent.jump_to() did not place agent correctly')

    """
    Depends on Model.tile(), which is not implemented on master yet.
    def test_agent_jump_to_tile(self):
        self.model.add_agent(self.test_agent)
        self.test_agent.jump_to_tile(self.model.tile(7,13))
        self.assertEqual(self.test_agent.current_tile(), self.model.tile(7,13),
                         'Agent.jump_to_tile() did not set the agent\'s tile correctly')
        tile_x = self.model.tile(7,13).x / self.model.tiles_x * self.model.width
        tile_y = self.model.tile(7,13).y / self.model.tiles_y * self.model.height
        self.assertEqual((self.test_agent.x,self.test_agent.y), (tile_x,tile_y),
                         'Agent.jump_to_tile() did not place the agent correctly')
    """

    def test_agent_direction_to(self):
        self.test_agent.jump_to(200,200)
        direction = self.test_agent.direction_to(0,0)
        self.assertEqual(round(direction), 225,
                         'Agent.direction_to() did not orient the agent correctly')
        direction = self.test_agent.direction_to(400,400)
        self.assertEqual(round(direction), 45,
                         'Agent.direction_to() did not orient the agent correctly')
        direction = self.test_agent.direction_to(200,400)
        self.assertEqual(round(direction), 90,
                         'Agent.direction_to() did not orient the agent correctly')
        direction = self.test_agent.direction_to(200,0)
        self.assertEqual(round(direction), 270,
                         'Agent.direction_to() did not orient the agent correctly')

    def test_agent_point_towards(self):
        self.test_agent.jump_to(200,200)
        self.test_agent.point_towards(0,0)
        self.assertEqual(round(self.test_agent.direction), 225,
                         'Agent.direction_to() did not orient the agent correctly')
        self.test_agent.point_towards(400,400)
        self.assertEqual(round(self.test_agent.direction), 45,
                         'Agent.direction_to() did not orient the agent correctly')
        self.test_agent.point_towards(200,400)
        self.assertEqual(round(self.test_agent.direction), 90,
                         'Agent.direction_to() did not orient the agent correctly')
        self.test_agent.point_towards(200,0)
        self.assertEqual(round(self.test_agent.direction), 270,
                         'Agent.direction_to() did not orient the agent correctly')

    def test_agent_forward(self):
        self.test_agent.direction = 0
        self.test_agent.jump_to(200,200)
        self.test_agent.speed = 1
        self.test_agent.forward()
        self.assertEqual((self.test_agent.x,self.test_agent.y),(201,200),
                         'Agent.forward() did not move the agent correctly')
        self.test_agent.jump_to(200,200)
        self.test_agent.speed = 10
        self.test_agent.forward()
        self.assertEqual((self.test_agent.x,self.test_agent.y),(210,200),
                         'Agent.forward() did not move the agent correctly')
        self.test_agent.jump_to(200,200)
        self.test_agent.speed = 0.1
        self.test_agent.forward()
        self.assertEqual((self.test_agent.x,self.test_agent.y),(200.1,200),
                         'Agent.forward() did not move the agent correctly')

if __name__ == '__main__':
    unittest.main()
