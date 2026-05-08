"""
Serial Bridge for Arduino/ESP32
Uses pyserial to communicate with microcontrollers.
Dependencies: pyserial
"""

import serial
import time

class SerialBridge:
    def __init__(self, port, baudrate=115200):
        self.port = port
        self.baudrate = baudrate
        self.serial_conn = None

    def connect(self):
        """Connect to the serial device."""
        try:
            self.serial_conn = serial.Serial(self.port, self.baudrate, timeout=1)
            print(f"[Serial] Connected to {self.port} at {self.baudrate} baud.")
            return True
        except Exception as e:
            print(f"[Serial] Connection failed: {e}")
            return False

    def send_command(self, command):
        """Send a command to the device."""
        if self.serial_conn:
            self.serial_conn.write(command.encode())
            print(f"[Serial] Sent: {command}")
        else:
            print("[Serial] Not connected.")

    def read_response(self):
        """Read a response from the device."""
        if self.serial_conn:
            response = self.serial_conn.readline().decode().strip()
            print(f"[Serial] Received: {response}")
            return response
        else:
            print("[Serial] Not connected.")
            return None

    def close(self):
        """Close the serial connection."""
        if self.serial_conn:
            self.serial_conn.close()
            print("[Serial] Disconnected.")

# Example Usage
if __name__ == "__main__":
    bridge = SerialBridge(port="/dev/ttyACM0", baudrate=115200)
    if bridge.connect():
        bridge.send_command("BLINK")  # Example: Blink an LED
        time.sleep(1)
        response = bridge.read_response()
        bridge.close()
