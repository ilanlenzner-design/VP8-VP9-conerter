#!/usr/bin/env python3
"""
Test batch video compression.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from video_compressor import VideoCompressor, BatchCompressor, BatchProgress


def main():
    # Find test videos
    search_dir = os.path.expanduser('~/Downloads')
    test_videos = []

    if os.path.exists(search_dir):
        for filename in os.listdir(search_dir):
            if filename.lower().endswith(('.mp4', '.mov')):
                test_videos.append(os.path.join(search_dir, filename))
                if len(test_videos) >= 3:
                    break

    if not test_videos:
        print("No test videos found in ~/Downloads")
        return

    print("=" * 60)
    print("Batch Video Compression Test")
    print("=" * 60)
    print(f"Found {len(test_videos)} videos to compress:")
    for video in test_videos:
        size_mb = os.path.getsize(video) / (1024 * 1024)
        print(f"  - {os.path.basename(video)} ({size_mb:.1f} MB)")
    print()

    # Create output directory
    output_dir = os.path.expanduser('~/video-compressor-sdk/test_output')
    os.makedirs(output_dir, exist_ok=True)
    print(f"Output directory: {output_dir}\n")

    # Create batch compressor
    compressor = VideoCompressor()
    batch = BatchCompressor(compressor, max_workers=2)

    # Create progress tracker
    batch_progress = BatchProgress(total_files=len(test_videos))

    print("Starting batch compression...\n")

    # Compress batch
    results = batch.compress_batch(
        files=test_videos,
        output_dir=output_dir,
        preset='web-small',  # Use small preset for faster testing
        progress_callback=batch_progress.create_callback()
    )

    # Print results
    print("\n" + "=" * 60)
    print("Batch Compression Results")
    print("=" * 60)

    total_input_size = 0
    total_output_size = 0

    for result in results:
        if result.success:
            total_input_size += result.input_size_mb
            total_output_size += result.output_size_mb
            print(f"✓ {result.filename}")
            print(f"  Input:  {result.input_size_mb:.2f} MB")
            print(f"  Output: {result.output_size_mb:.2f} MB")
            print(f"  Ratio:  {result.compression_ratio:.2f}x")
        else:
            print(f"✗ {result.filename}")
            print(f"  Error: {result.error}")
        print()

    if total_output_size > 0:
        overall_ratio = total_input_size / total_output_size
        space_saved = total_input_size - total_output_size
        print("=" * 60)
        print(f"Total input:       {total_input_size:.2f} MB")
        print(f"Total output:      {total_output_size:.2f} MB")
        print(f"Overall ratio:     {overall_ratio:.2f}x")
        print(f"Space saved:       {space_saved:.2f} MB ({(space_saved/total_input_size*100):.1f}%)")
        print(f"Files compressed:  {batch_progress.completed_files}/{batch_progress.total_files}")
        print("=" * 60)


if __name__ == '__main__':
    main()
