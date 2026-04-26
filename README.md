# 🧬 PhyloHGT
A machine learning framework for classifying phylogenetic tree patterns associated with interkingdom horizontal gene transfer (iHGT).
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
The first step is to extract quantitative features from phylogenetic trees.
```bash
python feature_extraction.py \
  -i dataset/benchmark_dataset/simulation_dataset/SIM1.nexus \
  -o SIM1.tsv \
  -r Opisthokonta \
  -id AAC04981.2 \
  -f nexus
```
### ⚙️ Parameters
asdf
