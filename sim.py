import math
import numpy as np
from collections import defaultdict
import hypergraph
import hrw

def calc_NRMSE(true_value: float, est_lst: list):

    return math.sqrt(np.average([math.pow((float(est_lst[i])/true_value)-1, 2) for i in range(0, len(est_lst))]))

def calc_L1_dist(true_dist: dict, est_dist: dict):
    l1_dist = 0
    for k in true_dist:
        l1_dist += math.fabs(true_dist[k] - est_dist.get(k, 0))

    return l1_dist

def calc_NRMSE_for_dist(true_dist: dict, est_lst: list):

    return math.sqrt(np.average([math.pow(calc_L1_dist(true_dist, est_lst[i]), 2) for i in range(0, len(est_lst))]))

def calc_l1_distance(true_dist, sampling_lst):
    sample_dist = defaultdict(float)
    for x in sampling_lst:
        v, m = x[0], x[2]
        sample_dist[(v, m)] += 1

    for (v, m) in sample_dist:
        sample_dist[(v, m)] = float(sample_dist[(v, m)]) / len(sampling_lst)

    return sum([math.fabs(true_dist[(v, m)] - sample_dist.get((v, m), 0)) for (v, m) in true_dist])

# Evaluation of number of queries
def sim_1(hypergraph_name: str, min_r:int, max_r: int, num_runs: int):

    num_queries_to_nodes = {
        'PRW': {r: [] for r in range(min_r, max_r + 1, 10)},
        'CRW': {r: [] for r in range(min_r, max_r + 1, 10)},
        'HORW': {r: [] for r in range(min_r, max_r + 1, 10)},
        'NBHORW': {r: [] for r in range(min_r, max_r + 1, 10)},
    }

    num_queries_to_hyperedges = {
        'PRW': {r: [] for r in range(min_r, max_r + 1, 10)},
        'CRW': {r: [] for r in range(min_r, max_r + 1, 10)},
        'HORW': {r: [] for r in range(min_r, max_r + 1, 10)},
        'NBHORW': {r: [] for r in range(min_r, max_r + 1, 10)},
    }

    H = hypergraph.read_hypergraph(hypergraph_name)

    for i in range(num_runs):

        sampling_lst, queried_node, queried_hyperedge = hrw.projected_random_walk(H, max_r)

        for r in range(min_r, max_r + 1, 10):

            n_q_v, n_q_e = hrw.calc_num_queries(sampling_lst[:r], 'PRW')
            num_queries_to_nodes['PRW'][r].append(n_q_v)
            num_queries_to_hyperedges['PRW'][r].append(n_q_e)

        sampling_lst, queried_node, queried_hyperedge = hrw.Carletti_random_walk(H, max_r)

        for r in range(min_r, max_r + 1, 10):

            n_q_v, n_q_e = hrw.calc_num_queries(sampling_lst[:r], 'CRW')
            num_queries_to_nodes['CRW'][r].append(n_q_v)
            num_queries_to_hyperedges['CRW'][r].append(n_q_e)

        #sampling_lst, queried_node, queried_hyperedge = hrw.higher_order_random_walk(H, max_r)

        for r in range(min_r, max_r + 1, 10):
            #n_q = hrw.calc_num_queries(sampling_lst[:r], 'HORW')
            num_queries_to_nodes['HORW'][r].append(r)
            num_queries_to_hyperedges['HORW'][r].append(r)

        #sampling_lst, queried_node, queried_hyperedge = hrw.non_backtracking_higher_order_random_walk(H, max_r)

        for r in range(min_r, max_r + 1, 10):
            #n_q = hrw.calc_num_queries(sampling_lst[:r], 'NBHORW')
            num_queries_to_nodes['NBHORW'][r].append(r)
            num_queries_to_hyperedges['NBHORW'][r].append(r)

    for rw in ["PRW", "CRW", "HORW", 'NBHORW']:
        with open("./results/" + hypergraph_name + "_number_of_queries_to_nodes_" + rw + ".txt", mode='w') as f:
            for r in range(min_r, max_r + 1, 10):
                f.write(",".join([str(r), str(np.average(num_queries_to_nodes[rw][r]))]) + "\n")

    for rw in ["PRW", "CRW", "HORW", 'NBHORW']:
        with open("./results/" + hypergraph_name + "_number_of_queries_to_hyperedges_" + rw + ".txt", mode='w') as f:
            for r in range(min_r, max_r + 1, 10):
                f.write(",".join([str(r), str(np.average(num_queries_to_hyperedges[rw][r]))]) + "\n")

    return

# Evaluation of average node degree estimator
def sim_2(hypergraph_name: str, min_r:int, max_r: int, num_runs: int):

    H: hypergraph.HyperGraph = hypergraph.read_hypergraph(hypergraph_name)

    est_lst = {r: [] for r in range(min_r, max_r + 1, 10)}
    est_lst_ = {r: [] for r in range(min_r, max_r + 1, 10)}
    true_val = np.average([len(H.elist[v]) for v in H.V])

    for i in range(num_runs):
        seed_v = np.random.choice(list(H.V))
        seed_m = np.random.choice(H.elist[seed_v])

        sampling_lst, queried_node, queried_hyperedge = hrw.higher_order_random_walk(H, max_r, seed_v, seed_m)
        for r in range(min_r, max_r + 1, 10):
            x = hrw.average_node_degree_estimator(sampling_lst[:r])
            est_lst[r].append(x)

        sampling_lst, queried_node, queried_hyperedge = hrw.non_backtracking_higher_order_random_walk(H, max_r, seed_v, seed_m)
        for r in range(min_r, max_r + 1, 10):
            x = hrw.average_node_degree_estimator(sampling_lst[:r])
            est_lst_[r].append(x)

    with open("./results/" + hypergraph_name + "_average_node_degree_nrmse_horw.txt", mode='w') as f:
        for r in range(min_r, max_r + 1, 10):
            nrmse = calc_NRMSE(true_val, est_lst[r])
            f.write(",".join([str(r), str(nrmse)]) + "\n")

    with open("./results/" + hypergraph_name + "_average_node_degree_nrmse_nbhorw.txt", mode='w') as f:
        for r in range(min_r, max_r + 1, 10):
            nrmse = calc_NRMSE(true_val, est_lst_[r])
            f.write(",".join([str(r), str(nrmse)]) + "\n")

    return

# Evaluation of node degree distribution estimator
def sim_3(hypergraph_name: str, min_r: int, max_r: int, num_runs: int):

    H: hypergraph.HyperGraph = hypergraph.read_hypergraph(hypergraph_name)

    est_lst = {r: [] for r in range(min_r, max_r + 1, 10)}
    est_lst_ = {r: [] for r in range(min_r, max_r + 1, 10)}
    true_dist = H.node_degree_distribution(func='prob')

    for i in range(num_runs):
        seed_v = np.random.choice(list(H.V))
        seed_m = np.random.choice(H.elist[seed_v])

        sampling_lst, queried_node, queried_hyperedge = hrw.higher_order_random_walk(H, max_r, seed_v, seed_m)
        for r in range(min_r, max_r + 1, 10):
            x = hrw.node_degree_dist_estimator(sampling_lst[:r])
            est_lst[r].append(x)

        sampling_lst, queried_node, queried_hyperedge = hrw.non_backtracking_higher_order_random_walk(H, max_r, seed_v, seed_m)
        for r in range(min_r, max_r + 1, 10):
            x = hrw.node_degree_dist_estimator(sampling_lst[:r])
            est_lst_[r].append(x)

    with open("./results/" + hypergraph_name + "_node_degree_dist_nrmse_horw.txt", mode='w') as f:
        for r in range(min_r, max_r + 1, 10):
            nrmse = calc_NRMSE_for_dist(true_dist, est_lst[r])
            f.write(",".join([str(r), str(nrmse)]) + "\n")

    with open("./results/" + hypergraph_name + "_node_degree_dist_nrmse_nbhorw.txt", mode='w') as f:
        for r in range(min_r, max_r + 1, 10):
            nrmse = calc_NRMSE_for_dist(true_dist, est_lst_[r])
            f.write(",".join([str(r), str(nrmse)]) + "\n")

    return

# Evaluation of average hyperedge size estimator
def sim_4(hypergraph_name: str, min_r:int, max_r: int, num_runs: int):

    H: hypergraph.HyperGraph = hypergraph.read_hypergraph(hypergraph_name)
    est_lst = {r: [] for r in range(min_r, max_r + 1, 10)}
    est_lst_ = {r: [] for r in range(min_r, max_r + 1, 10)}
    true_val = np.average([len(H.E[m]) for m in range(0, H.M)])

    for i in range(num_runs):
        seed_v = np.random.choice(list(H.V))
        seed_m = np.random.choice(H.elist[seed_v])

        sampling_lst, queried_node, queried_hyperedge = hrw.higher_order_random_walk(H, max_r, seed_v, seed_m)
        for r in range(min_r, max_r + 1, 10):
            x = hrw.average_hyperedge_size_estimator(sampling_lst[:r])
            est_lst[r].append(x)

        sampling_lst, queried_node, queried_hyperedge = hrw.non_backtracking_higher_order_random_walk(H, max_r, seed_v, seed_m)
        for r in range(min_r, max_r + 1, 10):
            x = hrw.average_hyperedge_size_estimator(sampling_lst[:r])
            est_lst_[r].append(x)

    with open("./results/" + hypergraph_name + "_average_hyperedge_size_nrmse_horw.txt", mode='w') as f:
        for r in range(min_r, max_r + 1, 10):
            nrmse = calc_NRMSE(true_val, est_lst[r])
            f.write(",".join([str(r), str(nrmse)]) + "\n")

    with open("./results/" + hypergraph_name + "_average_hyperedge_size_nrmse_nbhorw.txt", mode='w') as f:
        for r in range(min_r, max_r + 1, 10):
            nrmse = calc_NRMSE(true_val, est_lst_[r])
            f.write(",".join([str(r), str(nrmse)]) + "\n")

    return

# Evaluation of hyperedge size distribution estimator
def sim_5(hypergraph_name: str, min_r: int, max_r: int, num_runs: int):

    H: hypergraph.HyperGraph = hypergraph.read_hypergraph(hypergraph_name)
    est_lst = {r: [] for r in range(min_r, max_r + 1, 10)}
    est_lst_ = {r: [] for r in range(min_r, max_r + 1, 10)}
    true_dist = H.hyperedge_size_distribution(func='prob')

    for i in range(num_runs):
        seed_v = np.random.choice(list(H.V))
        seed_m = np.random.choice(H.elist[seed_v])

        sampling_lst, queried_node, queried_hyperedge = hrw.higher_order_random_walk(H, max_r, seed_v, seed_m)
        for r in range(min_r, max_r + 1, 10):
            x = hrw.hyperedge_size_dist_estimator(sampling_lst[:r])
            est_lst[r].append(x)

        sampling_lst, queried_node, queried_hyperedge = hrw.non_backtracking_higher_order_random_walk(H, max_r, seed_v, seed_m)
        for r in range(min_r, max_r + 1, 10):
            x = hrw.hyperedge_size_dist_estimator(sampling_lst[:r])
            est_lst_[r].append(x)

    with open("./results/" + hypergraph_name + "_hyperedge_size_dist_nrmse_horw.txt", mode='w') as f:
        for r in range(min_r, max_r + 1, 10):
            nrmse = calc_NRMSE_for_dist(true_dist, est_lst[r])
            f.write(",".join([str(r), str(nrmse)]) + "\n")

    with open("./results/" + hypergraph_name + "_hyperedge_size_dist_nrmse_nbhorw.txt", mode='w') as f:
        for r in range(min_r, max_r + 1, 10):
            nrmse = calc_NRMSE_for_dist(true_dist, est_lst_[r])
            f.write(",".join([str(r), str(nrmse)]) + "\n")

    return

# Evaluation of node degree distribution estimator by node degree
def sim_6(hypergraph_name: str, r: int, num_runs: int):

    H: hypergraph.HyperGraph = hypergraph.read_hypergraph(hypergraph_name)

    true_dist = H.node_degree_distribution(func='prob')
    node_degree_set = set(list(true_dist.keys()))
    est_lst = {k: [] for k in node_degree_set}
    est_lst_ = {k: [] for k in node_degree_set}

    for i in range(num_runs):
        seed_v = np.random.choice(list(H.V))
        seed_m = np.random.choice(H.elist[seed_v])

        sampling_lst, queried_node, queried_hyperedge = hrw.higher_order_random_walk(H, r, seed_v, seed_m)
        x = hrw.node_degree_dist_estimator(sampling_lst[:r])
        for k in node_degree_set:
            est_lst[k].append(x.get(k, 0.0))

        sampling_lst, queried_node, queried_hyperedge = hrw.non_backtracking_higher_order_random_walk(H, r, seed_v, seed_m)
        x = hrw.node_degree_dist_estimator(sampling_lst[:r])
        for k in node_degree_set:
            est_lst_[k].append(x.get(k, 0.0))

    with open("./results/" + hypergraph_name + "_node_degree_dist_by_k_nrmse_horw.txt", mode='w') as f:
        for k in node_degree_set:
            nrmse = calc_NRMSE(true_dist[k], est_lst[k])
            f.write(",".join([str(k), str(nrmse)]) + "\n")

    with open("./results/" + hypergraph_name + "_node_degree_dist_by_k_nrmse_nbhorw.txt", mode='w') as f:
        for k in node_degree_set:
            nrmse = calc_NRMSE(true_dist[k], est_lst_[k])
            f.write(",".join([str(k), str(nrmse)]) + "\n")

    return

# Evaluation of hyperedge size distribution estimator by hyperedge size
def sim_7(hypergraph_name: str, r: int, num_runs: int):
    H: hypergraph.HyperGraph = hypergraph.read_hypergraph(hypergraph_name)

    true_dist = H.hyperedge_size_distribution(func='prob')
    hyperedge_size_set = set(list(true_dist.keys()))
    est_lst = {s: [] for s in hyperedge_size_set}
    est_lst_ = {s: [] for s in hyperedge_size_set}

    for i in range(num_runs):
        seed_v = np.random.choice(list(H.V))
        seed_m = np.random.choice(H.elist[seed_v])

        sampling_lst, queried_node, queried_hyperedge = hrw.higher_order_random_walk(H, r, seed_v, seed_m)
        x = hrw.hyperedge_size_dist_estimator(sampling_lst[:r])
        for s in hyperedge_size_set:
            est_lst[s].append(x.get(s, 0.0))

        sampling_lst, queried_node, queried_hyperedge = hrw.non_backtracking_higher_order_random_walk(H, r, seed_v, seed_m)
        x = hrw.hyperedge_size_dist_estimator(sampling_lst[:r])
        for s in hyperedge_size_set:
            est_lst_[s].append(x.get(s, 0.0))

    with open("./results/" + hypergraph_name + "_hyperedge_size_dist_by_s_nrmse_horw.txt", mode='w') as f:
        for s in hyperedge_size_set:
            nrmse = calc_NRMSE(true_dist[s], est_lst[s])
            f.write(",".join([str(s), str(nrmse)]) + "\n")

    with open("./results/" + hypergraph_name + "_hyperedge_size_dist_by_s_nrmse_nbhorw.txt", mode='w') as f:
        for s in hyperedge_size_set:
            nrmse = calc_NRMSE(true_dist[s], est_lst_[s])
            f.write(",".join([str(s), str(nrmse)]) + "\n")

    return

# Evaluation of sample repeated ratio
def sim_8(hypergraph_name: str, min_r:int, max_r: int, num_runs: int):

    node_sample_repeated_ratio = {
        'HORW': {r: [] for r in range(min_r, max_r + 1, 10)},
        'NBHORW': {r: [] for r in range(min_r, max_r + 1, 10)},
    }

    hyperedge_sample_repeated_ratio = {
        'HORW': {r: [] for r in range(min_r, max_r + 1, 10)},
        'NBHORW': {r: [] for r in range(min_r, max_r + 1, 10)},
    }

    H = hypergraph.read_hypergraph(hypergraph_name)

    for i in range(num_runs):

        seed_v = np.random.choice(list(H.V))
        seed_m = np.random.choice(H.elist[seed_v])

        sampling_lst, queried_node, queried_hyperedge = hrw.higher_order_random_walk(H, max_r, seed_v, seed_m)

        for r in range(min_r, max_r + 1, 10):
            r_v, r_e = hrw.sample_repeated_ratio(sampling_lst[:r], 'HORW', l=1)
            node_sample_repeated_ratio['HORW'][r].append(r_v)
            hyperedge_sample_repeated_ratio['HORW'][r].append(r_e)

        sampling_lst, queried_node, queried_hyperedge = hrw.non_backtracking_higher_order_random_walk(H, max_r, seed_v, seed_m)

        for r in range(min_r, max_r + 1, 10):
            r_v, r_e = hrw.sample_repeated_ratio(sampling_lst[:r], 'NBHORW', l=1)
            node_sample_repeated_ratio['NBHORW'][r].append(r_v)
            hyperedge_sample_repeated_ratio['NBHORW'][r].append(r_e)

    for rw in ["HORW", 'NBHORW']:
        with open("./results/" + hypergraph_name + "_node_sample_repeated_ratio_" + rw + ".txt", mode='w') as f:
            for r in range(min_r, max_r + 1, 10):
                f.write(",".join([str(r), str(np.average(node_sample_repeated_ratio[rw][r]))]) + "\n")

    for rw in ["HORW", 'NBHORW']:
        with open("./results/" + hypergraph_name + "_hyperedge_sample_repeated_ratio_" + rw + ".txt", mode='w') as f:
            for r in range(min_r, max_r + 1, 10):
                f.write(",".join([str(r), str(np.average(hyperedge_sample_repeated_ratio[rw][r]))]) + "\n")

    return