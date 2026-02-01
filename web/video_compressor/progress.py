"""
Progress tracking for video compression operations.
"""

import re
import time
from typing import Optional, Callable, Protocol


class ProgressCallback(Protocol):
    """Protocol for progress callback functions.

    The callback function will be called periodically during compression
    with progress information.
    """

    def __call__(
        self,
        filename: str,
        percentage: float,
        current_time: float,
        total_time: float,
        eta: Optional[float]
    ) -> None:
        """Progress callback signature.

        Args:
            filename: Name of the file being processed
            percentage: Completion percentage (0-100)
            current_time: Current encoding time in seconds
            total_time: Total video duration in seconds
            eta: Estimated time remaining in seconds (None if unknown)
        """
        ...


class FFmpegProgressParser:
    """Parse FFmpeg progress output from stderr."""

    # Pattern to match FFmpeg progress output
    # Example: frame=  123 fps=30 q=28.0 size=1024kB time=00:00:04.10 bitrate=2048.0kbits/s speed=1.0x
    PROGRESS_PATTERN = re.compile(
        r'frame=\s*(\d+)\s+fps=\s*([\d.]+).*?time=(\d+):(\d+):([\d.]+).*?speed=\s*([\d.]+)x'
    )

    @classmethod
    def parse_progress(cls, line: str) -> Optional[dict]:
        """Parse a progress line from FFmpeg output.

        Args:
            line: Single line from FFmpeg stderr output

        Returns:
            Dictionary with progress information or None if line doesn't match
            {
                'frame': int,
                'fps': float,
                'current_time': float (seconds),
                'speed': float (encoding speed multiplier)
            }
        """
        match = cls.PROGRESS_PATTERN.search(line)
        if not match:
            return None

        try:
            frame = int(match.group(1))
            fps = float(match.group(2))
            hours = int(match.group(3))
            minutes = int(match.group(4))
            seconds = float(match.group(5))
            speed = float(match.group(6))

            current_time = hours * 3600 + minutes * 60 + seconds

            return {
                'frame': frame,
                'fps': fps,
                'current_time': current_time,
                'speed': speed
            }
        except (ValueError, IndexError):
            return None


class ProgressTracker:
    """Track compression progress with callback support."""

    def __init__(
        self,
        total_duration: float,
        filename: str,
        callback: Optional[ProgressCallback] = None
    ):
        """Initialize progress tracker.

        Args:
            total_duration: Total video duration in seconds
            filename: Name of file being processed
            callback: Optional callback function for progress updates
        """
        self.total_duration = total_duration
        self.filename = filename
        self.callback = callback
        self.start_time = time.time()
        self.last_update_time = 0.0
        self.update_interval = 0.5  # Minimum seconds between updates

    @property
    def elapsed_time(self) -> float:
        """Get elapsed time since compression started."""
        return time.time() - self.start_time

    def update(self, current_time: float, speed: float = 1.0) -> None:
        """Update progress with current encoding time.

        Args:
            current_time: Current position in video (seconds)
            speed: Encoding speed multiplier (e.g., 1.5x means 1.5 seconds per second)
        """
        now = time.time()

        # Throttle updates to avoid excessive callbacks
        if now - self.last_update_time < self.update_interval:
            return

        self.last_update_time = now

        # Calculate percentage
        percentage = min((current_time / self.total_duration) * 100, 100.0)

        # Calculate ETA
        eta = None
        if speed > 0 and current_time > 0:
            remaining_duration = self.total_duration - current_time
            eta = remaining_duration / speed

        # Call callback if provided
        if self.callback:
            self.callback(
                filename=self.filename,
                percentage=percentage,
                current_time=current_time,
                total_time=self.total_duration,
                eta=eta
            )

    def complete(self) -> None:
        """Mark compression as complete (100%)."""
        if self.callback:
            self.callback(
                filename=self.filename,
                percentage=100.0,
                current_time=self.total_duration,
                total_time=self.total_duration,
                eta=0.0
            )


def create_tqdm_callback() -> ProgressCallback:
    """Create a progress callback using tqdm progress bar.

    Returns:
        ProgressCallback that displays a tqdm progress bar

    Note:
        Requires tqdm package to be installed
    """
    try:
        from tqdm import tqdm

        pbar = None

        def callback(
            filename: str,
            percentage: float,
            current_time: float,
            total_time: float,
            eta: Optional[float]
        ) -> None:
            nonlocal pbar

            if pbar is None:
                pbar = tqdm(
                    total=100,
                    desc=f"Compressing {filename}",
                    unit="%",
                    bar_format='{l_bar}{bar}| {n:.1f}% [{elapsed}<{remaining}]'
                )

            pbar.n = percentage
            pbar.refresh()

            if percentage >= 100:
                pbar.close()
                pbar = None

        return callback

    except ImportError:
        # Fallback to simple print-based callback if tqdm not available
        return create_simple_callback()


def create_simple_callback() -> ProgressCallback:
    """Create a simple text-based progress callback.

    Returns:
        ProgressCallback that prints progress to stdout
    """
    last_percentage = [0]  # Use list to store mutable state

    def callback(
        filename: str,
        percentage: float,
        current_time: float,
        total_time: float,
        eta: Optional[float]
    ) -> None:
        # Only print every 5% to avoid spam
        if int(percentage / 5) > int(last_percentage[0] / 5):
            eta_str = f"{eta:.0f}s" if eta is not None else "unknown"
            print(
                f"[{filename}] {percentage:.1f}% complete "
                f"({current_time:.1f}s / {total_time:.1f}s, ETA: {eta_str})"
            )
            last_percentage[0] = percentage

    return callback
