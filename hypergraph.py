import numpy as np
from collections import Counter
from collections import deque
import pickle
import os

class HyperGraph():
    N = 0
    M = 0
    V = set()
    E = []
    elist = dict({})

    def __init__(self):
        self.N = 0
        self.M = 0
        self.V = set()
        self.E = []
        self.elist = {}

    def nodes(self):

        return set(self.V)

    def hyperedges(self):

        return list(self.E)

    def is_connected(self):

        searched = {v: 0 for v in self.V}
        nodes = set()
        v = np.random.choice(list(self.V))

        Q = deque()
        searched[v] = 1
        Q.append(v)
        while len(Q) > 0:
            v = Q.popleft()
            nodes.add(v)
            for m in self.elist[v]:
                for w in self.E[m]:
                    if searched[w] == 0:
                        searched[w] = 1
                        Q.append(w)

        return self.N == sum(list(searched.values()))

    def node_degree(self, v=None, ndarray=False):
        if v is None:
            if ndarray is False:
                node_degree = {}
                for m in range(0, self.M):
                    for v in self.E[m]:
                        node_degree[v] = node_degree.get(v, 0) + 1
                return node_degree
            else:
                node_degree = np.zeros(self.N, dtype=int)
                for m in range(0, self.M):
                    for v in self.E[m]:
                        node_degree[v] += 1
                return node_degree
        elif v not in self.elist:
            print("ERROR: node index is out of range.")
            return -1
        else:
            return len(self.elist[v])

    def hyperedge_size(self, m=None, ndarray=False):
        if m is None:
            if ndarray is False:
                return {m: len(self.E[m]) for m in range(0, self.M)}
            else:
                l = np.zeros(self.M, dtype=int)
                for m in range(0, self.M):
                    l[m] = len(self.E[m])
                return l
        elif m < 0 or m >= self.M:
            print("ERROR: hyperedge index is out of range.")
            return -1
        else:
            return len(self.E[m])

    def node_degree_distribution(self, func):
        if func == 'freq':
            return dict(Counter(list(self.node_degree().values())))
        elif func == 'prob':
            d = dict(Counter(list(self.node_degree().values())))
            return {k: float(d[k])/self.N for k in d}
        elif func == 'survival':
            d_ = dict(Counter(list(self.node_degree().values())))
            lst = sorted(list(d_.items()), key=lambda x:x[0], reverse=False)
            d = {}
            for i in range(0, len(lst)):
                k = lst[i][0]
                n = sum([lst[j][1] for j in range(i, len(lst))])
                d[k] = float(n)/self.N
            return d
        else:
            print("ERROR: given function is not supported.")
            return {}

    def hyperedge_size_distribution(self, func):
        if func == 'freq':
            return dict(Counter(list(self.hyperedge_size().values())))
        elif func == 'prob':
            d = dict(Counter(list(self.hyperedge_size().values())))
            return {k: float(d[k])/self.M for k in d}
        elif func == 'survival':
            d_ = dict(Counter(list(self.hyperedge_size().values())))
            lst = sorted(list(d_.items()), key=lambda x:x[0], reverse=False)
            d = {}
            for i in range(0, len(lst)):
                k = lst[i][0]
                n = sum([lst[j][1] for j in range(i, len(lst))])
                d[k] = float(n)/self.M
            return d
        else:
            print("ERROR: given function is not supported.")
            return {}

    def print_info(self):

        node_degree = {i: 0 for i in self.V}
        hyperedge_size = {m: 0 for m in range(0, self.M)}
        for m in range(0, self.M):
            for i in self.E[m]:
                node_degree[i] += 1
            hyperedge_size[m] = len(self.E[m])

        node_degree_lst = list(node_degree.values())
        hyperedge_size_lst = list(hyperedge_size.values())

        print("Number of nodes:", self.N)
        print("Number of hyperedges:", self.M)
        print("Average degree of node:", float(sum(node_degree_lst)) / self.N)
        print("Minimum degree of node:", min(node_degree_lst))
        print("Maximum degree of node:", max(node_degree_lst))
        print("Average size of hyperedge:", float(sum(hyperedge_size_lst)) / self.M)
        print("Minimum size of hyperedge:", min(hyperedge_size_lst))
        print("Maximum size of hyperedge:", max(hyperedge_size_lst))
        print("Proportion of nodes with degree one:", float(len([i for i in self.V if node_degree[i] == 1])) / self.N)
        print("Hypergraph is connected:", self.is_connected())
        print()

        return

def construct_hypergraph_from_hyperedge_list(E: list):
    H = HyperGraph()

    V = []
    for m in range(0, len(E)):
        e = E[m]
        V += list(e)
        for v in e:
            if v not in H.elist:
                H.elist[v] = []
            H.elist[v].append(m)

    H.V = set(V)
    H.N = len(H.V)
    H.E = E
    H.M = len(H.E)

    return H

def construct_hypergraph():

    dataset_name = {
        'coauth-DBLP-full': 'dblp',
        'coauth-MAG-Geology-full': 'mag-geology',
        'coauth-MAG-History-full': 'mag-history',
        'amazon-reviews': 'amazon',
        'threads-stack-overflow-full': 'stack-overflow',
    }

    for hypergraph_name in dataset_name:

        if hypergraph_name in {'coauth-DBLP-full', 'coauth-MAG-Geology-full', 'coauth-MAG-History-full', 'threads-stack-overflow-full'}:

            f1_path = "./data/" + str(hypergraph_name) + "/" + str(hypergraph_name) + "-nverts.txt"
            f1 = open(f1_path, 'r')
            f2_path = "./data/" + str(hypergraph_name) + "/" + str(hypergraph_name) + "-simplices.txt"
            f2 = open(f2_path, 'r')

            lines1 = f1.readlines()
            lines2 = f2.readlines()

            E = []
            c = 0
            for line1 in lines1:
                nv = int(line1[:-1].split(" ")[0])
                if nv < 2:
                    continue
                e = []
                for i in range(0, nv):
                    v = int(lines2[c+i][:-1])
                    e.append(v)
                e = list(set(e))
                if len(e) < 2:
                    continue
                E.append(e)
                c += nv

            f1.close()
            f2.close()

            H = construct_hypergraph_from_hyperedge_list(E)
            H_lcc = extract_largest_connected_component(H)
            print(hypergraph_name, "Number of nodes", H_lcc.N, "Number of hyperedges", H_lcc.M)

            with open("./data/" + dataset_name[hypergraph_name] + ".pickle", mode='wb') as f:
                pickle.dump(H_lcc, f)

        elif hypergraph_name == 'cat-edge-MAG-10':
            f1_path = "./data/" + str(hypergraph_name) + "/hyperedges.txt"
            f1 = open(f1_path, 'r')

            lines1 = f1.readlines()

            E = []
            c = 0
            for line1 in lines1:
                e = list(set(list(line1[:-1].split("	"))))
                if len(e) < 2:
                    continue
                E.append(e)
                c += len(e)

            f1.close()

            H = construct_hypergraph_from_hyperedge_list(E)
            H_lcc = extract_largest_connected_component(H)
            print(hypergraph_name, "Number of nodes", H_lcc.N, "Number of hyperedges", H_lcc.M)

            with open("./data/" + dataset_name[hypergraph_name] + ".pickle", mode='wb') as f:
                pickle.dump(H_lcc, f)

        elif hypergraph_name in {'contact-primary-school', 'contact-high-school', 'amazon-reviews'}:
            f1_path = "./data/" + str(hypergraph_name) + "/hyperedges-" + str(hypergraph_name) + ".txt"
            f1 = open(f1_path, 'r')

            lines1 = f1.readlines()

            E = []
            c = 0
            for line1 in lines1:
                e = list(set(list(line1[:-1].split(","))))
                if len(e) < 2:
                    continue
                E.append(e)
                c += len(e)

            f1.close()

            H = construct_hypergraph_from_hyperedge_list(E)
            H_lcc = extract_largest_connected_component(H)
            print(hypergraph_name, "Number of nodes", H_lcc.N, "Number of hyperedges", H_lcc.M)

            with open("./data/" + dataset_name[hypergraph_name] + ".pickle", mode='wb') as f:
                pickle.dump(H_lcc, f)

    return

def extract_largest_connected_component(H: HyperGraph):

    N = H.N
    searched = {v: 0 for v in H.V}
    lcc_nodes = set()
    lcc_hyperedges = set()
    while len(lcc_nodes) < N - sum(list(searched.values())):

        v = min([v_ for v_ in H.V if searched[v_] == 0])
        hyperedges_ = set()
        nodes_ = set()

        Q = deque()
        searched[v] = 1
        Q.append(v)
        while len(Q) > 0:
            v = Q.pop()
            nodes_.add(v)
            for m in H.elist[v]:
                hyperedges_.add(m)
                for w in H.E[m]:
                    if searched[w] == 0:
                        searched[w] = 1
                        Q.append(w)

        if len(nodes_) > len(lcc_nodes):
            lcc_nodes = nodes_
            lcc_hyperedges = hyperedges_

    H_lcc = construct_hypergraph_from_hyperedge_list([H.E[m] for m in sorted(list(lcc_hyperedges))])

    return H_lcc

def read_hypergraph(hypergraph_name, print_info=False):
    if not os.path.isfile("./data/" + hypergraph_name + ".pickle"):
        print("ERROR: given hypergraph data is not found.")
        return

    with open("./data/" + hypergraph_name + ".pickle", mode="rb") as f:
        H = pickle.load(f)

    if print_info:
        H.print_info()

    return H
