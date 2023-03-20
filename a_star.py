from enum import Enum
import math
import config
import pygame


class State(Enum):
    NONE = 0
    INIT = 1
    UPDATE = 2
    BACKTRACK = 3
    FAILED = 4


class Node:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.visited = False
        self.g_cost = math.inf
        self.f_cost = math.inf
        self.color = config.GRAY
        self.cameFrom = None

    def __str__(self):
        return f"x:{self.x}, y:{self.y}, angle:{self.angle}, visited:{self.visited}, [g:{self.g_cost}, f:{self.f_cost}]\n"


currentState = State.NONE

open_list: Node = []
closed_list:Node = []

astar_start = (0, 0)
astar_goal = (0, 0)
astar_threshold = 1

nodes: Node = []


def astar_reset():
    global currentState
    global open_list
    global closed_list
    global nodes
    currentState = State.NONE
    open_list = []
    closed_list = []
    nodes = []


def is_initialized():
    global currentState
    return currentState.value > State.NONE.value


def world_to_region(x, y):
    global astar_threshold
    gridX = math.floor(x / astar_threshold)
    gridY = math.floor(y / astar_threshold)
    return (gridX, gridY)


def region_to_world(x, y):
    global astar_threshold
    worldX = x * astar_threshold
    worldY = y * astar_threshold
    return (worldX, worldY)


def astar_init(start_point, goal_point, orientation, threshold=1):
    global currentState
    global astar_start
    global astar_goal
    global astar_threshold
    global nodes

    if (currentState != State.NONE):
        print("Reset the astar algorithm before initializing. Aborting")
        return
    print("AStar Initialized")
    astar_start = start_point
    astar_goal = goal_point
    # initial world
    astar_threshold = threshold
    cols = math.ceil(config.WIDTH / threshold)
    rows = math.ceil(config.HEIGHT / threshold)
    for y in range(rows):
        nodes.append([])
        for x in range(cols):
            nodes[y].append(Node(x, y))

    # Set the start node and add it to open list and what not.
    idxX, idxY = world_to_region(start_point[0], start_point[1])
    print((idxX,idxY))
    print(orientation)
    nodes[idxY][idxX].angle = orientation
    nodes[idxY][idxX].g_cost = 0
    nodes[idxY][idxX].f_cost = heuristic(nodes[idxY][idxX])
    open_list.append(nodes[idxY][idxX])
    currentState = State.UPDATE


def astar_update(next_move):
    global currentState
    global open_list
    global closed_list
    if not next_move:
        return

    if (currentState != State.UPDATE):
        return

    if len(open_list) == 0:
        currentState = State.FAILED
        print("No Path Exists")
        return

    currIndex = 0
    for i in range(len(open_list)):
        if (open_list[i].f_cost < open_list[currIndex].f_cost):
            currIndex = i
    current = open_list[currIndex]
    if (current.x == astar_goal[0] and current.y == astar_goal[1]):
        currentState = State.BACKTRACK
        print("Path Found. Backtracking")
        return

    del open_list[currIndex]

    nodes[current.y][current.x].visited = True
    closed_list.append(current)
    explore_nodes(current, config.STEP_SIZE)


def astar_backtrack():
    global currentState
    if (currentState != State.BACKTRACK):
        return

    # Now we either have a path that needs to be backtracked to the start. Or the algorithm has exited in unfavorable conditions.
    # YOUR CODE HERE


def heuristic(node):
    global astar_goal
    dX = astar_goal[0] - node.x
    dY = astar_goal[1] - node.y

    # because all the distances would be in squares, it wouldn't matter
    return dX**2 + dY**2


def explore_nodes(node: Node, step_size):
    global nodes
    
    nodeX, nodeY = region_to_world(node.x, node.y)
    print(f"processing neighbors of x:{node.x}, y:{node.y}, angle:{node.angle}")

    new_x = nodeX + step_size 
    new_y = nodeY + step_size 
    for k in range(-2, 2):
        print(f"neighbors at angle {k * 30} is x:{new_x}, y:{new_y}")
        edge_cost = math.fabs(k)

    tentative_g_cost = node.g_cost + edge_cost
    neighborX, neighborY = world_to_region(new_x, new_y)
    if (neighborX > config.WIDTH or neighborX < 0) or (neighborY > config.HEIGHT or neighborY < 0):
    
            
        neighbor = nodes[neighborY][neighborX]
        if (tentative_g_cost < neighbor.g_cost):
            nodes[neighborY][neighborX].cameFrom = node
            # nodes[neighborY][neighborX].angle = new_angle
            nodes[neighborY][neighborX].g_cost = tentative_g_cost
            nodes[neighborY][neighborX].f_cost = tentative_g_cost + heuristic(
                nodes[neighborY][neighborX])
            node_known = False
            for i in range(len(open_list)):
                if open_list[i].x == neighborX \
                    and open_list[i].y == neighborY:
                    node_known = True
            if not node_known:
                open_list.append(neighbor)


def astar_draw(window):
    global closed_list
    global open_list

    for i in range(len(open_list)):
        astar_draw_node(window, open_list[i])
    for i in range(len(closed_list)):
        astar_draw_node(window, closed_list[i])


def astar_draw_node(window, node: Node):
    node_color = config.YELLOW
    if (node.visited):
        node_color = config.GRAY
    nodeX, nodeY = region_to_world(node.x, node.y)
    if (node.cameFrom != None):
        cameFromX, cameFromY = region_to_world(node.cameFrom.x,
                                               node.cameFrom.y)

        #print(f"Drawing node: {node} that came from {node.cameFrom}")
        pygame.draw.line(window, node_color,
                         (cameFromX, config.HEIGHT - cameFromY),
                         #(nodeX + dirX, config.HEIGHT - (nodeY + dirY)),
                         (nodeX, config.HEIGHT - nodeY))

    
    #pygame.draw.circle(window, node_color, (nodeX, config.HEIGHT - nodeY), 3)


