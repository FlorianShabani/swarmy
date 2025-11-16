import random
from swarmy.actuation import Actuation

class MyController(Actuation):

    def __init__(self, agent, config):
        super().__init__(agent)
        self.config = config
        self.init_pos = True            # flag to set initial position of the robot

        self.linear_velocity = 1.0      # default forward speed
        self.angle_velocity = 15       # default turn speed (degrees per step)


    def controller(self):
        # Set initial robot position
        if self.init_pos:
            self.agent.initial_position()
            self.init_pos = False

        sensor_values = self.agent.get_perception()
        left, center, right = sensor_values[1]

        if min(left, center, right) > 0.5:
            self.turn_left(self.angle_velocity)
            return
        elif center > 0.4:
            if left < right:
                self.turn_left(self.angle_velocity)
            elif right > left:
                self.turn_right(self.angle_velocity)
            else:
                if random.choice([True, False]):
                    self.turn_left(self.angle_velocity)
                else:
                    self.turn_right(self.angle_velocity)
            self.stepForward(self.linear_velocity/2)

        elif left > 0.2:
            # obstacle on the left - turn right
            self.turn_left(self.angle_velocity)
            self.stepForward(self.linear_velocity/2)
        elif right > 0.2:
            # obstacle on the right - turn left
            self.turn_right(self.angle_velocity)
            self.stepForward(self.linear_velocity/2)
        else:
            # path clear - small random jitter to explore
            jitter = random.choice([-1, 0, 1])
            if jitter == -1:
                self.turn_left(int(1))
            elif jitter == 1:
                self.turn_right(int(1))
            # always step forward
            self.stepForward(self.linear_velocity)

        # handle torus wrapping
        self.torus()


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
