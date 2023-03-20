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

def draw_bloated_outline(window,polygon,color, width):
    pointCount = len(polygon)
    for i in range(pointCount):
        drawY = config.HEIGHT - polygon[i][1]
        pygame.draw.circle(window, color, (polygon[i][0],drawY),width)
        edgeX = polygon[(i+1)%pointCount][0] - polygon[i][0]
        edgeY = polygon[(i+1)%pointCount][1] - polygon[i][1]
        cross = normalized(cross_prod((edgeX,edgeY,0),(0,0,1)),width*0.5)
        newPoint1 = (polygon[i][0] + cross[0], drawY - cross[1])
        newPoint2 = (polygon[(i+1)%pointCount][0] + cross[0], config.HEIGHT - (polygon[(i+1)%pointCount][1] + cross[1]) ) 
        pygame.draw.line(window,color,newPoint1,newPoint2,width)

###### INTERSECTION #######
# a: Vector3D
# b: Vector3D
# returns the cross product vector of the a and b
def cross_prod(a, b):
    result = [
        a[1] * b[2] - a[2] * b[1], 
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0]
    ]
    return result
    
def normalized(a,newLength = 1):
    length = math.sqrt(a[0]**2 + a[1]**2 + a[2]**2)
    if(length == 0):
        return (0,0,0)

    return (newLength * a[0]/length, newLength * a[1]/length, newLength * a[2]/length)
    
def get_sign(val):
    if (val == 0):
        return 0
        
    return val / math.fabs(val)

def is_inside(point, polygon):
    sign = 0
    for i in range(len(polygon)):
        pX = point[0] - polygon[i][0]
        pY = point[1] - polygon[i][1]

        edgeX = polygon[(i + 1) % len(polygon)][0] - polygon[i][0]
        edgeY = polygon[(i + 1) % len(polygon)][1] - polygon[i][1]
        crossProd = cross_prod((edgeX, edgeY, 0), (pX, pY, 0))
        newSign = get_sign(crossProd[2]) #z coordinate
        if (sign == 0):
            sign = newSign
        if (newSign != 0 and newSign != sign):
            return False
    return True

