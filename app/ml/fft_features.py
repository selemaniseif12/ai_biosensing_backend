import numpy as np

def extract_fft_features(noise_series, n_fft=64):
    # Compute FFT
    fft_vals = np.fft.fft(noise_series, n=n_fft)
    fft_mag = np.abs(fft_vals)

    # Use first 10 FFT magnitudes as features
    top_fft = fft_mag[:10]

    return top_fft.tolist()
