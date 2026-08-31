# app/ml/fft_feature_extractor.py

import numpy as np

def compute_fft(signal):
    """
    Computes FFT magnitude spectrum for a 1D signal.

    Parameters:
        signal (np.ndarray): Raw sensor signal

    Returns:
        np.ndarray: FFT magnitude spectrum
    """
    fft_vals = np.fft.fft(signal)
    fft_mag = np.abs(fft_vals)
    return fft_mag


def extract_fft_features(signal, max_features=256):
    """
    Extracts FFT features from a raw signal and reduces
    the spectrum to a fixed number of features.

    Parameters:
        signal (np.ndarray): Raw sensor signal
        max_features (int): Number of FFT features to keep

    Returns:
        np.ndarray: Reduced FFT feature vector
    """
    fft_mag = compute_fft(signal)

    # Keep only the first N FFT bins
    if len(fft_mag) >= max_features:
        fft_reduced = fft_mag[:max_features]
    else:
        # Pad with zeros if signal is shorter
        fft_reduced = np.pad(fft_mag, (0, max_features - len(fft_mag)))

    return fft_reduced


def batch_fft_extraction(signals, max_features=256):
    """
    Applies FFT feature extraction to a batch of signals.

    Parameters:
        signals (list or np.ndarray): List of raw signals
        max_features (int): Number of FFT features per signal

    Returns:
        np.ndarray: Matrix of FFT feature vectors
    """
    feature_list = []

    for sig in signals:
        features = extract_fft_features(sig, max_features=max_features)
        feature_list.append(features)

    return np.array(feature_list)
