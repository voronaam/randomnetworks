#!/usr/bin/env python

"""detachment.py: Test program to simulate detachment in scalefree networks."""

__author__ = "Aleksey Vorona"

import networkx as nx
from networkx.utils import random_weighted_sample
from networkx.utils import weighted_choice
import matplotlib.pyplot as plt
import sys, getopt, random, collections
import progressbar

def generate_sf(n, m0, m):
    """
        Create Barabási–Albert graph (working around https://github.com/networkx/networkx/issues/3281)
    """
    G = nx.complete_graph(m0)
    while len(G) < n:
        degrees = {node: val for (node, val) in G.degree()}
        node = len(G)
        G.add_node(node)
        targets = random_weighted_sample(degrees, m)
        G.add_edges_from(zip([node]*m,targets))
    return G

def show_metrics(G):
    hubs = sorted(G, key=lambda n: len(G[n]), reverse=True)[0:6]
    print("hubs", ["%d %d" % (hub, len(G[hub])) for hub in hubs])
    print("Graph. Nodes", len(G), "Edges", len(G.edges()))

def plot_degree_rank_hist(G):
    degree_sequence=sorted([d[1] for d in G.degree()],reverse=True) # degree sequence
    dmax=max(degree_sequence)

    plt.loglog(degree_sequence,'b-',marker='o')
    plt.title("Degree rank plot")
    plt.ylabel("degree")
    plt.xlabel("rank")

    plt.savefig("degree_histogram.png")
    plt.show()

def plot_degree_hist(G):
    degree_sequence = sorted([d for n, d in G.degree()], reverse=True)  # degree sequence
    degreeCount = collections.Counter(degree_sequence)
    deg, cnt = zip(*degreeCount.items())

    fig, ax = plt.subplots()
    plt.bar(deg, cnt, width=0.80, color='b')

    plt.title("Degree Histogram")
    plt.ylabel("Count")
    plt.xlabel("Degree")
    ax.set_xticks([d + 0.4 for d in deg])
    ax.set_xticklabels(deg)

    plt.show()


def sim_first(n, m0, m, steps):
    print("Running first")
    # Static parameters
    G = generate_sf(n, m0, m)
    print(G)
    show_metrics(G)

    plot_degree_hist(G)

    for i in progressbar.progressbar(range(steps)):
        # choose an edge
        edge = random.choice(list(G.edges()))
        # choose which side of it to keep
        source = edge[0]
        if len(G[source]) > len(G[edge[1]]):
            source = edge[1]
        G.remove_edge(edge[0], edge[1])
        # connect to a new place
        degrees = {node: val for (node, val) in G.degree() if node not in G.neighbors(source)}
        target = weighted_choice(degrees)
        G.add_edge(source, target)

    show_metrics(G)
    plot_degree_hist(G)

def main(argv):
    usage = 'detachment.py -s <simulation>'
    simulation = 'preferntial_reattachment'
    n = 25
    m0 = 5
    m = 5
    steps = 100
    try:
      opts, args = getopt.getopt(argv,"hs:n:i:m:j:",["simulation="])
    except getopt.GetoptError:
      print(usage)
      sys.exit(2)
    for opt, arg in opts:
      if opt == '-h':
         print(usage)
         sys.exit()
      elif opt in ("-s", "--simulation"):
         simulation = arg
      elif opt == "-n":
         n = int(arg)
      elif opt == "-m":
         m = int(arg)
      elif opt == "-i":
         m0 = int(arg)
      elif opt == "-j":
         steps = int(arg)

    simulations = {
        "preferntial_reattachment": sim_first,
    }
    simulations.get(simulation, lambda: print("Invalid simulation"))(n, m0, m, steps)

if __name__ == "__main__":
   main(sys.argv[1:])


