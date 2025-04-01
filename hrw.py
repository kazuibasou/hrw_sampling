import numpy as np
import hypergraph

def projected_random_walk(H:hypergraph.HyperGraph, r: int):

    sampling_lst = []
    queried_node = {v: 0 for v in H.V}
    queried_hyperedge = {m: 0 for m in range(0, H.M)}

    v = np.random.choice(list(H.V))
    norm = np.sum([len(H.E[m]) - 1 for m in H.elist[v]])
    p = [float(len(H.E[m]) - 1)/norm for m in H.elist[v]]
    m = np.random.choice(H.elist[v], p=p)

    queried_node[v] = 1
    for m_ in H.elist[v]:
        queried_hyperedge[m_] = 1

    sampling_lst.append((v, H.elist[v], m, H.E[m]))

    while len(sampling_lst) < r:
        flag = True
        while flag:
            nextv = np.random.choice(H.E[m])
            if nextv != v:
                v = nextv
                flag = False

        norm = np.sum([len(H.E[m]) - 1 for m in H.elist[v]])
        p = [float(len(H.E[m]) - 1) / norm for m in H.elist[v]]
        m = np.random.choice(H.elist[v], p=p)

        queried_node[v] = 1
        for m_ in H.elist[v]:
            queried_hyperedge[m_] = 1

        sampling_lst.append((v, H.elist[v], m, H.E[m]))

    return sampling_lst, queried_node, queried_hyperedge

def Carletti_random_walk(H:hypergraph.HyperGraph, r: int):

    sampling_lst = []
    queried_node = {v: 0 for v in H.V}
    queried_hyperedge = {m: 0 for m in range(0, H.M)}

    v = np.random.choice(list(H.V))
    norm = np.sum([pow(len(H.E[m]) - 1, 2) for m in H.elist[v]])
    p = [float(pow(len(H.E[m]) - 1, 2))/norm for m in H.elist[v]]
    m = np.random.choice(H.elist[v], p=p)

    queried_node[v] = 1
    for m_ in H.elist[v]:
        queried_hyperedge[m_] = 1

    sampling_lst.append((v, H.elist[v], m, H.E[m]))

    while len(sampling_lst) < r:
        flag = True
        while flag:
            nextv = np.random.choice(H.E[m])
            if nextv != v:
                v = nextv
                flag = False

        norm = np.sum([pow(len(H.E[m]) - 1, 2) for m in H.elist[v]])
        p = [float(pow(len(H.E[m]) - 1, 2)) / norm for m in H.elist[v]]
        m = np.random.choice(H.elist[v], p=p)

        queried_node[v] = 1
        for m_ in H.elist[v]:
            queried_hyperedge[m_] = 1

        sampling_lst.append((v, H.elist[v], m, H.E[m]))

    return sampling_lst, queried_node, queried_hyperedge

def higher_order_random_walk(H:hypergraph.HyperGraph, r: int, seed_v: int, seed_m: int):
    sampling_lst = []
    queried_node = {v: 0 for v in H.V}
    queried_hyperedge = {m: 0 for m in range(0, H.M)}

    v = seed_v
    m = seed_m

    queried_node[v] = 1
    queried_hyperedge[m] = 1

    sampling_lst.append((v, H.elist[v], m, H.E[m]))

    while len(sampling_lst) < r:
        flag = True
        while flag:
            nextv = np.random.choice(H.E[m])
            if nextv != v:
                v = nextv
                flag = False

        m = np.random.choice(H.elist[v])

        queried_node[v] = 1
        queried_hyperedge[m] = 1

        sampling_lst.append((v, H.elist[v], m, H.E[m]))

    return sampling_lst, queried_node, queried_hyperedge

def non_backtracking_higher_order_random_walk(H:hypergraph.HyperGraph, r: int, seed_v: int, seed_m: int):
    sampling_lst = []
    queried_node = {v: 0 for v in H.V}
    queried_hyperedge = {m: 0 for m in range(0, H.M)}

    v = seed_v
    m = seed_m

    queried_node[v] = 1
    queried_hyperedge[m] = 1

    sampling_lst.append((v, H.elist[v], m, H.E[m]))

    while len(sampling_lst) < r:
        flag = True
        while flag:
            nextv = np.random.choice(H.E[m])
            if nextv != v:
                v = nextv
                flag = False

        if len(H.elist[v]) == 0:
            print("ERROR: zero node degree")
            exit()
        elif len(H.elist[v]) == 1:
            m = np.random.choice(H.elist[v])
        else:
            flag = True
            while flag:
                nextm = np.random.choice(H.elist[v])
                if nextm != m:
                    m = nextm
                    flag = False

        queried_node[v] = 1
        queried_hyperedge[m] = 1

        sampling_lst.append((v, H.elist[v], m, H.E[m]))

    return sampling_lst, queried_node, queried_hyperedge

def calc_num_queries(sampling_lst: list, hrw_: str):

    if hrw_ in {'PRW', 'CRW'}:
        num_queries = len(sampling_lst) + sum([len(x[1]) for x in sampling_lst])
    elif hrw_ in {'LRW', 'NBRW'}:
        num_queries = len(sampling_lst) * 2
    else:
        print("ERROR: given random walk is not supported.")
        exit()

    return num_queries

def sample_repeated_ratio(sampling_lst: list, hrw_: str, l: int):

    if l == 1:
        if hrw_ in {'LRW', 'NBRW'}:
            node_sample_repeated_ratio = float(len([k for k in range(1, len(sampling_lst))
                                               if sampling_lst[k][0] == sampling_lst[k-1][0]])) / (len(sampling_lst)-1)
            hyperedge_sample_repeated_ratio = float(len([k for k in range(1, len(sampling_lst))
                                               if sampling_lst[k][2] == sampling_lst[k - 1][2]])) / (len(sampling_lst) - 1)
        else:
            print("ERROR: given random walk is not supported.")
            exit()
    elif l == 2:
        if hrw_ in {'LRW', 'NBRW'}:
            node_sample_repeated_ratio = float(len([k for k in range(2, len(sampling_lst))
                                               if sampling_lst[k][0] in {sampling_lst[k-1][0], sampling_lst[k-2][0]}])) / (len(sampling_lst)-2)
            hyperedge_sample_repeated_ratio = float(len([k for k in range(2, len(sampling_lst))
                                               if sampling_lst[k][2] in {sampling_lst[k-1][2], sampling_lst[k-2][2]}])) / (len(sampling_lst)-2)
        else:
            print("ERROR: given random walk is not supported.")
            exit()
    else:
        print("ERROR: given length l is not valid.")
        exit()

    return node_sample_repeated_ratio, hyperedge_sample_repeated_ratio

def average_node_degree_estimator(sampling_lst: list):

    return float(1) / (np.average([float(1) / len(sampling_lst[i][1]) for i in range(1, len(sampling_lst))]))

def node_degree_dist_estimator(sampling_lst: list):
    Phi = np.sum([float(1) / len(sampling_lst[k][1]) for k in range(1, len(sampling_lst))])
    Phi_ = {}

    for k in range(1, len(sampling_lst)):
        x = sampling_lst[k]
        d = len(x[1])
        Phi_[d] = Phi_.get(d, 0) + float(1) / d

    return {d: float(Phi_[d]) / Phi for d in Phi_}

def average_hyperedge_size_estimator(sampling_lst: list):

    return float(1) / np.average([float(1) / (len(sampling_lst[k][3])) for k in range(1, len(sampling_lst))])

def hyperedge_size_dist_estimator(sampling_lst: list):
    Psi = np.sum([float(1) / len(sampling_lst[k][3]) for k in range(1, len(sampling_lst))])
    Psi_ = {}

    for k in range(1, len(sampling_lst)):
        x = sampling_lst[k]
        s = len(x[3])
        Psi_[s] = Psi_.get(s, 0) + float(1) / s

    return {s: float(Psi_[s]) / Psi for s in Psi_}
