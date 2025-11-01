# model_predict_hf.py
import os, sys, json
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from huggingface_hub import hf_hub_download

BASE = os.path.dirname(__file__)
MODEL_FILENAME = "efficientnetv2s.h5"
MODEL_PATH = os.path.join(BASE, MODEL_FILENAME)
HF_REPO = "Miguel764/efficientnetv2s-skin-cancer-classifier"

LABELS = [
    "akiec", "bcc", "bkl", "df", "mel", "nv", "vasc"
]

def ensure_model():
    if os.path.exists(MODEL_PATH):
        return MODEL_PATH
    print("Model not found locally — downloading from Hugging Face...")
    model_file = hf_hub_download(repo_id=HF_REPO, filename=MODEL_FILENAME)
    os.replace(model_file, MODEL_PATH)
    print("Downloaded model to:", MODEL_PATH)
    return MODEL_PATH

def load_model():
    path = ensure_model()
    print("Loading model...")
    return tf.keras.models.load_model(path)

def predict(model, img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    arr = image.img_to_array(img) / 255.0
    arr = np.expand_dims(arr, axis=0)
    preds = model.predict(arr)[0]
    idx = int(np.argmax(preds))
    return {"label": LABELS[idx],
            "confidence": float(preds[idx]),
            "scores": preds.tolist()}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python model_predict_hf.py path/to/image.jpg")
        sys.exit(1)
    img_path = sys.argv[1]
    if not os.path.exists(img_path):
        print(json.dumps({"error": "image not found"}))
        sys.exit(1)
    model = load_model()
    result = predict(model, img_path)
    print(json.dumps(result))
