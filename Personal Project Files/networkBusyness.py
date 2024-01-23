from dataReader import make_graph

"""function to determine network busyness (total number of passengers on all routes of network)"""


def network_busyness(year, month):
    # create a graph for the given year and month that is weighted and directed
    g = make_graph(year, month)
    # variable to store total number of passengers
    traffic = 0

    # iterate over every route in the graph adding up the number of passengers
    for (origin, dest) in g.edges():
        traffic += g[origin][dest]['passenger_count']

    # return total number of passengers
    return traffic
