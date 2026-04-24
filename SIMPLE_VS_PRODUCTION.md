# Simple vs Production Comparison Guide

## Quick Choice

**Use Simple Automation if:**
- You want just Arabic posts
- You prefer minimal dependencies
- You're testing/learning
- You like straightforward code

**Use Production System if:**
- You want daily automated posts (3x/day)
- You need English + Arabic support
- You want error recovery & monitoring
- You need GitHub Actions scheduling

## File Locations

```
repo/
├── simple_automation.py      # Enhanced simple script (Arabic-focused)
├── src/main.py              # Production system (full featured)
├── hybrid.py                # Choose between both
└── requirements.txt         # All dependencies
```

## Usage

### Simple Automation Only
```bash
python simple_automation.py
```

### Production System Only
```bash
python -m src.main
```

### Choose at Runtime
```bash
python hybrid.py --simple       # Run simple
python hybrid.py --production   # Run full
python hybrid.py --test         # Test connections
```

## Feature Comparison

| Feature | Simple | Production |
|---------|--------|------------|
| Language | Arabic only | English + Arabic |
| Manual Run | ✓ | ✓ |
| Scheduled (3x daily) | ✗ | ✓ |
| Error Retries | ✓ | ✓ |
| Logging | ✗ | ✓ |
| Image Validation | ✓ | ✓ |
| Duplicate Detection | ✗ | ✓ |
| GitHub Actions | ✗ | ✓ |
| Connection Testing | ✗ | ✓ |
| Lines of Code | ~250 | ~2000 |
| Modules | 1 | 8 |

## Simple Automation Features

✅ Fetch top Australian news
✅ Generate Arabic posts
✅ Validate images
✅ Post to Facebook
✅ Error handling & retries
✅ Exponential backoff
✅ Timeout protection
✅ Configuration validation

## How to Use Simple Automation

### 1. Local Testing
```bash
cd /home/moataz/work/fbautomation/repo
export NEWS_API_KEY="bd3749c6a550467da6dd1fe30fed9cbc"
export GEMINI_API_KEY="your_gemini_key"
export FB_PAGE_TOKEN="your_facebook_token"
export FB_PAGE_ID="your_page_id"

python simple_automation.py
```

### 2. With .env File
```bash
cp .env.example .env
# Edit .env with your keys
source venv/bin/activate
python simple_automation.py
```

### 3. Run Multiple Times
```bash
# Run every hour manually
for i in {1..24}; do
    python simple_automation.py
    sleep 3600
done
```

### 4. Change Language
```bash
export LANGUAGE=en  # English
python simple_automation.py

export LANGUAGE=ar  # Arabic (default)
python simple_automation.py
```

## Production System Benefits

If you graduate from simple automation, the production system provides:

✅ Automatic daily scheduling (9 AM, 12 PM, 6 PM)
✅ GitHub Actions deployment
✅ Comprehensive logging
✅ Connection testing
✅ Duplicate filtering
✅ Multiple language support
✅ Advanced error handling
✅ Performance monitoring

## Recommended Path

1. **Start with Simple** - Test the concept
   ```bash
   python simple_automation.py
   ```

2. **Verify it works** - Check Facebook page
   
3. **Move to Production** - For daily automation
   ```bash
   # Follow /home/moataz/work/fbautomation/documents/steps/COMPLETE_INTEGRATION_GUIDE.md
   ```

4. **Deploy to GitHub** - Serverless scheduling
   ```bash
   git push origin main
   ```

## Configuration

### Simple Automation Environment Variables
```
NEWS_API_KEY=bd3749c6a550467da6dd1fe30fed9cbc
GEMINI_API_KEY=your_gemini_key
FB_PAGE_TOKEN=your_facebook_token
FB_PAGE_ID=your_facebook_page_id
LANGUAGE=ar  # "ar" for Arabic, "en" for English
```

### Settings
```python
MAX_RETRIES = 3        # Retry failed requests
API_TIMEOUT = 30       # Seconds to wait per request
```

## Troubleshooting

### "Failed to fetch news"
- Check NewsAPI key is correct
- Verify internet connection
- Check if rate limited (100 requests/day)

### "Error generating post"
- Verify Gemini API key is valid
- Check free tier quota (60 requests/minute)
- Try again after a minute

### "Failed to post to Facebook"
- Verify Facebook token is current
- Check page ID is correct
- Ensure page is in Business mode
- Try regenerating the token

### "Image validation failed"
- Article may not have image URL
- Image server may be down
- Try a different news source

## Next Steps

1. **Test Simple** - Run and verify
2. **Compare** - See if you need production features
3. **Choose Path:**
   - Keep simple for occasional posts
   - Upgrade to production for daily automation
4. **Optimize** - Customize prompts/settings as needed

## Support Files

- [QUICK_REFERENCE.md](../documents/QUICK_REFERENCE.md) - Quick commands
- [COMPLETE_INTEGRATION_GUIDE.md](../documents/steps/COMPLETE_INTEGRATION_GUIDE.md) - Full setup
- [ARCHITECTURE.md](../documents/steps/ARCHITECTURE.md) - System design
