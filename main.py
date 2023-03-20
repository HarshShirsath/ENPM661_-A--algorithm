import pygame, sys
from pygame.locals import QUIT, MOUSEBUTTONDOWN
import shapes
import config
import math
import a_star

########## HELPERS #############

pygame.init()
display = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
pygame.display.set_caption("AStar")

start_point = ()
start_set = False

orientation = 0
orientation_set = False

goal_point = ()
goal_set = False


step_size = 5

world_threshold = 0.5
robot_radius = 5
goal_threshold = 1.5