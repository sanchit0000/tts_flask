from flask import Flask, request, send_file, jsonify
from TTS.api import TTS
import os
import uuid

app = Flask(__name__)

# Use a lighter model if memory is an issue (e.g. on Render)
# You can change to "tts_models/en/ljspeech/tacotron2-DDC" for better quality
model_name = "tts_models/en/ljspeech/fastspeech2"
tts = TTS(model_name)

# Make sure output directory exists
OUTPUT_DIR = "static"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.route("/api/tts", methods=["POST"])
def generate_audio():
    try:
        data = request.get_json()
        text = data.get("text", "").strip()

        if not text:
            return jsonify({"error": "Text is required"}), 400

        filename = f"{uuid.uuid4().hex}.wav"
        path = os.path.join(OUTPUT_DIR, filename)
        tts.tts_to_file(text=text, file_path=path)

        return send_file(
            path,
            as_attachment=True,
            download_name="output.wav",
            mimetype="audio/wav"
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Required for platforms like Render or Railway
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
