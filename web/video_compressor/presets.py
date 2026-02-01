"""
Compression preset configurations for different use cases.
"""

from dataclasses import dataclass
from typing import Optional, Tuple, Dict
from .exceptions import InvalidCodecError


@dataclass
class CompressionPreset:
    """Configuration for video compression presets.

    Attributes:
        name: Human-readable preset name
        codec: Video codec to use ('vp8' or 'vp9')
        video_bitrate: Target video bitrate (e.g., '1M', '500k')
        audio_bitrate: Target audio bitrate (e.g., '128k', '192k')
        crf: Constant Rate Factor (0-63, lower = better quality)
        speed: Encoding speed (0-5 for VP9, 0-16 for VP8, higher = faster but lower quality)
        format: Output format ('webm')
        two_pass: Whether to use two-pass encoding for better quality
        max_resolution: Optional maximum resolution as (width, height) tuple
        audio_codec: Audio codec to use (default: 'libopus' for WebM)
    """

    name: str
    codec: str
    video_bitrate: str
    audio_bitrate: str
    crf: int
    speed: int
    format: str = "webm"
    two_pass: bool = False
    max_resolution: Optional[Tuple[int, int]] = None
    audio_codec: str = "libopus"

    def __post_init__(self) -> None:
        """Validate preset parameters after initialization."""
        if self.codec not in ('vp8', 'vp9'):
            raise InvalidCodecError(
                f"Invalid codec: {self.codec}. Must be 'vp8' or 'vp9'"
            )

        if not 0 <= self.crf <= 63:
            raise ValueError(f"CRF must be between 0-63, got {self.crf}")

        if self.codec == 'vp9' and not 0 <= self.speed <= 5:
            raise ValueError(f"VP9 speed must be between 0-5, got {self.speed}")
        elif self.codec == 'vp8' and not 0 <= self.speed <= 16:
            raise ValueError(f"VP8 speed must be between 0-16, got {self.speed}")

        if self.format not in ('webm',):
            raise ValueError(f"Only 'webm' format is supported, got {self.format}")


# Built-in presets for common use cases
PRESETS: Dict[str, CompressionPreset] = {
    'web': CompressionPreset(
        name='Web Optimized',
        codec='vp9',
        video_bitrate='1M',
        audio_bitrate='128k',
        crf=31,
        speed=4,
        format='webm',
        two_pass=False,
        max_resolution=(1920, 1080),
    ),

    'web-small': CompressionPreset(
        name='Web Small',
        codec='vp9',
        video_bitrate='500k',
        audio_bitrate='96k',
        crf=35,
        speed=4,
        format='webm',
        two_pass=False,
        max_resolution=(1280, 720),
    ),

    'archive': CompressionPreset(
        name='Archive Quality',
        codec='vp9',
        video_bitrate='3M',
        audio_bitrate='192k',
        crf=20,
        speed=1,
        format='webm',
        two_pass=True,
        max_resolution=None,  # No resolution limit
    ),

    'high-quality': CompressionPreset(
        name='High Quality',
        codec='vp9',
        video_bitrate='5M',
        audio_bitrate='256k',
        crf=15,
        speed=2,
        format='webm',
        two_pass=True,
        max_resolution=None,
    ),

    'vp8-legacy': CompressionPreset(
        name='VP8 Legacy Compatible',
        codec='vp8',
        video_bitrate='1M',
        audio_bitrate='128k',
        crf=10,
        speed=3,
        format='webm',
        two_pass=False,
        max_resolution=(1920, 1080),
    ),

    'alpha-web': CompressionPreset(
        name='Web with Alpha Channel',
        codec='vp9',
        video_bitrate='1.5M',
        audio_bitrate='128k',
        crf=28,
        speed=3,
        format='webm',
        two_pass=False,
        max_resolution=(1920, 1080),
    ),
}


def get_preset(name: str) -> CompressionPreset:
    """Get a preset by name.

    Args:
        name: Preset name (e.g., 'web', 'archive', 'high-quality')

    Returns:
        CompressionPreset instance

    Raises:
        InvalidPresetError: If preset name doesn't exist
    """
    from .exceptions import InvalidPresetError

    if name not in PRESETS:
        available = ', '.join(PRESETS.keys())
        raise InvalidPresetError(
            f"Unknown preset '{name}'. Available presets: {available}"
        )

    return PRESETS[name]


def list_presets() -> Dict[str, str]:
    """List all available presets with descriptions.

    Returns:
        Dictionary mapping preset names to their descriptions
    """
    return {name: preset.name for name, preset in PRESETS.items()}
