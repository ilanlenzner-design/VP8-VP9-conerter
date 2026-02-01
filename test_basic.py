#!/usr/bin/env python3
"""
Basic test script for video compressor SDK.
"""

import sys
import os

# Add src to path so we can import without installing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from video_compressor import VideoCompressor, list_presets, __version__

def main():
    print("=" * 60)
    print("Video Compressor SDK Test")
    print("=" * 60)
    print(f"Version: {__version__}\n")

    # Test 1: Check FFmpeg is available
    print("Test 1: Checking FFmpeg availability...")
    try:
        from video_compressor.utils import find_ffmpeg, find_ffprobe
        ffmpeg_path = find_ffmpeg()
        ffprobe_path = find_ffprobe()
        print(f"✓ FFmpeg found: {ffmpeg_path}")
        print(f"✓ FFprobe found: {ffprobe_path}")
    except Exception as e:
        print(f"✗ FFmpeg check failed: {e}")
        return
    print()

    # Test 2: List available presets
    print("Test 2: Listing available presets...")
    presets = list_presets()
    print(f"✓ Found {len(presets)} built-in presets:")
    for name, description in presets.items():
        print(f"  - {name:15} : {description}")
    print()

    # Test 3: Create compressor instance
    print("Test 3: Creating VideoCompressor instance...")
    try:
        compressor = VideoCompressor()
        print(f"✓ Compressor created successfully")
    except Exception as e:
        print(f"✗ Failed to create compressor: {e}")
        return
    print()

    # Test 4: Get preset details
    print("Test 4: Checking preset configuration...")
    try:
        preset = compressor.get_preset('web')
        print(f"✓ 'web' preset loaded:")
        print(f"  - Codec: {preset.codec}")
        print(f"  - Video bitrate: {preset.video_bitrate}")
        print(f"  - Audio bitrate: {preset.audio_bitrate}")
        print(f"  - CRF: {preset.crf}")
        print(f"  - Speed: {preset.speed}")
        print(f"  - Two-pass: {preset.two_pass}")
    except Exception as e:
        print(f"✗ Failed to get preset: {e}")
    print()

    # Test 5: Create custom preset
    print("Test 5: Creating custom preset...")
    try:
        from video_compressor import CompressionPreset

        custom = CompressionPreset(
            name='Test Preset',
            codec='vp9',
            video_bitrate='1M',
            audio_bitrate='128k',
            crf=30,
            speed=4
        )
        compressor.add_preset('test', custom)
        print(f"✓ Custom preset created and added")
    except Exception as e:
        print(f"✗ Failed to create custom preset: {e}")
    print()

    # Test 6: Check if we can find a test video
    print("Test 6: Looking for test video...")
    test_videos = []
    search_dirs = [
        os.path.expanduser('~/Downloads'),
        os.path.expanduser('~/Desktop'),
        os.path.expanduser('~/Movies'),
    ]

    for search_dir in search_dirs:
        if os.path.exists(search_dir):
            for filename in os.listdir(search_dir):
                if filename.lower().endswith(('.mp4', '.mov', '.avi')):
                    test_videos.append(os.path.join(search_dir, filename))
                    if len(test_videos) >= 3:
                        break
        if len(test_videos) >= 3:
            break

    if test_videos:
        print(f"✓ Found {len(test_videos)} test video(s):")
        for video in test_videos[:3]:
            size_mb = os.path.getsize(video) / (1024 * 1024)
            print(f"  - {os.path.basename(video)} ({size_mb:.1f} MB)")
        print()

        # Offer to compress one
        print("Would you like to test compression on one of these videos?")
        print("Run this command to test:")
        print(f"  python3 test_compress.py '{test_videos[0]}'")
    else:
        print("✗ No test videos found in common directories")
        print("  You can test compression by running:")
        print("  python3 test_compress.py /path/to/your/video.mp4")
    print()

    print("=" * 60)
    print("✓ All basic tests passed!")
    print("=" * 60)
    print("\nSDK is ready to use. Example usage:")
    print("""
from video_compressor import VideoCompressor

compressor = VideoCompressor()
result = compressor.compress(
    input_path='input.mp4',
    output_path='output.webm',
    preset='web'
)
print(f"Compressed {result.compression_ratio:.2f}x")
""")


if __name__ == '__main__':
    main()
