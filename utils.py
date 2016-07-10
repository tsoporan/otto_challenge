""" Helpers for setting up the map """

def get_waypoints(inputs):
    """ Builds and returns the mapping of waypoint -> {coord, penalty}

    Args:
        inputs(list)    : A list containing string inputs, ex.  ['50 50 10', ...]

    Returns:
        dict            : The mapping
    """

    if not inputs: return {}

    waypoints = {}

    # Attach start
    waypoints[0] = { 'coord': (0, 0), 'penalty': 0 }

    for i,d in enumerate(inputs):
        x, y, penalty = map(lambda x : int(x), d.split(' '))
        waypoints[i+1] = { 'coord': (x, y), 'penalty': penalty }

    # Attach end
    waypoints[len(waypoints)] = { 'coord': (100, 100), 'penalty': 0 }

    return waypoints

def get_pathmap(num_points):
    """ Builds and returns the mapping which will hold current_cost and current_path in the format
        waypoint -> { current_cost, current_path }

    Args:
        num_points(int)     : Number of points on the map

    Returns:
        dict                : The mapping, initially point -> None
    """

    pathmap = {}

    end = num_points + 1

    for i in range(0, end):
        pathmap[i] = None

    # Attach end
    pathmap[end] = None

    return pathmap

def init_map(start, waypoints, pathmap, neighborsfunc, costfunc):
    """ Initializes the path map at the start position

    Args:
        start(int)              : Initialize at this point, default will be 0
        waypoints(dict)         : Mapping of waypoints
        pathmap(dict)           : Mapping of path
        neighborsfunc(function) : The function used to calculate neighbors
        costfunc(function)      : The function used to calculate cost
    """

    # Init the map for the start position
    for neighbor in neighborsfunc(start, waypoints):
        neighbor_cost = costfunc(start, neighbor, waypoints)
        pathmap[neighbor] = {'path': [start, neighbor], 'cost': neighbor_cost}
