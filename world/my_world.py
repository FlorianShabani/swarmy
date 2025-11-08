from swarmy.environment import Environment
import pygame
import numpy as np

class My_environment(Environment):
    def __init__(self, config):
        self.config = config
        super().__init__(config)

        self.light_dist = self.defineLight()

    def add_static_rectangle_object(self):
        """
        Add static rectangle object to the environment such as walls or obstacles.
        Example:
            self.staticRectList.append(color, pygame.Rect(x, y, width, height), border_width))
        Returns:
        """
        # self.staticRectList.append(['BLACK', pygame.Rect(5, 5, self.config['world_width'] - 10, 5),5])
        # self.staticRectList.append(['BLACK', pygame.Rect(5, 5, 5, self.config['world_height']-10), 5])
        # self.staticRectList.append(['BLACK', pygame.Rect(5, self.config['world_height']-10, self.config['world_width'] - 10,5), 5])
        # self.staticRectList.append(['BLACK', pygame.Rect(self.config['world_width'] - 10, 5, 5, self.config['world_height']-10), 5])


    def add_static_circle_object(self):
        """
        Add static circle object to the environment such as sources or sinks.
        Example:
            self.staticCircList.append([color, position, border_width, radius])
        Returns:
        """
        pass



    def set_background_color(self):
        """
        Set the background color of the environment.
        """
        self.displaySurface.fill(self.BACKGROUND_COLOR)
        light_surface = pygame.surfarray.make_surface(self.light_dist)
        self.displaySurface.blit(light_surface, (0, 0))

    ###  LIGHT DISTRIBUTION ###

    def defineLight(self):
        """
        Define the light distribution of the environment.
        Returns: 3 dimensional light distribution tuple (x,y,light_intensity)
        """
        center = np.array([self.width/2, self.height/2])
        max_dist = np.sqrt(self.width**2 + self.height**2) / 2
        light_dist = np.zeros((self.width, self.height, 3))
        
        for i in range(self.width):
            for j in range(self.height):
                p = np.array([i, j])
                dist = np.linalg.norm(center - p)
                intensity = max(0, 255 * (1 - dist / max_dist))
                light_dist[i][j][0] = int(intensity)
                light_dist[i][j][1] = int(intensity)
                light_dist[i][j][2] = int(intensity)
        return light_dist
    
    def get_light_intensity(self, position):
        """
        Get the light intensity at a given position.
        Returns: light intensity
        """
        x, y = position
        return self.light_dist[min(int(x), self.config["world_width"] - 1)][min(int(y), self.config["world_height"] - 1)][0]

