import time
import math
import numpy as np
import pygame
from swarmy.perception import Perception

class ProximitySensor(Perception):
    def __init__(self, agent, environment, config):
        super().__init__(agent, environment)
        self.agent = agent
        self.environment = environment
        self.config = config
        self.timer = time.time()

        # sensor range defined as 15% of world height
        self.range_r = 0.15 * self.config["world_height"]

        # angles relative to robot heading: left, center, right
        self.angles = [-40, 0, 40]

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

            # create a helper line (ray)
            helper_line = pygame.draw.line(
                self.agent.environment.displaySurface,
                (0, 255, 0),
                rob_pos,
                end_pos
            )

            # gather objects to check walls
            objects = [wall[1] for wall in self.environment.get_static_rect_list()]

            min_dist = self.range_r
            for obj in objects:
                intersection = np.asarray(obj.clip(helper_line))
                if intersection[2] > 0: # Check if intersection occurred
                    # distance along the ray to the collision
                    hit_point = pygame.Vector2(intersection[0], intersection[1])
                    dist = (hit_point - rob_pos).length()
                    if dist < min_dist:
                        min_dist = dist

            # convert to normalized sensor value (1.0 = closest, 0.0 = furthest)
            if min_dist < self.range_r:
                sensor_values.append(1.0 - min_dist / self.range_r)
            else:
                sensor_values.append(0.0)
        if self.timer < time.time():
            print("Sensor: ", sensor_values)
            self.timer = time.time() + 1

        # Returns [sl, sm, sr]
        return sensor_values