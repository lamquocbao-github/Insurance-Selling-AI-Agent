@echo off
echo 🧧 Tet Insurance AI Agent - Gemini Powered
echo ==========================================
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
echo 📦 Installing dependencies (Streamlit, Gemini SDK, NumPy)...
pip install -r requirements_gemini.txt

if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo ✅ Dependencies installed successfully
echo.

REM Display instructions
echo 🔑 IMPORTANT: You need a Gemini API Key
echo ==========================================
echo.
echo 1. Visit: https://makersuite.google.com/app/apikey
echo 2. Sign in with your Google account
echo 3. Click 'Create API Key'
echo 4. Copy your API key
echo.
echo You will need to enter this key in the application.
echo.
echo Press any key to continue...
pause >nul

REM Run the application
echo.
echo 🚀 Starting Tet Insurance AI Agent...
echo.
echo The application will open in your browser automatically.
echo If it doesn't, navigate to: http://localhost:8501
echo.
echo Don't forget to enter your Gemini API key in the sidebar!
echo.
echo Press Ctrl+C to stop the application
echo.

streamlit run tet_insurance_agent_gemini.py

pause
