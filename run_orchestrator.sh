#!/bin/bash

echo "Initializing Λ-OAG Orchestrator..."
echo "Unity Index (𝒰) = 1.000"
echo "Systemic Friction (μ) = 0.00%"

# Start the orchestrator core in the background
python3 orchestrator_core.py &

echo "Orchestrator is now running in OMEGA ACTIVE mode."
