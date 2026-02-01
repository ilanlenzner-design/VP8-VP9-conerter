#!/bin/bash

# Start Video Compressor Web Interface

echo "========================================================"
echo "Video Compressor Web Interface"
echo "========================================================"
echo ""

# Check if Flask is installed
if ! python3 -c "import flask" 2>/dev/null; then
    echo "Flask is not installed. Installing dependencies..."
    pip3 install flask werkzeug --user --break-system-packages 2>/dev/null || \
    pip3 install flask werkzeug --user
    echo ""
fi

# Check if Flask was successfully installed
if ! python3 -c "import flask" 2>/dev/null; then
    echo "❌ Failed to install Flask."
    echo ""
    echo "Please install Flask manually:"
    echo "  pip3 install flask werkzeug --user"
    echo ""
    exit 1
fi

echo "✓ Flask is installed"
echo ""
echo "Starting server..."
echo "========================================================"
echo ""

# Start the Flask app
cd "$(dirname "$0")"
python3 app.py
