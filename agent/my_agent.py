from swarmy.agent import Agent
import random
import pygame
from datetime import datetime

class MyAgent(Agent):
    def __init__(self,environment,controller, sensor, config, unique_id):
        self.environment = environment
        self.trajectory = []
        super().__init__(environment,controller, sensor, config, unique_id)
        

    def set_position(self, x: float, y: float, gamma: float):
        self.trajectory.append((x, y))
        return super().set_position(x, y, gamma)

    def initial_position(self):
        """
        Define the initial position of the agent.
        Hint:
        Use x,y,gamma = self.set_position(x-position, y-position, heading) to set the position of the agent.
        """
        # x = random.randint(0, self.config['world_width'])
        # y = random.randint(0, self.config['world_height'])

        # gamma = random.randint(0, 360)
        x = self.config['world_width'] / 10
        y = self.config['world_height'] / 10
        gamma = 0
        self.set_position(x, y, gamma)


    def save_information(self, last_robot):
        """
        Save information of the agent, e.g. trajectory or the environmental plot.
        Hint:
        - Use pygame.draw.lines() to draw the trajectory of the robot and access the surface of the environment with self.environment.displaySurface
        - pygame allows to save an image of the current environment
        """
        #print(self.trajectory)
        for i in range(len(self.trajectory) - 1):
            progress = i / max(1, len(self.trajectory) - 2)
            color = (int(255 * progress), 0, int(255 * (1 - progress)))
            pygame.draw.circle(self.environment.displaySurface, color, self.trajectory[i], 1)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        pygame.image.save(self.environment.displaySurface, f"plots/screenshot_{timestamp}.png")






