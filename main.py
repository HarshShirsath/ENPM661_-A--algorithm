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

triangle = [(460, 25), (510, 125), (460, 225)]
triangle_with_bloat = [(455, 3.81), (515, 125), (455, 246.18)]
rectangle1_points = shapes.get_rect_points(100, 0, 50, 100)
rectangle1_points_clearance = shapes.get_rect_points(100, 0, 50, 100, step_size)
rectangle2_points = shapes.get_rect_points(100, 150, 50, 100)
rectangle2_points_clearance = shapes.get_rect_points(100, 150, 50, 100, step_size)
hexagon = shapes.get_regular_polygon_points(300, 125, 75, 6, 0, 90)
hexagon_with_clearance = shapes.get_regular_polygon_points(
    300, 125, 75, 6, step_size, 90)

def draw_obstacles():
    ## Triangle
    shapes.draw_bloated_outline(display, triangle, config.GREEN, step_size)
    shapes.draw_polygon(display, config.RED, triangle)

    ## Hexagon
    shapes.draw_bloated_outline(display, hexagon, config.GREEN, step_size)
    shapes.draw_polygon(display, config.RED, hexagon)
    
    ## Lower Rect
    shapes.draw_bloated_outline(display, rectangle1_points, config.GREEN, step_size)
    shapes.draw_rectangle(display, config.RED, 100, 0, 50, 100)
    
    ## Upper Rect
    shapes.draw_bloated_outline(display, rectangle2_points, config.GREEN, step_size)
    shapes.draw_rectangle(display, config.RED, 100, 150, 50, 100)


def draw_start_goal_orientation():
    if start_set:
        pygame.draw.circle(display, config.BLUE, start_point, step_size)
        pygame.draw.line(display, config.MAGENTA, start_point,(start_point[0] + orientation_length * math.cos(orientation),start_point[1] + orientation_length * math.sin(orientation)),2)

    if goal_set:
        pygame.draw.circle(display, config.GREEN, goal_point, 5)
        pygame.draw.circle(display, config.MAGENTA, goal_point,
                           robot_radius * goal_threshold, 1)
    

isRunning = True
while isRunning:
    for event in pygame.event.get():
        if event.type == QUIT:
            isRunning = False
            break

        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                x, y = pygame.mouse.get_pos()
                if not start_set:
                    # Snap to Grid
                    start_point = (step_size *
                                   (math.floor(x / step_size) + 0.5),
                                   step_size *
                                   (math.floor(y / step_size) + 0.5))
                    start_set = True
                elif not orientation_set:
                    orientation_set = True  
                elif not goal_set:
                    # Snap to Grid
                    goal_point = (step_size *
                                  (math.floor(x / step_size) + 0.5),
                                  step_size *
                                  (math.floor(y / step_size) + 0.5))
                    goal_set = True
            elif event.button == 3:
                start_set = False
                goal_set = False
                orientation_set = False
                a_star.astar_reset()
        if event.type == MOUSEMOTION:
            mouseX, mouseY = pygame.mouse.get_pos()
            if start_set and not orientation_set:
                orientation = math.atan2(mouseY - start_point[1],mouseX - start_point[0])

        if not isRunning:
            break

display.fill(config.BACKGROUND)
draw_obstacles()
draw_start_goal_orientation()
if start_set and goal_set and not a_star.is_initialized():
    a_star.astar_init(start_point, goal_point,orientation,world_threshold)

a_star.astar_update()
a_star.astar_backtrack()
a_star.astar_draw(display)
pygame.display.update()

pygame.quit()
sys.exit()