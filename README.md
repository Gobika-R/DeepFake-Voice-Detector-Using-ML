# Deepfake Audio Detection

A Flask-based backend API for detecting deepfake audio files using machine learning.

## Features

- Audio file upload (WAV, MP3 formats)
- RESTful API endpoints
- Audio processing with librosa
- Machine learning classification support

## Project Structure

```
deepfake_audio_detection/
├── backend/
│   ├── app.py              # Flask application
│   ├── requirements.txt    # Python dependencies
│   ├── model/             # ML model directory
│   └── uploads/           # Uploaded audio files
└── README.md
```

## Prerequisites

- Python 3.8 or higher
- Virtual environment (recommended)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd deepfake_audio_detection
   ```

2. **Create and activate virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

## Usage

1. **Start the Flask server**
   ```bash
   cd backend
   python app.py
   ```
   
   The server will run on `http://127.0.0.1:5000` by default.

2. **Test the API**
   
   **Home endpoint:**
   ```bash
   curl http://127.0.0.1:5000/
   ```

   **Upload audio file:**
   ```bash
   # Windows PowerShell
   curl.exe -X POST -F "file=@path/to/audio.mp3" http://127.0.0.1:5000/upload
   
   # Or using PowerShell cmdlet
   $filePath = "path\to\audio.mp3"
   Invoke-WebRequest -Uri http://127.0.0.1:5000/upload -Method POST -Form @{file = Get-Item -Path $filePath}
   ```

## API Endpoints

### GET /
Returns a welcome message confirming the server is running.

**Response:**
```
Deepfake Audio Detection Backend is Running!
```

### POST /upload
Upload an audio file for processing.

**Parameters:**
- `file`: Audio file (WAV or MP3 format)

**Success Response:**
```json
{
  "message": "Audio file uploaded successfully",
  "file_path": "uploads/filename.mp3"
}
```

**Error Responses:**
```json
{
  "error": "No file part"
}
```
```json
{
  "error": "No selected file"
}
```
```json
{
  "error": "Invalid file format"
}
```

## Supported Audio Formats

- WAV (.wav)
- MP3 (.mp3)

## Dependencies

Key libraries:
- **Flask**: Web framework
- **librosa**: Audio analysis
- **scikit-learn**: Machine learning
- **soundfile**: Audio file I/O
- **numpy**: Numerical computing

See `backend/requirements.txt` for complete list.

## Development

### Debug Mode
The application runs in debug mode by default, which:
- Enables auto-reload on code changes
- Provides detailed error messages
- Should NOT be used in production

### Production Deployment
For production, use a WSGI server like Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## License

[Add your license here]

## Contributing

[Add contribution guidelines here]

## Authors

GOBIKA R
