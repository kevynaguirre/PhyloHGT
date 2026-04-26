# 🧬 PhyloHGT
## 📦 Installation
**Note:** You need conda to buil the environment
Please run the following instruction to install requirements:
```bash
git clone https://github.com/kevynaguirre/PhyloHGT.git
cd PhyloHGT
conda env create -f environment.yml
conda activate phylohgt
```
## ⚙️ Feature Extraction (Optional NCBI Setup)
Feature extraction may query NCBI services. To avoid rate limits and ensure stable execution, you can provide an NCBI API key:
```bash
export NCBI_API_KEY="your_api_key"
```
This step is optional but recommended for large-scale runs.

## 🚀 Running the Full Experiment
To reproduce the full pipeline (data acquisition, feature extraction, model training, prediction, and benchmarking), run:
```bash
./scripts/run_experiment.sh
```
## 🌳 Datasets
The repository includes a partial benchmark dataset:
- Simulated dataset (1000 trees): `dataset/benchmark_dataset/simulation_dataset`
- Real biological dataset (518 trees): `dataset/benchmark_dataset/real_biological_dataset`
### ⬇️ Automatic Dataset Reconstruction
The pipeline script will automatically:
Download additional phylogenetic trees from published studies:
- Training dataset: https://doi.org/10.1002/ece3.72653
- Additional real biological trees: https://doi.org/10.1242/bio.062387
Process and standardize all datasets

### 📊 Final datasets generated
After execution, the following datasets will be available:
- Training dataset (1012 trees): `dataset/training_dataset`
- Benchmark datasets:
  1. Simulated dataset (1000 trees): `dataset/benchmark_dataset/simulation_dataset`
  2. Real biological dataset (1438 trees): `dataset/benchmark_dataset/real_biological_dataset`
 
## 🔬 Pipeline Overview

The `run_experiment.sh` script performs the complete workflow:
- Dataset acquisition (download and preprocessing)
- Feature extraction from phylogenetic trees
- Model training
- Prediction on benchmark datasets
- Statistical analysis
- Benchmark comparison against AVP results
