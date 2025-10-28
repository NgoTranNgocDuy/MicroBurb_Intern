#!/bin/bash

echo "========================================"
echo "  MicroBurbs Property Dashboard"
echo "========================================"
echo ""
echo "Starting Flask server..."
echo ""

cd "$(dirname "$0")"
python3 app.py
