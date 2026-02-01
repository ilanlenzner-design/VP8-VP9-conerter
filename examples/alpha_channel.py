#!/usr/bin/env python3
"""
Alpha channel example for video-compressor-sdk.

This example demonstrates preserving transparency in videos using VP9.
"""

from video_compressor import VideoCompressor, VideoInfo


def main():
    # Create compressor
    compressor = VideoCompressor()

    # Example 1: Check if video has alpha channel
    print("Example 1: Detect alpha channel")
    print("-" * 50)

    input_file = 'logo_with_alpha.mov'
    video_info = VideoInfo.from_file(input_file)

    print(f"File: {input_file}")
    print(f"Resolution: {video_info.width}x{video_info.height}")
    print(f"Duration: {video_info.duration:.2f}s")
    print(f"Codec: {video_info.codec}")
    print(f"Has alpha channel: {video_info.has_alpha}")
    print()

    # Example 2: Compress with alpha channel preservation
    print("Example 2: Compress with alpha channel")
    print("-" * 50)

    if video_info.has_alpha:
        result = compressor.compress(
            input_path=input_file,
            output_path='logo_transparent.webm',
            preset='alpha-web',
            preserve_alpha=True
        )

        print(f"Success: {result.success}")
        print(f"Output: {result.output_path}")
        print(f"Size: {result.output_size_mb:.2f} MB")
        print("Alpha channel preserved!")
    else:
        print("Input video does not have alpha channel")
    print()

    # Example 3: Custom alpha settings
    print("Example 3: Custom alpha compression settings")
    print("-" * 50)

    result = compressor.compress(
        input_path='animation_with_alpha.mov',
        output_path='animation_transparent.webm',
        codec='vp9',
        preserve_alpha=True,
        video_bitrate='2M',  # Custom bitrate
        crf=25,  # Custom quality
        speed=2  # Slower encoding for better quality
    )

    if result.success:
        print(f"Custom alpha compression complete")
        print(f"Compression ratio: {result.compression_ratio:.2f}x")
    print()

    # Example 4: Error handling - alpha with VP8
    print("Example 4: Error handling (alpha requires VP9)")
    print("-" * 50)

    try:
        # This will raise AlphaChannelNotSupportedError
        result = compressor.compress(
            input_path='logo_with_alpha.mov',
            output_path='logo_vp8_alpha.webm',
            codec='vp8',  # VP8 doesn't support alpha
            preserve_alpha=True
        )
    except Exception as e:
        print(f"Expected error: {type(e).__name__}")
        print(f"Message: {e}")
    print()

    # Example 5: Batch process videos with alpha
    print("Example 5: Batch process alpha videos")
    print("-" * 50)

    from video_compressor import BatchCompressor

    batch = BatchCompressor(compressor, max_workers=2)

    alpha_videos = [
        'logo1.mov',
        'logo2.mov',
        'animation.mov',
    ]

    results = batch.compress_batch(
        files=alpha_videos,
        output_dir='./transparent_output',
        preset='alpha-web',
        preserve_alpha=True
    )

    for result in results:
        status = "✓" if result.success else "✗"
        print(f"{status} {result.filename}")

    successful = sum(1 for r in results if r.success)
    print(f"\nProcessed {successful}/{len(results)} videos successfully")


if __name__ == '__main__':
    main()
