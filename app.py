from flask import Flask, request, send_file
from TTS.api import TTS
import os
import uuid

app = Flask(__name__)
tts = TTS("tts_models/en/ljspeech/tacotron2-DDC")
OUTPUT_DIR = "static"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.route("/api/tts", methods=["POST"])
def generate_audio():
    data = request.get_json()
    text = data.get("text", "").strip()

    if not text:
        return {"error": "Text is required"}, 400

    filename = f"{uuid.uuid4().hex}.wav"
    path = os.path.join(OUTPUT_DIR, filename)
    tts.tts_to_file(text=text, file_path=path)

    return send_file(path, as_attachment=True, download_name="output.wav", mimetype="audio/wav")
