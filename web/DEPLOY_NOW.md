# 🚀 Deploy to Vercel NOW - Quick Guide

## ⚠️ IMPORTANT: Vercel Limitations

Vercel has a **10 second timeout** on free tier (60 seconds on Pro).
This means:
- ✅ Works for: Very short videos (< 5 seconds compression time)
- ❌ Fails for: Most videos (they take 30-60+ seconds)

**For production use, see [DEPLOYMENT.md](../DEPLOYMENT.md) for Railway (recommended).**

---

## Option 1: Deploy via Vercel Dashboard (Easiest)

### Step 1: Create GitHub Repository

```bash
cd ~/video-compressor-sdk

# Initialize git
git init

# Add all files
git add .
git commit -m "Initial commit"
```

### Step 2: Push to GitHub

1. Go to [GitHub.com](https://github.com)
2. Click **"New repository"**
3. Name it: `video-compressor-sdk`
4. Don't initialize with README
5. Copy the commands and run:

```bash
git remote add origin https://github.com/YOUR_USERNAME/video-compressor-sdk.git
git branch -M main
git push -u origin main
```

### Step 3: Deploy to Vercel

1. Go to [Vercel.com](https://vercel.com)
2. Click **"Add New Project"**
3. **Import Git Repository** → Select `video-compressor-sdk`
4. **Framework Preset:** Other
5. **Root Directory:** `web`
6. Click **"Deploy"**

**Done!** Vercel will give you a URL like: `https://video-compressor-xxx.vercel.app`

---

## Option 2: Deploy via Vercel CLI (Faster)

### Step 1: Install Vercel CLI

```bash
npm install -g vercel
# or
brew install vercel-cli
```

### Step 2: Login and Deploy

```bash
cd ~/video-compressor-sdk/web

# Login to Vercel
vercel login

# Deploy (production)
vercel --prod
```

### Step 3: Answer Prompts

```
? Set up and deploy? Y
? Which scope? [Your username]
? Link to existing project? N
? What's your project's name? video-compressor
? In which directory is your code located? ./
? Override settings? N
```

Vercel will deploy and give you a URL!

---

## ✅ Verify Deployment

After deployment:

1. **Open your Vercel URL**
2. **Test with a SHORT video** (< 10MB, will compress in ~5 seconds)
3. **Select "web-small" preset** (fastest)
4. **Watch for timeout errors** on longer videos

---

## 🐛 Common Issues

### Issue: "Serverless Function Timeout"

**Cause:** Video takes > 10 seconds to compress

**Solutions:**
1. Use shorter videos (< 5 seconds long)
2. Use "web-small" preset
3. **Upgrade to Vercel Pro** ($20/month for 60s timeout)
4. **Use Railway instead** (no timeout, $5/month free credit)

### Issue: "FFmpeg not found"

**Solution:** Vercel includes FFmpeg by default. If missing:
1. Check deployment logs
2. Ensure `vercel.json` is properly configured
3. Try redeploying

### Issue: "Module not found"

**Solution:**
1. Ensure `requirements.txt` exists in `web/` directory
2. Check it includes:
   ```
   Flask==3.0.0
   Werkzeug==3.0.1
   ```
3. Redeploy

---

## 🎯 Current Files Ready for Deployment

Your `web/` directory now has:

```
web/
├── app.py                  ✅ Updated for production
├── vercel.json            ✅ Vercel configuration
├── requirements.txt       ✅ Python dependencies
├── Procfile              ✅ For Railway
├── railway.json          ✅ For Railway
├── .vercelignore         ✅ Ignore unnecessary files
├── templates/
│   └── index.html        ✅ UI
└── static/
    ├── style.css         ✅ Styles
    └── script.js         ✅ Frontend logic
```

---

## 📊 What Happens on Vercel

When you deploy:
1. Vercel reads `vercel.json` configuration
2. Installs dependencies from `requirements.txt`
3. Creates serverless function from `app.py`
4. Serves static files (HTML, CSS, JS)
5. Gives you a HTTPS URL

---

## 🚀 Deploy Command Summary

**Fastest way (if you have Vercel CLI):**

```bash
cd ~/video-compressor-sdk/web
vercel --prod
```

**That's it!** Your app will be live in ~2 minutes.

---

## 🎬 After Deployment

### Test Your Deployment

1. Open Vercel URL
2. Upload a **short** test video
3. Select "web-small" preset
4. Click compress
5. If successful → Share your URL! 🎉
6. If timeout → Consider Railway (see [DEPLOYMENT.md](../DEPLOYMENT.md))

### Share Your App

Your app is live at: `https://video-compressor-xxx.vercel.app`

Share it with:
- Friends
- Portfolio
- GitHub README
- LinkedIn

---

## ⭐ Recommended: Deploy to Railway Too

For videos that actually work (no timeout):

```bash
# See full Railway guide in DEPLOYMENT.md
# Basically:
# 1. Push to GitHub
# 2. Connect Railway to GitHub repo
# 3. One-click deploy
# 4. Done! No timeouts!
```

Railway is **better** for video compression. Vercel is **better** for demos.

---

## 🎉 You're Ready!

Run this now:

```bash
cd ~/video-compressor-sdk/web
vercel --prod
```

Or follow the GitHub → Vercel dashboard method above.

**Happy deploying! 🚀**
