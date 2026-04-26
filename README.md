# 🧬 PhyloHGT
A machine learning framework for classifying phylogenetic tree patterns associated with interkingdom horizontal gene transfer (iHGT).
## 📦 Installation
**Note:** You need conda to buil the environment
Please run the following instruction to install requirements:
```bash
git clone https://github.com/kevynaguirre/PhyloHGT.git
cd PhyloHGT
conda env create -f environment.yml
conda activate phylohgt
```
## 🌳 Phylogenetic tree datasets
The first step is to extract quantitative features from phylogenetic trees.
```bash
python tools/feature_extraction.py \
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

### 🍄 Major Clade Definition

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

### 📊 Output Format

The feature extraction step generates a .tsv file with both quantitative features (used by the model) and additional metadata.
#### Example
| filename | query | p_donorMC | p_recipientMC | mean_p_aMCs | n_aMCs | topo_d | d | aMC | idaMC | dMC | rleca | max_topo | tag |
|----------|--------|------------|----------------|--------------|--------|--------|--------|-------------------------------|---------------------|----------------------|---------------|----------|--------|
| SIM1 | AAC04981.2 | 0.990196078 | 0.009803922 | 0 | 0 | nan | nan | Not_unexpected_MC | Not_unexpected_id | Prokaryota\|Bacteria | Saccharomyces | 29 | Unknown 


These features are used as input for the machine learning classifier:
| Feature | Description |
|--------|------------|
| `p_donorMC` | Proportion of sequences in the donor major clade |
| `p_recipientMC` | Proportion of sequences in the recipient major clade |
| `mean_p_aMCs` | Mean proportion of sequences across additional major clades |
| `n_aMCs` | Number of additional major clades |
| `topo_d` | Topological distance between the query and the closest sequence from an additional major clade |
| `d` | Patristic distance between the query and the closest sequence from an additional major clade |
| `max_topo` | Maximum topological distance observed in the tree |

There are additional fields which are not directly used by the model but provide biological context:
| Field | Description |
|------|------------|
| `filename` | Input tree name |
| `query` | Query sequence identifier |
| `aMC` | Additional major clade detected |
| `idaMC` | Identifier of sequence from additional major clade |
| `dMC` | Donor major clade assignment |
| `rleca` | Recipient lineage (Last eukaryotic common ancestor of recipent major clade) |
| `tag` | Will be Unknown until you predict it |

### 💡 Notes
- Missing values (e.g., nan) may occur when no additional major clades are present.
- The extracted features are designed to capture topological structure, lineage diversity, and taxonomic composition of the phylogenetic tree.
- These descriptors are subsequently used for classification of evolutionary scenarios (e.g., iHGT, NoHGT, Inconclusive patterns).

## 📦 Batch Processing
The feature extraction connects with NCBI is optional but you can set your ncbi api key in the variable `NCBI_API_KEY` to prevent hammer ncbi servers. Do this:
```bash
export NCBI_API_KEY="your_api_key"
```
To process multiple phylogenetic trees, follow these steps:

### 1. Prepare input data
Place all tree files in the following directory -> dataset/custom_dataset/

### 2. Create metadata file
Create a metadata file at-> metadata/custom_metadata.tsv
The file must be tab-separated, contain headers and include the columns in the same order:
#### Example:
| filename   | query       | recipientMC   | format |
|------------|------------|--------------|--------|
| SIM1.nexus | AAC04981.2 | Opisthokonta | nexus  |
| SIM2.nexus | AAC04981.2 | Opisthokonta | nexus  |
### 3. Run the pipeline
```bash
bash feature_extraction_pipeline.sh custom
```
The results will be saved in -> results/custom_results.tsv

## 🔮 Prediction
To run prediction use the scrip `predict_patterns.py` like this:
```bash
python tools/predict_patterns.py --input SIM1.tsv --output SIM1_pred.tsv
```
`--input` is the path of the file with the features  
`--output` is the output filename

The input file can contain as many observation by line in case your human is interested in run sanalysis in bathc please keep reading

## Note
If your human wants to reproduce the experiment please go to REPRODUCIBILITY.md and follow the instructions.
