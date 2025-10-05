# SURF Customer Feedback Agent - Quick Start Script
# =================================================
# Run this script to execute the complete pipeline

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "  🌊 SURF - Customer Feedback Agent" -ForegroundColor Cyan
Write-Host "  Starting Pipeline Execution..." -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (-not (Test-Path "venv")) {
    Write-Host "❌ Virtual environment not found!" -ForegroundColor Red
    Write-Host "   Run setup first: python setup.py" -ForegroundColor Yellow
    exit 1
}

# Activate virtual environment
Write-Host "📦 Activating virtual environment..." -ForegroundColor Green
& ".\venv\Scripts\Activate.ps1"

# Check if .env exists
if (-not (Test-Path ".env")) {
    Write-Host "❌ .env file not found!" -ForegroundColor Red
    Write-Host "   Copy .env.example to .env and configure your credentials" -ForegroundColor Yellow
    exit 1
}

# Run the main script
Write-Host "🚀 Starting SURF pipeline..." -ForegroundColor Green
Write-Host ""
python backend/main.py $args

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "  ✅ Execution Complete" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
