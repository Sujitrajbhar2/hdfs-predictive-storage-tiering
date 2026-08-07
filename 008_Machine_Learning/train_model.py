import warnings
warnings.filterwarnings("ignore")

import os
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.model_selection import RandomizedSearchCV
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (RandomForestClassifier,ExtraTreesClassifier,GradientBoostingClassifier)

from sklearn.metrics import (accuracy_score,precision_score,recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)


print("=" * 70)
print("DataTierAI - Enterprise Storage Prediction")
print("=" * 70)

# =====================================================
# Load Dataset
# =====================================================

df = pd.read_csv("enterprise_dataset.csv")

print("\nDataset Loaded Successfully")

print(f"Rows    : {len(df)}")
print(f"Columns : {len(df.columns)}")

print("\nDataset Preview\n")

print(df.head())

print("\nDataset Information\n")

print(df.info())

# =====================================================
# Remove Unnecessary Columns
# =====================================================

drop_columns = [

    "Object_Name","Owner","Location","Created_Date",
    "Modified_Date","Storage_Tier"
]

df.drop(
    columns=[c for c in drop_columns if c in df.columns],inplace=True
)

print("\nUnnecessary Columns Removed")

# =====================================================
# Handle Missing Values
# =====================================================

print("\nMissing Values Before Cleaning")

print(df.isnull().sum())

# Numeric Columns

numeric_columns = df.select_dtypes(include=["int64","float64"]).columns

for column in numeric_columns:
    df[column] = df[column].fillna(df[column].median())

# Categorical Columns

categorical_columns = df.select_dtypes(include="object").columns

for column in categorical_columns:
    df[column] = df[column].fillna(df[column].mode()[0])

print("\nMissing Values After Cleaning")

print(df.isnull().sum().sum())

print("\nMissing Values After Cleaning")
print(df.isnull().sum())
print("\nTotal Missing Values :", df.isnull().sum().sum())

# =====================================================
# Feature Selection
# =====================================================

target = "Storage_Label"

X = df.drop(columns=[target])

y = df[target]

print("\nTarget Column :", target)

print("Features :", len(X.columns))

print(X.columns.tolist())

# =====================================================
# Encode Categorical Features
# =====================================================

label_encoders = {}

for column in X.select_dtypes(include="object").columns:

    encoder = LabelEncoder()

    X[column] = encoder.fit_transform(X[column].astype(str))

    label_encoders[column] = encoder

# Encode Target

target_encoder = LabelEncoder()

y = target_encoder.fit_transform(y)

print("\nCategorical Encoding Completed")


# =====================================================
# Remove Weak Features
# =====================================================

X = X.drop(columns=["Source", "Enterprise_Score",
    "Priority_Business_Score",
    "Source_Business_Score",
    "Department_Business_Score",
    "Activity_Business_Score",
    "Age_Score",
    "Size_Score","Compliance"])

print("\nWeak Features Removed")
print("Remaining Features :", len(X.columns))

# =====================================================
# Train Test Split
# =====================================================

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.20,random_state=42,stratify=y)

print("\nTraining Records :", len(X_train))

print("Testing Records :", len(X_test))

# =====================================================
# Model Training
# =====================================================

print("\n" + "="*70)
print("Training Machine Learning Models")
print("="*70)

models = {

    "Decision Tree": DecisionTreeClassifier(random_state=42),

    "Random Forest": RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        n_jobs=-1
    ),

    "Extra Trees": ExtraTreesClassifier(
        n_estimators=200,
        random_state=42,
        n_jobs=-1
    ),

    "Gradient Boosting": GradientBoostingClassifier(
        random_state=42
    )

}

results = []

best_model = None
best_model_name = ""
best_accuracy = 0

for name, model in models.items():

    print(f"\nTraining : {name}")

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)

    precision = precision_score(
        y_test,
        predictions,
        average="weighted"
    )

    recall = recall_score(
        y_test,
        predictions,
        average="weighted"
    )

    f1 = f1_score(
        y_test,
        predictions,
        average="weighted"
    )

    print(f"Accuracy : {accuracy:.4f}")

    results.append({

        "Model": name,

        "Accuracy": accuracy,

        "Precision": precision,

        "Recall": recall,

        "F1 Score": f1

    })

    if accuracy > best_accuracy:

        best_accuracy = accuracy

        best_model = model

        best_model_name = name


# =====================================================
# Model Comparison
# =====================================================

results_df = pd.DataFrame(results)

results_df = results_df.sort_values(
    by="Accuracy",
    ascending=False
)

print("\n")
print("="*70)
print("Model Comparison")
print("="*70)

print(results_df)

os.makedirs("output", exist_ok=True)

results_df.to_csv(
    "output/model_metrics.csv",
    index=False
)

print("\nModel Metrics Saved Successfully")


# =====================================================
# Best Model
# =====================================================

print("\n")
print("="*70)

print("Best Model Selected")

print("="*70)

print(f"Model Name : {best_model_name}")

print(f"Accuracy   : {best_accuracy:.4f}")

# =====================================================
# Hyperparameter Tuning
# =====================================================

print("\n" + "="*70)
print("Hyperparameter Tuning - Random Forest")
print("="*70)

param_grid = {

    "n_estimators": [100, 200, 300],

    "max_depth": [10, 20, 30, None],

    "min_samples_split": [2, 5, 10],

    "min_samples_leaf": [1, 2, 4],

    "max_features": ["sqrt", "log2"]

}

random_search = RandomizedSearchCV(

    estimator=RandomForestClassifier(random_state=42),

    param_distributions=param_grid,

    n_iter=5,

    cv=2,

    scoring="accuracy",

    verbose=2,

    random_state=42,

    n_jobs=1

)

random_search.fit(X_train, y_train)

best_model = random_search.best_estimator_

print("\nBest Parameters")

print(random_search.best_params_)

print("\nBest Cross Validation Accuracy")

print(random_search.best_score_)

# =====================================================
# Final Random Forest Model
# =====================================================

print("\nCreating Final Random Forest Model...")

best_model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    min_samples_split=10,
    min_samples_leaf=2,
    max_features="sqrt",
    random_state=42,
    n_jobs=-1
)

best_model.fit(X_train, y_train)

print("Final Model Trained Successfully")

# =====================================================
# Save Model
# =====================================================

os.makedirs("models", exist_ok=True)

joblib.dump(best_model, "models/best_model.pkl")
joblib.dump(label_encoders, "models/label_encoders.pkl")
joblib.dump(target_encoder, "models/target_encoder.pkl")
joblib.dump(list(X.columns), "models/feature_columns.pkl")

print("\nModels Saved Successfully")
print("best_model.pkl")

print("label_encoders.pkl")
print("target_encoder.pkl")
print("feature_columns.pkl")