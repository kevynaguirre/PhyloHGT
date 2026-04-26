# 🧬 PhyloHGT
## 📦 Installation
**Note:** You need conda to buil the environment
Please run the following instruction to install requirements:
```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
conda env create -f environment.yml
conda activate phylohgt
```
## 🌳 Phylogenetic tree datasets
The repository already have benchmark dataset:
1. Simulated dataset of 1000 phylogenetic trees in `dataset/benchmark_dataset/simulation_dataset`
2. Real biological cases dataset of 518 phylogenetic trees in `dataset/benchmark_dataset/real_biological_dataset`

To obtain the training dataset and the rest of benchmark dataset please run the script `download_datasets.sh`.
This script will download phylogenetic trees from original articles:
1. Trainning dataset:  https://doi.org/10.1002/ece3.72653
2. Rest phylogenetic trees (920) of real biological cases dataset: https://doi.org/10.1242/bio.062387

The script will process the data and we will have:
1. Trainning dataset of 1012 phylogenetic trees in `dataset/training_dataset`
2. Benchmark dataset
    - Simulated dataset (1000 trees) in `dataset/benchmark_dataset/simulation_dataset`
    - Real biological dataset (1438 trees) in `dataset/benchmark_dataset/real_biological_dataset`

## ⚙️ Feature extraction
The feature extraction connects with NCBI is optional but you can set your ncbi api key in the variable `NCBI_API_KEY` to prevent hammer ncbi servers like this:
```bash
export NCBI_API_KEY="your_api_key"
```
To perform the experiment run:
```bash
./scripts/run_experiment.sh
```
