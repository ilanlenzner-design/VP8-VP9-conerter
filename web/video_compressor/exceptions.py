"""
Custom exceptions for the video compressor SDK.
"""


class VideoCompressorError(Exception):
    """Base exception for all video compressor errors."""
    pass


class FFmpegNotFoundError(VideoCompressorError):
    """Raised when FFmpeg binary is not found on the system."""

    def __init__(self, message: str = "FFmpeg not found"):
        super().__init__(
            f"{message}. Please install FFmpeg:\n"
            "  macOS: brew install ffmpeg\n"
            "  Ubuntu/Debian: sudo apt-get install ffmpeg\n"
            "  Windows: Download from https://ffmpeg.org/download.html"
        )


class InvalidCodecError(VideoCompressorError):
    """Raised when an invalid or unsupported codec is specified."""
    pass


class InvalidPresetError(VideoCompressorError):
    """Raised when an invalid preset name is specified."""
    pass


class CompressionFailedError(VideoCompressorError):
    """Raised when the compression process fails."""
    pass


class InvalidInputFileError(VideoCompressorError):
    """Raised when the input file is invalid, missing, or not a video file."""
    pass


class AlphaChannelNotSupportedError(VideoCompressorError):
    """Raised when alpha channel is requested but the codec doesn't support it."""

    def __init__(self, codec: str = ""):
        message = "Alpha channel is only supported with VP9 codec"
        if codec:
            message += f", but '{codec}' was specified"
        super().__init__(message)


class InvalidOutputPathError(VideoCompressorError):
    """Raised when the output path is invalid or cannot be written to."""
    pass
