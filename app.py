import os
from flask import Flask, render_template, request, jsonify
import easyocr

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load EasyOCR model once (important)
reader = easyocr.Reader(['en'], gpu=False)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/extract-text", methods=["POST"])
def extract_text():

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"})

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No file selected"})

    try:
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        result = reader.readtext(filepath, detail=0)

        text = "\n".join(result)

        os.remove(filepath)

        return jsonify({"text": text})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    port = int(os.environ.get("port", 5000))
    app.run(host="0.0.0.0", port=port)