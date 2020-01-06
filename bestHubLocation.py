#Kultigin Bozdemir @ 2019
# This project enable to solve a two-hub transport optimization problem by Klincewincz Algorithm.
from networkx import *
import matplotlib.pyplot as plt

G=nx.Graph()
nodelist=['a','b','c','d','e','f']
G.add_nodes_from(nodelist)

G.add_weighted_edges_from([('a', 'a', 0),('a', 'b',2),('a','c',5),('a','d',3),('a','e',5),('a','f',6),
                           ('b','b',0),('b','c',4),('b','d',8),('b','e',1),('b','f',2),
                           ('c','c',0),('c','d',2),('c','e',5),('c','f',3),
                           ('d','d',0),('d','e',6),('d','f',6),
                           ('e','e',0),('e','f',7),
                           ('f','f',0)])

print(G.edges(data=True))
nx.draw_networkx(G, with_labels=True)
plt.show()

K=nx.Graph()
L=nx.Graph()
#   the function below generates, from the given G graph above, two separated hub-spoke graphs which give min total weight
def hub(n2, n3):
    for n1 in nodelist:
        w12=G.get_edge_data(n1, n2)['weight']
        w13=G.get_edge_data(n1, n3)['weight']
        if w12 <= w13:
            K.add_nodes_from([n1, n2])
            K.add_weighted_edges_from([(n1, n2, w12)])
        else:
            L.add_nodes_from([n1,n3])
            L.add_weighted_edges_from([(n1, n3, w13)])


bundling=0.5       # bundling coefficient between hubs
d=dict()  # to save generated graphs into a dictionary
count=0
for n2 in nodelist:
    for n3 in nodelist:
        if n3<=n2: continue
        count=count+1
        hub(n2,n3)
        M=nx.union(K,L) # join two graphs
        w23=G.get_edge_data(n2, n3)['weight']   # get edge weight between two hubs
        M.add_edge(n2,n3,weight = w23*bundling)        # add an edge between two hubs, with defined bundling coefficient.
        d['M'+str(n2+n3)]=M         # creates a dictionary for generated Graphs.
        #nx.draw(M)
        #plt.show()
        K.clear()
        L.clear()

#   The function below calculates overall path lengths between all nodes in the graph.
def klin(X):
    total=0
    allDist=dict(nx.all_pairs_dijkstra_path_length(X, cutoff=None, weight='weight'))
    for a, b in allDist.items():
        for c,d in b.items():
            total=total+d
    return(total)

# below we find the best graph  in terms of overall shortest paths  between all nodes.
bestD=None      # variable for shortest total distance
bestG=None      # best Graph in terms of Klincewicz algorithm
for k, v in d.items():
    graphTotal=klin(v)
    print('Graph', k,':',graphTotal)
    if bestD is None or graphTotal<=bestD:
        bestD=graphTotal
        bestG=k
print('Result:', str(bestG), 'has the shortest distance with', bestD, 'units in', count, 'Graphs')
