# Facebook Automation - Australian News Daily Posts

Fully automated system to fetch, summarize, and post Australian news to your Facebook Page using Python and Gemini AI.

## 🎯 Choose Your Path

### 🚀 Simple Automation (5 minutes)
**Perfect for testing or Arabic-only posts**
- Simple, focused code (~250 lines)
- Arabic posts only
- Manual or cron scheduling
- Fast setup
- [📖 Get Started →](SIMPLE_QUICK_START.md)

### 🏢 Production System (2.5 hours)
**For daily automated posts at scale**
- Full-featured system (2000+ lines)
- English + Arabic support
- 3 posts/day via GitHub Actions
- Comprehensive logging & monitoring
- [📖 Get Started →](../documents/steps/COMPLETE_INTEGRATION_GUIDE.md)

## 🎯 Features

### All Systems Provide
✅ **AI-Powered Content** - Google Gemini API summarization  
✅ **Error Handling** - Retry logic with exponential backoff  
✅ **Image Integration** - Automatic image attachment  
✅ **Configuration Management** - Secure API key handling  
✅ **Zero-Cost Setup** - All free tier APIs

### Production System Only
✅ **Automated Daily Posts** - 3 posts/day (9 AM, 12 PM, 6 PM AEST)  
✅ **GitHub Actions** - Serverless scheduling  
✅ **Comprehensive Logging** - Track everything  
✅ **Duplicate Detection** - Avoid repetitive posts  
✅ **Connection Testing** - Verify setup before deployment  
✅ **Multiple Language Support** - Dynamic content generation  

## 🚀 Quick Start

### 1. Get API Keys

**NewsAPI** (Already provided):
```
Key: bd3749c6a550467da6dd1fe30fed9cbc
```

**Google Gemini API**:
1. Go to https://aistudio.google.com/app/apikeys
2. Create API Key

**Facebook Graph API**:
1. Visit https://developers.facebook.com/
2. Create app and generate Page Access Token

### 2. Clone & Setup

```bash
# Clone repository
git clone <your-repo-url> fbautomation
cd fbautomation/repo

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys
```

### 3. Test Locally

```bash
# Test all connections
python -m src.main --test

# Run pipeline
python -m src.main
```

### 4. Deploy to GitHub

```bash
# Add GitHub Secrets:
# - NEWS_API_KEY
# - GEMINI_API_KEY
# - FB_PAGE_TOKEN
# - FB_PAGE_ID

# Push code
git add .
git commit -m "Initial setup"
git push origin main

# GitHub Actions will auto-run on schedule
```

## 📁 Project Structure

```
fbautomation/
├── documents/
│   ├── plan/
│   │   └── PROJECT_PLAN.md
│   └── steps/
│       ├── SETUP_STEPS.md
│       └── ARCHITECTURE.md
└── repo/
    ├── src/
    │   ├── __init__.py
    │   ├── config.py              # Configuration management
    │   ├── logger.py              # Logging utilities
    │   ├── news_fetcher.py        # NewsAPI integration
    │   ├── content_processor.py    # Gemini AI processing
    │   ├── facebook_poster.py      # Facebook Graph API
    │   ├── image_handler.py        # Image management
    │   ├── utils.py               # Helper functions
    │   └── main.py                # Main orchestrator
    ├── .github/workflows/
    │   └── facebook-automation.yml # GitHub Actions workflow
    ├── requirements.txt            # Python dependencies
    ├── .env.example               # Environment template
    └── README.md                  # This file
```

## 🔄 How It Works

```
1. NewsAPI → Fetch latest Australian news
                    ↓
2. Gemini AI → Summarize & enhance content
                    ↓
3. Image Handler → Get image from article
                    ↓
4. Facebook API → Post to your page
                    ↓
5. Logging → Track execution & errors
```

## ⚙️ Configuration

### Environment Variables

```bash
# Required
NEWS_API_KEY=your_news_api_key
GEMINI_API_KEY=your_gemini_key
FB_PAGE_TOKEN=your_facebook_token
FB_PAGE_ID=your_facebook_page_id

# Optional
LOG_LEVEL=INFO
LOG_FILE=logs/facebook_automation.log
GENERATE_IMAGES=false
TRANSLATE_TO_ARABIC=false
```

### Scheduling

Edit `.github/workflows/facebook-automation.yml` to change post times:

```yaml
schedule:
  - cron: '0 23 * * *'  # 9 AM AEST (UTC+10)
  - cron: '0 2 * * *'   # 12 PM AEST (UTC+10)
  - cron: '0 8 * * *'   # 6 PM AEST (UTC+10)
```

## 📊 Module Overview

### config.py
Centralized configuration and API endpoint management.

### logger.py
Structured logging to file and console with timestamp tracking.

### news_fetcher.py
Fetches top Australian news headlines, filters duplicates, and validates content.

### content_processor.py
Uses Gemini AI to summarize articles, add emojis, hashtags, and optional Arabic translation.

### facebook_poster.py
Posts content to Facebook Page using Graph API v19.0 with image support.

### image_handler.py
Manages image URLs from articles with validation and optional AI generation.

### utils.py
Helper functions: retry logic, text sanitization, URL validation, etc.

### main.py
Orchestrates the complete pipeline from news to Facebook post.

## 🛠️ Testing

```bash
# Test connection to all APIs
python -m src.main --test

# Run full pipeline
python -m src.main

# Check logs
cat logs/facebook_automation_*.log
```

## 📝 Logs

Logs are automatically created in:
```
logs/facebook_automation_YYYYMMDD.log
```

View logs in GitHub Actions:
1. Go to repository → Actions tab
2. Select latest workflow run
3. View logs in job details

## ⚠️ Troubleshooting

### Invalid API Key
- Verify key is correctly added to GitHub Secrets
- Check key hasn't been revoked on API provider dashboard

### Facebook Post Fails
- Verify page token is still valid (may need regeneration)
- Check page ID is correct
- Ensure page is in Business mode

### Gemini API Rate Limited
- Free tier: 60 requests/minute
- Add delays or upgrade to paid tier

### No News Results
- Check NewsAPI free tier limit (100 requests/day)
- Verify internet connection

## 📈 Cost Breakdown

| Service | Cost | Tier |
|---------|------|------|
| NewsAPI | Free | 100 req/day |
| Gemini API | Free | 60 req/min |
| Facebook API | Free | Unlimited |
| GitHub Actions | Free | 2000 min/month |
| **Total** | **$0** | **Free** |

## 🔐 Security

- All API keys stored in GitHub Secrets
- No credentials in repository
- Environment variables for local development
- Rotate tokens every 3 months

## 📚 Documentation

- [PROJECT_PLAN.md](documents/plan/PROJECT_PLAN.md) - Full project overview
- [SETUP_STEPS.md](documents/steps/SETUP_STEPS.md) - Step-by-step setup guide
- [ARCHITECTURE.md](documents/steps/ARCHITECTURE.md) - System architecture details

## 🚀 Future Enhancements

- [ ] Image generation with DALL-E
- [ ] Analytics dashboard
- [ ] Multiple language support
- [ ] Docker containerization
- [ ] AWS Lambda deployment
- [ ] Notification system
- [ ] Database for tracking posts

## 📄 License

MIT License - Feel free to use and modify

## 👨‍💻 Author

Created as an automated news posting solution for Australian content.

---

**Questions?** Check the documentation files in the `documents/` folder for detailed setup and architecture information.
