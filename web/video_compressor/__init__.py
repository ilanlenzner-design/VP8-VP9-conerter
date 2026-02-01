"""
Video Compressor SDK - Python library for video compression using VP8/VP9 codecs.

This SDK provides a simple and powerful interface for compressing videos to WebM format
with support for alpha channels, batch processing, and real-time progress tracking.

Example:
    >>> from video_compressor import VideoCompressor
    >>> compressor = VideoCompressor()
    >>> result = compressor.compress('input.mp4', 'output.webm', preset='web')
    >>> print(f"Compressed {result.compression_ratio}x")
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__license__ = "MIT"

# Core compression
from .compressor import VideoCompressor, CompressionResult

# Batch processing
from .batch import BatchCompressor, BatchProgress

# Presets
from .presets import CompressionPreset, PRESETS, get_preset, list_presets

# Progress tracking
from .progress import (
    ProgressCallback,
    ProgressTracker,
    FFmpegProgressParser,
    create_tqdm_callback,
    create_simple_callback
)

# Utilities
from .utils import VideoInfo, get_file_size_mb, format_time

# Exceptions
from .exceptions import (
    VideoCompressorError,
    FFmpegNotFoundError,
    InvalidCodecError,
    InvalidPresetError,
    CompressionFailedError,
    InvalidInputFileError,
    AlphaChannelNotSupportedError,
    InvalidOutputPathError
)

__all__ = [
    # Core
    'VideoCompressor',
    'CompressionResult',

    # Batch
    'BatchCompressor',
    'BatchProgress',

    # Presets
    'CompressionPreset',
    'PRESETS',
    'get_preset',
    'list_presets',

    # Progress
    'ProgressCallback',
    'ProgressTracker',
    'FFmpegProgressParser',
    'create_tqdm_callback',
    'create_simple_callback',

    # Utils
    'VideoInfo',
    'get_file_size_mb',
    'format_time',

    # Exceptions
    'VideoCompressorError',
    'FFmpegNotFoundError',
    'InvalidCodecError',
    'InvalidPresetError',
    'CompressionFailedError',
    'InvalidInputFileError',
    'AlphaChannelNotSupportedError',
    'InvalidOutputPathError',
]
