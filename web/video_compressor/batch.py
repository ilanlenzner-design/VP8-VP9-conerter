"""
Batch video compression with concurrent processing.
"""

import os
import asyncio
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Union, Tuple, Optional, Dict
from pathlib import Path
from .compressor import VideoCompressor, CompressionResult
from .progress import ProgressCallback


class BatchCompressor:
    """Handle batch video compression with parallel processing."""

    def __init__(self, compressor: VideoCompressor, max_workers: int = 4):
        """Initialize batch compressor.

        Args:
            compressor: VideoCompressor instance to use
            max_workers: Maximum number of concurrent compression jobs
        """
        self.compressor = compressor
        self.max_workers = max_workers

    def compress_batch(
        self,
        files: List[Union[str, Tuple[str, str]]],
        output_dir: Optional[str] = None,
        preset: str = 'web',
        codec: Optional[str] = None,
        preserve_alpha: bool = False,
        progress_callback: Optional[ProgressCallback] = None,
        **kwargs
    ) -> List[CompressionResult]:
        """Compress multiple video files in parallel.

        Args:
            files: List of input file paths, or list of (input, output) tuples
            output_dir: Output directory (used if files are just input paths)
            preset: Compression preset name
            codec: Optional codec override
            preserve_alpha: Preserve alpha channel
            progress_callback: Optional progress callback
            **kwargs: Additional options passed to compress()

        Returns:
            List of CompressionResult objects (one per file)

        Examples:
            # Using input paths with output directory
            results = batch.compress_batch(
                files=['video1.mp4', 'video2.mp4'],
                output_dir='./output'
            )

            # Using input/output pairs
            results = batch.compress_batch(
                files=[
                    ('input1.mp4', 'output1.webm'),
                    ('input2.mp4', 'output2.webm')
                ]
            )
        """
        # Build file pairs (input, output)
        file_pairs = self._build_file_pairs(files, output_dir)

        results = []

        # Use ThreadPoolExecutor for parallel compression
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all jobs
            future_to_file = {}
            for input_path, output_path in file_pairs:
                future = executor.submit(
                    self._compress_single,
                    input_path=input_path,
                    output_path=output_path,
                    preset=preset,
                    codec=codec,
                    preserve_alpha=preserve_alpha,
                    progress_callback=progress_callback,
                    **kwargs
                )
                future_to_file[future] = (input_path, output_path)

            # Collect results as they complete
            for future in as_completed(future_to_file):
                input_path, output_path = future_to_file[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    # Create failed result
                    results.append(CompressionResult(
                        success=False,
                        input_path=input_path,
                        output_path=output_path,
                        error=str(e)
                    ))

        return results

    async def compress_batch_async(
        self,
        files: List[Union[str, Tuple[str, str]]],
        output_dir: Optional[str] = None,
        preset: str = 'web',
        codec: Optional[str] = None,
        preserve_alpha: bool = False,
        progress_callback: Optional[ProgressCallback] = None,
        **kwargs
    ) -> List[CompressionResult]:
        """Async version of compress_batch().

        Args:
            Same as compress_batch()

        Returns:
            List of CompressionResult objects
        """
        # Build file pairs
        file_pairs = self._build_file_pairs(files, output_dir)

        # Create async tasks
        tasks = []
        for input_path, output_path in file_pairs:
            task = self.compressor.compress_async(
                input_path=input_path,
                output_path=output_path,
                preset=preset,
                codec=codec,
                preserve_alpha=preserve_alpha,
                progress_callback=progress_callback,
                **kwargs
            )
            tasks.append(task)

        # Run all tasks concurrently
        results = []
        for coro in asyncio.as_completed(tasks):
            try:
                result = await coro
                results.append(result)
            except Exception as e:
                # Create failed result
                results.append(CompressionResult(
                    success=False,
                    input_path="",
                    output_path="",
                    error=str(e)
                ))

        return results

    def _compress_single(
        self,
        input_path: str,
        output_path: str,
        preset: str,
        codec: Optional[str],
        preserve_alpha: bool,
        progress_callback: Optional[ProgressCallback],
        **kwargs
    ) -> CompressionResult:
        """Compress a single file (used internally by ThreadPoolExecutor).

        Args:
            input_path: Input file path
            output_path: Output file path
            preset: Preset name
            codec: Optional codec override
            preserve_alpha: Preserve alpha channel
            progress_callback: Progress callback
            **kwargs: Additional options

        Returns:
            CompressionResult
        """
        try:
            return self.compressor.compress(
                input_path=input_path,
                output_path=output_path,
                preset=preset,
                codec=codec,
                preserve_alpha=preserve_alpha,
                progress_callback=progress_callback,
                **kwargs
            )
        except Exception as e:
            return CompressionResult(
                success=False,
                input_path=input_path,
                output_path=output_path,
                error=str(e)
            )

    def _build_file_pairs(
        self,
        files: List[Union[str, Tuple[str, str]]],
        output_dir: Optional[str]
    ) -> List[Tuple[str, str]]:
        """Build list of (input, output) file path pairs.

        Args:
            files: List of input paths or (input, output) tuples
            output_dir: Output directory (used if files are just paths)

        Returns:
            List of (input_path, output_path) tuples

        Raises:
            ValueError: If output_dir is required but not provided
        """
        file_pairs = []

        for item in files:
            if isinstance(item, tuple):
                # Already a (input, output) pair
                input_path, output_path = item
                file_pairs.append((input_path, output_path))
            else:
                # Just input path, need to construct output path
                if output_dir is None:
                    raise ValueError(
                        "output_dir must be provided when files are input paths only"
                    )

                input_path = item
                filename = os.path.basename(input_path)
                name, _ = os.path.splitext(filename)
                output_path = os.path.join(output_dir, f"{name}.webm")
                file_pairs.append((input_path, output_path))

        return file_pairs


class BatchProgress:
    """Aggregate progress tracking for batch operations."""

    def __init__(self, total_files: int):
        """Initialize batch progress tracker.

        Args:
            total_files: Total number of files to process
        """
        self.total_files = total_files
        self.completed_files = 0
        self.file_progress: Dict[str, float] = {}

    def update_file_progress(self, filename: str, percentage: float) -> None:
        """Update progress for a specific file.

        Args:
            filename: Name of file being processed
            percentage: Completion percentage (0-100)
        """
        old_percentage = self.file_progress.get(filename, 0.0)
        self.file_progress[filename] = percentage

        # If file just completed, increment counter
        if old_percentage < 100 and percentage >= 100:
            self.completed_files += 1

    @property
    def overall_percentage(self) -> float:
        """Calculate overall batch progress percentage.

        Returns:
            Overall completion percentage (0-100)
        """
        if not self.file_progress:
            return 0.0

        total_progress = sum(self.file_progress.values())
        return total_progress / self.total_files

    def create_callback(self) -> ProgressCallback:
        """Create a progress callback that updates batch progress.

        Returns:
            ProgressCallback function
        """
        def callback(
            filename: str,
            percentage: float,
            current_time: float,
            total_time: float,
            eta: Optional[float]
        ) -> None:
            self.update_file_progress(filename, percentage)
            print(
                f"[Batch {self.completed_files + 1}/{self.total_files}] "
                f"{filename}: {percentage:.1f}% "
                f"(Overall: {self.overall_percentage:.1f}%)"
            )

        return callback
