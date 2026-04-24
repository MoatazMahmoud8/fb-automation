# 🎯 Simple Automation Quick Start

Get started with Facebook automation in **5 minutes**! This is the simplified version that posts in Arabic.

## ⚡ Quick Setup

### Linux/Mac
```bash
cd /home/moataz/work/fbautomation/repo
chmod +x simple-start.sh
./simple-start.sh
```

### Windows
```cmd
cd C:\path\to\fbautomation\repo
simple-start.bat
```

### Manual Setup
```bash
# 1. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Copy and configure environment
cp .env.example .env
nano .env  # Edit with your API keys

# 4. Run
python simple_automation.py
```

## 🔑 Required API Keys

1. **NewsAPI** (Already provided ✓)
   ```
   bd3749c6a550467da6dd1fe30fed9cbc
   ```

2. **Gemini API Key**
   - Go to: https://aistudio.google.com/app/apikeys
   - Click "Create API Key"
   - Copy and paste into .env

3. **Facebook Page Token**
   - Go to: https://developers.facebook.com/tools/explorer
   - Select your app
   - Generate "Get Page Access Tokens"
   - Copy token to .env

4. **Facebook Page ID**
   - Go to: https://www.facebook.com/your-page
   - Add `?v=info` to URL
   - Find Page ID in page details
   - Or use: `https://graph.facebook.com/me?access_token=YOUR_TOKEN`

## 📝 Configuration (.env)

```bash
# Required
NEWS_API_KEY=bd3749c6a550467da6dd1fe30fed9cbc
GEMINI_API_KEY=your_gemini_key_here
FB_PAGE_TOKEN=your_facebook_token_here
FB_PAGE_ID=your_facebook_page_id_here

# Optional
LANGUAGE=ar  # "ar" for Arabic, "en" for English (default: ar)
```

## 🚀 Usage

### Run Once
```bash
python simple_automation.py
```

### Run with Language Override
```bash
export LANGUAGE=en  # English
python simple_automation.py

export LANGUAGE=ar  # Arabic
python simple_automation.py
```

### Run Every Hour (Linux/Mac)
```bash
# Create a loop
while true; do
    python simple_automation.py
    echo "Waiting 1 hour before next run..."
    sleep 3600
done
```

### Run on Schedule (Cron)
```bash
# Edit crontab
crontab -e

# Add: Run at 9 AM, 12 PM, 6 PM daily
0 9,12,18 * * * cd /home/moataz/work/fbautomation/repo && python simple_automation.py

# Or use: 
0 23 * * * (UTC 9 AM AEST)
0 2 * * * (UTC 12 PM AEST)
0 8 * * * (UTC 6 PM AEST)
```

## ✅ What It Does

1. ✓ Fetches top Australian news
2. ✓ Generates Arabic Facebook post
3. ✓ Validates image URL
4. ✓ Posts to your Facebook page
5. ✓ Retries on failure
6. ✓ Reports success/failure

## 📊 Output Example

```
============================================================
  Facebook Automation - Arabic Posts
============================================================

✓ Configuration validated
Fetching news (attempt 1/3)...
✓ News fetched: Australia's Tech Industry Continues...
✓ Image validated: https://newsapi.org/...
Generating AR post...
✓ Post generated (287 characters)
Posting to Facebook (attempt 1/3)...
✓ Post successful! ID: 123456789_987654321

============================================================
  ✓ Pipeline Completed Successfully!
============================================================
```

## 🐛 Troubleshooting

### "Missing required environment variables"
**Solution:** Check .env file has all 4 keys
```bash
cat .env
```

### "Failed to fetch news"
**Causes:**
- NewsAPI key invalid or rate limited (100/day)
- Internet connection issue
- No articles available for Australia

**Solution:** Wait 24 hours or verify key

### "Error generating post" 
**Causes:**
- Gemini API key invalid
- Rate limited (60 requests/minute)
- Empty response

**Solution:** Verify key, wait a minute, try again

### "Failed to post to Facebook"
**Causes:**
- Facebook token expired
- Page ID incorrect
- Page not in Business mode
- Image URL inaccessible

**Solution:**
```bash
# Regenerate token from https://developers.facebook.com/tools/explorer
# Update .env with new token
# Verify page ID: https://graph.facebook.com/me?access_token=TOKEN
```

## 📚 Next Steps

### Use Simple Automation If:
- ✓ You only want Arabic posts
- ✓ You prefer simple code
- ✓ You're testing first
- ✓ You run manually occasionally

### Upgrade to Production If:
- ✓ You want daily automatic posts
- ✓ You need English + Arabic
- ✓ You want GitHub Actions
- ✓ You need error monitoring

**Upgrade Command:**
```bash
python hybrid.py --production
# or
python -m src.main
```

## 🔗 Related Files

- [SIMPLE_VS_PRODUCTION.md](SIMPLE_VS_PRODUCTION.md) - Compare both systems
- [README.md](README.md) - Full project docs
- [QUICK_REFERENCE.md](../documents/QUICK_REFERENCE.md) - Command lookup
- [hybrid.py](hybrid.py) - Switch between simple/production

## 💡 Tips

1. **Test Connection First**
   ```bash
   # Make a test API call
   curl "https://newsapi.org/v2/top-headlines?country=au&apiKey=bd3749c6a550467da6dd1fe30fed9cbc"
   ```

2. **Check Logs**
   ```bash
   # View last run output
   python simple_automation.py 2>&1 | tee last-run.log
   ```

3. **Multiple Runs**
   ```bash
   # Run 3 times with delays
   for i in 1 2 3; do
       echo "Run $i"
       python simple_automation.py
       sleep 10
   done
   ```

4. **Change Language**
   ```bash
   # Quick English post
   LANGUAGE=en python simple_automation.py
   ```

## 🎓 Learn More

- **System Design**: [ARCHITECTURE.md](../documents/steps/ARCHITECTURE.md)
- **Full Integration**: [COMPLETE_INTEGRATION_GUIDE.md](../documents/steps/COMPLETE_INTEGRATION_GUIDE.md)
- **Production System**: [src/main.py](src/main.py)

---

**Created:** April 24, 2026  
**Status:** ✅ Ready to Use  
**Estimated Time:** 5 minutes setup + 1 minute per run
