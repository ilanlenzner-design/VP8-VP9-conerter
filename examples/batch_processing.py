#!/usr/bin/env python3
"""
Batch processing example for video-compressor-sdk.

This example demonstrates compressing multiple videos in parallel.
"""

import os
from video_compressor import VideoCompressor, BatchCompressor, BatchProgress


def main():
    # Create compressor and batch processor
    compressor = VideoCompressor()
    batch = BatchCompressor(compressor, max_workers=4)

    # Example 1: Batch compress with output directory
    print("Example 1: Batch compress to output directory")
    print("-" * 50)

    input_files = [
        'video1.mp4',
        'video2.mp4',
        'video3.mp4',
    ]

    results = batch.compress_batch(
        files=input_files,
        output_dir='./compressed',
        preset='web'
    )

    # Print results
    for result in results:
        if result.success:
            print(f"✓ {result.filename}: {result.compression_ratio:.2f}x compression")
        else:
            print(f"✗ {result.filename}: {result.error}")
    print()

    # Example 2: Batch compress with custom input/output pairs
    print("Example 2: Batch compress with custom paths")
    print("-" * 50)

    file_pairs = [
        ('input1.mp4', 'output/custom1.webm'),
        ('input2.mp4', 'output/custom2.webm'),
        ('input3.mp4', 'output/custom3.webm'),
    ]

    results = batch.compress_batch(
        files=file_pairs,
        preset='web'
    )

    for result in results:
        print(f"{'✓' if result.success else '✗'} {result.filename}")
    print()

    # Example 3: Batch compress with progress tracking
    print("Example 3: Batch compress with progress tracking")
    print("-" * 50)

    # Create batch progress tracker
    batch_progress = BatchProgress(total_files=len(input_files))

    results = batch.compress_batch(
        files=input_files,
        output_dir='./compressed_progress',
        preset='web',
        progress_callback=batch_progress.create_callback()
    )

    print(f"\nBatch complete: {batch_progress.completed_files}/{batch_progress.total_files} files")
    print()

    # Example 4: Process all videos in a directory
    print("Example 4: Process all videos in directory")
    print("-" * 50)

    input_dir = './videos'
    output_dir = './compressed_all'

    # Find all video files
    video_extensions = ('.mp4', '.mov', '.avi', '.mkv')
    video_files = [
        os.path.join(input_dir, f)
        for f in os.listdir(input_dir)
        if f.lower().endswith(video_extensions)
    ]

    print(f"Found {len(video_files)} videos")

    if video_files:
        results = batch.compress_batch(
            files=video_files,
            output_dir=output_dir,
            preset='web'
        )

        successful = sum(1 for r in results if r.success)
        failed = len(results) - successful

        print(f"Results: {successful} successful, {failed} failed")
    print()

    # Example 5: Compare different presets on same files
    print("Example 5: Compare presets")
    print("-" * 50)

    test_file = 'test.mp4'
    presets = ['web-small', 'web', 'high-quality']

    for preset_name in presets:
        result = compressor.compress(
            input_path=test_file,
            output_path=f'output_{preset_name}.webm',
            preset=preset_name
        )

        if result.success:
            print(f"{preset_name:15} -> {result.output_size_mb:6.2f} MB "
                  f"({result.compression_ratio:.2f}x)")


if __name__ == '__main__':
    main()
