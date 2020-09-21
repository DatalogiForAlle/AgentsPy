import unittest
import agents


class TestAgent(agents.Agent):
    def setup(self, model):
        self.test_variable = 42


class OtherAgent(agents.Agent):
    def setup(self, model):
        self.test_variable = 1337


class AgentTests(unittest.TestCase):
    def setUp(self):
        self.model = agents.Model("Test Model", 20, 20, tile_size=20)
        self.test_agent = TestAgent()

    def test_agent_setup_on_add(self):
        """
        Check that agents setup-function is called when added to a model
        """
        self.model.add_agent(self.test_agent)
        self.assertEqual(self.test_agent.test_variable, 42)

    def test_agent_center_in_tile(self):
        """
        Check that center_in_tile() centers the agent properly
        """
        self.model.add_agent(self.test_agent)
        self.test_agent.jump_to(1, 1)
        self.test_agent.center_in_tile()
        self.assertEqual((self.test_agent.x, self.test_agent.y), (10, 10))

    def test_agent_jump_to(self):
        """
        Check that agent.jump_to() sets the x/y coordinates as requested.
        """
        agent = self.test_agent
        self.model.add_agent(agent)

        # Simple jump
        agent.jump_to(42, 43)
        self.assertEqual((agent.x, agent.y), (42, 43))

        agent.jump_to(13, 37)
        self.assertEqual((agent.x, agent.y), (13, 37))

        # Edge cases
        agent.jump_to(0, 0)
        self.assertEqual((agent.x, agent.y), (0, 0))

        agent.jump_to(399, 399)
        self.assertEqual((agent.x, agent.y), (399, 399))

    def test_agent_jump_to_wrap(self):
        """Check that agent.jump_to() sets the x/y coordinates as requested,
        when wrapping
        """
        agent = self.test_agent
        self.model.add_agent(agent)

        # Wrapping horizontal
        agent.jump_to(400, 42)
        self.assertEqual((agent.x, agent.y), (0, 42))

        agent.jump_to(-1, 42)
        self.assertEqual((agent.x, agent.y), (399, 42))

        # Wrapping vertical
        agent.jump_to(42, 400)
        self.assertEqual((agent.x, agent.y), (42, 0))

        agent.jump_to(42, -1)
        self.assertEqual((agent.x, agent.y), (42, 399))

    def test_agent_jump_to_tile(self):
        """
        Check that jump_to_tile moves the agent correctly
        """
        agent = self.test_agent
        tile = self.model.tile(7, 13)

        # Check using current_tile
        self.model.add_agent(agent)
        agent.jump_to_tile(tile)
        self.assertEqual(agent.current_tile(), tile)

        # Check agents coordinates directly
        agent_x = 10 + tile.x / self.model.x_tiles * self.model.width
        agent_y = 10 + tile.y / self.model.y_tiles * self.model.height
        self.assertEqual((agent.x, agent.y), (agent_x, agent_y))

    def test_agent_current_tile(self):
        """
        Test that current_tile actually returns the current tile.
        """
        agent = self.test_agent
        self.model.add_agent(agent)
        agent.jump_to(25, 25)

        self.assertEqual(agent.current_tile(), self.model.tile(1, 1))

    def test_agent_direction_to(self):
        """
        Test that direction_to(x, y) correctly returns the angle
        """
        test_cases = [(0, 0, 225),
                      (400, 400, 45),
                      (200, 400, 90),
                      (200, 0, 270)]
        self.test_agent.jump_to(200, 200)
        for (x, y, expected_direction) in test_cases:
            with self.subTest(i=(x, y, expected_direction)):
                direction = self.test_agent.direction_to(x, y)
                self.assertAlmostEqual(direction, expected_direction)

    def test_agent_point_towards(self):
        """
        Test that agent.point_towards(x, y) correctly sets the agent direction
        """
        test_cases = [(0, 0, 225),
                      (400, 400, 45),
                      (200, 400, 90),
                      (200, 0, 270)]
        self.test_agent.jump_to(200, 200)
        for (x, y, expected_dir) in test_cases:
            with self.subTest(i=(x, y, expected_dir)):
                self.test_agent.point_towards(x, y)
                self.assertAlmostEqual(self.test_agent.direction, expected_dir)

    def test_agent_forward(self):
        """
        Check that forward correctly moves the agent forward
        """
        agent = self.test_agent
        test_cases = [(1, 201), (10, 210), (0.1, 200.1)]
        agent.direction = 0
        for (speed, x) in test_cases:
            with self.subTest(i=(speed, x)):
                agent.jump_to(200, 200)
                agent.speed = speed
                agent.forward()
                self.assertEqual((agent.x, agent.y), (x, 200))

    def test_agent_forward_wrap_right_edge(self):
        """
        Check that forward() correctly wraps horizontally on the right edge
        """
        agent = self.test_agent
        agent.jump_to(399, 200)
        agent.direction = 0
        agent.forward(1)
        self.assertEqual((agent.x, agent.y), (0, 200))

    def test_agent_forward_wrap_left_edge(self):
        """
        Check that forward() correctly wraps horizontally on the left edge
        """
        agent = self.test_agent
        agent.jump_to(0, 200)
        agent.direction = 180
        agent.forward(1)
        self.assertEqual((agent.x, agent.y), (399, 200))

    def test_agent_forward_wrap_bottom_edge(self):
        """
        Check that forward() correctly wraps vertically on the bottom edge
        """
        agent = self.test_agent
        agent.jump_to(0, 399)
        agent.direction = 90
        agent.forward(1)
        self.assertAlmostEqual(agent.x, 0)
        self.assertAlmostEqual(agent.y, 0)

    def test_agent_forward_wrap_top_edge(self):
        """
        Check that forward() correctly wraps vertically on the top edge
        """
        agent = self.test_agent
        agent.jump_to(0, 0)
        agent.direction = 270
        agent.forward(1)
        self.assertAlmostEqual(agent.x, 0)
        self.assertAlmostEqual(agent.y, 399)

    def test_agent_backward(self):
        """
        Check that backward() correctly moves to agent backward
        """
        agent = self.test_agent
        test_cases = [(1, 199), (10, 190), (0.1, 199.9)]
        agent.direction = 0
        for (speed, x) in test_cases:
            with self.subTest(i=(speed, x)):
                agent.jump_to(200, 200)
                agent.speed = speed
                agent.backward()
                self.assertEqual((agent.x, agent.y), (x, 200))

    def test_agent_backward_wrap_right_edge(self):
        """
        Check that backward() correctly wraps horizontally on the right edge
        """
        agent = self.test_agent
        agent.jump_to(399, 200)
        agent.direction = 180
        agent.backward(1)
        self.assertEqual((agent.x, agent.y), (0, 200))

    def test_agent_backward_wrap_left_edge(self):
        """
        Check that backward() correctly wraps horizontally on the left edge
        """
        agent = self.test_agent
        agent.jump_to(0, 200)
        agent.direction = 0
        agent.backward(1)
        self.assertEqual((agent.x, agent.y), (399, 200))

    def test_agent_backward_wrap_bottom_edge(self):
        """
        Check that backward() correctly wraps vertically on the bottom edge
        """
        agent = self.test_agent
        agent.jump_to(0, 399)
        agent.direction = 270
        agent.backward(1)
        self.assertAlmostEqual(agent.x, 0)
        self.assertAlmostEqual(agent.y, 0)

    def test_agent_backward_wrap_top_edge(self):
        """
        Check that backward() correctly wraps vertically on the top edge
        """
        agent = self.test_agent
        agent.jump_to(0, 0)
        agent.direction = 90
        agent.backward(1)
        self.assertAlmostEqual(agent.x, 0)
        self.assertAlmostEqual(agent.y, 399)

    def test_agent_left(self):
        """
        Check that left() changes the direction of the agent
        the given number of degrees
        """
        test_cases = [(45, 45), (270, 270), (360, 0), (405, 45)]
        for (turn, d) in test_cases:
            with self.subTest(i=(turn, d)):
                self.test_agent.direction = 0
                self.test_agent.left(turn)
                self.assertEqual(self.test_agent.direction, d)

    def test_agent_right(self):
        """
        Check that left() changes the direction of the agent
        the given number of degrees
        """
        test_cases = [(45, 315), (270, 90), (360, 0), (405, 315)]
        for (turn, d) in test_cases:
            with self.subTest(i=(turn, d)):
                self.test_agent.direction = 0
                self.test_agent.right(turn)
                self.assertEqual(self.test_agent.direction, d)

    def test_agent_distance_to(self):
        """
        Check that distance_to(x, y) is computed correctly
        """
        test_cases = [(200, 300, 100), (230, 160, 50), (0, 0, 282.842712475)]
        self.test_agent.jump_to(200, 200)
        for (x, y, dist) in test_cases:
            with self.subTest(i=(x, y, dist)):
                self.assertAlmostEqual(self.test_agent.distance_to(x, y), dist)

    def test_agent_agents_nearby(self):
        """
        Check that agents_nearby finds the correct number of agents
        """
        test_cases = [
            (200, 200, 100, None, 2),
            (150, 200, 50, None, 1),
            (150, 200, 50, OtherAgent, 0),
            (250, 200, 50, OtherAgent, 1),
        ]
        agent0 = self.test_agent
        agent1 = TestAgent()
        agent2 = OtherAgent()
        self.model.add_agents([agent1, agent2])
        agent1.jump_to(100, 200)
        agent2.jump_to(300, 200)

        for (x, y, range, a_type, num_agents) in test_cases:
            with self.subTest(i=(x, y, range, a_type, num_agents)):
                agent0.jump_to(x, y)
                nearby = agent0.agents_nearby(range, agent_type=a_type)
                self.assertEqual(len(nearby), num_agents)

    def test_agent_nearby_tile(self):
        """
        Check that nearby_tiles() return the correct number of tiles
        """
        # This test could probably be more sophisticated, but I'm not sure how.
        test_cases = [(-1, -1, 1, 1, 9), (-2, -2, 2, 2, 25), (-5, 2, 5, 4, 33)]
        self.test_agent.jump_to(200, 200)
        for (x1, y1, x2, y2, num_tiles) in test_cases:
            with self.subTest(i=(x1, y1, x2, y2, num_tiles)):
                nearby_tiles = self.test_agent.nearby_tiles(x1, y1, x2, y2)
                self.assertEqual(len(nearby_tiles), num_tiles)
