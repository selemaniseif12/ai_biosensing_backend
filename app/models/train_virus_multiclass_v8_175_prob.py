import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
import joblib

# -----------------------------
# Load CSV
# -----------------------------
csv_path = "app/models/data/virus_multiclass.csv"
df = pd.read_csv(csv_path)

print(f"Original CSV rows: {len(df)}")
print(df.head())

id_col = "virus_id"
target = "virus_id"

numeric_features = [
    "mass_fg",
    "frequency_mhz",
    "deposition_rate_s",
    "temperature_c",
    "humidity_pct",
    "flow_rate",
    "time_to_detection_s",
]

categorical_features = ["antibody", "antigen"]

# -----------------------------
# V8 AUGMENTATION (20 samples per virus, robust noise)
# -----------------------------
def augment_row(row, n_samples=20):
    base_numeric = row[numeric_features].values.astype(float)
    cat_vals = row[categorical_features].values

    noise_scales = np.array([
        abs(0.15 * base_numeric[0]) if base_numeric[0] != 0 else 1e-6,
        0.001,
        abs(0.20 * base_numeric[2]) if base_numeric[2] != 0 else 0.03,
        3.0,
        6.0,
        0.3,
        abs(0.20 * base_numeric[6]) if base_numeric[6] != 0 else 0.7,
    ])

    samples = []
    for _ in range(n_samples):
        noise = np.random.normal(0.0, noise_scales)
        noisy_numeric = base_numeric + noise

        sample_dict = {target: int(row[id_col])}
        for i, col in enumerate(numeric_features):
            sample_dict[col] = noisy_numeric[i]
        for j, col in enumerate(categorical_features):
            sample_dict[col] = cat_vals[j]

        samples.append(sample_dict)

    return samples

augmented_rows = []
for _, row in df.iterrows():
    augmented_rows.extend(augment_row(row, n_samples=20))

aug_df = pd.DataFrame(augmented_rows)
print(f"Augmented dataset size (V8): {len(aug_df)}")

# -----------------------------
# Train/test split
# -----------------------------
X = aug_df[numeric_features + categorical_features]
y = aug_df[target]

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    stratify=y,
    random_state=42
)

# -----------------------------
# Preprocessing + RandomForest
# -----------------------------
numeric_transformer = Pipeline([
    ("scaler", StandardScaler())
])

categorical_transformer = Pipeline([
    ("onehot", OneHotEncoder(handle_unknown="ignore"))
])

preprocessor = ColumnTransformer(
    [
        ("num", numeric_transformer, numeric_features),
        ("cat", categorical_transformer, categorical_features),
    ]
)

rf_clf = RandomForestClassifier(
    n_estimators=400,
    max_depth=None,
    class_weight="balanced",
    n_jobs=1,
    random_state=42
)

model = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", rf_clf),
])

# -----------------------------
# Train
# -----------------------------
print("Training V8 model...")
model.fit(X_train, y_train)

# -----------------------------
# Accuracy
# -----------------------------
test_accuracy = model.score(X_test, y_test)
print(f"V8 Hold-out test accuracy: {test_accuracy:.3f}")

# -----------------------------
# Probability predictions
# -----------------------------
probs = model.predict_proba(X_test)

prob_path = "app/models/v8_probabilities.npy"
np.save(prob_path, probs)
print(f"V8 probabilities saved: {prob_path}")

# -----------------------------
# Save model
# -----------------------------
model_path = "app/models/virus_multiclassify_V8_175_prob.pkl"
joblib.dump(model, model_path)

print(f"V8 probability-enabled model saved: {model_path}")
