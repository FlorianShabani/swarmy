import numpy as np
import pygame
from swarmy.perception import Perception


class LightSensor(Perception):
    def __init__(self, agent, environment, config, position):
        super().__init__(agent,environment)
        self.agent = agent
        self.environment = environment
        self.config = config
        # The position of the sensor relative to the agent
        self.position = position
    def sensor(self):
        robot_position_x, robot_position_y, robot_heading = self.agent.get_position()
        heading_rad = np.radians(-robot_heading)
        cos_h, sin_h = np.cos(heading_rad), np.sin(heading_rad)
        rotated_x = self.position[0] * cos_h - self.position[1] * sin_h
        rotated_y = self.position[0] * sin_h + self.position[1] * cos_h
        sensor_position = [robot_position_x + rotated_x, robot_position_y + rotated_y]
        light_intensity = self.environment.get_light_intensity(sensor_position)
        # print("Light intensity:", light_intensity)
        self.environment.add_dynamic_circle_object([(255, 255, 150), sensor_position, 3, 3])
        return light_intensity
