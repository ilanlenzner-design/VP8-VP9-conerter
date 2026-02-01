# Video Compressor SDK - Quick Start Guide

## ✅ Installation Complete!

Your video compression SDK is ready to use at: `~/video-compressor-sdk`

## 🚀 Quick Test Results

### Single File Compression
- **Input:** 2.49 MB → **Output:** 1.03 MB
- **Compression ratio:** 2.42x
- **Time:** ~4 seconds

### Batch Compression (3 files)
- **Total input:** 8.81 MB → **Total output:** 0.94 MB
- **Overall ratio:** 9.40x
- **Space saved:** 89.4%
- **Parallel processing:** 2 workers

## 📦 What's Included

```
video-compressor-sdk/
├── src/video_compressor/     # Core SDK library
├── examples/                  # 4 example scripts
├── test_basic.py             # Run basic tests
├── test_compress.py          # Compress single video
├── test_batch.py             # Batch compress videos
├── test_output/              # Compressed test videos
└── README.md                 # Full documentation
```

## 💻 Usage Examples

### 1. Simple Compression

```python
import sys
sys.path.insert(0, '/Users/ilan/video-compressor-sdk/src')

from video_compressor import VideoCompressor

compressor = VideoCompressor()
result = compressor.compress(
    input_path='video.mp4',
    output_path='video.webm',
    preset='web'
)
print(f"Compressed {result.compression_ratio:.2f}x")
```

### 2. With Progress Tracking

```python
def progress(filename, percentage, current_time, total_time, eta):
    print(f"{filename}: {percentage:.1f}% (ETA: {eta:.0f}s)")

result = compressor.compress(
    'video.mp4', 'output.webm',
    progress_callback=progress
)
```

### 3. Batch Processing

```python
from video_compressor import BatchCompressor

batch = BatchCompressor(compressor, max_workers=4)
results = batch.compress_batch(
    files=['video1.mp4', 'video2.mp4', 'video3.mp4'],
    output_dir='./compressed',
    preset='web'
)
```

### 4. Alpha Channel (Transparency)

```python
result = compressor.compress(
    'logo_with_alpha.mov',
    'logo.webm',
    preset='alpha-web',
    preserve_alpha=True
)
```

## 🎯 Built-in Presets

| Preset | Best For | Compression | Speed |
|--------|----------|-------------|-------|
| `web-small` | Small files, fast web | Very High | Fast |
| `web` | General web videos | High | Fast |
| `archive` | Long-term storage | Medium | Slow |
| `high-quality` | Maximum quality | Low | Slow |
| `vp8-legacy` | Old browser support | High | Fast |
| `alpha-web` | Transparent videos | High | Medium |

## 🛠️ Command-Line Tools

### Test Single Video
```bash
cd ~/video-compressor-sdk
python3 test_compress.py /path/to/video.mp4 --preset web
```

### Test Batch Compression
```bash
python3 test_batch.py
```

### Run Basic Tests
```bash
python3 test_basic.py
```

## 🔧 Custom Presets

```python
from video_compressor import CompressionPreset

mobile = CompressionPreset(
    name='Mobile',
    codec='vp9',
    video_bitrate='500k',
    audio_bitrate='64k',
    crf=36,
    speed=5,
    max_resolution=(854, 480)
)

compressor.add_preset('mobile', mobile)
result = compressor.compress('video.mp4', 'mobile.webm', preset='mobile')
```

## 📊 Performance Tips

1. **Fast encoding:** Use `web-small` preset or increase `speed` parameter
2. **Best quality:** Use `archive` or `high-quality` presets
3. **Batch processing:** Set `max_workers=4` or more for parallel compression
4. **Alpha channel:** Only VP9 supports transparency (`preserve_alpha=True`)

## 📝 Example Output

Check your test results:
- Single compressed video: `~/Downloads/Untitled video (6)_compressed.webm`
- Batch compressed videos: `~/video-compressor-sdk/test_output/`

## 🎓 Full Documentation

Read the complete documentation: [README.md](README.md)

## 🔗 Quick Links

- **Examples:** `~/video-compressor-sdk/examples/`
- **Source code:** `~/video-compressor-sdk/src/video_compressor/`
- **Test scripts:** `~/video-compressor-sdk/test_*.py`

## 🆘 Troubleshooting

**FFmpeg not found:**
```bash
brew install ffmpeg
```

**Import error:**
```python
import sys
sys.path.insert(0, '/Users/ilan/video-compressor-sdk/src')
```

**Slow encoding:**
- Use `web-small` preset
- Increase `speed` parameter (4-5)
- Set lower `max_resolution`

## ✨ What's Next?

1. Try different presets on your videos
2. Create custom presets for your needs
3. Integrate into your projects
4. Check out the example scripts for more ideas

---

**Your SDK is ready to compress videos like a pro! 🎬**
