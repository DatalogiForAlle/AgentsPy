import unittest
from agents import *

class TestAgent(Agent):
    def setup(self, model):
        self.test_variable = 42

class OtherAgent(Agent):
    def setup(self, model):
        self.test_variable = 1337

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
        test_cases = [(42,43),(0,0),(399,399),(13,37)]
        self.model.add_agent(self.test_agent)
        for (x,y) in test_cases:
            with self.subTest(i=(x,y)):
                self.test_agent.jump_to(x,y)
                self.assertEqual((self.test_agent.x,self.test_agent.y), (x,y),
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
        test_cases = [(0,0,225),(400,400,45),(200,400,90),(200,0,270)]
        self.test_agent.jump_to(200,200)
        for (x,y,d) in test_cases:
            with self.subTest(i=(x,y,d)):
                direction = self.test_agent.direction_to(x,y)
                self.assertEqual(round(direction), d,
                                 'Agent.direction_to() did not return the correct direction')

    def test_agent_point_towards(self):
        test_cases = [(0,0,225),(400,400,45),(200,400,90),(200,0,270)]
        self.test_agent.jump_to(200,200)
        for (x,y,d) in test_cases:
            with self.subTest(i=(x,y,d)):
                self.test_agent.point_towards(x,y)
                self.assertEqual(round(self.test_agent.direction), d,
                                 'Agent.point_towards() did not orient the agent correctly')

    def test_agent_forward(self):
        test_cases = [(1,201),(10,210),(0.1,200.1)]
        self.test_agent.direction = 0
        for (speed,x) in test_cases:
            with self.subTest(i=(speed,x)):
                self.test_agent.jump_to(200,200)
                self.test_agent.speed = speed
                self.test_agent.forward()
                self.assertEqual((self.test_agent.x,self.test_agent.y),(x,200),
                                 'Agent.forward() did not move the agent correctly')

    def test_agent_backward(self):
        test_cases = [(1,199),(10,190),(0.1,199.9)]
        self.test_agent.direction = 0
        for (speed,x) in test_cases:
            with self.subTest(i=(speed,x)):
                self.test_agent.jump_to(200,200)
                self.test_agent.speed = speed
                self.test_agent.backward()
                self.assertEqual((self.test_agent.x,self.test_agent.y),(x,200),
                                 'Agent.forward() did not move the agent correctly')


    def test_agent_left(self):
        test_cases = [(45,45),(270,270),(360,0),(405,45)]
        for (turn,d) in test_cases:
            with self.subTest(i=(turn,d)):
                self.test_agent.direction = 0
                self.test_agent.left(turn)
                self.assertEqual(self.test_agent.direction, d,
                                 'Agent.left() did not rotate the agent correctly')

    def test_agent_right(self):
        test_cases = [(45,315),(270,90),(360,0),(405,315)]
        for (turn,d) in test_cases:
            with self.subTest(i=(turn,d)):
                self.test_agent.direction = 0
                self.test_agent.right(turn)
                self.assertEqual(self.test_agent.direction, d,
                                 'Agent.right() did not rotate the agent correctly')

    def test_agent_distance_to(self):
        test_cases = [(200,300,100),(230,160,50),(0,0,282.842712475)]
        self.test_agent.jump_to(200,200)
        for (x,y,dist) in test_cases:
            with self.subTest(i=(x,y,dist)):
                self.assertAlmostEqual(
                    self.test_agent.distance_to(x,y), dist,
                    msg='Agent.distance_to() did not return the correct distance')

    def test_agent_agents_nearby(self):
        test_cases = [(200,200,100,None,2),(150,200,50,None,1),
                      (150,200,50,OtherAgent,0),(250,200,50,OtherAgent,1)]
        agent1 = TestAgent()
        agent2 = OtherAgent()
        self.model.add_agents([agent1,agent2])
        agent1.jump_to(100,200)
        agent2.jump_to(300,200)

        for (x,y,range,a_type,num_agents) in test_cases:
            with self.subTest(i=(x,y,range,a_type,num_agents)):
                self.test_agent.jump_to(x,y)
                nearby = self.test_agent.agents_nearby(range, agent_type=a_type)
                self.assertEqual(
                    len(nearby), num_agents,
                    'Agent.agents_nearby() did not find the correct number of agents')

    # This test could probably be more sophisticated, but I'm not sure how.
    def test_agent_nearby_tile(self):
        test_cases = [(-1,-1,1,1,9),(-2,-2,2,2,25),(-5,2,5,4,33)]
        self.test_agent.jump_to(200,200)
        for (x1,y1,x2,y2,num_tiles) in test_cases:
            with self.subTest(i=(x1,y1,x2,y2,num_tiles)):
                nearby_tiles = self.test_agent.nearby_tiles(x1,y1,x2,y2)
                self.assertEqual(
                    len(nearby_tiles), num_tiles,
                    'Agent.nearby_tiles() did not return the correct number of tiles')

if __name__ == '__main__':
    unittest.main()
