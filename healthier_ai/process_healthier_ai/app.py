import debugpy
import socket


# Check if port 5678 is available
def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("localhost", port)) == 0


debug_port = 5678

if is_port_in_use(debug_port):
    print(f"Port {debug_port} is in use. Please free the port and try again.")
    exit(1)

# Allow other computers to attach to debugpy at this IP address and port.
debugpy.listen(("0.0.0.0", debug_port))
print(f"Waiting for debugger attach on port {debug_port}...")
# Pause the program until a remote debugger is attached
debugpy.wait_for_client()
print("Debugger attached.")

from flask import Flask, request, jsonify
from PIL import Image
import tensorflow as tf
import numpy as np
import tensorflow_datasets as tfds

from custom_objects import swish, FixedDropout


app = Flask(__name__)
model = tf.keras.models.load_model(
    "food101_efficientnet_model.h5",
    custom_objects={"swish": swish, "FixedDropout": FixedDropout},
)

# Load the class labels from the Food-101 dataset
_, info = tfds.load(
    "food101", split=["train", "validation"], with_info=True, as_supervised=True
)
class_names = info.features["label"].names


@app.route("/process-image", methods=["POST"])
def process_image():
    try:
        file = request.files["file"]
        if not file:
            return jsonify({"error": "No file provided"}), 400

        img = Image.open(file.stream).convert("RGB")
        img = img.resize((224, 224))
        img_array = np.array(img)
        img_array = np.expand_dims(img_array, axis=0)

        predictions = model.predict(img_array)
        predicted_class = np.argmax(predictions[0])
        predicted_label = class_names[predicted_class]

        response = {
            "food_item": predicted_label,
            "confidence": float(np.max(predictions)),
        }

        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(port=8080)
