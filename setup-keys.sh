#!/bin/bash
# Setup script to add your Gemini API key securely

echo "╔════════════════════════════════════════════════════════════╗"
echo "║     Facebook Automation - Secure API Key Setup              ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
else
    echo "✓ .env file exists"
fi

# Prompt for API keys
echo ""
echo "🔑 Please provide your API keys:"
echo ""

# Gemini API Key
read -p "Enter your Gemini API Key: " GEMINI_KEY
if [ -z "$GEMINI_KEY" ]; then
    echo "❌ Gemini API Key is required"
    exit 1
fi

# Facebook Page Token
read -p "Enter your Facebook Page Token: " FB_TOKEN
if [ -z "$FB_TOKEN" ]; then
    echo "❌ Facebook Page Token is required"
    exit 1
fi

# Facebook Page ID
read -p "Enter your Facebook Page ID: " FB_PAGE
if [ -z "$FB_PAGE" ]; then
    echo "❌ Facebook Page ID is required"
    exit 1
fi

# Update .env file
echo ""
echo "💾 Updating .env file..."

# Use a safer method to update the file
cat > .env << EOF
# Facebook Automation Configuration
# DO NOT commit this file to git!

# News API (Already configured)
NEWS_API_KEY=bd3749c6a550467da6dd1fe30fed9cbc

# Google Gemini API
GEMINI_API_KEY=$GEMINI_KEY

# Facebook Graph API
FB_PAGE_TOKEN=$FB_TOKEN
FB_PAGE_ID=$FB_PAGE

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/facebook_automation.log

# Optional Features
GENERATE_IMAGES=false
TRANSLATE_TO_ARABIC=false
LANGUAGE=ar
EOF

echo "✓ .env file updated with your API keys"

# Verify .env is in .gitignore
if grep -q "\.env" .gitignore; then
    echo "✓ .env is protected in .gitignore"
else
    echo "⚠️  Warning: .env not in .gitignore!"
    echo ".env" >> .gitignore
    echo "✓ Added .env to .gitignore"
fi

echo ""
echo "✅ Configuration Complete!"
echo ""
echo "📋 Next steps:"
echo "   1. Test your setup:"
echo "      python simple_automation.py"
echo ""
echo "   2. Or test full system:"
echo "      python -m src.main --test"
echo ""
echo "   3. When ready, add to GitHub Secrets:"
echo "      - Go to GitHub repo → Settings → Secrets and variables → Actions"
echo "      - Add: GEMINI_API_KEY"
echo "      - Add: FB_PAGE_TOKEN"
echo "      - Add: FB_PAGE_ID"
echo ""
echo "⚠️  SECURITY REMINDER:"
echo "   ✓ Never commit .env to git"
echo "   ✓ Never share your API keys"
echo "   ✓ Rotate keys periodically"
echo "   ✓ Check GitHub Secrets are set (not .env)"
