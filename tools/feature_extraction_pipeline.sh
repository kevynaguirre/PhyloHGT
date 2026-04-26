#!/bin/bash
set -e

DATASET=$1

# Optional NCBI API key
API_KEY="${NCBI_API_KEY:-}"


if [ -z "$DATASET" ]; then
    echo "Usage: bash run_feature_extraction.sh [training|simulation|real_biological|custom]"
    exit 1
fi

# Paths
if [ "$DATASET" == "training" ]; then
    METADATA="metadata/training_metadata.tsv"
    TREES_DIR="dataset/training_dataset"
    OUTPUT_DIR="results/training_features"
    OUTPUT_FILE="results/training_results.tsv"
elif [ "$DATASET" == "simulation" ]; then
    METADATA="metadata/simulation_metadata.tsv"
    TREES_DIR="dataset/benchmark_dataset/simulation_dataset"
    OUTPUT_DIR="results/simulation_features"
    OUTPUT_FILE="results/simulation_results.tsv"
elif [ "$DATASET" == "real_biological" ]; then
    METADATA="metadata/real_bio_metadata.tsv"
    TREES_DIR="dataset/benchmark_dataset/real_biological_dataset"
    OUTPUT_DIR="results/real_biological_features"
    OUTPUT_FILE="results/real_biological_results.tsv"
elif [ "$DATASET" == "custom" ]; then
    METADATA="metadata/custom_metadata.tsv"
    TREES_DIR="dataset/custom_dataset"
    OUTPUT_DIR="results/custom_features"
    OUTPUT_FILE="results/custom_results.tsv"
else
    echo "Error: invalid dataset '$DATASET'"
    exit 1
fi

# Check inputs
if [ ! -f "$METADATA" ]; then
    echo "Error: metadata not found: $METADATA"
    exit 1
fi

if [ ! -d "$TREES_DIR" ]; then
    echo "Error: trees directory not found: $TREES_DIR"
    exit 1
fi

PYTHON_SCRIPT="tools/feature_extraction.py"

mkdir -p "$OUTPUT_DIR"

echo "Starting feature extraction for dataset: $DATASET"

# Process trees
tail -n +2 "$METADATA" | while IFS=$'\t' read -r id prot receptor format; do
    tree_file="${TREES_DIR}/${id}"
    id2="${id%.*}"
    output_file="${OUTPUT_DIR}/${id2}.tsv"

    if [ ! -f "$tree_file" ]; then
        echo "Warning: missing tree $tree_file"
        continue
    fi

    python "$PYTHON_SCRIPT" \
        -i "$tree_file" \
        -o "$output_file" \
        -r "$receptor" \
        -id "$prot" \
        -f "$format" \
        ${API_KEY:+-api "$API_KEY"}

done

echo "Merging feature files..."

# Ensure there are files
if [ -z "$(ls -A "$OUTPUT_DIR" 2>/dev/null)" ]; then
    echo "Error: no feature files generated"
    exit 1
fi

cat "$OUTPUT_DIR"/*.tsv > "$OUTPUT_FILE"
echo "Feature extraction completed."
echo "Final file: $OUTPUT_FILE"
