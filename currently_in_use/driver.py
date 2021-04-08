"""
Driver for entire program.
How to run the program:
The program takes four commad line arguments. 
The first is the program name, the second is the number of 
nodes in the original graph, the third is the number of seeds
we are choosing for our seed set, and the fourth is the criticality
parameter. For example, typing the following in the terminal would 
output an optimal seed set of size 5 for an original graph with 50 nodes
and a criticality threshold of 0.7 (any node whose criticality is above
0.7 will be an accepting node)

python3 driver.py 50 5 0.7

Note that the above line requires that you are inside the currently_in_use folder

The main method which reads in these arguments passes them onto runTests(),
which acts as a driver for the following algorithms:

1) greedy dynamic programming
2) greedy knapsack
3) recursive DP (optimal for trees where <=2 clusters share any rej node)
4) Brute force (commented out by default because it takes so long. User
can choose to uncomment it and run)
5) Linear Program (optimal only when <= 2 clusters share any rej node)
6) Bipartite linear program (optimal on any graph)

All of the results are printed to the terminal and then
written to an excel sheet which is within the folder currently_in_use/tests

We also print the original, cluster, and bipartite graph to be used for comparison.
Note that the first thing we do in runTests is try to create 
a graph that satisfies our requirements, namely:
    1) No rejecting node is shared by more than 2 clusters
    2) No cycles in the cluster graph

We continuously try to make the cluster graph until these
properties are satisfied.
TODO: find a more efficient way to satisfy these properties. For 
original graphs with >100 nodes, it takes a long time to create
a cluster graph which satisfies the properties.
"""
import create_clusters as cc
import DP_algorithms as dp
import greedy_approx_algorithms as greedy
import brute_force as bf
import bipartite_linear_program as blp
import create_graph_from_file as cff
import networkx as nx
import matplotlib.pyplot as plt
import make_bipartite_graph as mbg
import sys
import openpyxl
import xlwt
import cluster_linear_program as lp
from datetime import datetime

# use "currently_in_use/" if in Overexposue folder, "" if in currently_in_use already (personal war im fighting with the vs code debugger)
FILE_DIRECTORY_PREFIX = "currently_in_use/tests/"

#TODO: allow user to type in how many nodes they want in the graph
#TODO: timestamp each graph with when you ran it
#TODO: tree decomposition algorithm
#TODO: put graphs in a format that our files can read (Laura)

"""
Experiment Design:
    - previous experiments in previous papers
    - what kinds of networks they are building, how many nodes they are taking into account
    - SNAP graphs?
    - we are limited to cluster graphs
    - Erdos-Renyi
    - Barabasi-Alber
    - Watts-Strogatz
    - real world networks like college messaging

Come up with an experiment design based on papers that we've read, then see how they are doing their experiments section.
    What are the common things they are doing? What kinds of random graph structures?
    Outline what the things they are showing are
    Write some brief notes and then design the experiment and then go with that
    Present those things next week
    We want to save the graph and run tests based on that
"""

"""
Driver for all of our algorithms.
@params:
    num_nodes --> number of nodes in the original graph
    k --> number of seeds chosen. Corresponds to number of clusters
    picked in the cluster graph
    criticality --> criticality threshold for nodes in the original graph.
    Nodes above this value will be accepting
"""
def runTests(num_nodes, k, criticality):
    #create cluster graph
    G = False #initialize to false, when we get a graph that satisfies the requirements
    #this will be true
    #TODO: commented out. Used when we want to create a cluster graph without an original graph
    #max_weight = 5
    while G == False:
        G = cc.testOriginaltoCluster(num_nodes, criticality, k)
        print("G is ", G)
    #TODO: commented out. Comment out the above 3 lines and uncomment this to create a tree cluster
    #graph without starting with the original. Useful for testing.
    #G = cc.createClusterGraph(num_nodes, max_weight)
    
    #compute payoff for greedy DP
    max_val_greedyDP, seedset = greedy.greedyDP(G, G.number_of_nodes(), k)
    store_info(G,k)
    print("\nGreedy DP Payoff: ", max_val_greedyDP)
        
    #compute payoff for most basic greedy algorithm
    greedy_payoff, greedy_seedset = greedy.kHighestClusters(G, k)
    print("Greedy Approach Seeds Chosen:", greedy_seedset, " with payoff: ", greedy_payoff)

    #compute payoff for recursive DP
    payoff_root, payoff_no_root = dp.runRecursiveDP(G, k)
    print("Recursive DP payoff: \n Root: ", payoff_root, "\n No Root: ", payoff_no_root)

    #compute payoff using brute force algorithm --> uncomment out if you want to run
    #best_payoff_selection,best_payoff = bf.computePayoff(G, k)
    #print("Brute Force payoff: ", best_payoff_selection, best_payoff)

    #run linear program
    payoff_lp = lp.lp_setup(G, k)
    #run bipartite linear program
    bipartite = mbg.graph_to_bipartite(G)
    payoff_blp = blp.solve_lp(bipartite, k)

    #write the results to excel file
    write_results(max_val_greedyDP,greedy_payoff,payoff_root, payoff_no_root, payoff_lp, payoff_blp, num_nodes,k)
    #print cluster graph and bipartite graph
    printGraph(G)
    printBipartite(bipartite)

""" Print bipartite graph using network x. Saved to file"""
def printBipartite(bipartite):
    print("printing bipartite graph")
    plt.figure("bipartite graph")
    pos = nx.spring_layout(bipartite)
    nx.draw(bipartite, pos)

    node_labels = nx.get_node_attributes(bipartite,'weight')
    # do (id, weight) pair for lable instead of just weight
    for key,val in node_labels.items():
        node_labels[key] = (key,val)
    nx.draw_networkx_labels(bipartite, pos=pos, labels=node_labels)
    plt.savefig("bipartite.png")
    plt.show()

""" display cluster graph """
def printGraph(G):
    plt.figure("normal cluster graph")
    pos = nx.spring_layout(G)
    nx.draw(G, pos)

    node_labels = nx.get_node_attributes(G,'weight')
    # do (id, weight) pair for lable instead of just weight
    for key,val in node_labels.items():
        node_labels[key] = (key,val)
    nx.draw_networkx_labels(G, pos=pos, labels=node_labels)
    data_info = nx.get_edge_attributes(G,'rej_nodes') # edge lables rejecting node
    weight_info = nx.get_edge_attributes(G,'weight') # edge lables rejecting node
    edge_labels = {}
    for key in weight_info.keys():
        if key in data_info.keys():
            edge_labels[key] = (data_info[key],weight_info[key])
        else:
            edge_labels[key] = ("na",weight_info[key])
    nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=edge_labels)
    plt.savefig("cluster.png")

""" Store more specific info about each graph, to be used for testing if the 
results output in the excel sheet are inaccurate / do not make sense """
def store_info(G,k):
    print('\nNext Test:\n')
    with open("tests/cluster_graph_details.txt", 'w') as graph_info:
        timestamp = datetime.timestamp(datetime.now())
        date = datetime.fromtimestamp(timestamp)
        graph_info.write("Prints each node weight on a new line followed by each edge. \n \
Ie the first number printed is the weight of node 0. Then prints each edge followed by its weight and the rejecting nodes.\n \
For example, 0 2 1 -22 indicates that there is an edge (0,2) with weight 1, and the rejecting node in that edge is node 22. \n")
        graph_info.write("# Timestamp: " + str(date) + "\n")
        graph_info.write("# Nodes: " + str(G.number_of_nodes()) + "\n")
        data = G.edges.data()
        graph_info.write("# Edges: " + str(len(data)))
        weights = G.nodes.data('weight')
        for node in weights:
            graph_info.write("\n" + str(node[1]))
        for item in data:
            graph_info.write("\n" + str(item[0]) + " " + str(item[1]) + " " + str(item[2]['weight']))
            try:
                data = item[2]['rej_nodes']
                for reject in data:
                    graph_info.write(" " + str(reject))
            except:
                pass

""" Write results to an excel sheet stored in the currently_in_use/tests folder """
def write_results(max_val_greedyDP,greedy_payoff,payoff_root, payoff_no_root, payoff_lp, payoff_blp, n, k):
    wb = openpyxl.load_workbook('tests/Test_results.xlsx')
    ws = wb.active
    timestamp = datetime.timestamp(datetime.now())
    date = str(datetime.fromtimestamp(timestamp))
    row = ws.max_row+1
    items_to_add = [n, k, date, max_val_greedyDP,greedy_payoff,payoff_root, payoff_no_root, payoff_lp, payoff_blp]
    i = 1
    for item in items_to_add:
        c1 = ws.cell(row = row, column = i)
        c1.value = item
        i += 1
    wb.save('tests/Test_results.xlsx')


#main function, used for calling things
def main(num_seeds, k, criticality):
    num_seeds = int(num_seeds)
    k = int(k)
    criticality = float(criticality)
    runTests(num_seeds, k, criticality)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])