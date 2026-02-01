#!/usr/bin/env python3
"""
Test video compression with a real file.

Usage:
    python3 test_compress.py /path/to/video.mp4
    python3 test_compress.py /path/to/video.mp4 --preset web-small
    python3 test_compress.py /path/to/video.mp4 --alpha
"""

import sys
import os
import argparse

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from video_compressor import VideoCompressor, VideoInfo


def progress_callback(filename, percentage, current_time, total_time, eta):
    """Simple progress callback."""
    bar_length = 40
    filled = int(bar_length * percentage / 100)
    bar = '█' * filled + '░' * (bar_length - filled)

    eta_str = f"{eta:.0f}s" if eta is not None else "??s"
    print(f"\r{filename}: [{bar}] {percentage:.1f}% (ETA: {eta_str})", end='', flush=True)

    if percentage >= 100:
        print()  # New line when complete


def main():
    parser = argparse.ArgumentParser(description='Test video compression')
    parser.add_argument('input', help='Input video file')
    parser.add_argument('--output', '-o', help='Output file (default: input_compressed.webm)')
    parser.add_argument('--preset', '-p', default='web', help='Compression preset (default: web)')
    parser.add_argument('--alpha', action='store_true', help='Preserve alpha channel')
    parser.add_argument('--no-progress', action='store_true', help='Disable progress display')

    args = parser.parse_args()

    # Validate input
    if not os.path.exists(args.input):
        print(f"Error: Input file not found: {args.input}")
        return 1

    # Determine output path
    if args.output:
        output_path = args.output
    else:
        name, _ = os.path.splitext(args.input)
        output_path = f"{name}_compressed.webm"

    print("=" * 60)
    print("Video Compression Test")
    print("=" * 60)
    print(f"Input:  {args.input}")
    print(f"Output: {output_path}")
    print(f"Preset: {args.preset}")
    if args.alpha:
        print("Alpha:  Enabled (VP9)")
    print()

    # Get video info
    print("Analyzing video...")
    try:
        info = VideoInfo.from_file(args.input)
        print(f"✓ Duration: {info.duration:.2f}s")
        print(f"✓ Resolution: {info.width}x{info.height}")
        print(f"✓ Codec: {info.codec}")
        print(f"✓ FPS: {info.fps:.2f}" if info.fps else "")
        print(f"✓ Has Alpha: {info.has_alpha}")

        input_size = os.path.getsize(args.input) / (1024 * 1024)
        print(f"✓ Input size: {input_size:.2f} MB")
        print()
    except Exception as e:
        print(f"Warning: Could not analyze video: {e}")
        print("Proceeding with compression anyway...\n")

    # Compress
    print("Starting compression...")
    try:
        compressor = VideoCompressor()

        callback = None if args.no_progress else progress_callback

        result = compressor.compress(
            input_path=args.input,
            output_path=output_path,
            preset=args.preset,
            preserve_alpha=args.alpha,
            progress_callback=callback
        )

        print("\n" + "=" * 60)
        print("✓ Compression Complete!")
        print("=" * 60)
        print(f"Input size:        {result.input_size_mb:.2f} MB")
        print(f"Output size:       {result.output_size_mb:.2f} MB")
        print(f"Compression ratio: {result.compression_ratio:.2f}x")
        print(f"Space saved:       {result.input_size_mb - result.output_size_mb:.2f} MB")
        print(f"Output file:       {result.output_path}")
        print()

        return 0

    except Exception as e:
        print(f"\n✗ Compression failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
