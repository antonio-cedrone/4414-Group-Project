import operator

import networkx as nx

from dataReader import make_graph

"""determines the node importance by way of degree centrality for all the nodes in the given year at each month
considering total centrality as well as in and out degree centrality"""


def node_importance(year, month=None, top=None):
    # generates a graph based on the flight data and does not include weight because it will not be used
    g = make_graph(year, month)

    # creates a dictionary with the degree centrality
    airport_importance = nx.degree_centrality(g)  # will consider both in and out degrees
    # airport_importance_in = nx.in_degree_centrality(g)  # will consider only in degree
    # airport_importance_out = nx.out_degree_centrality(g)  # will consider only out degree

    if top is None:
        # sort and outputs result
        print("Importance by degree:")
        s = sorted(airport_importance.items(), key=operator.itemgetter(1), reverse=True)
        print(s)
    else:
        # sort and outputs result
        print("Importance by degree of top ", top, "nodes:")
        s = sorted(airport_importance.items(), key=operator.itemgetter(1), reverse=True)[:top]
        print(s)

    # print("Importance by in degree:")
    # print(sorted(airport_importance_in.items(), key=operator.itemgetter(1), reverse=True))

    # print("Importance by out degree:")
    # print(sorted(airport_importance_out.items(), key=operator.itemgetter(1), reverse=True))


if __name__ == "__main__":
    # Section 5.4 in report
    # get 10 most important airports by degree centrality before, during and after April 2020
    node_importance(2019, 4, 10)
    node_importance(2020, 4, 10)
    node_importance(2020, 5, 10)
    node_importance(2021, 4, 10)
    node_importance(2022, 4, 10)
