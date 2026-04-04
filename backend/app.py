from flask import Flask, request, jsonify, render_template
import os
from predict import predict_audio

app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static"
)

ALLOWED_EXTENSIONS = {"wav", "mp3"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def get_firebase_config():
    """Load Firebase web config from environment variables."""
    return {
        "apiKey": os.getenv("FIREBASE_API_KEY", "AIzaSyBcllMZLLOLRj1cYEH0AxDMyzXZQdzr0qw"),
        "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN", "deepfake-audio-detector.firebaseapp.com"),
        "projectId": os.getenv("FIREBASE_PROJECT_ID", "deepfake-audio-detector"),
        "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET", "deepfake-audio-detector.firebasestorage.app"),
        "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID", "359400343328"),
        "appId": os.getenv("FIREBASE_APP_ID", "1:359400343328:web:836106398a9d469363f945"),
        "measurementId": os.getenv("FIREBASE_MEASUREMENT_ID", ""),
    }


@app.context_processor
def inject_template_globals():
    return {"firebase_config": get_firebase_config()}

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/detector")
def detector():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_audio():

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Only WAV and MP3 supported"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    label, confidence = predict_audio(file_path)

    return jsonify({
        "prediction": label,
        "confidence": f"{confidence}%"
    })

if __name__ == "__main__":
    app.run(debug=True)
