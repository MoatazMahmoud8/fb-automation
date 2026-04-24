@echo off
REM Quick test of Gemini API key (Windows)

echo.
echo 🔍 Testing your Gemini API Key...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install it first.
    pause
    exit /b 1
)

REM Check if google-generativeai is installed
python -c "import google.generativeai" >nul 2>&1
if errorlevel 1 (
    echo 📦 Installing google-generativeai...
    pip install -q google-generativeai
)

REM Test the API key
echo Testing API Key: AIzaSyCsz1kt8TZQ4RwlmG-YOxjDB0_-NTwJ2Ro
echo.

python << 'EOF'
import google.generativeai as genai
import sys

try:
    # Configure with the provided API key
    api_key = "AIzaSyCsz1kt8TZQ4RwlmG-YOxjDB0_-NTwJ2Ro"
    genai.configure(api_key=api_key)
    
    # Try to create a model
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Send a simple test request
    print("📝 Sending test request to Gemini...")
    response = model.generate_content("Say 'Hello from Gemini!' exactly.")
    
    if response.text:
        print("✅ Gemini API Key is VALID!")
        print("")
        print("Response from Gemini:")
        print(f"  {response.text}")
        sys.exit(0)
    else:
        print("❌ Unexpected response from API")
        sys.exit(1)
        
except Exception as e:
    print(f"❌ API Key Test Failed: {str(e)}")
    print("")
    print("Possible issues:")
    print("  1. API key is invalid or revoked")
    print("  2. API is not enabled in Google Cloud")
    print("  3. Quota has been exceeded")
    print("  4. Network connection issue")
    sys.exit(1)
EOF

echo.
pause
