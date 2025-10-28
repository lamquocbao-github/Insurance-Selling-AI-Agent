#!/bin/bash

echo "🧧 Tet Insurance AI Agent - Gemini Powered"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python is installed"
echo ""

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip is not installed. Please install pip."
    exit 1
fi

echo "✅ pip is installed"
echo ""

# Install requirements
echo "📦 Installing dependencies (Streamlit, Gemini SDK, NumPy)..."
pip3 install -r requirements_gemini.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
    echo ""
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Display instructions
echo "🔑 IMPORTANT: You need a Gemini API Key"
echo "=========================================="
echo ""
echo "1. Visit: https://makersuite.google.com/app/apikey"
echo "2. Sign in with your Google account"
echo "3. Click 'Create API Key'"
echo "4. Copy your API key"
echo ""
echo "You will need to enter this key in the application."
echo ""
echo "Press Enter to continue..."
read

# Run the application
echo "🚀 Starting Tet Insurance AI Agent..."
echo ""
echo "The application will open in your browser automatically."
echo "If it doesn't, navigate to: http://localhost:8501"
echo ""
echo "Don't forget to enter your Gemini API key in the sidebar!"
echo ""
echo "Press Ctrl+C to stop the application"
echo ""

streamlit run tet_insurance_agent_gemini.py
