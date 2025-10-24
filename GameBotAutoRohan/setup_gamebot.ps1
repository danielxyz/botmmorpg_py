# ============================================
# Game Bot Auto Pilot - Complete Setup
# For Rohan 2 & LordNine
# Python 3.14
# ============================================

Write-Host "🎮 Game Bot Setup Starting..." -ForegroundColor Green
Write-Host ""

# Check Python
Write-Host "Checking Python installation..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Python not found! Please install Python 3.14" -ForegroundColor Red
    exit 1
}
Write-Host "✅ $pythonVersion" -ForegroundColor Green

# Create project
$projectPath = "C:\Projects\GameBotAutoRohan"
Write-Host "Creating project at $projectPath..." -ForegroundColor Yellow
New-Item -Path $projectPath -ItemType Directory -Force | Out-Null
Set-Location $projectPath

# Create venv
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
python -m venv venv
.\venv\Scripts\Activate.ps1

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip | Out-Null

# Install packages
Write-Host "Installing bot dependencies..." -ForegroundColor Yellow
pip install pyautogui pillow opencv-python numpy pytesseract keyboard mouse mss pywin32 customtkinter pyyaml loguru colorama pyinstaller | Out-Null

# Create structure
Write-Host "Creating project structure..." -ForegroundColor Yellow
New-Item -Path "bot\core", "bot\detection", "bot\actions", "bot\gui", "bot\utils", "config", "resources\images", "resources\templates", "logs", "screenshots" -ItemType Directory -Force | Out-Null
New-Item -Path "bot\__init__.py", "bot\core\__init__.py", "bot\detection\__init__.py", "bot\actions\__init__.py", "bot\gui\__init__.py", "bot\utils\__init__.py" -ItemType File -Force | Out-Null

Write-Host ""
Write-Host "✅ Setup Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Copy all Python files to their respective folders" -ForegroundColor White
Write-Host "2. Run calibration: .\calibrate.ps1" -ForegroundColor White
Write-Host "3. Start bot: .\run.ps1" -ForegroundColor White
Write-Host ""
Write-Host "Project location: $projectPath" -ForegroundColor Cyan
