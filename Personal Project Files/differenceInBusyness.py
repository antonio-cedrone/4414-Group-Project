from dataReader import make_graph

"""calculates total throughput (incoming and outgoing passengers) for a node in the graph"""


def total_node_throughput(graph, node):
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
    return passengers_in + passengers_out


"""calculates the differences in total node throughput between the start month and end month"""


def busyness_difference(start_year, start_month, end_year, end_month):
    # obtain the start and end graphs used to determine the difference in busyness between these times
    start_graph = make_graph(start_year, start_month)
    end_graph = make_graph(end_year, end_month)

    # dictionary to store differences
    change_in_busyness = {}

    # iterate over all of the nodes (airports) in the start graph
    for airport in start_graph.nodes():
        if airport in end_graph.nodes():
            # variables to hold start and end traffic values
            start_airport_traffic = total_node_throughput(start_graph, airport)
            end_airport_traffic = total_node_throughput(end_graph, airport)

            if (start_airport_traffic != 0) & (end_airport_traffic != 0):
                changeInAirportBusyness = 100 * ((end_airport_traffic - start_airport_traffic) / start_airport_traffic)
                change_in_busyness[airport] = changeInAirportBusyness

    sorted_changeInBusyness = sorted(change_in_busyness.items(), key=lambda item: item[1], reverse=True)
    print(sorted_changeInBusyness)

    for airport, change in sorted_changeInBusyness:
        if change > 1:
            print(f"{airport}: {change}")
