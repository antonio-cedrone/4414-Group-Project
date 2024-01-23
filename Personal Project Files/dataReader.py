import pandas as pd
import networkx as nx

"""function to read the data file for a particular year and
produce the corresponding networkx graph for a particular month's data within the year """


def make_graph(year, month=None):
    # create file path for data file
    file = 'Data Files/Data' + str(year) + '.csv'

    # read the data csv file
    routes = pd.read_csv(file, header=0)

    # get only the routes for the particular month, that do not go from an airport back to itself,
    # and that have passengers
    if month is not None:
        routes_month = routes[
            (routes['MONTH'] == month) &
            (routes['ORIGIN_AIRPORT_ID'] != routes['DEST_AIRPORT_ID']) &
            (routes['PASSENGERS'] != 0)
            ]
    else:
        routes_month = routes[
            (routes['ORIGIN_AIRPORT_ID'] != routes['DEST_AIRPORT_ID']) &
            (routes['PASSENGERS'] != 0)
            ]

    # get the airport id values only from airport month
    edges = routes_month[['ORIGIN_AIRPORT_ID', 'DEST_AIRPORT_ID']].values

    # create a directed graph
    g = nx.DiGraph()

    # get all nodes that exist within the graph (even those that only have excluded edges)
    # from both the origin and destination airports and set code to the 3 digit code for the airport
    for airport_id, airport_code in routes[['ORIGIN_AIRPORT_ID', 'ORIGIN']].values:
        g.add_node(airport_id, code=airport_code)
    for airport_id, airport_code in routes[['DEST_AIRPORT_ID', 'DEST']].values:
        g.add_node(airport_id, code=airport_code)
    # add the edges to the graph
    g.add_edges_from(edges)

    # dictionary to store edge weight values
    edge_weights = {}

    # iterate over route data
    for route in routes_month.itertuples():
        # get the origin, destination, and number of passengers for the route
        origin = route.ORIGIN_AIRPORT_ID
        dest = route.DEST_AIRPORT_ID
        passengers = route.PASSENGERS

        # check if the route already exists in the edge_weights dictionary
        if (origin, dest) in edge_weights:
            # add value of passengers from this route to existing edge weight
            # this is the case when multiple airlines have the same route between airports
            edge_weights[(origin, dest)] += passengers
        else:
            # add entry for new route with passenger count
            edge_weights[(origin, dest)] = passengers

    # Update edges with passenger count as weight
    for (origin, dest) in g.edges():
        g[origin][dest]['passenger_count'] = edge_weights[(origin, dest)]

    return g
