#!/usr/bin/env python3
"""
Custom presets example for video-compressor-sdk.

This example demonstrates creating and using custom compression presets.
"""

from video_compressor import VideoCompressor, CompressionPreset, list_presets


def main():
    # Create compressor
    compressor = VideoCompressor()

    # Example 1: List available built-in presets
    print("Example 1: List built-in presets")
    print("-" * 50)

    presets = list_presets()
    for name, description in presets.items():
        print(f"{name:15} - {description}")
    print()

    # Example 2: Create custom preset
    print("Example 2: Create custom preset")
    print("-" * 50)

    custom_preset = CompressionPreset(
        name='Social Media Optimized',
        codec='vp9',
        video_bitrate='800k',
        audio_bitrate='96k',
        crf=33,
        speed=4,
        format='webm',
        two_pass=False,
        max_resolution=(1280, 720)
    )

    # Add custom preset to compressor
    compressor.add_preset('social-media', custom_preset)

    # Use custom preset
    result = compressor.compress(
        input_path='input.mp4',
        output_path='output_social.webm',
        preset='social-media'
    )

    print(f"Custom preset result: {result.output_size_mb:.2f} MB")
    print()

    # Example 3: Create high-bitrate custom preset
    print("Example 3: Ultra high quality preset")
    print("-" * 50)

    ultra_hq_preset = CompressionPreset(
        name='Ultra High Quality',
        codec='vp9',
        video_bitrate='10M',
        audio_bitrate='320k',
        crf=10,
        speed=0,  # Slowest, best quality
        format='webm',
        two_pass=True,
        max_resolution=None  # No limit
    )

    compressor.add_preset('ultra-hq', ultra_hq_preset)

    result = compressor.compress(
        input_path='input.mp4',
        output_path='output_ultra.webm',
        preset='ultra-hq'
    )

    print(f"Ultra HQ size: {result.output_size_mb:.2f} MB")
    print(f"Compression ratio: {result.compression_ratio:.2f}x")
    print()

    # Example 4: Mobile-optimized preset
    print("Example 4: Mobile-optimized preset")
    print("-" * 50)

    mobile_preset = CompressionPreset(
        name='Mobile Optimized',
        codec='vp9',
        video_bitrate='500k',
        audio_bitrate='64k',
        crf=36,
        speed=5,  # Fastest
        format='webm',
        two_pass=False,
        max_resolution=(854, 480)  # 480p
    )

    compressor.add_preset('mobile', mobile_preset)

    result = compressor.compress(
        input_path='input.mp4',
        output_path='output_mobile.webm',
        preset='mobile'
    )

    print(f"Mobile size: {result.output_size_mb:.2f} MB")
    print()

    # Example 5: Override preset parameters at runtime
    print("Example 5: Override preset parameters")
    print("-" * 50)

    # Use 'web' preset but override specific parameters
    result = compressor.compress(
        input_path='input.mp4',
        output_path='output_custom_params.webm',
        preset='web',
        video_bitrate='1.5M',  # Override bitrate
        crf=28,  # Override quality
        max_resolution=(1920, 1080)  # Override max resolution
    )

    print(f"Custom parameters result: {result.output_size_mb:.2f} MB")
    print()

    # Example 6: Compare presets
    print("Example 6: Compare presets on same video")
    print("-" * 50)

    test_file = 'test_video.mp4'
    test_presets = {
        'mobile': mobile_preset,
        'social-media': custom_preset,
        'web': None,  # Built-in
        'ultra-hq': ultra_hq_preset
    }

    print(f"{'Preset':<15} {'Size (MB)':<12} {'Ratio':<8} {'Duration (s)'}")
    print("-" * 50)

    for preset_name, preset_obj in test_presets.items():
        if preset_obj:
            compressor.add_preset(preset_name, preset_obj)

        result = compressor.compress(
            input_path=test_file,
            output_path=f'compare_{preset_name}.webm',
            preset=preset_name
        )

        if result.success:
            print(f"{preset_name:<15} {result.output_size_mb:<12.2f} "
                  f"{result.compression_ratio:<8.2f} {result.duration:<10.2f}")


if __name__ == '__main__':
    main()
