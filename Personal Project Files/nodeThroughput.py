from matplotlib import pyplot as plt

from dataReader import make_graph

"""calculates the total number of incoming and outgoing passengers for a given graph and node"""


def single_node_throughput(graph, node):
    # get the in and out edges for the node along with the data present in the node
    # the important one is passengers
    in_edges = graph.in_edges(nbunch=node, data=True)
    out_edges = graph.out_edges(nbunch=node, data=True)

    # variables to store passenger totals
    passengers_in = 0
    passengers_out = 0

    # iterate over in and out edges calculating total in and out passenger counts
    for i in in_edges:
        passengers_in += i[2].get('passenger_count')
    for i in out_edges:
        passengers_out += i[2].get('passenger_count')

    # return the in and out passenger counts
    return {"in": passengers_in, "out": passengers_out}


"""gets the top nodes or all nodes by total throughput for the year and month if selected"""


def top_node_throughput(year, month=None, top=None):
    # make graph for year and if specified, month
    g = make_graph(year, month)

    throughput = []

    # iterate over all nodes and get throughput, putting it in list with node id
    for i in g.nodes():
        throughput.append((i, single_node_throughput(g, i)))

    # sort by total throughput
    sorted_airport_importance = sorted(throughput, key=lambda x: x[1].get('in') + x[1].get('out'), reverse=True)

    # check if the top number of nodes are selected and return them or return everything
    if top is None:
        return sorted_airport_importance
    else:
        return sorted_airport_importance[:top]


"""
def top_node_throughput_ranking(year, month=None, top=None):
    g = make_graph(year, month)

    throughput = []

    for i in g.nodes():
        throughput.append((i, single_node_throughput(g, i)))

    sorted_airport_importance = sorted(throughput, key=lambda x: x[1].get('in') + x[1].get('out'), reverse=True)

    if top is not None:
        sorted_airport_importance = sorted_airport_importance[:top]

    selected_airport_importance = []

    for i in sorted_airport_importance:
        selected_airport_importance.append((i[0], sorted_airport_importance.index(i) + 1))

    # outputs result
    return selected_airport_importance
"""

"""get the scaled throughput ranking of all nodes in the bunch"""


def top_bunch_throughput_ranking(year, month=None, bunch=None, scale=None):
    # make the graph
    g = make_graph(year, month)

    throughput = []

    # get the node and its throughput in the list
    for i in g.nodes():
        throughput.append((i, single_node_throughput(g, i)))

    # sort by total throughput
    sorted_airport_importance = sorted(throughput, key=lambda x: x[1].get('in') + x[1].get('out'), reverse=True)

    # store rankings
    airport_ranking = []
    # r stores the current ranking
    r = 1
    # get total throughput
    v = sorted_airport_importance[0][1].get('in') + sorted_airport_importance[0][1].get('out')
    # add the nodes and its rank to the list
    airport_ranking.append([sorted_airport_importance[0][0], r])
    # iterate over every airport but the first one
    for x in sorted_airport_importance[1:]:
        # check if its total throughput value is different from others at that rank
        if x[1].get('in') + x[1].get('out') != v:
            # if it is add 1 to the rank
            r += 1
            # calculate the value at this rank
            v = x[1].get('in') + x[1].get('out')
        # add the airport and its rank
        airport_ranking.append([x[0], r])

    # if check scale is not None
    if scale is not None:
        # iterate over every airport and scale the ranking to between 1 and scale
        for i in airport_ranking:
            i[1] = round((scale - 1) * (i[1] - 1) / (r - 1) + 1, 0)

    # check if the bunch is none
    if bunch is None:
        return airport_ranking
    else:
        # if the bunch is not not find all of the nodes
        bunch_nodes = []
        found = False
        for i in bunch:
            # iterate over rankings
            for j in airport_ranking:
                # check if airport in the bunch desired
                if i in j:
                    # add the ranking of the node in the bunch to the list
                    bunch_nodes.append((i, j[1]))
                    found = True
                    break
            # if the airport from the bunch is not found append its rank as None
            if not found:
                bunch_nodes.append((i, None))
            else:
                found = False

        return bunch_nodes


if __name__ == "__main__":
    # Section 5.2 in report
    nodes = []

    # get the most important
    top_rank_2019 = top_bunch_throughput_ranking(2019, 4, None, 452)

    # get ranking of airports from 2019 in 452 scale
    rankings_2020 = top_bunch_throughput_ranking(2020, 4, [x[0] for x in top_rank_2019], 452)

    # iterate to find the same node in both lists
    for r2019 in top_rank_2019:
        for r2020 in rankings_2020:
            if r2019[0] == r2020[0]:
                # confirm the rank is not none
                if r2019[1] is not None and r2020[1] is not None:
                    # add the node and its 2019 rank to the list
                    nodes.append((r2019[0], r2019[1]))
                break

    # get only the airports with a rank above 400
    selected_airports = [airport[0] for airport in nodes if airport[1] <= 400]

    # get the ranking of 2019 nodes with rank of 400 or above in 2019
    rank2019 = top_bunch_throughput_ranking(2019, 4, selected_airports, 452)
    # get the ranking of 2019 nodes with rank of 400 or above in 2020
    rank2020 = top_bunch_throughput_ranking(2020, 4, selected_airports, 452)
    # get the ranking of 2019 nodes with rank of 400 or above in 2021
    rank2021 = top_bunch_throughput_ranking(2021, 4, selected_airports, 452)
    # get the ranking of 2019 nodes with rank of 400 or above in 2022
    rank2022 = top_bunch_throughput_ranking(2022, 4, selected_airports, 452)
    # get the ranking of 2019 nodes with rank of 400 or above in 2023
    rank2023 = top_bunch_throughput_ranking(2023, 4, selected_airports, 452)

    # make each rank list a line
    y_axis_2019 = [x[1] for x in rank2019]
    y_axis_2020 = [x[1] for x in rank2020]
    y_axis_2021 = [x[1] for x in rank2021]
    y_axis_2022 = [x[1] for x in rank2022]
    y_axis_2023 = [x[1] for x in rank2023]

    ax = plt.subplot()
    # plot the lines
    ax.plot(y_axis_2019, label=2019)
    ax.plot(y_axis_2020, label=2020)
    ax.plot(y_axis_2021, label=2021)
    ax.plot(y_axis_2022, label=2022)
    ax.plot(y_axis_2023, label=2023)
    # set the size of the ticks
    ax.tick_params(axis='y', which='major', labelsize=18)
    # make no x-axis ticks
    plt.gca().xaxis.set_ticklabels([])
    # plt.axhline(y=50, color="black", linestyle='-')
    # set the title
    plt.title("Busyness rankings of airports with a April 2019 ranking of 400 or above", fontsize=24)
    # set x axis label
    plt.xlabel("April 2019 Airports", fontsize=22)
    # set y label
    plt.ylabel("April Busyness Ranking", fontsize=22)
    # set legend size
    plt.legend(fontsize=18)
    plt.show()
