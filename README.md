# Deepfake Audio Detection

Full-stack Flask application for detecting fake vs real audio using ML models, with Firebase authentication and a private user dashboard.

## Features

- Deepfake audio prediction for WAV and MP3 files
- Modern web UI served by Flask (home, login, detector)
- Firebase authentication:
   - Email and password sign-in/sign-up
   - Google sign-in
- Session controls:
   - User is logged out when leaving the detector page
   - User is logged out when returning to home page
   - Session is browser-session based
- Per-user dashboard history on detector page
   - Each signed-in user sees only their own analysis history

## Project Structure

```text
deepfake_audio_detection/
├── backend/
│   ├── app.py
│   ├── predict.py
│   ├── train_model.py
│   ├── train_models.py
│   ├── extract_features.py
│   ├── requirements.txt
│   ├── models/
│   ├── features/
│   ├── preprocessing/
│   └── uploads/
├── dataset/
├── frontend/
│   ├── static/
│   │   ├── style.css
│   │   └── auth.js
│   └── templates/
│       ├── home.html
│       ├── login.html
│       └── index.html
└── README.md
```

## Requirements

- Python 3.10+
- Virtual environment recommended
- Firebase project with Auth enabled

## Local Setup

1. Clone and open project

```bash
git clone <repository-url>
cd deepfake_audio_detection
```

2. Create and activate virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies

```bash
cd backend
pip install -r requirements.txt
```

4. Configure Firebase (recommended via environment variables)

```bash
# Windows PowerShell example
$env:FIREBASE_API_KEY="<your-key>"
$env:FIREBASE_AUTH_DOMAIN="<your-project>.firebaseapp.com"
$env:FIREBASE_PROJECT_ID="<your-project-id>"
$env:FIREBASE_STORAGE_BUCKET="<your-bucket>"
$env:FIREBASE_MESSAGING_SENDER_ID="<sender-id>"
$env:FIREBASE_APP_ID="<app-id>"
$env:FIREBASE_MEASUREMENT_ID="<measurement-id>"   # optional
```

5. Run the app

```bash
python app.py
```

App runs at:

`http://127.0.0.1:5000`

## Routes

- `GET /` -> Home page
- `GET /login` -> Sign-in/sign-up page
- `GET /detector` -> Auth-protected detector page
- `POST /upload` -> Audio analysis endpoint

## API

### POST /upload

Uploads and analyzes one audio file.

Request:
- `multipart/form-data`
- field name: `file`
- supported: `.wav`, `.mp3`

Success response example:

```json
{
   "prediction": "FAKE",
   "confidence": "92.41%"
}
```

Error response example:

```json
{
   "error": "Only WAV and MP3 supported"
}
```

## Firebase Auth Setup Checklist

In Firebase Console:

1. Enable Authentication
2. Enable `Email/Password` provider
3. Enable `Google` provider
4. Add your app domains to Authorized domains:
    - `localhost`
    - deployed domain (for production)

## Deployment

This app can be deployed as a single Flask service (frontend is server-rendered templates).

### Option A: Render / Railway / similar

- Root directory: `backend`
- Build command:

```bash
pip install -r requirements.txt
```

- Start command:

```bash
gunicorn app:app
```

- Set environment variables:
   - `FIREBASE_API_KEY`
   - `FIREBASE_AUTH_DOMAIN`
   - `FIREBASE_PROJECT_ID`
   - `FIREBASE_STORAGE_BUCKET`
   - `FIREBASE_MESSAGING_SENDER_ID`
   - `FIREBASE_APP_ID`
   - `FIREBASE_MEASUREMENT_ID` (optional)

### Option B: VPS (Ubuntu example)

1. Install Python and dependencies
2. Create virtual environment and install requirements
3. Run with gunicorn behind nginx
4. Configure HTTPS with certbot

Gunicorn example:

```bash
cd backend
gunicorn -w 2 -b 0.0.0.0:5000 app:app
```

## Notes

- `uploads/` is used for temporary file handling. Configure storage/cleanup policy for production.
- Use environment variables for Firebase config in production.
- Do not run Flask debug mode in production.

## Author

GOBIKA R
