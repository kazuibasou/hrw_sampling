import time
import pickle
import requests
import numpy as np
import math
import datetime
import collections
from collections import defaultdict
import pycountry_convert as pc

# We checked that our code worked well against the OpenAlex API as of February 2025.

def get_single_work(work_id):
    try:
        url = "https://api.openalex.org/works/" + str(work_id)
        headers = {"User-Agent": 'Mozilla/5.0'}
        r = requests.get(url, headers=headers)
        d = r.json()
        return {key: d[key] for key in ['id', 'authorships', 'primary_topic', 'open_access']}
    except Exception as e:
        time.sleep(60)
        return {}

def get_work_list(author_id):
    try:
        url = "https://api.openalex.org/works?per-page=200&filter=author.id:" + author_id
        headers = {"User-Agent": 'Mozilla/5.0'}
        r = requests.get(url, headers=headers)

        d = r.json()

        if "meta" not in d:
            return []

        if "count" not in d["meta"] or "per_page" not in d["meta"]:
            return []

        work_count = int(d["meta"]["count"])
        per_page = int(d["meta"]["per_page"])
        num_pages = int(math.ceil(float(work_count) / per_page))

        work_lst = []
        for i in range(num_pages):
            url = "https://api.openalex.org/works?page=" + str(i+1) + "&per-page=200&filter=author.id:" + author_id
            headers = {"User-Agent": 'Mozilla/5.0'}
            r = requests.get(url, headers=headers)

            d_i = r.json()
            if int(d_i["meta"]["page"]) != i + 1:
                print("ERROR: page number is wrong.", int(d_i["meta"]["page"]), i + 1)

            for work in d_i["results"]:
                if len(work['authorships']) > 1:
                    work_lst.append({key: work[key] for key in ['id', 'authorships', 'primary_topic', 'open_access']})

        # if len(work_lst) != work_count:
        #     print("ERROR: work count is wrong.", len(work_lst), work_count)

        return work_lst
    except Exception as e:
        time.sleep(60)
        return {}

def horw(num_samples, restart):

    if restart:
        with open("./data/openalex_sampling_lst.pickle", mode="rb") as f:
            sampling_lst = pickle.load(f)
        (a_id, w_id, work_lst, work, a_lst) = sampling_lst[-1]
    else:
        sampling_lst = []

        a_id = "A5088448789" # "Federico Battiston"
        w_id = "W3035258118" # https://doi.org/10.1016/j.physrep.2020.05.004

        work_lst = get_work_list(a_id)
        work = get_single_work(w_id)
        a_lst = list(work['authorships'])

        sampling_lst.append((a_id, w_id, work_lst, work, a_lst))
        print(datetime.datetime.now(), a_id, w_id, len(work_lst), len(a_lst))

    flag = True
    while flag:
        next_a = np.random.choice(a_lst, size=1)[0]
        if 'author' not in next_a or 'id' not in next_a['author']:
            continue
        next_a_id = str(next_a['author']['id']).replace("https://openalex.org/", "")
        if next_a_id == a_id:
            continue
        next_work_lst = get_work_list(next_a_id)
        if len(next_work_lst) > 0:
            flag = False
            a_id = next_a_id
            work_lst = next_work_lst

    num_samples_per_sleep = 100
    ii = 1

    while len(sampling_lst) < num_samples:
        print(len(sampling_lst))

        flag = True
        while flag:
            next_work = np.random.choice(work_lst, size=1)[0]
            if 'id' not in next_work or 'authorships' not in next_work:
                continue
            next_w_id = next_work['id'].replace("https://openalex.org/", "")
            if len(next_work["authorships"]) >= 2:
                flag = False
                w_id = next_w_id
                work = next_work

        a_lst = list(work['authorships'])

        sampling_lst.append((a_id, w_id, work_lst, work, a_lst))
        print(datetime.datetime.now(), a_id, w_id, len(work_lst), len(a_lst))

        flag = True
        while flag:
            next_a = np.random.choice(a_lst, size=1)[0]
            if 'author' not in next_a or 'id' not in next_a['author']:
                continue
            next_a_id = str(next_a['author']['id']).replace("https://openalex.org/", "")
            if next_a_id == a_id:
                continue
            next_work_lst = get_work_list(next_a_id)
            if len(next_work_lst) > 0:
                flag = False
                a_id = next_a_id
                work_lst = next_work_lst

        ii += 1

        if ii == num_samples_per_sleep:
            time.sleep(60)
            ii = 1

            with open("./data/openalex_sampling_lst.pickle", mode='wb') as f:
                pickle.dump(sampling_lst, f)
        else:
            time.sleep(5)

    return

def nbhorw(num_samples, restart):

    if restart:
        with open("./data/openalex_sampling_lst.pickle", mode="rb") as f:
            sampling_lst = pickle.load(f)
        (a_id, w_id, work_lst, work, a_lst) = sampling_lst[-1]
    else:
        sampling_lst = []

        a_id = "A5088448789" # "Federico Battiston"
        w_id = "W3035258118" # https://doi.org/10.1016/j.physrep.2020.05.004

        work_lst = get_work_list(a_id)
        work = get_single_work(w_id)
        a_lst = list(work['authorships'])

        sampling_lst.append((a_id, w_id, work_lst, work, a_lst))
        print(datetime.datetime.now(), a_id, w_id, len(work_lst), len(a_lst))

    flag = True
    while flag:
        next_a = np.random.choice(a_lst, size=1)[0]
        if 'author' not in next_a or 'id' not in next_a['author']:
            continue
        next_a_id = str(next_a['author']['id']).replace("https://openalex.org/", "")
        if next_a_id == a_id:
            continue
        next_work_lst = get_work_list(next_a_id)
        if len(next_work_lst) > 0:
            flag = False
            a_id = next_a_id
            work_lst = next_work_lst

    flag = True
    while flag:
        next_work = np.random.choice(work_lst, size=1)[0]
        if 'id' not in next_work or 'authorships' not in next_work:
            continue
        next_w_id = next_work['id'].replace("https://openalex.org/", "")
        if len(work_lst) == 1:
            flag = False
            w_id = next_w_id
            work = next_work
            a_lst = list(work['authorships'])
        elif len(next_work["authorships"]) < 2:
            continue
        elif next_w_id != w_id:
            flag = False
            w_id = next_w_id
            work = next_work
            a_lst = list(work['authorships'])
        else:
            continue

    sampling_lst.append((a_id, w_id, work_lst, work, a_lst))

    num_samples_per_sleep = 100
    ii = 1

    while len(sampling_lst) < num_samples:
        print(len(sampling_lst))

        flag = True
        while flag:
            next_a = np.random.choice(a_lst, size=1)[0]
            if 'author' not in next_a or 'id' not in next_a['author']:
                continue
            next_a_id = str(next_a['author']['id']).replace("https://openalex.org/", "")
            if next_a_id == a_id:
                continue
            next_work_lst = get_work_list(next_a_id)
            if len(next_work_lst) > 0:
                flag = False
                a_id = next_a_id
                work_lst = next_work_lst

        flag = True
        while flag:
            next_work = np.random.choice(work_lst, size=1)[0]
            if 'id' not in next_work or 'authorships' not in next_work:
                continue
            next_w_id = next_work['id'].replace("https://openalex.org/", "")
            if len(work_lst) == 1:
                flag = False
                w_id = next_w_id
                work = next_work
                a_lst = list(work['authorships'])
            elif len(next_work["authorships"]) < 2:
                continue
            elif next_w_id != w_id:
                flag = False
                w_id = next_w_id
                work = next_work
                a_lst = list(work['authorships'])
            else:
                continue

        sampling_lst.append((a_id, w_id, work_lst, work, a_lst))
        print(datetime.datetime.now(), a_id, w_id, len(work_lst), len(a_lst))

        ii += 1

        if ii == num_samples_per_sleep:
            time.sleep(60)
            ii = 1

            with open("./data/openalex_sampling_lst_.pickle", mode='wb') as f:
                pickle.dump(sampling_lst, f)
        else:
            time.sleep(5)

    return

def assign_discipline_to_author(author_work_lst):
    discipline_lst = []
    for work in author_work_lst:
        if "primary_topic" in work and work["primary_topic"] != None and "domain" in work["primary_topic"]:
            domain = str(work["primary_topic"]["domain"]["display_name"])
            discipline_lst.append(domain)

    if len(discipline_lst) == 0:
        return set()

    discipline_count = collections.Counter(discipline_lst)
    (dsp, n_dsp) = discipline_count.most_common()[0]

    discipline_set = {dsp}
    for dsp_ in discipline_count:
        if dsp_ != dsp and discipline_count[dsp_] == n_dsp:
            discipline_set.add(dsp_)

    return discipline_set

def calc_ccdf(dist):
    lst = sorted(list(dist.items()), key=lambda x:x[0], reverse=False)
    ccdf = {k: 0.0 for (k, p) in lst}
    min_k, max_k = lst[0][0], lst[-1][0]
    for (k, p) in lst:
        for k_ in range(min_k, k+1):
            if k_ in ccdf:
                ccdf[k_] += p

    return ccdf

def extract_continent_set(work):
    if 'authorships' not in work:
        return set()

    continent_set = []
    authorships = work['authorships']

    for authorship in authorships:
        if 'countries' not in authorship:
            continue

        for country_code in authorship['countries']:
            try:
                continent_set.append(pc.country_alpha2_to_continent_code(country_code))
            except:
                print("ERROR", country_code)

    return set(continent_set)

def estimation(num_burn_in_samples=5000, num_samples_per_step=1000, num_samples=40000):

    with open("./data/openalex_sampling_lst.pickle", mode="rb") as f:
        sampling_lst = pickle.load(f)

    Phi_by_r = defaultdict(lambda: defaultdict(float))
    Psi_by_r = defaultdict(lambda: defaultdict(float))
    Xi_by_r = defaultdict(lambda: defaultdict(float))
    sample_count_by_r = defaultdict(lambda: defaultdict(int))

    for r in range(num_burn_in_samples+1000, num_samples+1, num_samples_per_step):
        for i in range(num_burn_in_samples, r):
            (a_id, w_id, work_lst, work, a_lst) = sampling_lst[i]
            d = len(work_lst)

            sample_count_by_r['All'][r] += 1

            Phi_by_r['All'][r] += float(1) / d

            discipline_set = assign_discipline_to_author(work_lst)
            if len(discipline_set) > 0:
                for dsp in discipline_set:
                    sample_count_by_r[dsp][r] += 1
                    Phi_by_r[dsp][r] += float(1) / d

            s = len(a_lst)

            Psi_by_r['All'][r] += float(1) / s

            if "primary_topic" in work and work["primary_topic"] != None and "domain" in work["primary_topic"]:
                dsp = str(work["primary_topic"]["domain"]["display_name"])
                Psi_by_r[dsp][r] += float(1) / s

            Xi_by_r['All'][r] += float(1) / s

            if "open_access" in work and "oa_status" in work["open_access"]:
                oa_status = str(work["open_access"]["oa_status"])
                if oa_status not in {'diamond', 'gold', 'green', 'hybrid', 'bronze', 'closed'}:
                    oa_status = 'N/A'

                Xi_by_r[oa_status][r] += float(1) / s

    Phi = defaultdict(float)
    Phi_ = defaultdict(lambda: defaultdict(float))
    Psi = defaultdict(float)
    Psi_ = defaultdict(lambda: defaultdict(float))
    Xi = defaultdict(lambda: defaultdict(float))
    Eta = defaultdict(lambda: defaultdict(float))
    Eta_ = defaultdict(float)

    for i in range(num_burn_in_samples, num_samples):
        (a_id, w_id, work_lst, work, a_lst) = sampling_lst[i]
        d = len(work_lst)

        Phi['All'] += float(1) / d
        Phi_['All'][d] += float(1) / d

        discipline_set = assign_discipline_to_author(work_lst)
        if len(discipline_set) > 0:
            for dsp in discipline_set:
                Phi[dsp] += float(1) / d
                Phi_[dsp][d] += float(1) / d

        s = len(a_lst)

        Psi['All'] += float(1) / s
        Psi_['All'][s] += float(1) / s

        if "open_access" in work and "oa_status" in work["open_access"]:
            oa_status = str(work["open_access"]["oa_status"])
            if oa_status not in {'diamond', 'gold', 'green', 'hybrid', 'bronze', 'closed'}:
                oa_status = 'N/A'

            Xi['All'][oa_status] += float(1) / s

            continent_set = extract_continent_set(work)
            for continent in continent_set:
                Eta_[continent] += float(1) / s
                Eta[continent][oa_status] += float(1) / s

        if "primary_topic" in work and work["primary_topic"] != None and "domain" in work["primary_topic"]:
            dsp = str(work["primary_topic"]["domain"]["display_name"])
            Psi[dsp] += float(1) / s
            Psi_[dsp][s] += float(1) / s

            if "open_access" in work and "oa_status" in work["open_access"]:
                oa_status = str(work["open_access"]["oa_status"])
                if oa_status not in {'diamond', 'gold', 'green', 'hybrid', 'bronze', 'closed'}:
                    oa_status = 'N/A'

                Xi[dsp][oa_status] += float(1) / s

    mean_author_work_count = {}
    for dsp in Phi_by_r:
        mean_author_work_count[dsp] = {}
        for r in range(num_burn_in_samples+1000, num_samples + 1, num_samples_per_step):
            mean_author_work_count[dsp][r] = float(sample_count_by_r[dsp][r]) / Phi_by_r[dsp][r]

    mean_team_size = {}
    for dsp in Psi_by_r:
        mean_team_size[dsp] = {}
        for r in range(num_burn_in_samples+1000, num_samples + 1, num_samples_per_step):
            mean_team_size[dsp][r] = float(sample_count_by_r[dsp][r]) / Psi_by_r[dsp][r]

    prob_oa_status = {}
    for oa_status in Xi_by_r:
        prob_oa_status[oa_status] = {}
        for r in range(num_burn_in_samples+1000, num_samples + 1, num_samples_per_step):
            prob_oa_status[oa_status][r] = float(Xi_by_r[oa_status][r]) / Xi_by_r['All'][r]

    author_work_count_dist = {}
    for dsp in Phi_:
        author_work_count_dist[dsp] = {}
        for d in Phi_[dsp]:
            author_work_count_dist[dsp][d] = float(Phi_[dsp][d]) / Phi[dsp]

    team_size_dist = {}
    for dsp in Psi_:
        team_size_dist[dsp] = {}
        for s in Psi_[dsp]:
            team_size_dist[dsp][s] = float(Psi_[dsp][s]) / Psi[dsp]

    oa_status_dist = {}
    for dsp in Xi:
        oa_status_dist[dsp] = {}
        for oa_status in Xi[dsp]:
            oa_status_dist[dsp][oa_status] = float(Xi[dsp][oa_status]) / Psi[dsp]

    oa_status_dist_by_continent = {}
    for continent in Eta:
        oa_status_dist_by_continent[continent] = {}
        for oa_status in Eta[continent]:
            oa_status_dist_by_continent[continent][oa_status] = float(Eta[continent][oa_status]) / Eta_[continent]

    print(len(author_work_count_dist),author_work_count_dist)
    print(len(team_size_dist),team_size_dist)
    print(len(oa_status_dist),oa_status_dist)
    print(len(oa_status_dist_by_continent), oa_status_dist_by_continent)

    with open("./result/estimation_results.pickle", mode='wb') as f:
        pickle.dump(tuple((mean_author_work_count, mean_team_size, author_work_count_dist, team_size_dist,
                           prob_oa_status, oa_status_dist, oa_status_dist_by_continent)), f)

    return