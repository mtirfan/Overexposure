# wq:NAME IN PROGRASS!!!!!!!!!!!!
"""
wq:have not updated yet
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
2) greedy payoff_knapsack
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
import graph_creation
import view
import general_case
import tree_case
import assumption_one_case
# import DP_algorithms as dp
# import greedy_approx_algorithms as greedy
# import brute_force as bf
# import bipartite_linear_program as blp
# import bipartite_approx_algs as baa
# import cluster_linear_program as clp
import create_graph_from_file as cff
import networkx as nx
import matplotlib.pyplot as plt
import sys
import openpyxl
import random
import timeit
from datetime import datetime
import networkx as nx
import networkx.algorithms.isomorphism as iso

# use "currently_in_use/" if in Overexposue folder, "" if in currently_in_use already (personal war im fighting with the vs code debugger)
FILE_DIRECTORY_PREFIX = "currently_in_use/"#"currently_in_use/"
FILE_LOCATION_PREFIX = "test_files/"


#TODO: run more rigorous tests
#TODO: fix logging output to take max of root and no root
#TODO: work on paper, write analysis on run times/approximation factor
#TODO: tree decomposition algorithm

"""
wq:have not updated yet
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

# #main function, used for calling things
# def test_new_file(num_nodes, k, criticality, do_remove_cycles, do_assumption_1, plot_graphs="False", do_debug="False"):
#     num_nodes = int(num_nodes)
#     k = int(k)
#     criticality = float(criticality)
#     do_remove_cycles = string_to_boolean(do_remove_cycles)
#     do_assumption_1 = string_to_boolean(do_assumption_1)
#     plot_graphs = string_to_boolean(plot_graphs)
#     debug = string_to_boolean(do_debug)

#     do_recursive_DP = False
#     if num_nodes < 200:
#         do_recursive_DP = True
#     do_forward = False
#     if num_nodes < 2000:
#         do_forward = True

#     # all algorithms that require trees ALSO need to satisfy assumption 1!!!!!
#     # cannot do remove cycles but not assumption 1 for any algorithms
#     if do_remove_cycles:
#         do_assumption_1 = 1

#     m = 2
#     p = 0.2
#     print("Generating original graphs")
#     # create three types of graphs (ba, er, ws) or roughly the same size
#     original_graphs, original_types = generate_original_graphs(num_nodes, m, p)
    
#     # for each graph, create cluster and bipartite graphs then save results, graphs, and plot them
#     for O, graph_type in zip(original_graphs, original_types):
#         tree_case_graph, assumption_one_graph, general_graph, loops_through_while = graph_creation.generate_test_graphs(O, criticality)
#         runtimes, seeds, payoffs_by_algorithim = run_tests_on_graph(tree_case_graph, assumption_one_graph, general_graph, k, do_recursive_DP, debug, do_forward)
#         payoffs = []
#         for seed_set in seeds:
#             if seed_set == '-':
#                 payoffs.append('-')
#             else:
#                 payoffs.append(calculate_payoff(general_graph, seed_set))
        
#         ID = view.generate_ID()

#         # save the different graphs by ID
#         location = view.save_original(O, criticality, k, graph_type, ID, do_remove_cycles, do_assumption_1)
#         # view.save_cluster(C, k, criticality, ID, do_remove_cycles, do_assumption_1)
#         # make sure these are clear so original graphs do not accidentally interfere with each other

#         max_degree = "-"
#         max_height = "-"
#         if do_remove_cycles and O.number_of_nodes() < 1000:
#             max_degree, max_height = get_max_degree_and_height(tree_case_graph)
        
#         # save to excel. Also provides unique ID for each row to a test can be ran again
#         view.write_results_to_excel([num_nodes, k, criticality, graph_type, location], payoffs, runtimes, payoffs_by_algorithim, max_degree, max_height, seeds[8])
            
#         # plot the different graphs
#         if plot_graphs:
#             # get error if attempt to plot more than 500 nodes
#             if num_nodes < 500:
#                 view.plot_original(O, criticality)
#             if len(tree_case_graph.nodes()) < 500:
#                 view.plot_cluster(tree_case_graph, graph_type + " tree cluster graph")
#             if len(assumption_one_graph.nodes()) < 500:
#                 view.plot_cluster(assumption_one_graph, graph_type + " assumption 1 cluster graph")
#             if len(general_graph.nodes()) < 500:
#                 view.plot_bipartite(general_graph, graph_type + " general bipartite graph")
#             plt.show()
#         if debug: print(tree_case_graph.edges.data())

#         tree_case_graph.clear()
#         assumption_one_graph.clear()
#         general_graph.clear()

# def retest_old_file(original_graph_filename, k_val=None, do_remove_cycles=None, do_assumption_1=None, plot_graphs="False", do_debug="False"):
#     # get all information used to make ID in excel sheet
#     if original_graph_filename[-4:] != ".txt":
#        original_graph_filename = original_graph_filename + ".txt"
#     location = FILE_LOCATION_PREFIX + original_graph_filename
#     k, criticality, graph_type, ID, file_remove_cycles, file_assumption_1, O = cff.create_from_file(location)
#     num_nodes = O.number_of_nodes()
#     do_recursive_DP = False
#     if num_nodes < 200:
#         do_recursive_DP = True
#     do_forward = False
#     if num_nodes < 2000:
#         do_forward = True
#     print("Retesting " + original_graph_filename)
#     plot_graphs = string_to_boolean(plot_graphs)
#     debug = string_to_boolean(do_debug)
#     # use what file originally did unless ow specified
#     if do_remove_cycles == None:
#         do_remove_cycles = file_remove_cycles
#     else:
#         do_remove_cycles = string_to_boolean(do_remove_cycles)
#     if do_assumption_1 == None:
#         do_assumption_1 = file_assumption_1
#     else:
#         do_assumption_1 = string_to_boolean(do_assumption_1)
#     if k_val != None:
#         k = int(k_val)
    
#     if do_remove_cycles: print("Remove Cycs: " + str(do_remove_cycles))
#     if do_assumption_1: print("Ass 1: " + str(do_assumption_1))
    
#     # create cluster and bipartite based on information from file
#     tree_case_graph, assumption_one_graph, general_graph, loops_through_while = graph_creation.generate_test_graphs(O, criticality)
#     if loops_through_while != 1:
#         print("Criticalities were reset. Assumption 1 may not have been satisfied in this file")
#         sys.exit()
    
#     runtimes, seeds, payoffs_by_algorithim= run_tests_on_graph(tree_case_graph, assumption_one_graph, general_graph, k, do_recursive_DP, debug, do_forward)
#     payoffs = []
#     for seed_set in seeds:
#         if seed_set == '-':
#             payoffs.append('-')
#         else:
#             payoffs.append(calculate_payoff(general_graph, seed_set))
    
#     print("BSG seeds: ", seeds[5])
#     print("BG seeds: ", seeds[6])

#     max_degree = "-"
#     max_height = "-"
#     if do_remove_cycles and O.number_of_nodes() < 1000:
#         max_degree, max_height = get_max_degree_and_height(tree_case_graph)
        
#     # save to excel. Also provides unique ID for each row to a test can be ran again
#     view.write_results_to_excel([num_nodes, k, criticality, graph_type, location], payoffs, runtimes, payoffs_by_algorithim, max_degree, max_height, seeds[8])
    
#     # plot the different graphs
#     if plot_graphs:
#         # get error if attempt to plot more than 500 nodes
#         if num_nodes < 500:
#             view.plot_original(O, criticality)
#         if len(tree_case_graph.nodes()) < 500:
#             view.plot_cluster(tree_case_graph, graph_type + " tree cluster graph")
#         if len(assumption_one_graph.nodes()) < 500:
#             view.plot_cluster(assumption_one_graph, graph_type + " assumption 1 cluster graph")
#         if len(general_graph.nodes()) < 500:
#             view.plot_bipartite(general_graph, graph_type + " general bipartite graph")
#         plt.show()
#     if debug: print(tree_case_graph.edges.data())

#     tree_case_graph.clear()
#     assumption_one_graph.clear()
#     general_graph.clear()
#     O.clear()

def test_file(original_graph_filename, k, appeal, record_cluster_data="False", plot_graphs="False", do_debug="False"):
    print("=============================================")
    print("Running on " + original_graph_filename + ". k = " + k + ". a = " + appeal)
    # convert command line args to proper types
    if original_graph_filename[-4:] != ".txt":
       original_graph_filename = original_graph_filename + ".txt"
    plot_graphs = string_to_boolean(plot_graphs)
    debug = string_to_boolean(do_debug)
    record_cluster_data = string_to_boolean(record_cluster_data)
    k = int(k)
    appeal = float(appeal)
    location = FILE_LOCATION_PREFIX + original_graph_filename

    # getting info from file. Ignore all values except O graph
    file_k, file_appeal, graph_type, ID, file_remove_cycles, file_assumption_1, O = cff.create_from_file(location)
    num_nodes = O.number_of_nodes()

    # restrictions on running algorithms (due to run time)
    do_recursive_DP = False
    if num_nodes < 200:
        do_recursive_DP = True
    do_forward = True
    # if num_nodes < 2000:
    #     do_forward = True

    # create cluster and bipartite based on information from file
    tree_case_cluster, tree_case_bipartite, assumption_one_cluster, assumption_one_bipartite, general_bipartite, loops_through_while = graph_creation.generate_test_graphs(O, appeal, record_cluster_data)
    if loops_through_while != 1:
        print("Criticalities were reset. Assumption 1 may not have been satisfied in this file")
        sys.exit()

    # if cluster data is being recorded, do not run tests on graphs
    if record_cluster_data:
        tree_case_cluster.clear()
        tree_case_bipartite.clear()
        assumption_one_cluster.clear()
        assumption_one_bipartite.clear()
        general_bipartite.clear()
        O.clear() 
        return
    
    # run tests and calculate payoffs
    relative_results, seeds = run_tests_on_graph(tree_case_cluster, tree_case_bipartite, assumption_one_cluster, assumption_one_bipartite, general_bipartite, k, debug, do_recursive_DP, do_forward)
    payoffs = []
    for seed_set in seeds:
        if seed_set == '-':
            payoffs.append('-')
        else:
            payoffs.append(calculate_payoff(general_bipartite, seed_set))
    
    # print("BSG seeds: ", seeds[5])
    # print("BG seeds: ", seeds[6])

    max_degree = "-"
    max_height = "-"
    if O.number_of_nodes() < 1000:
        max_degree, max_height = get_max_degree_and_height(tree_case_cluster)

    # if record_cluster_data:
        #view.record_clusters(num_nodes, k, appeal, graph_type, location, cluster_occurences)
    # save to excel. Also provides unique ID for each row to a test can be ran again
    view.write_results_to_excel([num_nodes, k, appeal, graph_type, location], payoffs, relative_results, max_degree, max_height, seeds[8])
    
    # plot the different graphs
    if plot_graphs:
        # get error if attempt to plot more than 500 nodes
        if num_nodes < 500:
            view.plot_original(O, appeal)
        if len(tree_case_cluster.nodes()) < 500:
            view.plot_cluster(tree_case_cluster, graph_type + " tree cluster graph")
        if len(assumption_one_graph.nodes()) < 500:
            view.plot_cluster(assumption_one_graph, graph_type + " assumption 1 cluster graph")
        if len(general_graph.nodes()) < 500:
            view.plot_bipartite(general_graph, graph_type + " general bipartite graph")
        plt.show()
    if debug: print(tree_case_cluster.edges.data())
    tree_case_cluster.clear()
    tree_case_bipartite.clear()
    assumption_one_cluster.clear()
    assumption_one_bipartite.clear()
    general_bipartite.clear()
    O.clear() 

'''
Generate three types of original graphs (Barabasi-Albert, Erdos-Renyi, and Watts-Strogatz) of the same size
@params:
    num_nodes           --> number of nodes in graph
    num_links           --> links used for BA and ER
    prob_rewrite_edge   --> used for WS
@returns
    list of three graphs (as networkx graphs!)
    list of three graph types (as strings)
'''
def generate_original_graphs(num_nodes, num_links, prob_rewrite_edge):
    # the math here is used to create three graphs with the same number of nodes and
    # roughly the same number of edges, so the three are comparable
    BA = nx.barabasi_albert_graph(num_nodes, num_links)
    ER = nx.erdos_renyi_graph(num_nodes, (2 * num_links) / num_nodes)
    avg_num_edges = (BA.number_of_edges() + ER.number_of_edges()) / 2
    WS = nx.watts_strogatz_graph(num_nodes, round((2 * avg_num_edges) / num_nodes), prob_rewrite_edge)

    original_graphs = [BA, ER, WS]
    # assign the basic attributes of each node (criticality is random!)
    for O in original_graphs:
        for node_ID in O.nodes():
            O.nodes[node_ID]["visited"] = False
            O.nodes[node_ID]['criticality'] = random.uniform(0, 1)
            O.nodes[node_ID]["cluster"] = -1
    return [BA, ER, WS], ["BA", "ER", "WS"]

"""
Run algorithms on cluster graph, and its corresponding bipartite graph, based on class of algorithm.
Uses booleans remove_cycles and assumption_1 to id class of algorithm
@params:
    C               --> cluster graph (can be tree, assumption 1, or unmodified)
    B               --> bipartite graph created from this cluster graph
    k               --> number of nodes to seed
    remove_cycles   --> if true, test knapsack, greedy, recurisve DP
    assumption_1    --> if true, test cluster linear program
    NOTE: bipartite algorithms will run for all, regardless of boolean variables
@returns:
    list of payoffs
        Indecies are based off of excel speadsheet "Experimental_Results.xlsx" with each algorithm result
        contained in one index. If the algorithm was not run, contains '-'
    list of runtimes
        Indecies are based off of excel speadsheet "Experimental_Results.xlsx" with each algorithm result
        contained in one index. If the algorithm was not run, contains '-'
"""
def run_tests_on_graph(tree_case_cluster, tree_case_bipartite, assumption_one_cluster, assumption_one_bipartite, general_bipartite, k, debug, do_recursive_DP, do_forward):
    # set default value of array (if an algorithm is not run)
    relative_payoff_tree = []
    relative_payoff_ass_1 = []
    relative_payoff_general = []
    relative_runtimes_tree = []
    relative_runtimes_ass_1 = []
    relative_runtimes_general = []
    seeds = [] # only saving the seed results from the actual graph type
    for i in range(9):
        relative_payoff_tree.append('-')
        relative_payoff_ass_1.append('-')
        relative_payoff_general.append('-')
        relative_runtimes_tree.append('-')
        relative_runtimes_ass_1.append('-')
        relative_runtimes_general.append('-')
        seeds.append([])

    # trivial. take node.
    if len(tree_case_cluster.nodes()) == 1:
        for i in range(9):
            if i != 2 and i != 0:
                weight = tree_case_cluster.nodes[0]['weight']
                relative_payoff_tree[i] = weight
                relative_payoff_ass_1[i] = weight
                relative_payoff_general[i] = weight
                relative_runtimes_tree[i] = 0
                relative_runtimes_ass_1[i] = 0
                relative_runtimes_general[i] = 0
                seeds[i] = ([0])
        return [relative_payoff_tree, relative_payoff_ass_1, relative_payoff_general, relative_runtimes_tree, relative_runtimes_ass_1, relative_runtimes_general], seeds
    
    print("Testing on tree graphs")
    tree_tests(tree_case_cluster, tree_case_bipartite, relative_payoff_tree, seeds, relative_runtimes_tree, k, debug, do_recursive_DP, do_forward, True)
    
    print("Testing on assumption one graphs")
    assumption_one_tests(assumption_one_cluster, assumption_one_bipartite, relative_payoff_ass_1, seeds, relative_runtimes_ass_1, k, debug, do_recursive_DP, do_forward, True)

    print("Testing on general graphs")
    general_tests(general_bipartite, relative_payoff_general, seeds, relative_runtimes_general, k, debug, do_recursive_DP, True, True)

    return [relative_payoff_tree, relative_payoff_ass_1, relative_payoff_general, relative_runtimes_tree, relative_runtimes_ass_1, relative_runtimes_general], seeds

def tree_tests(cluster, bipartite, payoffs, seeds, runtimes, k, debug, do_recursive_DP, do_forward, save_seeds=False):
    # tree algorithms
    print("Doing Tree Algorithms with Assumption 1 Satisfied")

    # compute payoff using knapsack approach
    start = timeit.default_timer()
    payoff_knapsack, seedset = tree_case.knapsack(cluster, cluster.number_of_nodes(), k)
    stop = timeit.default_timer()
    # # if payoff is less than 0, best to not pick any seeds
    # if payoff_knapsack < 0:
    #     payoff_knapsack = 0
    #     seedset = []
    runtimes[1] = stop - start
    payoffs[1] = payoff_knapsack
    if save_seeds: seeds[1] = seedset
    if debug: print("Knacpsack (Greedy DP) Payoff: ", payoff_knapsack)
    if do_recursive_DP:
        # compute payoff for recursive DP
        start = timeit.default_timer()
        payoff_root, payoff_no_root = tree_case.runRecursiveDP(cluster, k)
        payoff_recursive_dp = max(payoff_root, payoff_no_root)
        stop = timeit.default_timer()
        runtimes[2] = stop - start
        payoffs[2] = payoff_recursive_dp
        if debug: print("Recursive DP payoff: ", payoff_recursive_dp)

    # tree case graphs also satisfy assumption 1, so can run those algorithms on tree graph
    assumption_one_tests(cluster, bipartite, payoffs, seeds, runtimes, k, debug, do_recursive_DP, do_forward)

def assumption_one_tests(cluster, bipartite, payoffs, seeds, runtimes, k, debug, do_recursive_DP, do_forward, save_seeds=False):
    # algorithms for assumption 1 (nodes cannot share more than two rejecting nodes, which means that there CAN be cycles)
    print("Doing Assumption 1 Algorithms")

    # compute payoff for most basic greedy algorithm
    start = timeit.default_timer()
    payoff_greedy, greedy_seedset = assumption_one_case.kHighestClusters(cluster, k, debug)
    stop = timeit.default_timer()
    # # if payoff is less than 0, best to not pick any seeds
    # if payoff_greedy < 0:
    #     payoff_greedy = 0
    #     greedy_seedset = []
    runtimes[3] = stop - start
    payoffs[3] = payoff_greedy
    if save_seeds: seeds[3] = greedy_seedset
    if debug: print("K-Highest Seeds Chosen: ", greedy_seedset, " with payoff: ", payoff_greedy)

    # run linear program on cluster graph
    start = timeit.default_timer()
    payoff_clp, clp_seedset = assumption_one_case.lp_setup(cluster, k, debug)
    stop = timeit.default_timer()
    runtimes[4] = stop - start
    payoffs[4] = payoff_clp
    if save_seeds: seeds[4] = clp_seedset
    if debug: print("Cluster LP payoff: ", payoff_clp)

    # assumption one graphs can also run general algorithms
    general_tests(bipartite, payoffs, seeds, runtimes, k, debug, do_recursive_DP, do_forward)

def general_tests(bipartite, payoffs, seeds, runtimes, k, debug, do_recursive_DP, do_forward, save_seeds=False):
    # all general test cases (no restrictions)
    print("Doing General Algorithms")
    
    # # run bipartite random selection
    # start = timeit.default_timer()
    # payoff_random, random_seeds = general_case.random_selection(bipartite, k)
    # stop = timeit.default_timer()
    # runtimes[0] = stop - start
    # payoffs[0] = payoff_random
    # if save_seeds: seeds[0] = random_seeds
    # if debug: print("Random selection payoff: ", payoff_random)
    
    # run bipartite simple greedy algorithm
    start = timeit.default_timer()
    payoff_simple_greedy, bipartite_simple_greedy_seeds = general_case.simple_greedy_selection(bipartite, k)
    stop = timeit.default_timer()
    # if payoff_simple_greedy < 0:
    #     payoff_simple_greedy = 0
    #     bipartite_simple_greedy_seeds = []
    runtimes[5] = stop - start
    payoffs[5] = payoff_simple_greedy
    if save_seeds: seeds[5] = bipartite_simple_greedy_seeds
    if debug: print("Bipartite Simple Greedy payoff: ", payoff_simple_greedy)
    
    # run bipartite greedy algorithm
    start = timeit.default_timer()
    # payoff_greedy, bipartite_greedy_seeds = general_case.greedy_selection(bipartite, k, debug)
    payoff_greedy, bipartite_greedy_seeds = general_case.greedy_selection_graph_implementation(bipartite, k)
    stop = timeit.default_timer()
    runtimes[6] = stop - start
    payoffs[6] = payoff_greedy
    if save_seeds: seeds[6] = bipartite_greedy_seeds
    if debug: print("Bipartite Greedy payoff: ", payoff_greedy)

    if do_forward:
        # run bipartite forward thinking algorithm
        start = timeit.default_timer()
        # payoff_forward_thinking, forward_seeds = general_case.forward_thinking_greedy(bipartite, k, debug)
        payoff_forward_thinking, forward_seeds = general_case.forward_thinking_greedy_graph_implementation(bipartite, k)
        stop = timeit.default_timer()
        runtimes[7] = stop - start
        payoffs[7] = payoff_forward_thinking
        if save_seeds: seeds[7] = forward_seeds
        if debug: print("Forward-Thinking payoff: ", payoff_forward_thinking)

    # run bipartite linear program
    start = timeit.default_timer()
    payoff_blp, blp_seeds = general_case.solve_blp(bipartite, k, debug)
    stop = timeit.default_timer()
    runtimes[8] = stop - start
    payoffs[8] = payoff_blp
    if save_seeds: seeds[8] = blp_seeds
    if debug: print("Bipartite LP payoff: ", payoff_blp)


def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

# # wildly silly way of doing this
# def calculate_payoff(unmodified_B, seeds):
#     weight_dict = dict(nx.get_node_attributes(unmodified_B,'weight'))
#     edges = list(unmodified_B.edges())
#     rej_nodes = set()
#     real_payoff = 0
#     for node in seeds:
#         #compute intersection of in edges from unmodified graph and
#         #the edges we have not yet removed from the modified graph
#         num_neg = len(intersection(edges, unmodified_B.in_edges(node)))
#         real_payoff = real_payoff - num_neg + weight_dict[node]
#         rej_nodes = [x[0] for x in unmodified_B.in_edges(node)]
#         #iterate through edges, remove any edge that contains rej nodes connected to picked cluster
#         i = 0
#         while i < len(edges):
#             if edges[i][0] in rej_nodes:
#                 edges.pop(i)
#             else:
#                 i += 1
#         #print("Num edges: ", num_neg, " Max weight node: ", max_weight_node)
#         #unmodified_B.remove_node(max_weight_node)
#         rej_nodes = set()
#     return real_payoff

def calculate_payoff(unmodified_B, seeds):
    rej_nodes = set()
    real_payoff = 0
    for node in seeds:
        real_payoff += unmodified_B.nodes[node]['weight']
        for rejects in unmodified_B.in_edges(node):
            rej_nodes.add(rejects[0])
    return real_payoff - len(rej_nodes)

def string_to_boolean(input):
    if input == "false" or input == "False" or input == "0":
        return 0
    elif input == "true" or input == "True" or input == "1":
        return 1
    else:
        print('ERROR: Invalid boolean input (try using "True", "true", or "1" [same for false variations])')
        sys.exit()

def get_max_degree_and_height(G):
    # get the max degree
    # node with max degree is most likley root
    max_degree = -1
    root = None
    for n, d in G.degree():
        if d > max_degree:
            max_degree = d
            root = n

    shortest_path_from_root_to_all_nodes = nx.shortest_path(G, source=root)
    max_height = -1
    # get largest of the shortest paths (this will necissarily be the path from root to leaf)
    for node, path in shortest_path_from_root_to_all_nodes.items():
        if len(path) > max_height:
            max_height = len(path)
    return max_degree, max_height - 1 # max height subtracts 1 bc height of root is 1

# # Uncomment to run using command line!
# if __name__ == "__main__":
#     # test old file, not plot
#     if len(sys.argv) == 2:
#         retest_old_file(sys.argv[1])
#     # test old file, specify do plot (if possible)
#     elif len(sys.argv) == 3:
#         retest_old_file(sys.argv[1], sys.argv[2])
#     # test olf file,  specify do plot (if possible), specifiy print debug info
#     elif len(sys.argv) == 4:
#         retest_old_file(sys.argv[1], sys.argv[2], sys.argv[3])
#     # create and test a new file, not plot
#     elif len(sys.argv) == 6:
#         # test_if_saved_graphs_same(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
#         test_new_file(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
#     # create and test a new file, specify do plot (if possible)
#     elif len(sys.argv) == 7:
#         test_new_file(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
#     # create and test a new file,  specify do plot (if possible), specifiy print debug info
#     elif len(sys.argv) == 8:
#         test_new_file(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7])
#     else:
#         print('ERROR: Invalid input')
#         sys.exit()

# test_if_saved_graphs_same("100","5","0.5","True","True")
# test_new_file("500","10","0.5","False","False","False")
# test_new_file("40","2","1","True","True")
# retest_old_file("0.5/BA/500/20/139.txt", "True","True","True")


# retest_old_file("0.5/BA/500/10/37.txt", "False","False","False")
# retest_old_file("0.5/BA/500/10/73.txt", "False","False","False")

# test_file("BA/5000/298.txt", "10", "0.5")
# test_file("ER/5000/233.txt", "100", "0.25", "True")
# plt.show()

# '''
# Written for debugging purposes. Testing if generated graphs and their saved counterparts generate the same graph (isomorphic). Created
# because tests of generation vs repeated tests were not matching in values.
# '''
# def test_if_saved_graphs_same(num_nodes, k, criticality, do_remove_cycles, do_assumption_1):
#     num_nodes = int(num_nodes)
#     k = int(k)
#     criticality = float(criticality)
#     do_remove_cycles = string_to_boolean(do_remove_cycles)
#     do_assumption_1 = string_to_boolean(do_assumption_1)
#     m = 2
#     p = 0.2
#     print("generating original graphs")
#     # create three types of graphs (ba, er, ws) or roughly the same size
#     original_graphs, original_types = generate_original_graphs(num_nodes, m, p)
#     count = 0
#     for O, graph_type in zip(original_graphs, original_types):
#         ID = "test-" + str(count)
#         print(ID)
#         C, B = graph_creation.generate_test_graphs(O, criticality, do_remove_cycles, do_assumption_1)
#         view.save_original(O, criticality, k, graph_type, ID, do_remove_cycles, do_assumption_1)
#         count += 1
#         k, criticality, graph_type, new_ID, do_remove_cycles, do_assumption_1, saved_O = cff.create_from_file(ORIGINAL_FILE_LOCATION + ID + ".txt")
#         saved_C, saved_B = graph_creation.generate_test_graphs(saved_O, criticality, do_remove_cycles, do_assumption_1)
#         nm = iso.categorical_node_match("criticality",0)
#         is_O_copy = nx.is_isomorphic(O,saved_O, node_match=nm)

#         # # never got this bit to work
#         # nm = iso.categorical_node_match("weight",0)
#         # em = iso.numerical_multiedge_match(["weight", "rej_nodes"], [0, None])
#         # is_C_copy = nx.is_isomorphic(C,saved_C, node_match=nm, edge_match=em)
#         print(ID + " originial same? " + str(is_O_copy))
#         print(ID + " cluster same? " + str(is_C_copy))
#         C.clear()
#         B.clear()
#         saved_O.clear()

# def test_counter_example():
#     location = "counter_ex.txt"
#     C = cff.create_from_file(location)
#     plot_graphs = True
#     debug = False
#     k = 6
    
#     view.plot_cluster(C, "counter_ex" + " cluster graph")
#     plt.show()

#     payoff_knapsack, seedset = tree_case.knapsack(C, C.number_of_nodes(), k)
# test_counter_example()