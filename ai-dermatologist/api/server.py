from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from PIL import Image
from flask_cors import CORS
import numpy as np
import io
import os

# ✅ 1. Create Flask app FIRST
app = Flask(__name__)
CORS(app)
# ✅ 2. Load model
MODEL_PATH = os.path.join(
    "C:/Users/Bijendra Singh/Desktop/epidora/ai-dermatologist/model",
    "efficientnetv2s.h5"
)
print(f"🔍 Loading skin cancer model from {MODEL_PATH} ...")
model = load_model(MODEL_PATH)

# ✅ 3. Label map
label_map = {
    0: "Actinic Keratoses and Intraepithelial Carcinoma (AKIEC)",
    1: "Basal Cell Carcinoma (BCC)",
    2: "Benign Keratosis-like Lesions (BKL)",
    3: "Dermatofibroma (DF)",
    4: "Melanoma (MEL)",
    5: "Melanocytic Nevus (Mole / NV)",
    6: "Vascular Lesion (VASC)"
}

# ✅ 4. Route
@app.route("/analyze-image", methods=["POST"])
def analyze_image():
    try:
        if "image" not in request.files:
            return jsonify({"error": "No image uploaded"}), 400

        file = request.files["image"]
        img = Image.open(io.BytesIO(file.read())).convert("RGB")
        img = img.resize((224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0) / 255.0

        preds = model.predict(x)
        pred_idx = int(np.argmax(preds))
        confidence = float(np.max(preds))

        result = {
            "condition": label_map[pred_idx],
            "confidence": round(confidence, 4)
        }

        return jsonify(result)

    except Exception as e:
        print(f"❌ Error analyzing image: {e}")
        return jsonify({"error": "Failed to analyze image"}), 500

# ✅ 5. Run app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
