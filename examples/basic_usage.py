#!/usr/bin/env python3
"""
Basic usage example for video-compressor-sdk.

This example demonstrates simple video compression with different presets.
"""

from video_compressor import VideoCompressor, create_simple_callback


def main():
    # Create compressor instance
    compressor = VideoCompressor()

    # Example 1: Simple compression with default 'web' preset
    print("Example 1: Basic compression with 'web' preset")
    print("-" * 50)
    result = compressor.compress(
        input_path='input.mp4',
        output_path='output_web.webm',
        preset='web'
    )
    print(f"Success: {result.success}")
    print(f"Input size: {result.input_size_mb:.2f} MB")
    print(f"Output size: {result.output_size_mb:.2f} MB")
    print(f"Compression ratio: {result.compression_ratio:.2f}x")
    print()

    # Example 2: Compression with progress tracking
    print("Example 2: Compression with progress tracking")
    print("-" * 50)

    def progress_callback(filename, percentage, current_time, total_time, eta):
        print(f"{filename}: {percentage:.1f}% complete (ETA: {eta:.0f}s)")

    result = compressor.compress(
        input_path='input.mp4',
        output_path='output_progress.webm',
        preset='web',
        progress_callback=progress_callback
    )
    print(f"Completed: {result.filename}")
    print()

    # Example 3: High quality compression
    print("Example 3: High quality compression")
    print("-" * 50)
    result = compressor.compress(
        input_path='input.mp4',
        output_path='output_hq.webm',
        preset='high-quality'
    )
    print(f"High quality output: {result.output_size_mb:.2f} MB")
    print()

    # Example 4: Small file size optimization
    print("Example 4: Small file size (web-small preset)")
    print("-" * 50)
    result = compressor.compress(
        input_path='input.mp4',
        output_path='output_small.webm',
        preset='web-small'
    )
    print(f"Small output: {result.output_size_mb:.2f} MB")
    print()

    # Example 5: VP8 for legacy compatibility
    print("Example 5: VP8 codec for legacy browsers")
    print("-" * 50)
    result = compressor.compress(
        input_path='input.mp4',
        output_path='output_vp8.webm',
        preset='vp8-legacy'
    )
    print(f"VP8 output: {result.output_size_mb:.2f} MB")
    print()


if __name__ == '__main__':
    main()
