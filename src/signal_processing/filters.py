"""
EEG Signal Filtering for Zenith Neural Interface
Implements notch, bandpass, and artifact removal.
Dependencies: numpy, scipy, mne
"""

import numpy as np
from scipy.signal import butter, lfilter, notch, welch
# from mne.filter import filter_data

class EEGFilters:
    def __init__(self, sfreq=256):
        self.sfreq = sfreq  # Sampling frequency (Hz)

    def notch_filter(self, data, freq=50):
        """Apply notch filter to remove powerline noise (50Hz or 60Hz)."""
        nyquist = 0.5 * self.sfreq
        low = freq / nyquist
        high = (freq + 2) / nyquist
        b, a = butter(4, [low, high], btype='bandstop')
        return lfilter(b, a, data)

    def bandpass_filter(self, data, low=0.5, high=100):
        """Apply bandpass filter (0.5-100Hz for EEG)."""
        nyquist = 0.5 * self.sfreq
        low = low / nyquist
        high = high / nyquist
        b, a = butter(4, [low, high], btype='band')
        return lfilter(b, a, data)

    def remove_artifacts(self, data, threshold=3.0):
        """Remove artifacts using Z-score thresholding."""
        z_scores = np.abs((data - np.mean(data)) / np.std(data))
        clean_data = np.where(z_scores < threshold, data, 0)
        return clean_data

    def process(self, data):
        """Full processing pipeline: notch + bandpass + artifact removal."""
        data = self.notch_filter(data, freq=50)  # Remove 50Hz noise
        data = self.bandpass_filter(data)       # Isolate EEG bands
        data = self.remove_artifacts(data)     # Clean artifacts
        return data

# Example Usage
if __name__ == "__main__":
    # Generate mock EEG data (8 channels)
    sfreq = 256
    t = np.linspace(0, 1, sfreq)  # 1 second of data
    eeg_data = np.array([
        np.sin(2 * np.pi * 10 * t) + np.random.normal(0, 0.5, sfreq),  # Alpha waves + noise
        np.sin(2 * np.pi * 20 * t) + np.random.normal(0, 0.5, sfreq),  # Beta waves + noise
        np.sin(2 * np.pi * 4 * t) + np.random.normal(0, 0.5, sfreq),   # Theta waves + noise
        np.sin(2 * np.pi * 0.5 * t) + np.random.normal(0, 0.5, sfreq), # Delta waves + noise
        np.sin(2 * np.pi * 10 * t) + np.random.normal(0, 0.5, sfreq),
        np.sin(2 * np.pi * 20 * t) + np.random.normal(0, 0.5, sfreq),
        np.sin(2 * np.pi * 4 * t) + np.random.normal(0, 0.5, sfreq),
        np.sin(2 * np.pi * 0.5 * t) + np.random.normal(0, 0.5, sfreq)
    ])

    filters = EEGFilters(sfreq=sfreq)
    processed_data = np.array([filters.process(channel) for channel in eeg_data])
    print("[EEG Filters] Data processed. Shape:", processed_data.shape)
