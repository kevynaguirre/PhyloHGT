#!/bin/bash
set -e  # stop on error
cd dataset

# This script downloads and prepares the training dataset of phylogenetic trees

# Create directory
mkdir -p training training_dataset
cd training

# Download dataset from Zenodo
wget  "https://zenodo.org/records/17552462/files/Phylogenetic_SM_HGT_Analysis-Plantae.zip"

# Unzip dataset
unzip -o Phylogenetic_SM_HGT_Analysis-Plantae.zip

# Path to tree files
TREE_DIR="Phylogenetic_SM_HGT_Analysis-Plantae/Phylogenetic_Trees_HGT_Analysis-Plantae"

# Rename files: remove "_tree" from filenames
echo "Renaming tree files..."

for file in "$TREE_DIR"/*_tree*; do
    # Skip if no match
    [ -e "$file" ] || continue

    # Create new filename without "_tree"
    new_name=$(echo "$file" | sed 's/_tree//g')

    mv "$file" "$new_name"
done

# Now lets clean trees not were used to train because they do not belong to studied phylogenetic patterns
# Path to metadata file
METADATA="../../metadata/training_metadata.tsv"

echo "Filtering trees based on metadata..."

# Extract allowed filenames (first column, skip header)
cut -f1 "$METADATA" | tail -n +2 > allowed_ids.txt

# Loop through all tree files
for file in "$TREE_DIR"/*; do
    base=$(basename "$file")
    name="${base%.*}"

    # Check if name is in metadata
    if ! grep -Fxq "$name" allowed_ids.txt; then
        rm "$file"
    fi
done

rm allowed_ids.txt

echo "Filtering complete."

echo "Trees in training dataset:"
ls "$TREE_DIR" | wc -l


# Move trees to final directory
cp "$TREE_DIR"/* ../training_dataset/

# Return and clean
cd ..
rm -rf training

echo "Done. Training Dataset is ready."

###########################################################################################################
#Lets download and build real biological dataset to perform benchmark agains avp
#This is real biological dataset

#Create directory
mkdir -p real_bio
cd real_bio

#Download trees
wget  "https://zenodo.org/records/18435322/files/Phylogenetic_SM_HGT_Analysis-Katz_Update.zip"
unzip -o Phylogenetic_SM_HGT_Analysis-Katz_Update.zip
TREE_DIR="Phylogenetic_Trees_HGT_Analysis-Katz_Update"

#In real_biological_dataset dir already exist 518 trees tha we build for the current project
#Complement real_biological_dataset dir with downloaded info
cp "$TREE_DIR"/* ../benchmark_dataset/real_biological_dataset/


#Deduplicate cases that alreadt were used to train the model using a deduplication metadata file
TREE_DIR="../benchmark_dataset/real_biological_dataset"
# Now lets clean trees not were used to train because they do not belong to studied phylogenetic patterns
# Path to metadata file
METADATA="../../metadata/real_bio_metadata.tsv"

echo "Filtering trees based on metadata..."

# Extract allowed filenames (first column, skip header)
cut -f1 "$METADATA" | tail -n +2 > allowed_ids.txt

# Loop through all tree files
for file in "$TREE_DIR"/*; do
    base=$(basename "$file")
    name="${base%.*}"

    # Check if name is in metadata
    if ! grep -Fxq "$name" allowed_ids.txt; then
        rm "$file"
    fi
done

rm allowed_ids.txt

echo "Filtering complete."

echo "Trees in training dataset:"
ls "$TREE_DIR" | wc -l

# Return and clean
cd ..
rm -rf real_bio

echo "Done. Benchmark Dataset is ready."
