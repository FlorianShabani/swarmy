# =============================================================================
# created by:   Samer Al-Magazachi
# created on:   18/02/2021 -- 13/04/2022
# modified by: Eduard Buss  (17.03.2023)
# version:      0.9
# status:       prototype
# =============================================================================
"""
Description:
In this module one specific experiment can be executed.
The module initilizes pygame.
The parameters for the simulation are:
    - simulation speed
    - maximum agent speed
    - number of obstacles
"""

# =============================================================================
# Imports
# =============================================================================
import pygame
import random
import sys
sys.path.insert(0, '..')  # add parent directory to path
# import internal object classes
#from .environment import Environment
#from world.my_world import my_environment
##from .item import Obstacle
##from .agent import Agent

# =============================================================================
# Class
# =============================================================================
class Experiment():
    
    def __init__(self, config, agent_controller, agent_sensing, world, agent):
        super(Experiment, self).__init__()

        self.config = config
        self.agent_controller = agent_controller
        self.agent_sensing = agent_sensing
        self.world = world(config)
        self.agent = agent
        



        
    def run(self, rendering):
        """
        Start swarm simulation expermiment
        
        Args:
            rendering               (int):   1 = show simulation; -1 = hide simulation; 0 = black screen (capture mode)           
        """
        # pygame presets
        pygame.init() 					        # initialize pygame
            
        # -----------------------------------------------------------------------------
        # instantiations

        # instantiate environment
        environment = self.world
        environment.render_init()

        # instantiate agents
        agent_list = self.initialize_agents(environment)
        # initializations
        if agent_list:
            agent_list[0].body.helperLUT()    # global lookup table needs to be calculated only once
        # -----------------------------------------------------------------------------
        self.run_experiment(environment, rendering, agent_list, self.config['max_timestep'])

        for i in range(self.config['generations']):
            scores = self.evaluate(agent_list)
            self.run_experiment(environment, rendering, agent_list, self.config['max_timestep'])
            # agent_list = self.crossover(scores, agent_list)

        

        if self.config['save_trajectory']:
            for i,agent in enumerate(agent_list):
                if i == len(agent_list)-1:
                    agent.save_information(True)
                else:
                    agent.save_information(False)


        print('Experiment finished by manual stopping or maximum timesteps reached. Check config.yaml to increase the maximum timesteps.')
        pygame.quit()
        return None
        
    
    def run_experiment(self, environment, rendering, agentList, iterations = 100):
        timesteps_counter = 0

        # =============================================================================
        # Run experiment: Loop-Processing
        # =============================================================================
        while timesteps_counter < iterations:
            timesteps_counter += 1

            
            #-----------------------------------------------------------------------------
            # ASYNCHRON 
            
            # get the set of keys pressed and check for user input
            pressedKeys = pygame.key.get_pressed()
                       
            #-----------------------------------------------------------------------------
            # SYNCHRON         
            for agent in agentList:
                environment.agent_object_list.append(
                    pygame.Rect(agent.actuation.position[0] - 15, agent.actuation.position[1] - 15, 30, 30))
            for newAgent in agentList:
                newAgent.processing.perform(pressedKeys)

            if(rendering == 1):
                for newAgent in agentList:
                    newAgent.body.render()         # update agent bod
                environment.render()           # update content on display

            environment.agent_object_list = []

    def initialize_agents(self, environment):
        # instatiate agent
        agentList = []
        controller_counter = 0
        for agent_counter in range(self.config['number_of_agents']):
            if agent_counter/self.config['number_of_agents'] >= self.config['controller_1']:
                controller_counter = 1

            newAgent = self.agent(environment, self.agent_controller[controller_counter],self.agent_sensing, self.config, agent_counter)
            agentList.append(newAgent)
        return agentList

    def evaluate(self, agentList):
        scores = []
        grid_size = 0.01 * min(self.config['world_width'], self.config['world_height'])
        
        for agent in agentList:
            visited_cells = set()
            for x, y in agent.trajectory:
                grid_x = int(x // grid_size)
                grid_y = int(y // grid_size)
                visited_cells.add((grid_x, grid_y))
            scores.append(len(visited_cells))
        
        return scores
    
    def crossover(self, scores, agent_list):
        # Only 1 agent for now
        return agent_list