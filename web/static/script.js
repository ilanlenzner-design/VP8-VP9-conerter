// Global state
let currentFileId = null;
let currentFilename = null;
let selectedPreset = 'web';

// Initialize when page loads
document.addEventListener('DOMContentLoaded', () => {
    initializeUpload();
    loadPresets();
    setupEventListeners();
});

// Initialize upload area
function initializeUpload() {
    const uploadArea = document.getElementById('upload-area');
    const fileInput = document.getElementById('file-input');

    // Click to upload
    uploadArea.addEventListener('click', () => {
        fileInput.click();
    });

    // File selected
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFile(e.target.files[0]);
        }
    });

    // Drag and drop
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');

        if (e.dataTransfer.files.length > 0) {
            handleFile(e.dataTransfer.files[0]);
        }
    });
}

// Load presets from API
async function loadPresets() {
    try {
        const response = await fetch('/api/presets');
        const presets = await response.json();

        const presetGrid = document.getElementById('preset-grid');
        presetGrid.innerHTML = '';

        Object.entries(presets).forEach(([key, preset]) => {
            const card = document.createElement('div');
            card.className = 'preset-card';
            if (key === selectedPreset) {
                card.classList.add('selected');
            }

            card.innerHTML = `
                <div class="preset-name">${preset.description}</div>
                <div class="preset-description">${key}</div>
                <div class="preset-details">
                    ${preset.codec.toUpperCase()} • ${preset.video_bitrate} • CRF ${preset.crf}
                </div>
            `;

            card.addEventListener('click', () => {
                document.querySelectorAll('.preset-card').forEach(c => c.classList.remove('selected'));
                card.classList.add('selected');
                selectedPreset = key;
            });

            presetGrid.appendChild(card);
        });
    } catch (error) {
        console.error('Failed to load presets:', error);
    }
}

// Handle file upload
async function handleFile(file) {
    // Validate file type
    const allowedTypes = ['video/mp4', 'video/quicktime', 'video/x-msvideo', 'video/x-matroska', 'video/webm'];
    if (!allowedTypes.includes(file.type)) {
        showError('Invalid file type. Please select a video file.');
        return;
    }

    // Show loading
    showSection('upload-section');
    document.getElementById('upload-area').innerHTML = '<div class="upload-icon">⏳</div><h3>Uploading...</h3>';

    // Upload file
    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Upload failed');
        }

        const data = await response.json();
        currentFileId = data.file_id;
        currentFilename = data.filename;

        // Show file info
        displayFileInfo(data.info, data.filename);

        // Show preset selection
        showSection('preset-section');

    } catch (error) {
        console.error('Upload error:', error);
        showError(`Upload failed: ${error.message}`);
    }
}

// Display file information
function displayFileInfo(info, filename) {
    const fileInfo = document.getElementById('file-info');
    const infoContent = document.getElementById('info-content');

    fileInfo.classList.remove('hidden');

    infoContent.innerHTML = `
        <div class="info-item">
            <div class="info-label">Filename</div>
            <div class="info-value">${filename}</div>
        </div>
        <div class="info-item">
            <div class="info-label">Size</div>
            <div class="info-value">${info.size_mb} MB</div>
        </div>
        <div class="info-item">
            <div class="info-label">Duration</div>
            <div class="info-value">${info.duration || '--'} sec</div>
        </div>
        <div class="info-item">
            <div class="info-label">Resolution</div>
            <div class="info-value">${info.width || '--'}x${info.height || '--'}</div>
        </div>
        <div class="info-item">
            <div class="info-label">Codec</div>
            <div class="info-value">${info.codec || '--'}</div>
        </div>
        <div class="info-item">
            <div class="info-label">Alpha Channel</div>
            <div class="info-value">${info.has_alpha ? '✓ Yes' : '✗ No'}</div>
        </div>
    `;
}

// Setup event listeners
function setupEventListeners() {
    document.getElementById('compress-btn').addEventListener('click', startCompression);
    document.getElementById('download-btn').addEventListener('click', downloadFile);
    document.getElementById('compress-another-btn').addEventListener('click', reset);
    document.getElementById('try-again-btn').addEventListener('click', reset);
}

// Start compression
async function startCompression() {
    if (!currentFileId) return;

    const preserveAlpha = document.getElementById('preserve-alpha').checked;

    // Update UI
    document.getElementById('progress-filename').textContent = currentFilename;
    document.getElementById('progress-preset').textContent = `Preset: ${selectedPreset}`;
    showSection('progress-section');

    try {
        // Start compression
        const response = await fetch('/api/compress', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                file_id: currentFileId,
                filename: currentFilename,
                preset: selectedPreset,
                preserve_alpha: preserveAlpha
            })
        });

        if (!response.ok) {
            throw new Error('Failed to start compression');
        }

        // Listen for progress updates
        listenForProgress(currentFileId);

    } catch (error) {
        console.error('Compression error:', error);
        showError(`Compression failed: ${error.message}`);
    }
}

// Listen for progress updates via Server-Sent Events
function listenForProgress(fileId) {
    const eventSource = new EventSource(`/api/progress/${fileId}`);

    eventSource.onmessage = (event) => {
        const data = JSON.parse(event.data);

        if (data.status === 'compressing') {
            updateProgress(data);
        } else if (data.status === 'complete') {
            eventSource.close();
            showResults(data.result);
        } else if (data.status === 'error') {
            eventSource.close();
            showError(data.error);
        }
    };

    eventSource.onerror = () => {
        eventSource.close();
        showError('Connection lost. Please try again.');
    };
}

// Update progress bar
function updateProgress(data) {
    document.getElementById('progress-bar').style.width = `${data.percentage}%`;
    document.getElementById('progress-percentage').textContent = `${data.percentage.toFixed(1)}%`;
    document.getElementById('progress-time').textContent =
        `Time: ${data.current_time}s / ${data.total_time}s`;
    document.getElementById('progress-eta').textContent =
        `ETA: ${data.eta ? Math.round(data.eta) + 's' : '--'}`;
}

// Show compression results
function showResults(result) {
    document.getElementById('result-input-size').textContent = `${result.input_size_mb} MB`;
    document.getElementById('result-output-size').textContent = `${result.output_size_mb} MB`;
    document.getElementById('result-ratio').textContent = `${result.compression_ratio}x`;

    const saved = result.input_size_mb - result.output_size_mb;
    const savedPercent = ((saved / result.input_size_mb) * 100).toFixed(1);
    document.getElementById('result-saved').textContent = `${saved.toFixed(2)} MB (${savedPercent}%)`;

    showSection('results-section');
}

// Download compressed file
function downloadFile() {
    if (!currentFileId) return;
    window.location.href = `/api/download/${currentFileId}`;
}

// Reset for another compression
async function reset() {
    // Cleanup files
    if (currentFileId) {
        try {
            await fetch(`/api/cleanup/${currentFileId}`, {
                method: 'DELETE'
            });
        } catch (error) {
            console.error('Cleanup error:', error);
        }
    }

    // Reset state
    currentFileId = null;
    currentFilename = null;
    selectedPreset = 'web';

    // Reset UI
    document.getElementById('upload-area').innerHTML = `
        <div class="upload-icon">📁</div>
        <h3>Drop your video here</h3>
        <p>or click to browse</p>
        <p class="file-types">Supported: MP4, MOV, AVI, MKV, WebM</p>
    `;
    document.getElementById('file-info').classList.add('hidden');
    document.getElementById('file-input').value = '';

    // Show upload section
    showSection('upload-section');
    loadPresets();
}

// Show specific section and hide others
function showSection(sectionId) {
    const sections = ['upload-section', 'preset-section', 'progress-section', 'results-section', 'error-section'];
    sections.forEach(id => {
        document.getElementById(id).classList.add('hidden');
    });
    document.getElementById(sectionId).classList.remove('hidden');
}

// Show error message
function showError(message) {
    document.getElementById('error-message').textContent = message;
    showSection('error-section');
}
