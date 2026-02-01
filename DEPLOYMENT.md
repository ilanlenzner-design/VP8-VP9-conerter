# Video Compressor - Deployment Guide

## 🚀 Deployment Options

Your video compressor can be deployed to various platforms. Here are the best options:

---

## 1. Railway (⭐ RECOMMENDED for Video Processing)

**Why Railway?**
- ✅ No timeout limits (perfect for long video processing)
- ✅ $5/month free credit
- ✅ Persistent storage
- ✅ Easy deployment from GitHub
- ✅ Automatic HTTPS

### Deploy to Railway

#### Step 1: Create GitHub Repository

```bash
cd ~/video-compressor-sdk

# Initialize git if not already done
git init

# Create .gitignore
cat > .gitignore << 'EOF'
__pycache__/
*.pyc
*.log
web/uploads/*
web/compressed/*
.env
venv/
*.mp4
*.webm
*.mov
EOF

# Add files
git add .
git commit -m "Initial commit - Video Compressor SDK"
```

#### Step 2: Push to GitHub

```bash
# Create a new repository on GitHub first, then:
git remote add origin https://github.com/YOUR_USERNAME/video-compressor-sdk.git
git branch -M main
git push -u origin main
```

#### Step 3: Deploy to Railway

1. Go to [Railway.app](https://railway.app)
2. Sign up with GitHub
3. Click **"New Project"**
4. Select **"Deploy from GitHub repo"**
5. Choose your `video-compressor-sdk` repository
6. Railway will auto-detect Python and deploy!

#### Step 4: Configure Railway

Railway should automatically:
- Detect `web/app.py`
- Install dependencies from `requirements.txt`
- Use the `Procfile` to start the app

If needed, set these environment variables in Railway:
- `PORT`: Railway sets this automatically
- `PYTHONPATH`: `/app/src` (if imports fail)

#### Step 5: Get Your URL

Railway will give you a URL like: `https://video-compressor-production.up.railway.app`

**That's it! Your app is live! 🎉**

---

## 2. Vercel (⚠️ Limited - For Demo Only)

**Why Vercel?**
- ✅ Free tier
- ✅ Fast deployment
- ❌ 10 second timeout (Hobby) / 60 seconds (Pro)
- ❌ Only good for VERY short videos

### Deploy to Vercel

#### Step 1: Install Vercel CLI

```bash
npm install -g vercel
```

#### Step 2: Deploy

```bash
cd ~/video-compressor-sdk/web

# Login to Vercel
vercel login

# Deploy
vercel
```

Follow the prompts:
- Set up and deploy? **Y**
- Which scope? **Your username**
- Link to existing project? **N**
- Project name? **video-compressor**
- Directory? **./web**
- Override settings? **N**

#### Step 3: Get Your URL

Vercel will give you a URL like: `https://video-compressor.vercel.app`

**⚠️ WARNING:** Vercel will timeout on videos that take more than 10 seconds to compress. Use Railway for production!

---

## 3. Render (Alternative)

**Why Render?**
- ✅ Free tier available
- ✅ No timeout limits
- ✅ Easy deployment

### Deploy to Render

1. Go to [Render.com](https://render.com)
2. Sign up and connect GitHub
3. Click **"New +"** → **"Web Service"**
4. Select your repository
5. Configure:
   - **Name:** video-compressor
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `cd web && python app.py`
6. Click **"Create Web Service"**

Render will deploy and give you a URL like: `https://video-compressor.onrender.com`

---

## 4. DigitalOcean App Platform

1. Go to [DigitalOcean App Platform](https://cloud.digitalocean.com/apps)
2. Click **"Create App"**
3. Connect GitHub repository
4. Configure:
   - **Resource Type:** Web Service
   - **Run Command:** `cd web && python app.py`
5. Deploy!

Starts at $5/month.

---

## 📦 Pre-Deployment Checklist

Before deploying, ensure:

### 1. Update requirements.txt

Your `web/requirements.txt` should include:
```
Flask>=3.0.0
Werkzeug>=3.0.1
```

### 2. Environment Variables

Set these if needed:
- `PORT` - Usually set automatically by platform
- `FLASK_ENV` - Set to `production`

### 3. Security (For Production)

Add to your deployment:
- Rate limiting
- File size limits (already set to 500MB)
- Authentication (if needed)
- CORS configuration (if accessing from different domain)

---

## 🧪 Testing Deployed App

After deployment, test:

1. **Upload a short video** (< 10MB)
2. **Select preset** (try "web-small" for fastest processing)
3. **Monitor progress**
4. **Download result**

---

## 🔧 Troubleshooting

### Railway Issues

**App not starting:**
- Check logs in Railway dashboard
- Ensure `Procfile` exists
- Verify FFmpeg is available (usually auto-installed)

**Imports failing:**
- Set `PYTHONPATH=/app/src` in environment variables

### Vercel Issues

**Timeout errors:**
- Use smaller videos (< 5 seconds long)
- Use faster preset ("web-small")
- Consider upgrading to Pro ($20/month for 60s timeout)
- Or switch to Railway/Render

**Import errors:**
- Ensure `vercel_requirements.txt` includes all dependencies
- Check function logs in Vercel dashboard

### General Issues

**FFmpeg not found:**
- Ensure platform has FFmpeg installed
- For Railway: Add `nixpacks.toml`:
  ```toml
  [phases.setup]
  nixPkgs = ['python39', 'ffmpeg']
  ```

**File upload fails:**
- Check max file size (500MB limit)
- Verify upload directory is writable
- Check platform storage limits

---

## 🎯 Recommended Setup

For the best experience:

### Development (Local)
```bash
cd ~/video-compressor-sdk/web
python3 launch.py
# Access at http://localhost:5000
```

### Demo/Testing (Vercel)
- Quick deploys
- Good for showing off
- Short videos only

### Production (Railway)
- No timeout limits
- Handle long videos
- $5/month free credit
- Best for real use

---

## 📊 Platform Comparison

| Feature | Railway | Vercel | Render | DigitalOcean |
|---------|---------|--------|--------|--------------|
| **Free Tier** | $5/month credit | Yes | Yes | No ($5/mo) |
| **Timeout** | None | 10-60s | None | None |
| **Storage** | Persistent | Ephemeral | Persistent | Persistent |
| **FFmpeg** | ✅ | ✅ | ✅ | ✅ |
| **Best For** | Production | Demo | Production | Production |
| **Difficulty** | Easy | Easy | Easy | Medium |

---

## 🚀 Quick Deploy Commands

### Railway (Recommended)
```bash
# 1. Push to GitHub
git add . && git commit -m "Deploy" && git push

# 2. Deploy via Railway dashboard (one-click)
```

### Vercel
```bash
cd ~/video-compressor-sdk/web
vercel --prod
```

### Manual (Any VPS)
```bash
# SSH into your server
ssh user@your-server.com

# Clone repository
git clone https://github.com/YOUR_USERNAME/video-compressor-sdk.git
cd video-compressor-sdk/web

# Install dependencies
pip3 install -r requirements.txt

# Install FFmpeg
sudo apt-get install ffmpeg

# Run with gunicorn (production)
pip3 install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

## 📝 Next Steps

1. **Choose your platform** (Railway recommended)
2. **Push to GitHub** (if deploying to Railway/Render)
3. **Follow platform-specific steps above**
4. **Test your deployment**
5. **Share your URL!** 🎉

---

**Need help?** Check the platform-specific documentation:
- [Railway Docs](https://docs.railway.app)
- [Vercel Docs](https://vercel.com/docs)
- [Render Docs](https://render.com/docs)
