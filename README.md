# PhyloHGT
PhyloHGT is a machine learning tool for classifying phylogenetic trees into evolutionary patterns associated with interkingdom horizontal gene transfer (iHGT). It uses topology- and taxonomy-based features to provide scalable, reproducible, and interpretable analysis.
🧬 PhyloHGT-ML
A machine learning framework for classifying phylogenetic tree patterns associated with horizontal gene transfer (HGT).
---
📦 Installation
Clone the repository and create the conda environment:
```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo

conda env create -f environment.yml
conda activate phylohgt2
```
---
⚙️ Feature Extraction
Feature extraction is performed from phylogenetic trees using the main script:
```bash
python DT_HGT_v7.py \
    -i <input_tree> \
    -o <output_features.tsv> \
    -r <receptor_clade> \
    -id <query_id> \
    -api <ncbi_api_key> \
    -f <format: nexus|newick> \
    -p <pattern>
```
Example
```bash
python DT_HGT_v7.py \
    -i data/training_trees/example.nexus \
    -o results/features/example.tsv \
    -r Opisthokonta \
    -id XP_123456 \
    -api YOUR_API_KEY \
    -f nexus \
    -p pattern1
```
---
📂 Datasets
Training dataset
Trees: `data/training_trees/`
Metadata (parameters): `data/training_metadata.tsv`
Each row in the metadata file corresponds to one tree and contains the required parameters.
After processing all trees, merge the generated feature files:
```bash
cat results/features/*.tsv > training_dataset.tsv
```
---
Additional datasets
Simulated dataset: `data/simulated/`
Real biological dataset: `data/real/`
Metadata files: `data/*_metadata.tsv`
---
🤖 Model Training
Once the dataset has been generated:
Launch Jupyter Lab:
```bash
jupyter lab
```
Open and run:
`notebooks/model_training.ipynb`
---
📊 Benchmarking
Benchmark results can be compared against AVP outputs:
AVP results: `data/benchmark/avp_results.tsv`
Supplementary data: see original publication
---
🔁 Reproducibility Workflow
Clone the repository
Create the conda environment
Extract features from all trees
Merge features into a dataset
Run the training notebook
Compare results with AVP
---
📌 Notes
An NCBI API key is recommended to avoid request limits
Feature extraction relies on BioPython, ETE toolkit, and NCBI Taxonomy
Large datasets may require batching
---
📄 Citation
Your paper citation here
---
📬 Contact
For questions or issues, please open a GitHub issue.
