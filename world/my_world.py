from swarmy.environment import Environment
import pygame
import numpy as np


class My_environment(Environment):
    def __init__(self, config):
        self.config = config
        super().__init__(config)
        self.light_dist = self.defineLight()

        # Grid size for visualization (10 pixels for a clear grid display)
        self.GRID_CELL_SIZE = 10

    def add_static_rectangle_object(self):
        """
        Add static rectangle object to the environment such as walls or obstacles.
        """
        world_w = self.config['world_width']
        world_h = self.config['world_height']

        # Outer Walls
        self.staticRectList.append(['BLACK', pygame.Rect(5, 5, world_w - 10, 5), 5])
        self.staticRectList.append(['BLACK', pygame.Rect(5, 5, 5, world_h - 10), 5])
        self.staticRectList.append(['BLACK', pygame.Rect(5, world_h - 10, world_w - 10, 5), 5])
        self.staticRectList.append(['BLACK', pygame.Rect(world_w - 10, 5, 5, world_h - 10), 5])

        # Inner Obstacles (Labyrinth elements)
        self.staticRectList.append(['BLACK', pygame.Rect(world_w // 2 - 2, world_h // 8, 4, int(0.75 * world_h)), 4])
        self.staticRectList.append(['BLACK', pygame.Rect(world_w // 4, world_h // 4 - 2, world_w // 4, 4), 4])
        self.staticRectList.append(['BLACK', pygame.Rect(world_w // 2, int(0.75 * world_h) - 2, world_w // 4, 4), 4])

    def add_static_circle_object(self):
        """
        Add static circle object to the environment.
        """
        pass


    def set_background_color(self):
        """
        Set the background color of the environment and draw the grid.
        """
        self.displaySurface.fill(self.BACKGROUND_COLOR)
        # light_surface = pygame.surfarray.make_surface(self.light_dist)
        # self.displaySurface.blit(light_surface, (0, 0))

    def defineLight(self):
        """
        Define the light distribution of the environment (unchanged).
        """
        center = np.array([self.width / 2, self.height / 2])
        max_dist = np.sqrt(self.width ** 2 + self.height ** 2) / 2
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
        """
        x, y = position
        return \
        self.light_dist[min(int(x), self.config["world_width"] - 1)][min(int(y), self.config["world_height"] - 1)][0]