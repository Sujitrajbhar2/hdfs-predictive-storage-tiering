import joblib
import pandas as pd
import matplotlib.pyplot as plt

print("=" * 70)
print("DataTierAI - Feature Importance")
print("=" * 70)

# ---------------------------------------------------
# Load Model
# ---------------------------------------------------

model = joblib.load("models/best_model.pkl")
feature_columns = joblib.load("models/feature_columns.pkl")

print("\nModel Loaded Successfully")

# ---------------------------------------------------
# Get Feature Importance
# ---------------------------------------------------

importance = pd.DataFrame({
    "Feature": feature_columns,
    "Importance": model.feature_importances_
})

importance = importance.sort_values(
    by="Importance",
    ascending=False
)

print("\nTop 10 Important Features\n")
print(importance.head(10))

# ---------------------------------------------------
# Save CSV
# ---------------------------------------------------

importance.to_csv(
    "output/feature_importance.csv",
    index=False
)

# ---------------------------------------------------
# Plot
# ---------------------------------------------------

plt.figure(figsize=(8,6))

plt.barh(
    importance["Feature"][:10],
    importance["Importance"][:10]
)

plt.gca().invert_yaxis()

plt.title("Top 10 Important Features")

plt.xlabel("Importance")

plt.tight_layout()

plt.savefig(
    "output/feature_importance.png",
    dpi=300
)

plt.show()

print("\nFeature Importapython nce Saved Successfully")
print("CSV  : output/feature_importance.csv")
print("Image: output/feature_importance.png")