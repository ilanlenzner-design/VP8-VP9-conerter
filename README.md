# Video Compressor SDK

A powerful Python library for video compression using VP8/VP9 codecs with WebM output. Features include alpha channel support, batch processing, real-time progress tracking, and flexible preset configurations.

## Features

- **VP8/VP9 Codecs** - Modern, efficient video compression
- **WebM Output** - Web-optimized video format
- **Alpha Channel Support** - Preserve transparency in videos (VP9)
- **Batch Processing** - Compress multiple files concurrently
- **Progress Tracking** - Real-time compression progress with callbacks
- **Quality Presets** - Built-in presets for common use cases
- **Custom Presets** - Create your own compression profiles
- **Async Support** - Non-blocking compression operations
- **Type Hints** - Full type annotation for better IDE support

## Installation

### Prerequisites

FFmpeg must be installed on your system:

```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

### Install Package

```bash
# From source (development)
cd video-compressor-sdk
pip install -e .

# Or install dependencies directly
pip install -r requirements.txt
```

## Quick Start

```python
from video_compressor import VideoCompressor

# Create compressor
compressor = VideoCompressor()

# Compress video with 'web' preset
result = compressor.compress(
    input_path='input.mp4',
    output_path='output.webm',
    preset='web'
)

print(f"Compressed {result.compression_ratio:.2f}x")
print(f"Output size: {result.output_size_mb:.2f} MB")
```

## Built-in Presets

| Preset | Codec | Use Case | Bitrate | Quality | Resolution Limit |
|--------|-------|----------|---------|---------|------------------|
| `web` | VP9 | General web videos | 1M | Medium | 1920x1080 |
| `web-small` | VP9 | Small file size | 500k | Lower | 1280x720 |
| `archive` | VP9 | Long-term storage | 3M | High | None |
| `high-quality` | VP9 | Maximum quality | 5M | Very High | None |
| `vp8-legacy` | VP8 | Older browser support | 1M | Medium | 1920x1080 |
| `alpha-web` | VP9 | Transparency support | 1.5M | Medium | 1920x1080 |

## Usage Examples

### Basic Compression

```python
from video_compressor import VideoCompressor

compressor = VideoCompressor()

# Simple compression
result = compressor.compress('input.mp4', 'output.webm', preset='web')
```

### Progress Tracking

```python
def progress_callback(filename, percentage, current_time, total_time, eta):
    print(f"{filename}: {percentage:.1f}% complete (ETA: {eta:.0f}s)")

result = compressor.compress(
    input_path='video.mp4',
    output_path='output.webm',
    preset='high-quality',
    progress_callback=progress_callback
)
```

### Alpha Channel (Transparency)

```python
from video_compressor import VideoCompressor, VideoInfo

compressor = VideoCompressor()

# Check if video has alpha channel
video_info = VideoInfo.from_file('logo_with_alpha.mov')
print(f"Has alpha: {video_info.has_alpha}")

# Compress with alpha preservation
result = compressor.compress(
    input_path='logo_with_alpha.mov',
    output_path='logo.webm',
    preset='alpha-web',
    preserve_alpha=True
)
```

### Batch Processing

```python
from video_compressor import VideoCompressor, BatchCompressor

compressor = VideoCompressor()
batch = BatchCompressor(compressor, max_workers=4)

# Compress multiple files
files = ['video1.mp4', 'video2.mp4', 'video3.mp4']

results = batch.compress_batch(
    files=files,
    output_dir='./compressed',
    preset='web'
)

# Check results
for result in results:
    if result.success:
        print(f"✓ {result.filename}: {result.compression_ratio:.2f}x")
    else:
        print(f"✗ {result.filename}: {result.error}")
```

### Custom Presets

```python
from video_compressor import VideoCompressor, CompressionPreset

compressor = VideoCompressor()

# Create custom preset
mobile_preset = CompressionPreset(
    name='Mobile Optimized',
    codec='vp9',
    video_bitrate='500k',
    audio_bitrate='64k',
    crf=36,
    speed=5,
    max_resolution=(854, 480)
)

# Add and use custom preset
compressor.add_preset('mobile', mobile_preset)
result = compressor.compress('input.mp4', 'output.webm', preset='mobile')
```

### Async Compression

```python
import asyncio
from video_compressor import VideoCompressor

async def compress_multiple():
    compressor = VideoCompressor()

    # Compress multiple files concurrently
    tasks = [
        compressor.compress_async('video1.mp4', 'output1.webm'),
        compressor.compress_async('video2.mp4', 'output2.webm'),
        compressor.compress_async('video3.mp4', 'output3.webm')
    ]

    results = await asyncio.gather(*tasks)
    return results

# Run
results = asyncio.run(compress_multiple())
```

## API Reference

### VideoCompressor

Main class for video compression.

```python
VideoCompressor(ffmpeg_path: Optional[str] = None)
```

#### Methods

##### compress()

```python
compress(
    input_path: str,
    output_path: str,
    preset: str = 'web',
    codec: Optional[str] = None,
    preserve_alpha: bool = False,
    progress_callback: Optional[ProgressCallback] = None,
    **custom_options
) -> CompressionResult
```

Compress a video file.

**Parameters:**
- `input_path` - Path to input video file
- `output_path` - Path to output WebM file
- `preset` - Preset name (default: 'web')
- `codec` - Override codec ('vp8' or 'vp9')
- `preserve_alpha` - Preserve alpha channel (VP9 only)
- `progress_callback` - Optional callback for progress updates
- `**custom_options` - Override preset parameters (video_bitrate, crf, speed, etc.)

**Returns:** `CompressionResult` object

##### compress_async()

Async version of `compress()`. Same parameters and return type.

### BatchCompressor

Batch processing with concurrent compression.

```python
BatchCompressor(compressor: VideoCompressor, max_workers: int = 4)
```

#### Methods

##### compress_batch()

```python
compress_batch(
    files: List[Union[str, Tuple[str, str]]],
    output_dir: Optional[str] = None,
    preset: str = 'web',
    codec: Optional[str] = None,
    preserve_alpha: bool = False,
    progress_callback: Optional[ProgressCallback] = None,
    **kwargs
) -> List[CompressionResult]
```

### CompressionResult

Result object with compression statistics.

**Attributes:**
- `success` (bool) - Whether compression succeeded
- `input_path` (str) - Input file path
- `output_path` (str) - Output file path
- `input_size_mb` (float) - Input file size in MB
- `output_size_mb` (float) - Output file size in MB
- `compression_ratio` (float) - Compression ratio
- `duration` (float) - Video duration in seconds
- `error` (Optional[str]) - Error message if failed

### VideoInfo

Video metadata utility.

```python
VideoInfo.from_file(path: str) -> VideoInfo
```

**Attributes:**
- `duration` (float) - Video duration in seconds
- `width` (int) - Video width in pixels
- `height` (int) - Video height in pixels
- `codec` (str) - Video codec name
- `has_alpha` (bool) - Whether video has alpha channel
- `bitrate` (Optional[int]) - Video bitrate
- `fps` (Optional[float]) - Frames per second

### ProgressCallback

Callback function signature for progress tracking.

```python
def callback(
    filename: str,
    percentage: float,
    current_time: float,
    total_time: float,
    eta: Optional[float]
) -> None:
    ...
```

## Examples

See the [examples/](examples/) directory for complete examples:

- [basic_usage.py](examples/basic_usage.py) - Simple compression examples
- [batch_processing.py](examples/batch_processing.py) - Batch compression
- [alpha_channel.py](examples/alpha_channel.py) - Transparency preservation
- [custom_presets.py](examples/custom_presets.py) - Custom preset creation

## Error Handling

The SDK provides specific exceptions for different error cases:

```python
from video_compressor import (
    VideoCompressorError,
    FFmpegNotFoundError,
    InvalidCodecError,
    InvalidPresetError,
    CompressionFailedError,
    InvalidInputFileError,
    AlphaChannelNotSupportedError
)

try:
    result = compressor.compress('input.mp4', 'output.webm')
except FFmpegNotFoundError:
    print("Please install FFmpeg")
except InvalidInputFileError as e:
    print(f"Invalid input: {e}")
except CompressionFailedError as e:
    print(f"Compression failed: {e}")
```

## Advanced Usage

### Custom FFmpeg Options

Override any preset parameter:

```python
result = compressor.compress(
    input_path='input.mp4',
    output_path='output.webm',
    preset='web',
    video_bitrate='2M',  # Override
    crf=25,  # Override
    speed=3,  # Override
    audio_bitrate='192k'  # Override
)
```

### Two-Pass Encoding

For better quality, use presets with two-pass encoding:

```python
result = compressor.compress(
    input_path='input.mp4',
    output_path='output.webm',
    preset='archive'  # Uses two-pass encoding
)
```

### Processing All Videos in Directory

```python
import os
from video_compressor import VideoCompressor, BatchCompressor

compressor = VideoCompressor()
batch = BatchCompressor(compressor, max_workers=4)

# Find all videos
video_extensions = ('.mp4', '.mov', '.avi', '.mkv')
video_files = [
    os.path.join('./videos', f)
    for f in os.listdir('./videos')
    if f.lower().endswith(video_extensions)
]

# Compress all
results = batch.compress_batch(
    files=video_files,
    output_dir='./compressed',
    preset='web'
)
```

## Performance Tips

1. **Adjust max_workers** - Set based on your CPU cores and available RAM
2. **Use faster presets** - Higher speed values (4-5) for quick encoding
3. **Two-pass for quality** - Use when file size and quality are critical
4. **Resolution limits** - Set max_resolution to reduce processing time
5. **Batch processing** - Process multiple files to maximize CPU usage

## Technical Details

### FFmpeg Commands

The SDK generates FFmpeg commands like:

**VP9 Basic:**
```bash
ffmpeg -i input.mp4 -c:v libvpx-vp9 -b:v 1M -crf 31 -speed 4 \
  -c:a libopus -b:a 128k -row-mt 1 -y output.webm
```

**VP9 with Alpha:**
```bash
ffmpeg -i input.mov -c:v libvpx-vp9 -pix_fmt yuva420p \
  -auto-alt-ref 0 -b:v 1.5M -crf 28 output.webm
```

### Codec Parameters

- **CRF (Constant Rate Factor):** 0-63, lower = better quality
- **Speed:** 0-5 for VP9, 0-16 for VP8, higher = faster encoding
- **Bitrate:** Target bitrate (e.g., '1M', '500k')

## Requirements

- Python 3.8+
- FFmpeg (with libvpx and libvpx-vp9 support)
- Dependencies: ffmpeg-python, tqdm

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## Troubleshooting

**FFmpeg not found:**
```
FFmpegNotFoundError: FFmpeg not found. Please install FFmpeg:
  macOS: brew install ffmpeg
  Ubuntu/Debian: sudo apt-get install ffmpeg
```

**Alpha channel not working:**
- Ensure you're using VP9 codec (not VP8)
- Use `preserve_alpha=True` parameter
- Check input video has alpha with `VideoInfo.from_file()`

**Slow encoding:**
- Increase `speed` parameter (4-5 for faster)
- Disable two-pass encoding
- Set `max_resolution` to limit output size
- Reduce `video_bitrate` and increase `crf`

**Memory issues:**
- Reduce `max_workers` in BatchCompressor
- Process files sequentially instead of batch
- Set `max_resolution` to reduce memory usage

## Support

For issues, questions, or contributions, please visit the GitHub repository.
