# Core
import pandas as pd
import joblib
import argparse
def main():
    parser = argparse.ArgumentParser(description="Predict HGT classes")
    parser.add_argument("--input", required=True, help="Input TSV file")
    parser.add_argument("--output", required=True, help="Output TSV file")
    args = parser.parse_args()
    # Load trained model and encoder
    model = joblib.load("HGT_RF_model_v2.joblib")
    le = joblib.load("label_encoder_v2.joblib")
    # Load dataset
    df = pd.read_csv(args.input, sep="\t", header=None)
    # Add column names
    cols = [
        "filename", "query", "p_donorMC", "p_recipientMC",
        "mean_p_aMCs", "n_aMCs", "topo_d", "d",
        "aMC", "idaMC", "dMC", "rleca", "max_topo", "tag"
    ]
    df.columns = cols
    # Select feature columns (same as training!)
    X = df.drop(['filename', 'query', 'aMC', 'idaMC', 'dMC', 'rleca', 'tag'], axis=1)
    # Predict
    y_pred = model.predict(X)
    # Convert labels back
    predicted_labels = le.inverse_transform(y_pred)
    # ✅ Add prediction column to original dataframe
    df["pred"] = predicted_labels
    # Save updated file
    df.to_csv(args.output, sep="\t", index=False)
    print(f"Predictions saved to {args.output}")
if __name__ == "__main__":
    main()
