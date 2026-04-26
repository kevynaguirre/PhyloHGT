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
| Argument | Description |
|----------|------------|
| `-i` / `--input` | Path to the phylogenetic tree file (Newick or Nexus format) |
| `-o` / `--output` | Output file name (TSV format) |
| `-r` / `--receptor` | Candidate major clade (recipient MC) |
| `-id` / `--id` | Query sequence identifier |
| `-f` / `--format` | Tree format (`newick` or `nexus`) |

### 🌳 Major Clade Definition

The receptor (-r) must correspond to one of the following major clades:

| Major Clade | Minor Clades |
|-------------|-------------|
| **Opisthokonta** | Aphelida, Choanoflagellata, Filasterea, Fungi, Ichthyosporea, Metazoa, Opisthokonta incertae sedis, Rotosphaerida, unclassified Opisthokonta |
| **SAR** | Alveolata, Rhizaria, Stramenopiles |
| **Amoebozoa** | Discosea, Evosea, Tubulinea, Amoebozoa incertae sedis, unclassified Amoebozoa |
| **Archaeplastida** | Viridiplantae, Rhodophyta, Glaucocystophyceae |
| **Excavata** | Metamonada, Malawimonadida, Discoba |
| **Prokaryota** | Bacteria, Archaea |
| **Viruses** | Viruses |
| **Unclassified** | Ancyromonadida, Apusozoa, Breviatea, Cryptophyceae, Haptista, Hemimastigophora, Provora, Rhodelphea, unclassified eukaryotes, CRuMs |
