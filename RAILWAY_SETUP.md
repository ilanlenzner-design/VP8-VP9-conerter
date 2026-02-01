# Railway Deployment - Terminal Commands

## Step 1: Login to Railway CLI

```bash
railway login
```

This will open a browser window - authorize the CLI.

## Step 2: Link to Your Project

```bash
cd ~/video-compressor-sdk
railway link
```

Select your project: **VP8-VP9-conerter**

## Step 3: Check Current Status

```bash
railway status
```

## Step 4: View Deployment Logs

```bash
railway logs
```

Look for errors in the logs.

## Step 5: Force Redeploy

```bash
railway up
```

This will redeploy your app.

## Step 6: Get Your URL

```bash
railway domain
```

## Common Issues:

### If "No service found":
1. Go to Railway dashboard
2. Click your project
3. Click "New Service"
4. Select "GitHub Repo"
5. Choose VP8-VP9-conerter

### If builds keep failing:
Check that these files exist:
- `nixpacks.toml` ✓
- `web/requirements.txt` ✓  
- `web/app.py` ✓
- `web/video_compressor/` folder ✓

All present! ✅

### Alternative: Manual Railway Setup

If CLI doesn't work:
1. Go to https://railway.app/dashboard
2. Delete current project
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose "VP8-VP9-conerter"
6. Railway will auto-detect and deploy

