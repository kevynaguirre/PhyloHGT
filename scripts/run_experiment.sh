#Download and prepare data
./scripts/download_datasets.sh

#Extract features from training dataset
./scripts/feature_extraction_pipeline.sh training

#Train the model
python scripts/training.py

#Run statistical analysis between models
Rscript scripts/statistical_analysis.R

#Extract features from simulation dataset
./scripts/feature_extraction_pipeline.sh simulation

#Extract features from real_biological dataset
./scripts/feature_extraction_pipeline.sh real_biological

#Predict patterns of simulation and real_biological dataset
python scripts/predict_patterns.py --input results/simulation_results.tsv --output results/simulation_pred.tsv
python scripts/predict_patterns.py --input results/real_biological_results.tsv --output results/real_biological_pred.tsv

#Run benchmark agains avp
Rscript scripts/benchmark.R

#Organise data
mkdir results/graphics
mv *.tiff *.pdf results/graphics

mkdir results/models_performance
mv *.csv results/models_performance

mkdir results/joblib_files
mv *.joblib results/joblib_files
