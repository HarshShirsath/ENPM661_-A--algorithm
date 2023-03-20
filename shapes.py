import config
import math
import pygame
from pygame.locals import Rect


####### DRAWING #########
def draw_rectangle(window, color, x, y, width, height, boundary = 0):
    pygame.draw.rect(
        window, color,
        pygame.Rect(x - boundary, config.HEIGHT - (y + height + boundary), width +  2 * boundary, height + 2 * boundary))

def draw_polygon(window, color, points):
    newPoints = []
    for i in range(len(points)):
        newPoints.append((points[i][0], config.HEIGHT - points[i][1]))
    pygame.draw.polygon(window, color, newPoints)


####### POLYGONS #######
def get_rect_points(x, y, width, height, boundary):
    return [
        (x - boundary, y - boundary), 
        (x + width + boundary, y - boundary), 
        (x + width + boundary, y + height + boundary), 
        (x - boundary, y + height + boundary)]

def get_regular_polygon_points(x, y, length, sides, boundary, angle_offset):
    if (sides < 2):
        print("can't draw a regular polygon with less than 2 sides")
        return []
    internal_angle = 2 * math.pi / sides
    circle_radius = 0.5 * length / math.sin(internal_angle * 0.5) + boundary / math.cos(internal_angle * 0.5)
    points = []
    for i in range(sides):
        pX = x + circle_radius * math.cos(i * internal_angle +
                                          math.radians(angle_offset))
        pY = y + circle_radius * math.sin(i * internal_angle +
                                          math.radians(angle_offset))
        points.append((pX, pY))

    return points
