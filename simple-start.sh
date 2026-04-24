#!/bin/bash
# Quick start script for Simple Automation

echo "╔════════════════════════════════════════════════════════════╗"
echo "║   Facebook Automation - Simple Setup (Arabic Posts)        ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check if running from correct directory
if [ ! -f "simple_automation.py" ]; then
    echo "❌ Error: Please run this script from the repo directory"
    echo "   cd /home/moataz/work/fbautomation/repo"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -q requests google-generativeai

# Check for .env file
if [ ! -f ".env" ]; then
    echo ""
    echo "⚠️  No .env file found!"
    echo "📝 Creating .env from template..."
    cp .env.example .env
    echo ""
    echo "📋 Please edit .env and add your API keys:"
    echo "   • NEWS_API_KEY: bd3749c6a550467da6dd1fe30fed9cbc (already provided)"
    echo "   • GEMINI_API_KEY: Get from https://aistudio.google.com/app/apikeys"
    echo "   • FB_PAGE_TOKEN: Get from https://developers.facebook.com"
    echo "   • FB_PAGE_ID: Your Facebook page ID"
    echo ""
    echo "   Run: nano .env"
    exit 0
fi

# Load environment variables
echo "⚙️  Loading environment variables..."
export $(cat .env | grep -v '^#' | xargs)

# Run simple automation
echo ""
echo "🚀 Starting Simple Automation..."
echo ""
python simple_automation.py

echo ""
echo "✅ Done! Check your Facebook page for the new post."
