import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
import joblib

# -----------------------------
# 1. Load CSV
# -----------------------------
csv_path = "app/models/data/virus_multiclass.csv"
df = pd.read_csv(csv_path)

print(f"Original CSV rows: {len(df)}")
print(df.head())

# -----------------------------
# 2. Define columns
# -----------------------------
id_col = "virus_id"
target = "virus_id"  # multiclass label

numeric_features = [
    "mass_fg",
    "frequency_mhz",
    "deposition_rate_s",
    "temperature_c",
    "humidity_pct",
    "flow_rate",
    "time_to_detection_s",
]

categorical_features = [
    "antibody",
    "antigen",
]

# -----------------------------
# 3. FIXED & SAFE AUGMENTATION FUNCTION
#    (NO NEGATIVE SCALES + realistic noise)
# -----------------------------
def augment_row(row, n_samples=100):
    """
    Generate n_samples of noisy versions of a single virus row.
    Numeric features get Gaussian noise; categorical stay the same.
    Noise scales are ALWAYS positive using abs().
    """
    base_numeric = row[numeric_features].values.astype(float)
    cat_vals = row[categorical_features].values

    # Always positive noise scales using absolute values
    noise_scales = np.array([
        abs(0.15 * base_numeric[0]) if base_numeric[0] != 0 else 1e-6,   # mass_fg
        0.0005,                                                         # frequency_mhz drift
        abs(0.20 * base_numeric[2]) if base_numeric[2] != 0 else 0.05,  # deposition_rate_s
        2.0,                                                            # temperature_c (±2°C)
        5.0,                                                            # humidity_pct (±5%)
        0.3,                                                            # flow_rate (±0.3)
        abs(0.20 * base_numeric[6]) if base_numeric[6] != 0 else 1.0,   # time_to_detection_s
    ])

    samples = []
    for _ in range(n_samples):
        noise = np.random.normal(loc=0.0, scale=noise_scales)
        noisy_numeric = base_numeric + noise

        sample_dict = {target: int(row[id_col])}
        for i, col in enumerate(numeric_features):
            sample_dict[col] = noisy_numeric[i]
        for j, col in enumerate(categorical_features):
            sample_dict[col] = cat_vals[j]

        samples.append(sample_dict)

    return samples

# -----------------------------
# 4. Build augmented dataset
# -----------------------------
augmented_rows = []
for _, row in df.iterrows():
    augmented_rows.extend(augment_row(row, n_samples=100))

aug_df = pd.DataFrame(augmented_rows)
print(f"Augmented dataset size: {len(aug_df)}")

# -----------------------------
# 5. Train/test split
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
# 6. Preprocessing + model pipeline
# -----------------------------
numeric_transformer = Pipeline(steps=[
    ("scaler", StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ("onehot", OneHotEncoder(handle_unknown="ignore"))
])

preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, numeric_features),
        ("cat", categorical_transformer, categorical_features),
    ]
)

clf = RandomForestClassifier(
    n_estimators=400,
    max_depth=None,
    min_samples_split=2,
    min_samples_leaf=1,
    class_weight="balanced",
    n_jobs=-1,
    random_state=42,
)

model = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("classifier", clf),
])

# -----------------------------
# 7. Cross-validation (business sanity check)
# -----------------------------
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
cv_scores = cross_val_score(model, X_train, y_train, cv=cv, n_jobs=-1)

print(f"Cross-val accuracy (5-fold): {cv_scores.mean():.3f} ± {cv_scores.std():.3f}")

# -----------------------------
# 8. Fit on full training set
# -----------------------------
model.fit(X_train, y_train)

test_accuracy = model.score(X_test, y_test)
print(f"Hold-out test accuracy: {test_accuracy:.3f}")

# -----------------------------
# 9. Save model
# -----------------------------
model_path = "app/models/virus_multiclassify_V8_175_robust.pkl"
joblib.dump(model, model_path)

print(f"Business-ready multiclass model saved: {model_path}")
