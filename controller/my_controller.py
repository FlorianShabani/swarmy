import random
from swarmy.actuation import Actuation

class MyController(Actuation):

    def __init__(self, agent, config):
        super().__init__(agent)
        self.config = config

        self.linear_velocity = 1.0      # default forward speed
        self.angle_velocity = 15       # default turn speed (degrees per step)
        self.genome = [random.random() for _ in range(6)]
        print(self.genome)

    def controller(self):
    
        sensor_values = self.agent.get_perception()
        left, center, right = sensor_values[1]
            
        v_l = self.genome[0] * left + self.genome[1]
        v_r = self.genome[2] * center + self.genome[3] + self.genome[4] * right + self.genome[5]
        self.turn_right(int((v_r - v_l)))

        if (sensor_values[2] == 0):
            self.stepForward(1)
            
    def mutate(self):
        for i in range(len(self.genome)):
            if random.random() < self.config['mutation_rate']:
                self.genome[i] += random.random() * self.config['mutation_strength']

        print(self.genome)

    def torus(self):
        robot_x, robot_y, robot_heading = self.agent.get_position()

        if robot_x > self.config['world_width']:
            robot_x = 0
        elif robot_x < 0:
            robot_x = self.config['world_width']

        if robot_y > self.config['world_height']:
            robot_y = 0
        elif robot_y < 0:
            robot_y = self.config['world_height']

        self.agent.set_position(robot_x, robot_y, robot_heading)
