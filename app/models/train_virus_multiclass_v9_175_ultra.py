import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier
import joblib

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
# V9 ULTRA AUGMENTATION (300 samples per virus)
# -----------------------------
def augment_row(row, n_samples=300):
    base_numeric = row[numeric_features].values.astype(float)
    cat_vals = row[categorical_features].values

    noise_scales = np.array([
        abs(0.20 * base_numeric[0]) if base_numeric[0] != 0 else 1e-6,
        0.001,
        abs(0.25 * base_numeric[2]) if base_numeric[2] != 0 else 0.05,
        3.0,
        7.0,
        0.4,
        abs(0.25 * base_numeric[6]) if base_numeric[6] != 0 else 1.0,
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
    augmented_rows.extend(augment_row(row, n_samples=300))

aug_df = pd.DataFrame(augmented_rows)
print(f"Augmented dataset size: {len(aug_df)}")

X = aug_df[numeric_features + categorical_features]
y = aug_df[target]

# -----------------------------
# FIX: Shift labels to start at 0
# -----------------------------
y = y - 1

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

numeric_transformer = Pipeline([("scaler", StandardScaler())])

categorical_transformer = Pipeline([
    ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=True))
])

preprocessor = ColumnTransformer(
    [
        ("num", numeric_transformer, numeric_features),
        ("cat", categorical_transformer, categorical_features),
    ]
)

model = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", XGBClassifier(
        objective="multi:softmax",
        num_class=175,
        max_depth=6,
        learning_rate=0.1,
        n_estimators=150,
        tree_method="hist",
        max_bin=256,
        subsample=0.8,
        colsample_bytree=0.8,
        eval_metric="mlogloss",
        n_jobs=1
    ))
])

model.fit(X_train, y_train)

test_accuracy = model.score(X_test, y_test)
print(f"Hold-out test accuracy: {test_accuracy:.3f}")

model_path = "app/models/virus_multiclassify_V9_175_ultra.pkl"
joblib.dump(model, model_path)

print(f"V9 multiclass model saved: {model_path}")
