# app/ml/data_preprocessor.py

import numpy as np

def normalize_features(X):
    """
    Normalizes feature vectors using mean/std normalization.
    Works for FFT-based or raw sensor features.

    Parameters:
        X (np.ndarray): Feature matrix

    Returns:
        np.ndarray: Normalized feature matrix
    """
    mean = np.mean(X, axis=0)
    std = np.std(X, axis=0)

    # Avoid division by zero
    std[std == 0] = 1.0

    X_norm = (X - mean) / std
    return X_norm


def clip_outliers(X, threshold=4.0):
    """
    Clips extreme outliers to reduce noise spikes.

    Parameters:
        X (np.ndarray): Feature matrix
        threshold (float): Z-score clipping threshold

    Returns:
        np.ndarray: Clipped feature matrix
    """
    X_clipped = np.clip(X, -threshold, threshold)
    return X_clipped


def preprocess_dataset(X):
    """
    Full preprocessing pipeline for 100-virus training.

    Steps:
        1. Normalize features
        2. Clip outliers
        3. Return cleaned feature matrix

    Parameters:
        X (np.ndarray): Raw feature matrix

    Returns:
        np.ndarray: Preprocessed feature matrix
    """

    X_norm = normalize_features(X)
    X_clean = clip_outliers(X_norm)

    return X_clean
