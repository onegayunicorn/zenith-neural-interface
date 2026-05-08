"""
FFT Analysis for Zenith Neural Interface
Extracts frequency bands (Delta, Theta, Alpha, Beta, Gamma).
Dependencies: numpy, scipy, matplotlib
"""

import numpy as np
from scipy.signal import welch
import matplotlib.pyplot as plt

class FFTAnalyzer:
    def __init__(self, sfreq=256):
        self.sfreq = sfreq
        self.bands = {
            "Delta": (0.5, 4),
            "Theta": (4, 8),
            "Alpha": (8, 12),
            "Beta": (12, 30),
            "Gamma": (30, 100)
        }

    def compute_psd(self, data):
        """Compute Power Spectral Density (PSD) using Welch's method."""
        freqs, psd = welch(data, fs=self.sfreq, nperseg=256)
        return freqs, psd

    def extract_band_power(self, freqs, psd):
        """Extract power for each frequency band."""
        band_power = {}
        for band, (low, high) in self.bands.items():
            mask = (freqs >= low) & (freqs <= high)
            band_power[band] = np.trapz(psd[mask], freqs[mask])
        return band_power

    def analyze(self, data):
        """Full FFT analysis: PSD + band power extraction."""
        freqs, psd = self.compute_psd(data)
        band_power = self.extract_band_power(freqs, psd)
        return freqs, psd, band_power

    def plot_psd(self, freqs, psd, title="Power Spectral Density"):
        """Plot the PSD."""
        plt.figure(figsize=(10, 4))
        plt.plot(freqs, psd, label="PSD")
        for band, (low, high) in self.bands.items():
            plt.axvspan(low, high, color='red', alpha=0.1, label=band)
        plt.title(title)
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("Power")
        plt.legend()
        plt.grid()
        plt.show()

# Example Usage
if __name__ == "__main__":
    # Generate mock EEG data (1 channel)
    sfreq = 256
    t = np.linspace(0, 1, sfreq)
    eeg_data = np.sin(2 * np.pi * 10 * t) + 0.5 * np.sin(2 * np.pi * 20 * t) + np.random.normal(0, 0.2, sfreq)

    analyzer = FFTAnalyzer(sfreq=sfreq)
    freqs, psd, band_power = analyzer.analyze(eeg_data)
    print("[FFT] Band Power:", band_power)
    # analyzer.plot_psd(freqs, psd)
