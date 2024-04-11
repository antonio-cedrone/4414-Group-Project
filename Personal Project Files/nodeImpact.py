from dataReader import make_graph
from nodeThroughput import single_node_throughput

"""determines the change in node throughput between two periods of time for a specific node"""


def node_impact(node, start_year, end_year, start_month=None, end_month=None):
    # make the graphs for the given years and months
    start_g = make_graph(start_year, start_month)
    end_g = make_graph(end_year, end_month)

    # get the start throughput from the start graphs for the selected node
    start_throughput = single_node_throughput(start_g, node)

    # confirm that the node exists in the end graph
    if node in end_g.nodes:
        # retrieve the end throughput
        end_throughput = single_node_throughput(end_g, node)

        # return the difference in and out throughput for the airport
        return {"in": (end_throughput.get("in") - start_throughput.get("in")),
                "out": (end_throughput.get("out") - start_throughput.get("out"))}
    else:
        # return none if the airport is not in the end graph
        return None


"""determine the difference in node impact for all nodes in the chosen start month that exist within the ending
month"""


def node_impact_all_nodes(start_year, start_month, end_year, end_month):
    # create the start and end graphs based on entered year and month information
    start_g = make_graph(start_year, start_month)
    end_g = make_graph(end_year, end_month)

    # variable to hold throughput for nodes
    throughput = {}

    # iterate over start graph nodes
    for node in start_g.nodes:
        # confirm the node is in the end graph
        if node in end_g.nodes:
            # get the start and end throughput for the node
            start_throughput_v = single_node_throughput(start_g, node)
            end_throughput_v = single_node_throughput(end_g, node)

            # add the iata code and the start and end throughput to the throughput variable
            throughput[node] = {"start_in": start_throughput_v.get("in"), "start_out": start_throughput_v.get("out"),
                                "change_in": (end_throughput_v.get("in") - start_throughput_v.get("in")),
                                "change_out": (end_throughput_v.get("out")) - start_throughput_v.get("out")}

    # return the throughput for the nodes
    return throughput


if __name__ == "__main__":
    # section 5.3
    # get the node impact of every year from April to June
    impact2018 = node_impact_all_nodes(2018, 4, 2018, 6)
    impact2019 = node_impact_all_nodes(2019, 4, 2019, 6)
    impact2020 = node_impact_all_nodes(2020, 4, 2020, 6)

    sorted_airports = []

    for iata, throughput2020 in impact2020.items():
        throughput2018 = impact2018.get(iata)
        throughput2019 = impact2019.get(iata)

        # confirm that there is data for this time and that it is not zero
        if throughput2018 is None or throughput2019 is None or throughput2018.get(
                'start_in') == 0 or throughput2018.get('start_out') == 0 or throughput2019.get(
                'start_in') == 0 or throughput2019.get('start_out') == 0 or throughput2020.get(
                'start_in') == 0 or throughput2020.get('start_out') == 0:
            continue

        # add the sorted start incoming and outgoing passengers as well as the percentage
        # they change in June
        sorted_airports.append(
            (iata,
             int(throughput2018.get('start_in')),
             int(throughput2018.get('start_out')),
             round(throughput2018.get('change_in') / throughput2018.get('start_in') * 100, 1),
             round(throughput2018.get('change_out') / throughput2018.get('start_out') * 100, 1),
             int(throughput2019.get('start_in')),
             int(throughput2019.get('start_out')),
             round(throughput2019.get('change_in') / throughput2019.get('start_in') * 100, 1),
             round(throughput2019.get('change_out') / throughput2019.get('start_out') * 100, 1),
             int(throughput2020.get('start_in')),
             int(throughput2020.get('start_out')),
             round(throughput2020.get('change_in') / throughput2020.get('start_in') * 100, 1),
             round(throughput2020.get('change_out') / throughput2020.get('start_out') * 100, 1)))

    # sort by total change in 2020
    impactData = sorted(sorted_airports, key=lambda x: x[11] + x[12], reverse=True)

    # print the nodes in order of most changed from April 2020 to June 2020
    # output in this format for easy entry into latex
    for airport in impactData:
        print(airport[0], "&", airport[1], "&", airport[2], "&", airport[3], "&",
              airport[4], "&", airport[5], "&", airport[6], "&", airport[7], "&",
              airport[8], "&", airport[9], "&", airport[10], "&", airport[11], "&", airport[12])
