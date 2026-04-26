# Core
import pandas as pd
import numpy as np

# Visualization (optional)
import matplotlib.pyplot as plt
import seaborn as sns

# Preprocessing
from sklearn.preprocessing import LabelEncoder, label_binarize
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

# Models
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
import xgboost as xgb

# Model selection
from sklearn.model_selection import (
    train_test_split,
    RepeatedStratifiedKFold,
    GridSearchCV,
    RandomizedSearchCV
)

# Metrics
from sklearn.metrics import (
    roc_auc_score,
    precision_score,
    recall_score,
    f1_score,
    accuracy_score,
    roc_curve,
    auc
)

# Explainability
from sklearn.inspection import permutation_importance
import shap

# Utilities
from scipy.stats import randint
import joblib


###############################################################################
############################################################################

########################### 1. Load data #####################################
# load training dataset
df = pd.read_csv("results/training_results.tsv", sep="\t", header=None)
# add colnames
cols = [
    "filename", "query", "p_donorMC", "p_recipientMC",
    "mean_p_aMCs", "n_aMCs", "topo_d", "d",
    "aMC", "idaMC", "dMC", "rleca", "max_topo", "tag"
]

df = pd.read_csv("results/training_results.tsv", sep="\t", header=None)
df.columns = cols

#define X & Y
X = df.drop(['filename','query', 'aMC', 'idaMC','dMC','rleca', 'tag'], axis=1) #Because i nee to graphic
# Encode target labels
le = LabelEncoder()
y = le.fit_transform(df['tag'])

############################################################################
############################################################################
########################### 2. Train Models ################################
# This is for T1: RF
# Store the values scores from the repetitions
# Define variable to store metrics values
auc_scores = []
precision_scores = []
recall_scores = []
f1_scores = []
accuracy_scores = []

#Define the pipeline
# Define your model pipeline
pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="constant", fill_value=-1)),
    ("clf", RandomForestClassifier(random_state=42))
])


# # Define the repeated stratified k-fold CV
cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=10, random_state=42)

for train_idx, test_idx in cv.split(X, y):
    #Train
    pipeline.fit(X.iloc[train_idx], y[train_idx])
    #Evalueate
    y_pred = pipeline.predict(X.iloc[test_idx])
    y_proba = pipeline.predict_proba(X.iloc[test_idx])
    auc_score = roc_auc_score(y[test_idx], y_proba, multi_class="ovr", average="weighted")
    precision = precision_score(y[test_idx], y_pred, average='weighted')
    recall = recall_score(y[test_idx], y_pred, average='weighted')
    f1 = f1_score(y[test_idx], y_pred, average='weighted')
    acc = accuracy_score(y[test_idx], y_pred)

    auc_scores.append(auc_score)
    precision_scores.append(precision)
    recall_scores.append(recall)
    f1_scores.append(f1)
    accuracy_scores.append(acc)

#Save output
df_T1 = pd.DataFrame({
    "fold": range(1, len(auc_scores) + 1),
    "auc": auc_scores,
    "precision": precision_scores,
    "recall": recall_scores,
    "f1": f1_scores,
    "accuracy": accuracy_scores
})

print(df_T1.head())  # to preview

#Save info info csv
df_T1.to_csv("df_T1_results.csv", index=False)

# T2: XGboost
#Define variable
auc_scores = []
precision_scores = []
recall_scores = []
f1_scores = []
accuracy_scores = []

#Define the pipeline
# Define XGBoost model
model = xgb.XGBClassifier(
    random_state=42,
    eval_metric="mlogloss"
)

# Define your model pipeline
pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="constant", fill_value=-1)),
    ("model", model)
])
# # Define the repeated stratified k-fold CV
cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=10, random_state=42)

for train_idx, test_idx in cv.split(X, y):
    #Train
    pipeline.fit(X.iloc[train_idx], y[train_idx])
    #Evalueate
    y_pred = pipeline.predict(X.iloc[test_idx])
    y_proba = pipeline.predict_proba(X.iloc[test_idx])
    auc_score = roc_auc_score(y[test_idx], y_proba, multi_class="ovr", average="weighted")
    precision = precision_score(y[test_idx], y_pred, average='weighted')
    recall = recall_score(y[test_idx], y_pred, average='weighted')
    f1 = f1_score(y[test_idx], y_pred, average='weighted')
    acc = accuracy_score(y[test_idx], y_pred)

    auc_scores.append(auc_score)
    precision_scores.append(precision)
    recall_scores.append(recall)
    f1_scores.append(f1)
    accuracy_scores.append(acc)



# After your loop
df_T2 = pd.DataFrame({
    "fold": range(1, len(auc_scores) + 1),
    "auc": auc_scores,
    "precision": precision_scores,
    "recall": recall_scores,
    "f1": f1_scores,
    "accuracy": accuracy_scores
})

print(df_T2.head())  # to preview

#Save info info csv
df_T2.to_csv("df_T2_results.csv", index=False)

# T3: Logistic Regression
# Initialize metric containers
auc_scores, precision_scores, recall_scores, f1_scores, accuracy_scores = [], [], [], [], []

# Define Logistic Regression model
model_lr = LogisticRegression(
    solver="lbfgs",            # robust optimizer for multiclass
    max_iter=500,             # ensure convergence
    random_state=42
)

# Define your model pipeline
pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="constant", fill_value=-1)),
    ("model", model_lr)
])
# # Define the repeated stratified k-fold CV
cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=10, random_state=42)

for train_idx, test_idx in cv.split(X, y):
    #Train
    pipeline.fit(X.iloc[train_idx], y[train_idx])
    #Evalueate
    y_pred = pipeline.predict(X.iloc[test_idx])
    y_proba = pipeline.predict_proba(X.iloc[test_idx])
    auc_score = roc_auc_score(y[test_idx], y_proba, multi_class="ovr", average="weighted")
    precision = precision_score(y[test_idx], y_pred, average='weighted', zero_division=0)
    recall = recall_score(y[test_idx], y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y[test_idx], y_pred, average='weighted', zero_division=0)
    acc = accuracy_score(y[test_idx], y_pred)

    auc_scores.append(auc_score)
    precision_scores.append(precision)
    recall_scores.append(recall)
    f1_scores.append(f1)
    accuracy_scores.append(acc)



# After your loop
df_T3 = pd.DataFrame({
    "fold": range(1, len(auc_scores) + 1),
    "auc": auc_scores,
    "precision": precision_scores,
    "recall": recall_scores,
    "f1": f1_scores,
    "accuracy": accuracy_scores
})

print(df_T3.head())  # to preview

#Save info info csv
df_T3.to_csv("df_T3_results.csv", index=False)


# T4: Gaussian Naive 
# Initialize metric containers
auc_scores, precision_scores, recall_scores, f1_scores, accuracy_scores = [], [], [], [], []

# Define pipeline
pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="constant", fill_value=-1)),  # handle missing values
    ("clf", GaussianNB())  # Naive Bayes classifier
])


# # Define the repeated stratified k-fold CV
cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=10, random_state=42)

for train_idx, test_idx in cv.split(X, y):
    #Train
    pipeline.fit(X.iloc[train_idx], y[train_idx])
    #Evalueate
    y_pred = pipeline.predict(X.iloc[test_idx])
    y_proba = pipeline.predict_proba(X.iloc[test_idx])
    auc_score = roc_auc_score(y[test_idx], y_proba, multi_class="ovr", average="weighted")
    precision = precision_score(y[test_idx], y_pred, average='weighted', zero_division=0)
    recall = recall_score(y[test_idx], y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y[test_idx], y_pred, average='weighted', zero_division=0)
    acc = accuracy_score(y[test_idx], y_pred)

    auc_scores.append(auc_score)
    precision_scores.append(precision)
    recall_scores.append(recall)
    f1_scores.append(f1)
    accuracy_scores.append(acc)



# After your loop
df_T4 = pd.DataFrame({
    "fold": range(1, len(auc_scores) + 1),
    "auc": auc_scores,
    "precision": precision_scores,
    "recall": recall_scores,
    "f1": f1_scores,
    "accuracy": accuracy_scores
})

print(df_T4.head())  # to preview

#Save info info csv
df_T4.to_csv("df_T4_results.csv", index=False)

# T5: K-Nearest Neighbors (KNN)
# Initialize metric containers
auc_scores, precision_scores, recall_scores, f1_scores, accuracy_scores = [], [], [], [], []

# Define pipeline
pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="constant", fill_value=-1)),  # handle missing values
    ("clf", KNeighborsClassifier())  # Naive Bayes classifier
])


# # Define the repeated stratified k-fold CV
cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=10, random_state=42)

for train_idx, test_idx in cv.split(X, y):
    #Train
    pipeline.fit(X.iloc[train_idx], y[train_idx])
    #Evalueate
    y_pred = pipeline.predict(X.iloc[test_idx])
    y_proba = pipeline.predict_proba(X.iloc[test_idx])
    auc_score = roc_auc_score(y[test_idx], y_proba, multi_class="ovr", average="weighted")
    precision = precision_score(y[test_idx], y_pred, average='weighted', zero_division=0)
    recall = recall_score(y[test_idx], y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y[test_idx], y_pred, average='weighted', zero_division=0)
    acc = accuracy_score(y[test_idx], y_pred)

    auc_scores.append(auc_score)
    precision_scores.append(precision)
    recall_scores.append(recall)
    f1_scores.append(f1)
    accuracy_scores.append(acc)



# After your loop
df_T5 = pd.DataFrame({
    "fold": range(1, len(auc_scores) + 1),
    "auc": auc_scores,
    "precision": precision_scores,
    "recall": recall_scores,
    "f1": f1_scores,
    "accuracy": accuracy_scores
})

print(df_T5.head())  # to preview

#Save info info csv
df_T5.to_csv("df_T5_results.csv", index=False)


# T6: Support vector machines classifier SVC
# Initialize metric containers
auc_scores, precision_scores, recall_scores, f1_scores, accuracy_scores = [], [], [], [], []
# Define model
model = SVC(
    kernel="rbf",              # non-linear kernel
    probability=True,          # enables predict_proba for AUC
    class_weight="balanced",   # handles class imbalance
    random_state=42
)
# Define pipeline
pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="constant", fill_value=-1)),  # handle missing values
    ("model", model)  # SVM
])

# # Define the repeated stratified k-fold CV
cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=10, random_state=42)

for train_idx, test_idx in cv.split(X, y):
    #Train
    pipeline.fit(X.iloc[train_idx], y[train_idx])
    #Evalueate
    y_pred = pipeline.predict(X.iloc[test_idx])
    y_proba = pipeline.predict_proba(X.iloc[test_idx])
    auc_score = roc_auc_score(y[test_idx], y_proba, multi_class="ovr", average="weighted")
    precision = precision_score(y[test_idx], y_pred, average='weighted', zero_division=0)
    recall = recall_score(y[test_idx], y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y[test_idx], y_pred, average='weighted', zero_division=0)
    acc = accuracy_score(y[test_idx], y_pred)

    auc_scores.append(auc_score)
    precision_scores.append(precision)
    recall_scores.append(recall)
    f1_scores.append(f1)
    accuracy_scores.append(acc)

# After your loop
df_T6 = pd.DataFrame({
    "fold": range(1, len(auc_scores) + 1),
    "auc": auc_scores,
    "precision": precision_scores,
    "recall": recall_scores,
    "f1": f1_scores,
    "accuracy": accuracy_scores
})

print(df_T6.head())  # to preview

#Save info info csv
df_T6.to_csv("df_T6_results.csv", index=False)

# T7: MLP Multiple Layer Perceptron
# Initialize metric containers
auc_scores, precision_scores, recall_scores, f1_scores, accuracy_scores = [], [], [], [], []

# Define model
model = MLPClassifier(max_iter=5000, random_state=42, hidden_layer_sizes=(100,))

# Define pipeline
pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="constant", fill_value=-1)),  # handle missing values
    ("model", model)  # MLP
])


# # Define the repeated stratified k-fold CV
cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=10, random_state=42)

for train_idx, test_idx in cv.split(X, y):
    #Train
    pipeline.fit(X.iloc[train_idx], y[train_idx])
    #Evalueate
    y_pred = pipeline.predict(X.iloc[test_idx])
    y_proba = pipeline.predict_proba(X.iloc[test_idx])
    auc_score = roc_auc_score(y[test_idx], y_proba, multi_class="ovr", average="weighted")
    precision = precision_score(y[test_idx], y_pred, average='weighted', zero_division=0)
    recall = recall_score(y[test_idx], y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y[test_idx], y_pred, average='weighted', zero_division=0)
    acc = accuracy_score(y[test_idx], y_pred)

    auc_scores.append(auc_score)
    precision_scores.append(precision)
    recall_scores.append(recall)
    f1_scores.append(f1)
    accuracy_scores.append(acc)



# After your loop
df_T7 = pd.DataFrame({
    "fold": range(1, len(auc_scores) + 1),
    "auc": auc_scores,
    "precision": precision_scores,
    "recall": recall_scores,
    "f1": f1_scores,
    "accuracy": accuracy_scores
})

print(df_T7.head())  # to preview

#Save info info csv
df_T7.to_csv("df_T7_results.csv", index=False)



### Join all data

# Load all results
dfs = []
models = {
    "RF": "df_T1_results.csv",
    "XGBoost": "df_T2_results.csv",
    "LR": "df_T3_results.csv",
    "GNB": "df_T4_results.csv",
    "MLP": "df_T7_results.csv",
    "KNN": "df_T5_results.csv",
    "SVC": "df_T6_results.csv"
}

for model_name, file in models.items():
    df = pd.read_csv(file)
    df["model"] = model_name
    dfs.append(df)

# Combine everything
df_all = pd.concat(dfs, ignore_index=True)

#Reorder columns
df_all = df_all[["model", "fold", "auc", "precision", "recall", "f1", "accuracy"]]

#Export
df_all.to_csv("all_models_results.csv", index=False)


############################################################################
############################################################################
########################### 3. Hyperparameter Tunning ######################

#We already know is RF
# T8: RF+Grid Search fine tunning
########### Store the values scores from the repetitions
#Define variable
auc_scores = []
precision_scores = []
recall_scores = []
f1_scores = []
accuracy_scores = []

#Define the pipeline
# Define your model pipeline
pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="constant", fill_value=-1)),
    ("clf", RandomForestClassifier(random_state=42))
])

#Define Para Grid
# Define hyperparameter grid (RF params) ### WARNING add "clf__" to each parameter because we are working in a pipeline
#Need to prefix your hyperparameters with the name of the step they belong to, followed by __ (double underscore).
param_grid = {
    "clf__n_estimators": [100, 400, 500, 800, 1000],
    "clf__max_depth": [None, 5, 10, 20],
    "clf__min_samples_split": [2, 5, 10],
    "clf__min_samples_leaf": [1, 2, 4],
    "clf__max_features": ["sqrt", "log2", None],
    "clf__bootstrap": [True, False],
    "clf__class_weight": [None, "balanced"]
}

param_grid = {
    "clf__n_estimators": [100, 400],
    "clf__max_depth": [5],
    "clf__min_samples_split": [2],
    "clf__min_samples_leaf": [1],
    "clf__max_features": ["sqrt"],
    "clf__bootstrap": [True, False],
    "clf__class_weight": [None]
}



# # Define the repeated stratified k-fold CV
cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=10, random_state=42)

#Define Grid Search

grid_searchRF = GridSearchCV(
    estimator=pipeline,
    param_grid=param_grid,
    scoring='roc_auc_ovr_weighted',  # weighted AUC roc_auc_ovr_weighted
    cv=cv,
    n_jobs=-1,
    verbose=2
)

#Train you use the complete set because in cv is defined how to split the data in train and test
grid_searchRF.fit(X, y)

print("Best params:", grid_searchRF.best_params_)
print("Mean AUC:", grid_searchRF.best_score_)

#Pick the best model
best_modelRF_GS = grid_searchRF.best_estimator_

#Define variable # Containers for scores
auc_scores = []
precision_scores = []
recall_scores = []
f1_scores = []
accuracy_scores = []
for train_idx, test_idx in cv.split(X, y):
    best_modelRF_GS.fit(X.iloc[train_idx], y[train_idx])
    y_pred = best_modelRF_GS.predict(X.iloc[test_idx])
    y_proba = best_modelRF_GS.predict_proba(X.iloc[test_idx])

    auc_score = roc_auc_score(y[test_idx], y_proba, multi_class="ovr", average="weighted")
    f1  = f1_score(y[test_idx], y_pred, average="weighted")
    pre = precision_score(y[test_idx], y_pred, average="weighted")
    rec = recall_score(y[test_idx], y_pred, average="weighted")
    acc = accuracy_score(y[test_idx], y_pred)
    auc_scores.append(auc_score)
    f1_scores.append(f1)
    precision_scores.append(pre)
    recall_scores.append(rec)
    accuracy_scores.append(acc)

# After your loop
df_T8 = pd.DataFrame({
    "fold": range(1, len(auc_scores) + 1),
    "auc": auc_scores,
    "precision": precision_scores,
    "recall": recall_scores,
    "f1": f1_scores,
    "accuracy": accuracy_scores
})

print(df_T8.head())  # to preview

#Save info info csv
df_T8.to_csv("df_T8_results.csv", index=False)


#T9: RF+ Randome Search fine tunning
#Define variable
auc_scores = []
precision_scores = []
recall_scores = []
f1_scores = []
accuracy_scores = []

#Define the pipeline
# Define your model pipeline
pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="constant", fill_value=-1)),
    ("clf", RandomForestClassifier(random_state=42, class_weight="balanced"))
])

#Define Param for Randome Search
# Define hyperparameter grid (RF params) ### WARNING add "clf__" to each parameter because we are working in a pipeline
#Need to prefix your hyperparameters with the name of the step they belong to, followed by __ (double underscore).

# Random search space around best parameters
param_dist = {
    "clf__n_estimators": randint(100, 1500),         # combines 150–300 and 200–1500
    "clf__max_depth": [None] + list(range(4, 50)),   # combines 4–25 and 10–50
    "clf__min_samples_split": randint(2, 20),        # unified range
    "clf__min_samples_leaf": randint(1, 10),         # unified range
    "clf__max_features": [None, "sqrt", "log2"],     # full set
    "clf__bootstrap": [True, False],                 # both options
    "clf__class_weight": [None, "balanced"]          # add class weight options
}

# # Define the repeated stratified k-fold CV
cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=10, random_state=42)

# Randomized search
random_searchRF = RandomizedSearchCV(
    estimator=pipeline,
    param_distributions=param_dist,
    n_iter=200,                 # try 2000 random combinations
    scoring="roc_auc_ovr_weighted",     # or "roc_auc_ovr" for multiclass
    cv=cv,
    verbose=2,
    random_state=42,
    n_jobs=-1
)

#Train you use the complete set because in cv is defined how to split the data in train and test
random_searchRF.fit(X, y)

print("Best params:", random_searchRF.best_params_)
print("Mean AUC:", random_searchRF.best_score_)

#Pick the best model
best_modelRF_RS = random_searchRF.best_estimator_
for train_idx, test_idx in cv.split(X, y):
    best_modelRF_RS.fit(X.iloc[train_idx], y[train_idx])
    y_pred = best_modelRF_RS.predict(X.iloc[test_idx])
    y_proba = best_modelRF_RS.predict_proba(X.iloc[test_idx])
    
    auc_score = roc_auc_score(y[test_idx], y_proba, multi_class="ovr", average="weighted")
    f1  = f1_score(y[test_idx], y_pred, average="weighted")
    pre = precision_score(y[test_idx], y_pred, average="weighted")
    rec = recall_score(y[test_idx], y_pred, average="weighted")
    acc = accuracy_score(y[test_idx], y_pred)
    
    auc_scores.append(auc_score)
    f1_scores.append(f1)
    precision_scores.append(pre)
    recall_scores.append(rec)
    accuracy_scores.append(acc)

# After your loop
df_T9 = pd.DataFrame({
    "fold": range(1, len(auc_scores) + 1),
    "auc": auc_scores,
    "precision": precision_scores,
    "recall": recall_scores,
    "f1": f1_scores,
    "accuracy": accuracy_scores
})

print(df_T9.head())  # to preview

#Save info info csv
df_T9.to_csv("df_T9_results.csv", index=False)

#join data of RF  model hyperparameter tuned

dfs = []
models = {
    "RF": "df_T1_results.csv",
    "RF+GS": "df_T8_results.csv",
    "RF+RS": "df_T9_results.csv"
}

for model_name, file in models.items():
    df = pd.read_csv(file)
    df["model"] = model_name
    dfs.append(df)

# Combine everything
df_all = pd.concat(dfs, ignore_index=True)

#Reorder columns
df_all = df_all[["model", "fold", "auc", "precision", "recall", "f1", "accuracy"]]

#Export
df_all.to_csv("op_models_results.csv", index=False)

############################################################################
############################################################################
########################### 4. Model evaluation ############################

# Plot AUC-ROC curves
# Split data
# Train/test split (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
## This is the best model
pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="constant", fill_value=-1)),
    ("clf", RandomForestClassifier(random_state=42))
])

# Extract the Random Forest inside the pipeline
best_rf = pipeline.named_steps["clf"]

#Fit the model
pipeline.fit(X_train, y_train)
y_proba = pipeline.predict_proba(X_test)

# Binarize test labels for ROC
classes = pipeline.named_steps["clf"].classes_
y_test_bin = label_binarize(y_test, classes=classes)

plt.figure(figsize=(8, 6))

for i, cls in enumerate(classes):
    
    # Convert encoded class back to original label
    real_label = le.inverse_transform([cls])[0]

    fpr, tpr, _ = roc_curve(y_test_bin[:, i], y_proba[:, i])
    roc_auc = auc(fpr, tpr)

    plt.plot(fpr, tpr, label=f"{real_label} (AUC = {roc_auc:.3f})")

plt.plot([0, 1], [0, 1], "k--", label="Random classifier")
plt.title("Multiclass ROC Curve – Random Forest")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.legend()



plt.tight_layout()
plt.savefig("AUC-ROC.tiff", dpi=400, bbox_inches="tight")

# Permutaion Analysis
# IMPORTANT: permutation importance must be computed on a validation set
result = permutation_importance(
    pipeline, X_test, y_test,
    n_repeats=20,
    scoring="roc_auc_ovr_weighted",
    random_state=42,
    n_jobs=-1
)

perm_df = pd.DataFrame({
    "Feature": X_test.columns,
    "Importance Mean": result.importances_mean,
    "Importance Std": result.importances_std
}).sort_values("Importance Mean", ascending=False)

# Select top N features (15 recommended for papers)
TOP_N = 15
plot_df = perm_df.head(TOP_N).iloc[::-1]  # reverse for top-down plotting

#plt.figure(figsize=(10, 7))

# Colors: gradient based on importance
norm = plt.Normalize(plot_df["Importance Mean"].min(), plot_df["Importance Mean"].max())
colors = plt.cm.viridis(norm(plot_df["Importance Mean"]))

sns.barplot(
    x="Importance Mean", 
    y="Feature", 
    data=plot_df,
    color='dimgrey',
    orient="h"
)

# Add error bars (std)
plt.errorbar(
    plot_df["Importance Mean"],
    np.arange(len(plot_df)),
    xerr=plot_df["Importance Std"],
    fmt='none',
    ecolor='black',
    elinewidth=1,
    capsize=3
)

plt.title("Permutation Feature Importance (AUC-based)", fontsize=18, pad=15)
plt.xlabel("Decrease in AUC (Mean)", fontsize=14)
plt.ylabel("")
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

sns.despine(left=True, bottom=True)

plt.tight_layout()
plt.savefig("permutation_barplot.tiff", dpi=400, bbox_inches="tight")

# Train SHAP explainer
explainer = shap.TreeExplainer(best_rf)

# Compute SHAP values
shap_values = explainer.shap_values(X)
# Summary plot
#shap.summary_plot(shap_values, X, plot_type="dot", max_display=20)
shap.summary_plot(shap_values, X, plot_type="bar", max_display=20, class_names=le.classes_, show=False)


# Resize the figure AFTER SHAP creates it
plt.gcf().set_size_inches(10, 5)

plt.tight_layout()

# ✅ Save BEFORE showing
plt.savefig("shap_summary_bar.tiff", dpi=400, bbox_inches="tight")





############################################################################
############################################################################
########################### 5. Save the full model##########################
pipeline.fit(X, y)


joblib.dump(pipeline, "HGT_RF_model_v2.joblib")
joblib.dump(le, "label_encoder_v2.joblib")
