"""
OpenBCI Bridge for Zenith Neural Interface
Supports BLE and USB connections to OpenBCI headsets.
Dependencies: pyOpenBCI, numpy
"""

import time
from pyOpenBCI import OpenBCICyton
from numpy import array, mean, std

class OpenBCIBridge:
    def __init__(self, port=None, ble=False):
        self.port = port
        self.ble = ble
        self.board = None
        self.sample_rate = 250  # Hz (OpenBCI default)
        self.channels = ["Fp1", "Fp2", "C3", "C4", "T3", "T4", "O1", "O2"]

    def connect(self):
        """Connect to OpenBCI headset."""
        try:
            if self.ble:
                self.board = OpenBCICyton(port=self.port, ble=True)
            else:
                self.board = OpenBCICyton(port=self.port)
            print("[OpenBCI] Connected to headset.")
            return True
        except Exception as e:
            print(f"[OpenBCI] Connection failed: {e}")
            return False

    def start_stream(self, callback):
        """Start streaming data."""
        if not self.board:
            print("[OpenBCI] Not connected. Call connect() first.")
            return False
        self.board.start_stream(callback)
        print("[OpenBCI] Streaming started.")
        return True

    def stop_stream(self):
        """Stop the EEG stream."""
        if self.board:
            self.board.stop()
            print("[OpenBCI] Streaming stopped.")

    def close(self):
        """Disconnect from the headset."""
        if self.board:
            self.board.close()
            print("[OpenBCI] Disconnected.")

# Example Usage
if __name__ == "__main__":
    def eeg_callback(sample):
        """Callback for incoming EEG data."""
        print(f"[OpenBCI] Sample: {sample.channels_data}")

    bridge = OpenBCIBridge(port="/dev/ttyUSB0")
    if bridge.connect():
        bridge.start_stream(eeg_callback)
        time.sleep(10)  # Stream for 10 seconds
        bridge.stop_stream()
        bridge.close()
