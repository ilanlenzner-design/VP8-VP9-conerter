# Video Compressor - Web UI Guide

## 🎉 Your Web Interface is Ready!

The web interface for the Video Compressor SDK is now running at:

**🌐 http://localhost:5000**

## 🚀 Quick Start

1. **Open your browser** and go to: http://localhost:5000
2. **Drag and drop** a video file or **click to browse**
3. **Select a compression preset** (web, web-small, archive, etc.)
4. **Click "Start Compression"**
5. **Watch real-time progress** with ETA
6. **Download your compressed video!**

## ✨ Features

### Beautiful UI
- 🎨 Modern gradient design
- 📱 Fully responsive (works on mobile)
- 🎯 Drag-and-drop file upload
- ⏳ Real-time progress tracking

### Compression Options
- **6 Built-in Presets:**
  - `web` - General web videos (1M bitrate)
  - `web-small` - Small files (500k bitrate)
  - `archive` - High quality archive (3M bitrate)
  - `high-quality` - Maximum quality (5M bitrate)
  - `vp8-legacy` - VP8 for older browsers
  - `alpha-web` - Transparency support

- **Alpha Channel Support** - Check the box to preserve transparency (VP9 only)

### Real-Time Feedback
- Upload progress
- Video metadata display (resolution, duration, codec)
- Compression progress with percentage and ETA
- Detailed results (compression ratio, space saved)

## 📊 How It Works

### 1. Upload Phase
Drop or select your video → Server uploads → Shows video info

### 2. Compression Phase
Select preset → Start compression → Watch progress in real-time

### 3. Results Phase
View statistics → Download compressed video → Compress another

## 🎮 Server Control

### Start Server
```bash
cd ~/video-compressor-sdk/web
python3 launch.py
```

### Stop Server
Press `Ctrl+C` in the terminal running the server

### Restart Server
Stop with `Ctrl+C`, then run `python3 launch.py` again

## 📁 File Structure

```
web/
├── app.py              # Flask server (API endpoints)
├── launch.py           # Launcher script
├── templates/
│   └── index.html     # Main UI page
├── static/
│   ├── style.css      # Beautiful styling
│   └── script.js      # Client-side functionality
├── uploads/           # Temporary uploaded files
└── compressed/        # Compressed output files
```

## 🔧 API Endpoints

The web interface uses these REST API endpoints:

- `GET /` - Main page
- `GET /api/presets` - List available presets
- `POST /api/upload` - Upload video file
- `POST /api/compress` - Start compression
- `GET /api/progress/<file_id>` - Real-time progress (Server-Sent Events)
- `GET /api/download/<file_id>` - Download compressed video
- `DELETE /api/cleanup/<file_id>` - Clean up files

## 💡 Usage Tips

### For Best Results:
1. **Small files:** Use `web-small` preset
2. **Quality matters:** Use `archive` or `high-quality`
3. **Fast encoding:** Use `web` or `web-small`
4. **Transparency:** Use `alpha-web` with "Preserve Alpha" checked

### File Size Limits:
- Maximum upload: 500 MB
- Supported formats: MP4, MOV, AVI, MKV, WebM

### Performance:
- Compression happens server-side
- Progress updates every 0.5 seconds
- Files are automatically cleaned up

## 🐛 Troubleshooting

**Server won't start:**
```bash
# Check if port 5000 is already in use
lsof -i :5000

# Kill existing process if needed
kill -9 <PID>

# Restart server
python3 launch.py
```

**Can't access from browser:**
- Check firewall settings
- Try http://127.0.0.1:5000 instead
- Make sure server is running (check terminal)

**Upload fails:**
- Check file size (max 500 MB)
- Verify file format is supported
- Check available disk space

**Compression fails:**
- Ensure FFmpeg is installed: `ffmpeg -version`
- Check server terminal for error messages
- Try a different preset

## 🔒 Security Note

This web interface is designed for **local use only**. It:
- Runs on localhost (127.0.0.1)
- Is not production-ready for public deployment
- Has no authentication
- Stores files temporarily on disk

For production use, you would need to add:
- User authentication
- File size/rate limiting
- HTTPS/SSL
- Cloud storage integration
- Better error handling

## 🎯 Next Steps

1. **Test with your videos** - Try different presets
2. **Compare results** - See compression ratios
3. **Integrate the SDK** - Use the Python API in your own projects
4. **Customize presets** - Create your own compression profiles

## 📖 Documentation

- Full SDK docs: [README.md](../README.md)
- Quick start: [QUICKSTART.md](../QUICKSTART.md)
- Code examples: [examples/](../examples/)

## 🎬 Enjoy Compressing!

Your web interface is ready to compress videos with beautiful UI and real-time progress tracking!

---

**Currently running at:** http://localhost:5000
