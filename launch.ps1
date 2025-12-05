# StellarForge Quick Launch Script for Windows
# Activates virtual environment and runs the application

Write-Host "Starting StellarForge..." -ForegroundColor Cyan

# Check if virtual environment exists
if (-not (Test-Path "venv")) {
    Write-Host "Virtual environment not found. Please run install.ps1 first." -ForegroundColor Red
    exit 1
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Gray
try {
    & ".\venv\Scripts\Activate.ps1"
} catch {
    Write-Host "Could not activate virtual environment." -ForegroundColor Red
    Write-Host "Try running: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser" -ForegroundColor Yellow
    exit 1
}

# Run the application
Write-Host "Launching StellarForge..." -ForegroundColor Green
Write-Host ""
python main.py

# Deactivate on exit
deactivate
