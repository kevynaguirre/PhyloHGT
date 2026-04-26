#!/bin/bash
#SBATCH --job-name=extracting_features_from_tree
#SBATCH --output=extracting_features_%A_%a.out
#SBATCH --error=extracting_features_%A_%a.err
#SBATCH --array=751-1000%5  # Adjust the range and concurrency limit (%10) as needed
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --nodes=1
#SBATCH --partition=Bioinfo
#SBATCH --nodelist=cn04

# Define paths
filename="/medicina/kaguirre/HGT_decision_tree/reprod_test/data/metadat_sim.txt"
trees_dir="/medicina/kaguirre/HGT_decision_tree/reprod_test/data/simulations/trees_v2"
candidates_list="/medicina/kaguirre/HGT_decision_tree/reprod_test/data/ids_sim.txt"
python_dir="/medicina/kaguirre/HGT_decision_tree/scripts"
sqlite_db_path="/medicina/kaguirre/HGT_decision_tree/dbs/prot.accession2taxid.sqlite"

api_key="4ea24840beae77b6a7b84e80a0f0f76cfb09"

# Set output folder
features="features"
#Create output directory
mkdir -p "${features}"

# Define the samples to work on
sample=$(cat "$candidates_list" | sed -n "${SLURM_ARRAY_TASK_ID}p")

# Get the line corresponding to the SLURM_ARRAY_TASK_ID
line=$(grep "$sample" "$filename")

# Read the values from the line
IFS=$'\t' read -r id prot receptor <<< "$line"

# Run python script
python "${python_dir}/DT_HGT_v7.py" -i "${trees_dir}/${id}.nexus" -o "${features}/${id}.tsv"  -r "${receptor}" -id "${prot}"  -api "${api_key}" -f "nexus"

