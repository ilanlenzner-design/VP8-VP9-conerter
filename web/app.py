#!/usr/bin/env python3
"""
Flask web interface for Video Compressor SDK.
"""

import os
import json
import time
import uuid
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_file, Response
from werkzeug.utils import secure_filename

# Import SDK (local copy for Vercel deployment)
from video_compressor import VideoCompressor, VideoInfo, list_presets

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max file size
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
app.config['COMPRESSED_FOLDER'] = os.path.join(os.path.dirname(__file__), 'compressed')

# Ensure folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['COMPRESSED_FOLDER'], exist_ok=True)

# Store compression progress
compression_progress = {}

ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi', 'mkv', 'webm'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Render main page."""
    return render_template('index.html')


@app.route('/api/presets')
def get_presets():
    """Get available compression presets."""
    presets = list_presets()

    # Add detailed info for each preset
    compressor = VideoCompressor()
    preset_details = {}

    for name, description in presets.items():
        preset = compressor.get_preset(name)
        preset_details[name] = {
            'name': name,
            'description': description,
            'codec': preset.codec,
            'video_bitrate': preset.video_bitrate,
            'crf': preset.crf,
            'speed': preset.speed,
            'two_pass': preset.two_pass
        }

    return jsonify(preset_details)


@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle file upload."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Allowed: mp4, mov, avi, mkv, webm'}), 400

    # Generate unique filename
    file_id = str(uuid.uuid4())
    original_filename = secure_filename(file.filename)
    name, ext = os.path.splitext(original_filename)
    unique_filename = f"{file_id}_{original_filename}"

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
    file.save(filepath)

    # Get video info
    try:
        video_info = VideoInfo.from_file(filepath)
        info = {
            'duration': round(video_info.duration, 2),
            'width': video_info.width,
            'height': video_info.height,
            'codec': video_info.codec,
            'has_alpha': video_info.has_alpha,
            'fps': round(video_info.fps, 2) if video_info.fps else None,
            'size_mb': round(os.path.getsize(filepath) / (1024 * 1024), 2)
        }
    except Exception as e:
        info = {
            'error': str(e),
            'size_mb': round(os.path.getsize(filepath) / (1024 * 1024), 2)
        }

    return jsonify({
        'file_id': file_id,
        'filename': original_filename,
        'filepath': unique_filename,
        'info': info
    })


@app.route('/api/compress', methods=['POST'])
def compress_video():
    """Start video compression."""
    data = request.json

    file_id = data.get('file_id')
    filename = data.get('filename')
    preset = data.get('preset', 'web')
    preserve_alpha = data.get('preserve_alpha', False)

    if not file_id or not filename:
        return jsonify({'error': 'Missing file_id or filename'}), 400

    # Find uploaded file
    upload_path = None
    for f in os.listdir(app.config['UPLOAD_FOLDER']):
        if f.startswith(file_id):
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], f)
            break

    if not upload_path or not os.path.exists(upload_path):
        return jsonify({'error': 'Upload file not found'}), 404

    # Output path
    name, _ = os.path.splitext(filename)
    output_filename = f"{file_id}_{name}_compressed.webm"
    output_path = os.path.join(app.config['COMPRESSED_FOLDER'], output_filename)

    # Initialize progress
    compression_progress[file_id] = {
        'status': 'starting',
        'percentage': 0,
        'filename': filename,
        'preset': preset
    }

    # Start compression in background
    import threading

    def compress_task():
        try:
            compressor = VideoCompressor()

            # Progress callback
            def progress_callback(filename, percentage, current_time, total_time, eta):
                compression_progress[file_id] = {
                    'status': 'compressing',
                    'percentage': round(percentage, 1),
                    'current_time': round(current_time, 1),
                    'total_time': round(total_time, 1),
                    'eta': round(eta, 1) if eta else None,
                    'filename': filename,
                    'preset': preset
                }

            # Compress
            result = compressor.compress(
                input_path=upload_path,
                output_path=output_path,
                preset=preset,
                preserve_alpha=preserve_alpha,
                progress_callback=progress_callback
            )

            # Update final status
            compression_progress[file_id] = {
                'status': 'complete',
                'percentage': 100,
                'filename': filename,
                'preset': preset,
                'result': {
                    'input_size_mb': round(result.input_size_mb, 2),
                    'output_size_mb': round(result.output_size_mb, 2),
                    'compression_ratio': round(result.compression_ratio, 2),
                    'duration': round(result.duration, 2),
                    'output_filename': output_filename
                }
            }

        except Exception as e:
            compression_progress[file_id] = {
                'status': 'error',
                'percentage': 0,
                'error': str(e),
                'filename': filename
            }

    thread = threading.Thread(target=compress_task)
    thread.daemon = True
    thread.start()

    return jsonify({
        'file_id': file_id,
        'status': 'started'
    })


@app.route('/api/progress/<file_id>')
def get_progress(file_id):
    """Get compression progress via Server-Sent Events."""
    def generate():
        while True:
            if file_id in compression_progress:
                data = compression_progress[file_id]
                yield f"data: {json.dumps(data)}\n\n"

                # Stop if complete or error
                if data['status'] in ('complete', 'error'):
                    break

            time.sleep(0.5)

    return Response(generate(), mimetype='text/event-stream')


@app.route('/api/download/<file_id>')
def download_file(file_id):
    """Download compressed video."""
    # Find compressed file
    for f in os.listdir(app.config['COMPRESSED_FOLDER']):
        if f.startswith(file_id):
            filepath = os.path.join(app.config['COMPRESSED_FOLDER'], f)
            return send_file(
                filepath,
                as_attachment=True,
                download_name=f.split('_', 1)[1]  # Remove UUID prefix
            )

    return jsonify({'error': 'File not found'}), 404


@app.route('/api/cleanup/<file_id>', methods=['DELETE'])
def cleanup_files(file_id):
    """Clean up uploaded and compressed files."""
    deleted = []

    # Delete uploaded file
    for f in os.listdir(app.config['UPLOAD_FOLDER']):
        if f.startswith(file_id):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], f)
            os.remove(filepath)
            deleted.append(f)

    # Delete compressed file
    for f in os.listdir(app.config['COMPRESSED_FOLDER']):
        if f.startswith(file_id):
            filepath = os.path.join(app.config['COMPRESSED_FOLDER'], f)
            os.remove(filepath)
            deleted.append(f)

    # Clear progress
    if file_id in compression_progress:
        del compression_progress[file_id]

    return jsonify({
        'deleted': deleted,
        'count': len(deleted)
    })


if __name__ == '__main__':
    print("=" * 60)
    print("Video Compressor Web Interface")
    print("=" * 60)

    # Get port from environment (for Railway, Heroku, etc.) or default to 5000
    port = int(os.environ.get('PORT', 5000))

    print(f"Server starting at: http://0.0.0.0:{port}")
    print("Press Ctrl+C to stop")
    print("=" * 60)

    app.run(debug=False, host='0.0.0.0', port=port)
