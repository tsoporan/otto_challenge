"""
Otto Challenge
==============

Given a 100x100m grid, and a set of waypoints along the grid, we
want to find the quickest path from (0,0) to (100,100).

Waypoints may be skipped but incur a penalty, otherwise waypoints
should be followed in order, that is you can go 1 -> 2 but not 2 -> 1.

Each waypoint also incurs a waiting time of 10 seconds.
"""

from utils import get_waypoints, get_pathmap, init_map

import math

INPUTS_FILE = 'inputs.txt' # TODO: would be nice to get this from command line
ROBOT_SPEED = 2 # Speed at which robot travels, m/s
ROBOT_WAIT_TIME = 10 # Time robot waits to load at waypoint

def cost(a, b, all_points):
    """ Return the cost between two points, this takes into account penalties and wait times

    Args:
        a (int)             : Start point
        b (int)             : End point
        all_points (dict)   : The mapping of all waypoints to coords and penalties

    Returns:
        float               : Total cost
    """

    total_cost = 0

    pointA = all_points[a]
    pointB = all_points[b]

    x1 = pointA['coord'][0]
    x2 = pointB['coord'][0]
    y1 = pointA['coord'][1]
    y2 = pointB['coord'][1]

    # Travel time
    total_cost += math.hypot(x2 - x1, y2 - y1) / ROBOT_SPEED

    # Penalties incurred for skipping
    for i in range(a+1, b):
        total_cost += all_points[i]['penalty']

    # Add waiting time
    total_cost += ROBOT_WAIT_TIME

    return total_cost

def get_neighbors(point, all_points):
    """ Get all neighbors for this waypoint

    Args:
        point (int)         : The point to find the neighbors of
        all_points (dict)   : The mapping of all waypoints to coords and penalties

    Returns:
        list                : List of all points greater than (point)
    """

    return filter(lambda x: x > point, all_points.keys())


def find_best_time(pathmap, waypoints):
    """ Find the best time between waypoints on the map

    Args:
        pathmap (dict)      : Mapping of waypoint to current path and current cost
        waypoints (dict)    : Mapping of all waypoints to coords and penalties

    Returns:
        float:              : Best time found in seconds, rounded to three decimals
    """

    end = pathmap.keys()[-1]

    for waypoint in range(1, len(waypoints.keys()) - 1):

        source_path = pathmap[waypoint]['path']
        source_cost = pathmap[waypoint]['cost']

        for neighbor in get_neighbors(waypoint, waypoints):

            neighbor_cost = cost(waypoint, neighbor, waypoints)

            # Compare cost and keep only the cheapest
            if source_cost + neighbor_cost < pathmap[neighbor]['cost']:
                pathmap[neighbor]['cost'] = source_cost + neighbor_cost
                pathmap[neighbor]['path'] = source_path + [neighbor]

    best_time = pathmap[end]['cost']

    return round(best_time, 3)


if __name__ == '__main__':
    """ Read in the sample inputs and setup the data """

    inputs = open(INPUTS_FILE).readlines()
    testcases = int(inputs.pop(0))

    while testcases != 0:

        data = inputs[:testcases]

        waypoints = get_waypoints(data)
        pathmap = get_pathmap(testcases)
        init_map(0, waypoints, pathmap, get_neighbors, cost)

        best_time = find_best_time(pathmap, waypoints)

        print("Best time is: %s" % best_time)

        # Move to next input
        inputs = inputs[testcases:]
        testcases = int(inputs.pop(0))
