@echo off
echo 🧧 Tet Insurance AI Agent Demo - Quick Start
echo ===========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

echo ✅ Python is installed
echo.

REM Install requirements
echo 📦 Installing dependencies...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo ✅ Dependencies installed successfully
echo.

REM Run the application
echo 🚀 Starting Tet Insurance AI Agent...
echo.
echo The application will open in your browser automatically.
echo If it doesn't, navigate to: http://localhost:8501
echo.
echo Press Ctrl+C to stop the application
echo.

streamlit run tet_insurance_agent.py

pause
