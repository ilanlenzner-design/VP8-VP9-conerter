"""
Utility functions for video compression and validation.
"""

import os
import shutil
import subprocess
import json
from typing import Dict, Optional, Tuple
from pathlib import Path
from .exceptions import (
    FFmpegNotFoundError,
    InvalidInputFileError,
    InvalidOutputPathError
)


def find_ffmpeg() -> str:
    """Find FFmpeg binary on the system.

    Returns:
        Path to FFmpeg executable

    Raises:
        FFmpegNotFoundError: If FFmpeg is not found
    """
    ffmpeg_path = shutil.which('ffmpeg')
    if ffmpeg_path is None:
        raise FFmpegNotFoundError()
    return ffmpeg_path


def find_ffprobe() -> str:
    """Find FFprobe binary on the system.

    Returns:
        Path to FFprobe executable

    Raises:
        FFmpegNotFoundError: If FFprobe is not found
    """
    ffprobe_path = shutil.which('ffprobe')
    if ffprobe_path is None:
        raise FFmpegNotFoundError("FFprobe not found")
    return ffprobe_path


def validate_input_file(path: str) -> None:
    """Validate that input file exists and is accessible.

    Args:
        path: Path to input file

    Raises:
        InvalidInputFileError: If file doesn't exist or is not accessible
    """
    if not os.path.exists(path):
        raise InvalidInputFileError(f"Input file not found: {path}")

    if not os.path.isfile(path):
        raise InvalidInputFileError(f"Input path is not a file: {path}")

    if not os.access(path, os.R_OK):
        raise InvalidInputFileError(f"Input file is not readable: {path}")


def validate_output_path(path: str) -> None:
    """Validate that output path can be written to.

    Args:
        path: Path to output file

    Raises:
        InvalidOutputPathError: If output path is invalid or not writable
    """
    output_dir = os.path.dirname(os.path.abspath(path))

    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir, exist_ok=True)
        except OSError as e:
            raise InvalidOutputPathError(
                f"Cannot create output directory: {output_dir}. Error: {e}"
            )

    if os.path.exists(path) and not os.access(path, os.W_OK):
        raise InvalidOutputPathError(f"Output file is not writable: {path}")

    if not os.access(output_dir, os.W_OK):
        raise InvalidOutputPathError(f"Output directory is not writable: {output_dir}")


class VideoInfo:
    """Extract and store video file metadata."""

    def __init__(
        self,
        duration: float,
        width: int,
        height: int,
        codec: str,
        has_alpha: bool,
        bitrate: Optional[int] = None,
        fps: Optional[float] = None,
    ):
        self.duration = duration
        self.width = width
        self.height = height
        self.codec = codec
        self.has_alpha = has_alpha
        self.bitrate = bitrate
        self.fps = fps

    @classmethod
    def from_file(cls, path: str) -> 'VideoInfo':
        """Extract video information from file using FFprobe.

        Args:
            path: Path to video file

        Returns:
            VideoInfo instance with metadata

        Raises:
            InvalidInputFileError: If file is not a valid video
        """
        validate_input_file(path)
        ffprobe_path = find_ffprobe()

        try:
            # Run ffprobe to get video metadata
            cmd = [
                ffprobe_path,
                '-v', 'quiet',
                '-print_format', 'json',
                '-show_streams',
                '-show_format',
                path
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )

            data = json.loads(result.stdout)

            # Find video stream
            video_stream = None
            for stream in data.get('streams', []):
                if stream.get('codec_type') == 'video':
                    video_stream = stream
                    break

            if not video_stream:
                raise InvalidInputFileError(f"No video stream found in: {path}")

            # Extract metadata
            duration = float(data.get('format', {}).get('duration', 0))
            width = int(video_stream.get('width', 0))
            height = int(video_stream.get('height', 0))
            codec = video_stream.get('codec_name', 'unknown')
            bitrate = int(data.get('format', {}).get('bit_rate', 0))

            # Check for alpha channel
            pix_fmt = video_stream.get('pix_fmt', '')
            has_alpha = 'yuva' in pix_fmt or 'rgba' in pix_fmt or 'gbra' in pix_fmt

            # Extract FPS
            fps = None
            fps_str = video_stream.get('r_frame_rate', '0/1')
            if '/' in fps_str:
                num, denom = fps_str.split('/')
                if int(denom) != 0:
                    fps = int(num) / int(denom)

            return cls(
                duration=duration,
                width=width,
                height=height,
                codec=codec,
                has_alpha=has_alpha,
                bitrate=bitrate,
                fps=fps
            )

        except subprocess.CalledProcessError as e:
            raise InvalidInputFileError(
                f"Failed to read video metadata from {path}. Error: {e.stderr}"
            )
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            raise InvalidInputFileError(
                f"Failed to parse video metadata from {path}. Error: {e}"
            )

    def __repr__(self) -> str:
        return (
            f"VideoInfo(duration={self.duration:.2f}s, "
            f"resolution={self.width}x{self.height}, "
            f"codec={self.codec}, has_alpha={self.has_alpha})"
        )


def get_file_size_mb(path: str) -> float:
    """Get file size in megabytes.

    Args:
        path: Path to file

    Returns:
        File size in MB
    """
    if not os.path.exists(path):
        return 0.0
    return os.path.getsize(path) / (1024 * 1024)


def format_time(seconds: float) -> str:
    """Format seconds into HH:MM:SS string.

    Args:
        seconds: Time in seconds

    Returns:
        Formatted time string
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"
