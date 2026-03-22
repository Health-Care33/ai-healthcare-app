import pandas as pd
import joblib
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

print("Starting Health Risk Model Training...")

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "dataset" / "health_risk_dataset.csv"
MODEL_PATH = BASE_DIR / "model" / "health_risk_model.pkl"

print("Dataset Path:", DATA_PATH)

# Load dataset
df = pd.read_csv(DATA_PATH)

print("Dataset Loaded Successfully")
print("Total Rows:", len(df))

# Split features and target
X = df.drop("risk", axis=1)
y = df["risk"]

# Train test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ML Pipeline
pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("model", RandomForestClassifier(
        n_estimators=200,
        max_depth=10,
        random_state=42
    ))
])

print("Training Model...")

pipeline.fit(X_train, y_train)

preds = pipeline.predict(X_test)

accuracy = accuracy_score(y_test, preds)

print("Model Accuracy:", accuracy)

# Save model
joblib.dump(pipeline, MODEL_PATH)

print("Model Saved Successfully!")
print("Model Location:", MODEL_PATH)