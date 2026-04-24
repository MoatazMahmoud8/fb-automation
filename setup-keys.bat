@echo off
REM Setup script to add API keys securely (Windows)

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║     Facebook Automation - Secure API Key Setup              ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Check if .env exists
if not exist ".env" (
    echo 📝 Creating .env file from template...
    copy .env.example .env
) else (
    echo ✓ .env file exists
)

REM Prompt for API keys
echo.
echo 🔑 Please provide your API keys:
echo.

set /p GEMINI_KEY="Enter your Gemini API Key: "
if "!GEMINI_KEY!"=="" (
    echo ❌ Gemini API Key is required
    pause
    exit /b 1
)

set /p FB_TOKEN="Enter your Facebook Page Token: "
if "!FB_TOKEN!"=="" (
    echo ❌ Facebook Page Token is required
    pause
    exit /b 1
)

set /p FB_PAGE="Enter your Facebook Page ID: "
if "!FB_PAGE!"=="" (
    echo ❌ Facebook Page ID is required
    pause
    exit /b 1
)

REM Update .env file
echo.
echo 💾 Updating .env file...

(
    echo # Facebook Automation Configuration
    echo # DO NOT commit this file to git!
    echo.
    echo # News API ^(Already configured^)
    echo NEWS_API_KEY=bd3749c6a550467da6dd1fe30fed9cbc
    echo.
    echo # Google Gemini API
    echo GEMINI_API_KEY=%GEMINI_KEY%
    echo.
    echo # Facebook Graph API
    echo FB_PAGE_TOKEN=%FB_TOKEN%
    echo FB_PAGE_ID=%FB_PAGE%
    echo.
    echo # Logging
    echo LOG_LEVEL=INFO
    echo LOG_FILE=logs/facebook_automation.log
    echo.
    echo # Optional Features
    echo GENERATE_IMAGES=false
    echo TRANSLATE_TO_ARABIC=false
    echo LANGUAGE=ar
) > .env

echo ✓ .env file updated with your API keys

echo.
echo ✅ Configuration Complete!
echo.
echo 📋 Next steps:
echo    1. Test your setup:
echo       python simple_automation.py
echo.
echo    2. Or test full system:
echo       python -m src.main --test
echo.
echo    3. When ready, add to GitHub Secrets:
echo       - Go to GitHub repo Settings ^> Secrets and variables ^> Actions
echo       - Add: GEMINI_API_KEY
echo       - Add: FB_PAGE_TOKEN
echo       - Add: FB_PAGE_ID
echo.
echo ⚠️  SECURITY REMINDER:
echo    ✓ Never commit .env to git
echo    ✓ Never share your API keys
echo    ✓ Rotate keys periodically
echo    ✓ Check GitHub Secrets are set ^(not .env^)
echo.
pause
