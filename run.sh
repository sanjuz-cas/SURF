#!/bin/bash
# SURF Customer Feedback Agent - Quick Start Script (Unix/Mac)
# =============================================================

echo ""
echo "================================================================"
echo "  🌊 SURF - Customer Feedback Agent"
echo "  Starting Pipeline Execution..."
echo "================================================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "   Run setup first: python setup.py"
    exit 1
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found!"
    echo "   Copy .env.example to .env and configure your credentials"
    exit 1
fi

# Run the main script
echo "🚀 Starting SURF pipeline..."
echo ""
python backend/main.py "$@"

echo ""
echo "================================================================"
echo "  ✅ Execution Complete"
echo "================================================================"
