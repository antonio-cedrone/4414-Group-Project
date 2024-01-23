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
    throughput = []

    # iterate over start graph nodes
    for node in start_g.nodes:
        # confirm the node is in the end graph
        if node in end_g.nodes:
            # get the start and end throughput for the node
            start_throughput_v = single_node_throughput(start_g, node)
            end_throughput_v = single_node_throughput(end_g, node)

            # add the iata code and the start and end throughput to the throughput variable
            throughput.append(
                (node, {"start_in": start_throughput_v.get("in"), "start_out": start_throughput_v.get("out"),
                        "change_in": (end_throughput_v.get("in") - start_throughput_v.get("in")),
                        "change_out": (end_throughput_v.get("out")) - start_throughput_v.get("out")}))

    # return the throughput for the nodes
    return throughput


if __name__ == "__main__":
    # section 5.4
    # get the node impact of every year from April to June
    result = node_impact_all_nodes(2017, 4, 2017, 6)
    result2 = node_impact_all_nodes(2018, 4, 2018, 6)
    result3 = node_impact_all_nodes(2019, 4, 2019, 6)
    result4 = node_impact_all_nodes(2020, 4, 2020, 6)

    sorted_airports = []

    for r2020 in result4:
        for r2018 in result2:
            if r2020[0] == r2018[0]:
                for r2019 in result3:
                    if r2020[0] == r2019[0]:
                        for r2017 in result:
                            if r2020[0] == r2017[0]:
                                # confirm it is the same airport and then make sure that none of the starting values are
                                # 0 to avoid division by 0
                                if ((r2017[1].get('start_in') > 0 and r2017[1].get('start_out') > 0
                                     and r2018[1].get('start_in') > 0 and r2018[1].get('start_out') > 0)
                                        and r2019[1].get('start_in') > 0 and r2019[1].get('start_out') > 0
                                        and r2020[1].get('start_in') > 0 and r2020[1].get('start_out') > 0):
                                    # add the sorted start incoming and outgoing passengers as well as the percentage
                                    # they change in June
                                    sorted_airports.append((r2017[0],
                                                            int(r2017[1].get('start_in')),
                                                            int(r2017[1].get('start_out')),
                                                            round(
                                                                r2017[1].get('change_in') / r2017[1].get(
                                                                    'start_in') * 100,
                                                                1),
                                                            round(r2017[1].get('change_out') / r2017[1].get(
                                                                'start_out') * 100, 1),
                                                            int(r2018[1].get('start_in')),
                                                            int(r2018[1].get('start_out')),
                                                            round(
                                                                r2018[1].get('change_in') / r2018[1].get(
                                                                    'start_in') * 100,
                                                                1),
                                                            round(r2018[1].get('change_out') / r2018[1].get(
                                                                'start_out') * 100, 1),
                                                            int(r2019[1].get('start_in')),
                                                            int(r2019[1].get('start_out')),
                                                            round(
                                                                r2019[1].get('change_in') / r2019[1].get(
                                                                    'start_in') * 100,
                                                                1),
                                                            round(r2019[1].get('change_out') / r2019[1].get(
                                                                'start_out') * 100, 1),
                                                            int(r2020[1].get('start_in')),
                                                            int(r2020[1].get('start_out')),
                                                            round(
                                                                r2020[1].get('change_in') / r2020[1].get(
                                                                    'start_in') * 100,
                                                                1),
                                                            round(r2020[1].get('change_out') / r2020[1].get(
                                                                'start_out') * 100, 1)))
                                break
                        break
                break

    # sort by total change
    r = sorted(sorted_airports, key=lambda x: x[15] + x[16], reverse=True)

    # print the nodes in order of most changed from April 2020 to June 2020
    for j in r:
        print(j[0], "&", j[5], "&", j[6], "&", j[7], "&", j[8], "&", j[9], "&", j[10],
              "&", j[11], "&", j[12], "&", j[13], "&", j[14], "&", j[15], "&", j[16])
