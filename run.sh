#!/bin/bash
# run.sh — Start the MindGuard AI Application

set -e

echo ""
echo "======================================"
echo "  🧠 MindGuard — AI Addiction Detector"
echo "======================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
  echo "❌ Python3 not found. Please install Python 3.9+."
  exit 1
fi

PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "✅ Python $PYTHON_VERSION detected"

# Create venv if not exists
if [ ! -d "venv" ]; then
  echo "📦 Creating virtual environment..."
  python3 -m venv venv
fi

# Activate venv
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt --quiet

echo ""
echo "✅ All dependencies installed"
echo ""

# Run tests
if [ "$1" == "--test" ]; then
  echo "🧪 Running tests..."
  python -m pytest tests/test_basic.py -v
  exit $?
fi

# Start server
export FLASK_APP=app.py
export FLASK_ENV=development

PORT=${PORT:-5000}
HOST=${HOST:-0.0.0.0}

echo "🚀 Starting MindGuard on http://$HOST:$PORT"
echo "   Press Ctrl+C to stop"
echo ""

if [ "$1" == "--prod" ]; then
  echo "🔒 Production mode (gunicorn)"
  gunicorn -w 4 -b $HOST:$PORT app:app
else
  python3 app.py
fi
