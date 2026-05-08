"""
WebSocket Bridge for Simulated BCI (Base44 Compatible)
Uses websockets to stream mock EEG data.
Dependencies: websockets, numpy, asyncio
"""

import asyncio
import websockets
import numpy as np
import json
from datetime import datetime

class WebSocketBridge:
    def __init__(self, host="0.0.0.0", port=8765):
        self.host = host
        self.port = port
        self.server = None
        self.clients = set()
        self.sample_rate = 256  # Hz
        self.channels = ["Fp1", "Fp2", "C3", "C4", "T3", "T4", "O1", "O2"]

    async def generate_mock_eeg(self):
        """Generate mock EEG data (sine waves + noise)."""
        t = datetime.now().timestamp()
        data = {
            "type": "eeg_data",
            "channels": self.channels,
            "values": [np.sin(t * 2 * np.pi * f) + np.random.normal(0, 0.1) for f in [1, 2, 4, 8, 10, 12, 20, 30]],
            "timestamp": datetime.now().isoformat() + "Z"
        }
        return json.dumps(data)

    async def handler(self, websocket, path):
        """Handle WebSocket connections."""
        self.clients.add(websocket)
        print(f"[WebSocket] New client connected. Total clients: {len(self.clients)}")
        try:
            while True:
                data = await self.generate_mock_eeg()
                await websocket.send(data)
                await asyncio.sleep(1 / self.sample_rate)
        except websockets.exceptions.ConnectionClosed:
            print("[WebSocket] Client disconnected.")
            self.clients.remove(websocket)

    def start_server(self):
        """Start the WebSocket server."""
        self.server = websockets.serve(self.handler, self.host, self.port)
        asyncio.get_event_loop().run_until_complete(self.server)
        print(f"[WebSocket] Server started on ws://{self.host}:{self.port}")
        asyncio.get_event_loop().run_forever()

# Example Usage
if __name__ == "__main__":
    bridge = WebSocketBridge(host="0.0.0.0", port=8765)
    bridge.start_server()
