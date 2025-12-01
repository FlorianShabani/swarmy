import time

from swarmy.perception import Perception
import pygame
import math
import numpy as np

class ProximitySensor(Perception):
    def __init__(self, agent, environment, config):
        super().__init__(agent, environment)
        self.agent = agent
        self.environment = environment
        self.config = config

        # sensor range defined as 15% of world height
        self.range_r = 0.15 * self.config["world_height"]

        # angles relative to robot heading
        self.angles = [-40, 0, 40]  # left, center, right

        # gather objects to check walls
        self.objects = [wall[1] for wall in self.environment.get_static_rect_list()]


    def sensor(self):
        robot_x, robot_y, robot_heading = self.agent.get_position()
        rob_pos = pygame.Vector2(robot_x, robot_y)

        sensor_values = []

        for offset in self.angles:
            abs_angle = robot_heading + offset

            # compute end point of ray for visualization and collision
            end_x = robot_x + math.sin(math.radians(abs_angle)) * self.range_r
            end_y = robot_y + math.cos(math.radians(abs_angle)) * self.range_r
            end_pos = pygame.Vector2(end_x, end_y)

            # draw ray for visualization
            self.environment.add_dynamic_line_object(
                [(0, 255, 0), (robot_x, robot_y), (end_x, end_y)]
            )

            # create a helper line (like bumper sensor)
            helper_line = pygame.draw.line(
                self.agent.environment.displaySurface,
                (0, 255, 0),
                rob_pos,
                end_pos
            )

            min_dist = self.range_r
            for idx, obj in enumerate(self.objects):
                intersection = np.asarray(obj.clip(helper_line))
                #print(intersection , " for object ", obj)
                if intersection[2] > 0:
                    # distance along the ray to the collision
                    hit_point = pygame.Vector2(intersection[0], intersection[1])
                    #print("Hit ", obj)
                    dist = (hit_point - rob_pos).length()
                    if dist < min_dist:
                        min_dist = dist

            # convert to normalized sensor value
            if min_dist < self.range_r:
                sensor_values.append(1.0 - min_dist / self.range_r)
            else:
                sensor_values.append(0.0)

        # print("Sensor_value:", sensor_values)
        #time.sleep(0.1)
        return sensor_values
