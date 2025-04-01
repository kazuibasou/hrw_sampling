<h1 align="center">
Hyper dK-series <br/>  
<i>Sampling nodes and hyperedges via random walks on large hypergraphs</i>
</h1>

<p align="center">
<a href="https://github.com/kazuibasou/hrw_sampling/blob/main/LICENSE" target="_blank">
<img alt="License: MIT" src="https://img.shields.io/github/license/kazuibasou/hrw_sampling">
</a>

<a href="https://arxiv.org/abs/2502.19030" target="_blank">
<img alt="ARXIV: 2502.19030" src="https://img.shields.io/badge/arXiv-2502.19030-red.svg">
</a>

</p>

This is the Python code that was used for producting the numerical results shown in [our paper](https://arxiv.org/abs/2502.19030).

If you use this code, please cite

- [Kazuki Nakajima, Masanao Kodakari, and Masaki Aida. "Sampling nodes and hyperedges via random walks on large hypergraphs." *arXiv preprint arXiv:2502.19030* (2025).](https://arxiv.org/abs/2502.19030)

# Requirements

We have confirmed that our code works in the following environment.

## Python and its libraries

- Python 3.10.15
- numpy 1.26.0
- requests 2.32.3

## OS
- macOS 14.4

## Usage

First, clone this repository:

	git clone git@github.com:kazuibasou/hrw_sampling.git

### Datasets

To use the same source code as used in [our paper](https://arxiv.org/abs/2502.19030), download the following hypergraph datasets from [Austin R. Benson's dataset repository](https://www.cs.cornell.edu/~arb/data/).

- [amazon-reviews](https://drive.google.com/open?id=1dOeke9Rdh0vySIrsSqIZbGXIggVFqZwP)
- [coauth-DBLP-full](https://drive.google.com/open?id=1tC0TdzV_IMTzhkIN_4P8y9M1a3lH-ScK)
- [coauth-MAG-Geology-full](https://drive.google.com/open?id=1bk5uTnuijgHEAOi5sA-sM8Cxyg3Ejr43)
- [coauth-MAG-History-full](https://drive.google.com/open?id=1KBSQyz6BVO1HM6tjCGh8aLcugNW9pDjA)
- [threads-stack-overflow-full](https://drive.google.com/open?id=1aUwsvAhse-5tfbVZ494y9Z3cGm5lhXPX)

Place the downloaded zip files in the `hrw_sampling/data/` folder and unzip them. 
This will result in the following directory structure:

	hrw_sampling/
	├ data/
	   ├ amazon-reviews/
	   ├ coauth-DBLP-full/
	   ├ coauth-MAG-Geology-full/
	   ├ coauth-MAG-History-full/
	   └ threads-stack-overflow-full/
	├ data/
	└ result/

### Sampling and estimation in empirical hypergraphs

Please see the notebook [hrw_sim.ipynb](https://github.com/kazuibasou/hyper-dk-series/blob/main/py/1_basics.ipynb) and [2_randomization.ipynb](https://github.com/kazuibasou/hyper-dk-series/blob/main/py/2_randomization.ipynb) located in the folder `hyper-dk-series/py/` for instructions on using the hyper dk-series in Python.

## Benchmark (October 2024)

We measured the runtime (in seconds) for generating a single randomized instance using the hyper dK-series implemented in Python with Numba.  
We used the same four empirical hypergraph datasets as in [[K. Nakajima et al. *IEEE TNSE* (2021)]](https://doi.org/10.1109/TNSE.2021.3133380): `drug`, `Enron`, `primary-school`, and `high-school`. 

While the hyper dK-series with *d<sub>v</sub>* = 2 or 2.5 requires more time due to frequent hyperedge rewiring attempts, **the current version is 20–30 times faster than the previous version, which did not employ Numba.**

| (*d<sub>v</sub>*, *d<sub>e</sub>*) | drug | Enron | primary-school | high-school |
| ---- | ---- | ---- | ---- | ---- |
| (0, 0) | 0.02 | 0.008 | 0.06 | 0.05 |
| (1, 0) | 0.008 | 0.005 | 0.03 | 0.02 |
| (2, 0) | 5.6 | 3.1 | 23.6 | 9.7 |
| (2.5, 0) | 101 | 42.7 | 709 | 188 |
| (0, 1) | 0.02 | 0.008 | 0.16 | 0.05 |
| (1, 1) | 0.008 | 0.005 | 0.03 | 0.02 |
| (2, 1) | 5.1 | 1.9 | 21.1 | 7.7 |
| (2.5, 1) | 97 | 40.0 | 605 | 166 |

## Application: Rich club detection

We define a higher-order rich club in which the nodes with the largest degrees are densely interconnected by hyperedges. 
Please see the notebook [3_rich_club.ipynb](https://github.com/kazuibasou/hyper-dk-series/blob/main/py/3_rich_club.ipynb) located in the folder `hyper-dk-series/py/` for instructions on the detection of higher-order rich clubs in Python.
Please also see [[K. Nakajima et al. *Scientometrics* (2023)]](https://doi.org/10.1007/s11192-022-04621-1) for details on the detection method.
