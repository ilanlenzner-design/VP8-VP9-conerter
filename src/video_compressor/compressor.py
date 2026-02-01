"""
Core video compression functionality.
"""

import os
import subprocess
import asyncio
from dataclasses import dataclass
from typing import Optional, List, Dict
from .presets import CompressionPreset, get_preset, PRESETS
from .progress import ProgressCallback, ProgressTracker, FFmpegProgressParser
from .utils import (
    find_ffmpeg,
    validate_input_file,
    validate_output_path,
    VideoInfo,
    get_file_size_mb
)
from .exceptions import (
    CompressionFailedError,
    AlphaChannelNotSupportedError,
    InvalidCodecError
)


@dataclass
class CompressionResult:
    """Result of a video compression operation.

    Attributes:
        success: Whether compression succeeded
        input_path: Path to input file
        output_path: Path to output file
        input_size_mb: Input file size in MB
        output_size_mb: Output file size in MB
        compression_ratio: Compression ratio (input_size / output_size)
        duration: Video duration in seconds
        error: Error message if compression failed
    """
    success: bool
    input_path: str
    output_path: str
    input_size_mb: float = 0.0
    output_size_mb: float = 0.0
    compression_ratio: float = 0.0
    duration: float = 0.0
    error: Optional[str] = None

    @property
    def filename(self) -> str:
        """Get input filename."""
        return os.path.basename(self.input_path)


class VideoCompressor:
    """Main video compression class supporting VP8/VP9 codecs with WebM output."""

    def __init__(self, ffmpeg_path: Optional[str] = None):
        """Initialize video compressor.

        Args:
            ffmpeg_path: Optional path to FFmpeg binary. If not provided, will search PATH.

        Raises:
            FFmpegNotFoundError: If FFmpeg is not found
        """
        self.ffmpeg_path = ffmpeg_path or find_ffmpeg()
        self.custom_presets: Dict[str, CompressionPreset] = {}

    def add_preset(self, name: str, preset: CompressionPreset) -> None:
        """Add a custom preset.

        Args:
            name: Preset name
            preset: CompressionPreset instance
        """
        self.custom_presets[name] = preset

    def get_preset(self, name: str) -> CompressionPreset:
        """Get preset by name (checks custom presets first, then built-in).

        Args:
            name: Preset name

        Returns:
            CompressionPreset instance

        Raises:
            InvalidPresetError: If preset doesn't exist
        """
        if name in self.custom_presets:
            return self.custom_presets[name]
        return get_preset(name)

    def compress(
        self,
        input_path: str,
        output_path: str,
        preset: str = 'web',
        codec: Optional[str] = None,
        preserve_alpha: bool = False,
        progress_callback: Optional[ProgressCallback] = None,
        **custom_options
    ) -> CompressionResult:
        """Compress a video file.

        Args:
            input_path: Path to input video file
            output_path: Path to output WebM file
            preset: Preset name (default: 'web')
            codec: Override codec ('vp8' or 'vp9'). If None, uses preset's codec.
            preserve_alpha: Preserve alpha channel (VP9 only)
            progress_callback: Optional callback for progress updates
            **custom_options: Additional FFmpeg options to override preset

        Returns:
            CompressionResult with compression statistics

        Raises:
            InvalidInputFileError: If input file is invalid
            InvalidOutputPathError: If output path is invalid
            CompressionFailedError: If compression fails
            AlphaChannelNotSupportedError: If alpha requested with non-VP9 codec
        """
        # Validate inputs
        validate_input_file(input_path)
        validate_output_path(output_path)

        # Get preset configuration
        preset_config = self.get_preset(preset)

        # Override codec if specified
        if codec:
            if codec not in ('vp8', 'vp9'):
                raise InvalidCodecError(f"Invalid codec: {codec}")
            preset_config.codec = codec

        # Validate alpha channel request
        if preserve_alpha and preset_config.codec != 'vp9':
            raise AlphaChannelNotSupportedError(preset_config.codec)

        # Get video info
        video_info = VideoInfo.from_file(input_path)
        input_size = get_file_size_mb(input_path)

        try:
            # Build FFmpeg command
            cmd = self._build_command(
                input_path=input_path,
                output_path=output_path,
                preset=preset_config,
                preserve_alpha=preserve_alpha,
                video_info=video_info,
                **custom_options
            )

            # Run compression with progress tracking
            self._run_ffmpeg(
                cmd=cmd,
                video_info=video_info,
                filename=os.path.basename(input_path),
                progress_callback=progress_callback
            )

            # Calculate results
            output_size = get_file_size_mb(output_path)
            compression_ratio = input_size / output_size if output_size > 0 else 0

            return CompressionResult(
                success=True,
                input_path=input_path,
                output_path=output_path,
                input_size_mb=input_size,
                output_size_mb=output_size,
                compression_ratio=compression_ratio,
                duration=video_info.duration
            )

        except Exception as e:
            # Clean up partial output file
            if os.path.exists(output_path):
                try:
                    os.remove(output_path)
                except OSError:
                    pass

            if isinstance(e, CompressionFailedError):
                raise

            raise CompressionFailedError(f"Compression failed: {str(e)}")

    async def compress_async(
        self,
        input_path: str,
        output_path: str,
        preset: str = 'web',
        codec: Optional[str] = None,
        preserve_alpha: bool = False,
        progress_callback: Optional[ProgressCallback] = None,
        **custom_options
    ) -> CompressionResult:
        """Async version of compress().

        Args:
            Same as compress()

        Returns:
            CompressionResult
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            lambda: self.compress(
                input_path=input_path,
                output_path=output_path,
                preset=preset,
                codec=codec,
                preserve_alpha=preserve_alpha,
                progress_callback=progress_callback,
                **custom_options
            )
        )

    def _build_command(
        self,
        input_path: str,
        output_path: str,
        preset: CompressionPreset,
        preserve_alpha: bool,
        video_info: VideoInfo,
        **custom_options
    ) -> List[str]:
        """Build FFmpeg command from preset and options.

        Args:
            input_path: Input file path
            output_path: Output file path
            preset: Compression preset
            preserve_alpha: Whether to preserve alpha channel
            video_info: Video metadata
            **custom_options: Custom options to override preset

        Returns:
            List of command arguments
        """
        cmd = [self.ffmpeg_path, '-i', input_path]

        # Video codec
        if preset.codec == 'vp9':
            cmd.extend(['-c:v', 'libvpx-vp9'])
        else:  # vp8
            cmd.extend(['-c:v', 'libvpx'])

        # Alpha channel support (VP9 only)
        if preserve_alpha:
            cmd.extend([
                '-pix_fmt', 'yuva420p',
                '-auto-alt-ref', '0',
                '-metadata:s:v:0', 'alpha_mode=1'
            ])

        # Video bitrate and CRF
        cmd.extend([
            '-b:v', custom_options.get('video_bitrate', preset.video_bitrate),
            '-crf', str(custom_options.get('crf', preset.crf))
        ])

        # Encoding speed
        if preset.codec == 'vp9':
            cmd.extend(['-speed', str(custom_options.get('speed', preset.speed))])
        else:  # VP8
            cmd.extend(['-cpu-used', str(custom_options.get('speed', preset.speed))])

        # Resolution scaling
        max_res = custom_options.get('max_resolution', preset.max_resolution)
        if max_res:
            max_width, max_height = max_res
            if video_info.width > max_width or video_info.height > max_height:
                cmd.extend([
                    '-vf', f'scale=min({max_width}\\,iw):min({max_height}\\,ih):force_original_aspect_ratio=decrease'
                ])

        # Row-based multithreading (VP9)
        if preset.codec == 'vp9':
            cmd.extend(['-row-mt', '1'])

        # Audio codec
        if preset.audio_codec:
            cmd.extend([
                '-c:a', preset.audio_codec,
                '-b:a', custom_options.get('audio_bitrate', preset.audio_bitrate)
            ])

        # Output options
        cmd.extend([
            '-y',  # Overwrite output file
            output_path
        ])

        return cmd

    def _run_ffmpeg(
        self,
        cmd: List[str],
        video_info: VideoInfo,
        filename: str,
        progress_callback: Optional[ProgressCallback]
    ) -> None:
        """Run FFmpeg command with progress tracking.

        Args:
            cmd: FFmpeg command arguments
            video_info: Video metadata for progress calculation
            filename: Input filename for progress display
            progress_callback: Optional progress callback

        Raises:
            CompressionFailedError: If FFmpeg fails
        """
        # Create progress tracker
        tracker = None
        if progress_callback:
            tracker = ProgressTracker(
                total_duration=video_info.duration,
                filename=filename,
                callback=progress_callback
            )

        # Run FFmpeg
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )

        parser = FFmpegProgressParser()

        # Read stderr for progress updates
        while True:
            line = process.stderr.readline()

            if not line:
                if process.poll() is not None:
                    break
                continue

            # Parse progress
            if tracker:
                progress = parser.parse_progress(line)
                if progress:
                    tracker.update(
                        current_time=progress['current_time'],
                        speed=progress['speed']
                    )

        # Wait for process to complete
        return_code = process.wait()

        # Mark as complete
        if tracker:
            tracker.complete()

        # Check for errors
        if return_code != 0:
            stderr = process.stderr.read() if process.stderr else ""
            raise CompressionFailedError(
                f"FFmpeg failed with return code {return_code}. Error: {stderr}"
            )
