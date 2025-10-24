# Screen Calibration Tool

Write-Host "🎯 Starting Calibration Tool..." -ForegroundColor Yellow

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Run calibration
python bot\utils\calibration.py
