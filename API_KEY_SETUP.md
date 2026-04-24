# 🔐 API Key Setup & Security Guide

## Your Gemini API Key Details

```
API Key: AIzaSyCsz1kt8TZQ4RwlmG-YOxjDB0_-NTwJ2Ro
Project: projects/999369531191
Project Number: 999369531191
Name: Gemini API Key
```

## ⚠️ IMPORTANT: Security Best Practices

### DO ✅
- Store in .env file (local development)
- Store in GitHub Secrets (for GitHub Actions)
- Use environment variables at runtime
- Rotate keys periodically
- Keep .env in .gitignore

### DON'T ❌
- Commit .env to git
- Share keys in messages/chat
- Hardcode keys in Python files
- Upload keys to GitHub repo
- Use same key for multiple projects

## 🔧 Setup Options

### Option 1: Interactive Setup (Recommended)

**Linux/Mac:**
```bash
cd /home/moataz/work/fbautomation/repo
chmod +x setup-keys.sh
./setup-keys.sh
```

**Windows:**
```cmd
cd C:\path\to\fbautomation\repo
setup-keys.bat
```

This will:
- Prompt for all 3 API keys
- Create .env file securely
- Protect .env in .gitignore
- Show next steps

### Option 2: Manual Setup

**1. Create .env file:**
```bash
cd /home/moataz/work/fbautomation/repo
cp .env.example .env
```

**2. Edit .env with your keys:**
```bash
# Linux/Mac
nano .env

# Windows
notepad .env
```

**3. Add your credentials:**
```
NEWS_API_KEY=bd3749c6a550467da6dd1fe30fed9cbc

GEMINI_API_KEY=AIzaSyCsz1kt8TZQ4RwlmG-YOxjDB0_-NTwJ2Ro

FB_PAGE_TOKEN=your_facebook_page_token_here

FB_PAGE_ID=your_facebook_page_id_here
```

**4. Save and close**

### Option 3: Environment Variables (No .env file)

**Linux/Mac:**
```bash
export NEWS_API_KEY="bd3749c6a550467da6dd1fe30fed9cbc"
export GEMINI_API_KEY="AIzaSyCsz1kt8TZQ4RwlmG-YOxjDB0_-NTwJ2Ro"
export FB_PAGE_TOKEN="your_facebook_page_token_here"
export FB_PAGE_ID="your_facebook_page_id_here"

python simple_automation.py
```

**Windows:**
```cmd
set NEWS_API_KEY=bd3749c6a550467da6dd1fe30fed9cbc
set GEMINI_API_KEY=AIzaSyCsz1kt8TZQ4RwlmG-YOxjDB0_-NTwJ2Ro
set FB_PAGE_TOKEN=your_facebook_page_token_here
set FB_PAGE_ID=your_facebook_page_id_here

python simple_automation.py
```

## ✅ Verify Setup

### Test Local Configuration

```bash
# Activate virtual environment
source venv/bin/activate  # Mac/Linux
# or
venv\Scripts\activate  # Windows

# Test all connections
python simple_automation.py
```

**Expected Output:**
```
✓ Configuration validated
✓ News fetched: Australia's Tech Industry...
✓ Image validated: https://...
✓ Post generated (287 characters)
✓ Post successful! ID: 123456789_987654321
```

### Test Gemini API Specifically

```python
import os
import google.generativeai as genai

os.environ["GEMINI_API_KEY"] = "AIzaSyCsz1kt8TZQ4RwlmG-YOxjDB0_-NTwJ2Ro"
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

model = genai.GenerativeModel('gemini-1.5-flash')
response = model.generate_content("Say hello in Arabic")
print(response.text)
```

### Test Facebook API

```bash
# Replace YOUR_TOKEN and YOUR_PAGE_ID
curl "https://graph.facebook.com/YOUR_PAGE_ID?access_token=YOUR_TOKEN"

# Should return:
# {"id":"YOUR_PAGE_ID","name":"Your Page Name",...}
```

## 🚀 GitHub Actions Setup

When deploying to GitHub, you need to add secrets (NOT in .env):

### Step 1: Go to GitHub Repository Settings
```
https://github.com/YOUR_USERNAME/fb-automation/settings/secrets/actions
```

### Step 2: Add These Secrets

**Secret 1: NEWS_API_KEY**
- Name: `NEWS_API_KEY`
- Value: `bd3749c6a550467da6dd1fe30fed9cbc`
- Click "Add secret"

**Secret 2: GEMINI_API_KEY**
- Name: `GEMINI_API_KEY`
- Value: `AIzaSyCsz1kt8TZQ4RwlmG-YOxjDB0_-NTwJ2Ro`
- Click "Add secret"

**Secret 3: FB_PAGE_TOKEN**
- Name: `FB_PAGE_TOKEN`
- Value: Your Facebook page token
- Click "Add secret"

**Secret 4: FB_PAGE_ID**
- Name: `FB_PAGE_ID`
- Value: Your Facebook page ID
- Click "Add secret"

### Step 3: Verify Secrets Added

```bash
# GitHub will show checkmarks for added secrets
# Go back to settings to verify all 4 are listed
```

## 🔄 Workflow

**Local Development:**
```
Python Script → reads from .env → uses API keys → posts to Facebook
```

**GitHub Actions:**
```
GitHub Actions → reads from GitHub Secrets → uses API keys → posts to Facebook
```

## ⏰ Key Rotation (Every 3 Months)

### Generate New Gemini Key
1. Go to https://aistudio.google.com/app/apikeys
2. Click the old key → Delete
3. Create new key
4. Update .env and GitHub Secrets

### Generate New Facebook Token
1. Go to https://developers.facebook.com/tools/explorer
2. Select your app
3. Get new Page Access Token
4. Update .env and GitHub Secrets

## 🔒 Security Checklist

- [x] API Key provided: AIzaSyCsz1kt8TZQ4RwlmG-YOxjDB0_-NTwJ2Ro
- [ ] .env file created with all keys
- [ ] .env is in .gitignore
- [ ] .env NOT committed to git
- [ ] GitHub Secrets added (4 keys)
- [ ] Local test passes (python simple_automation.py)
- [ ] GitHub Actions test passes
- [ ] Keys not shared/visible anywhere
- [ ] Plan to rotate keys in 3 months

## 📝 Next Steps

1. **Setup .env:**
   ```bash
   ./setup-keys.sh  # or setup-keys.bat on Windows
   ```

2. **Test locally:**
   ```bash
   python simple_automation.py
   ```

3. **Add to GitHub (if deploying):**
   - Go to Settings → Secrets
   - Add all 4 secrets

4. **Run automated test:**
   ```bash
   python -m src.main --test
   ```

5. **First post:**
   ```bash
   python simple_automation.py
   ```

## 🆘 Troubleshooting

### "GEMINI_API_KEY not set"
**Solution:**
1. Check .env file exists: `ls -la .env`
2. Check key is in .env: `grep GEMINI .env`
3. Check quotes are correct: `GEMINI_API_KEY=key_not_"key"`
4. Reload shell: `source venv/bin/activate`

### "Invalid API Key"
**Solution:**
1. Copy key exactly from: https://aistudio.google.com/app/apikeys
2. No extra spaces or quotes
3. Verify with test call
4. Regenerate if necessary

### "Facebook authentication failed"
**Solution:**
1. Check FB token is current
2. Verify page ID is correct
3. Test with curl command (see above)
4. Regenerate token if expired

## 📞 Support

See these files for help:
- [SIMPLE_QUICK_START.md](SIMPLE_QUICK_START.md) - Quick start guide
- [SIMPLE_VS_PRODUCTION.md](SIMPLE_VS_PRODUCTION.md) - Compare systems
- [../documents/QUICK_REFERENCE.md](../documents/QUICK_REFERENCE.md) - Commands

---

**API Key Status:** ✅ Provided  
**Setup Status:** ⏳ Follow one of the setup options above  
**Next:** Run setup script or manual configuration
