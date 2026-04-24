@echo off
REM Quick start script for Simple Automation (Windows)

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║   Facebook Automation - Simple Setup (Arabic Posts)        ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Check if running from correct directory
if not exist "simple_automation.py" (
    echo ❌ Error: Please run this script from the repo directory
    echo    cd C:\path\to\fbautomation\repo
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📚 Installing dependencies...
pip install -q requests google-generativeai

REM Check for .env file
if not exist ".env" (
    echo.
    echo ⚠️  No .env file found!
    echo 📝 Creating .env from template...
    copy .env.example .env
    echo.
    echo 📋 Please edit .env and add your API keys:
    echo    • NEWS_API_KEY: bd3749c6a550467da6dd1fe30fed9cbc (already provided)
    echo    • GEMINI_API_KEY: Get from https://aistudio.google.com/app/apikeys
    echo    • FB_PAGE_TOKEN: Get from https://developers.facebook.com
    echo    • FB_PAGE_ID: Your Facebook page ID
    echo.
    echo    Run: notepad .env
    pause
    exit /b 0
)

REM Run simple automation
echo.
echo 🚀 Starting Simple Automation...
echo.
python simple_automation.py

echo.
echo ✅ Done! Check your Facebook page for the new post.
pause
