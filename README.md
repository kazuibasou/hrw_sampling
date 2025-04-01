<h1 align="center">
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

This is the Python code used to produce the numerical results presented in [our paper](https://arxiv.org/abs/2502.19030).

If you use this code, please cite

- [Kazuki Nakajima, Masanao Kodakari, and Masaki Aida. "Sampling nodes and hyperedges via random walks on large hypergraphs." *arXiv preprint arXiv:2502.19030* (2025).](https://arxiv.org/abs/2502.19030)

# Requirements

We have confirmed that our code works in the following environment.

## Python and its libraries

- Python 3.10.15
- numpy 1.26.0
- pycountry-convert 0.7.2
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

Please see the notebook [*hrw_sim.ipynb*](https://github.com/kazuibasou/hrw_sampling/blob/main/hrw_sim.ipynb) for instructions on running numerical simulations on these five empirical hypergraphs.

### Sampling and estimation in OpenAlex

Please see the notebook [*hrw_openalex.ipynb*](https://github.com/kazuibasou/hrw_sampling/blob/main/hrw_openalex.ipynb) for instructions on performing a random walk on the [OpenAlex](https://openalex.org/) database.

# License

This source code is released under the MIT License, see LICENSE.txt.

# Contact
- Kazuki Nakajima (https://kazuibasou.github.io/)

(Last update: April 2025)