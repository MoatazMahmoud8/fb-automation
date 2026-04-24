#!/bin/bash
# Quick test of Gemini API key

echo "🔍 Testing your Gemini API Key..."
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install it first."
    exit 1
fi

# Check if google-generativeai is installed
if ! python3 -c "import google.generativeai" 2>/dev/null; then
    echo "📦 Installing google-generativeai..."
    pip install -q google-generativeai
fi

# Test the API key
echo "Testing API Key: YOUR_GEMINI_API_KEY"
echo ""

python3 << 'EOF'
import google.generativeai as genai
import sys

try:
    # Configure with the provided API key
    api_key = "YOUR_GEMINI_API_KEY"
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

echo ""
