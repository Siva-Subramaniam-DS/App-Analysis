from flask import Flask, render_template, request, jsonify, session
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import tensorflow as tf
import numpy as np
import os

# Flask app
app = Flask(__name__)

# Constants
UPLOAD_FOLDER = "uploads"
IMG_SIZE = 224
CLASS_NAMES = ['Good', 'Bad', 'Neutral']

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "your_secret_key"  # Required for session storage

# Load model
MODEL_PATH = "model.h5"  # Update with the correct model path
try:
    model = load_model(MODEL_PATH)
    print(f"Model loaded successfully from {MODEL_PATH}")
except Exception as e:
    print(f"Failed to load model: {e}")
    model = None

# Initialize session storage for predictions
@app.before_request
def init_session():
    if 'predictions' not in session:
        session['predictions'] = {"Good": 0, "Bad": 0, "Neutral": 0}

@app.route('/imageclassify', methods=['GET'])
def imageclassify():
    """
    Render the image classification page.
    """
    return render_template("image_Classifier.html")


@app.route('/upload', methods=['POST'])
def upload():
    """
    Handle the image upload and return classification results.
    """
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']

    if file and file.filename != '':
        # Save the file locally
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        file.save(file_path)

        try:
            # Preprocess the image
            image = load_img(file_path, target_size=(IMG_SIZE, IMG_SIZE))
            img_array = img_to_array(image)
            img_array = np.expand_dims(img_array, axis=0)
            img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)

            # Predict
            predictions = model.predict(img_array)
            predicted_class = CLASS_NAMES[np.argmax(predictions)]
            confidence = np.max(predictions)

            # Update session storage
            session['predictions'][predicted_class] += 1

            # Cleanup
            os.remove(file_path)

            return jsonify({
                "prediction": predicted_class,
                "confidence": f"{confidence:.2f}"
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return jsonify({"error": "Invalid file or filename"}), 400


@app.route('/summary', methods=['GET'])
def summary():
    """
    Calculate and return the overall summary metrics.
    """
    total_images = sum(session['predictions'].values())
    if total_images == 0:
        return jsonify({"error": "No images uploaded yet"}), 400

    summary_metrics = {
        "total_images": total_images,
        "class_distribution": session['predictions'],
        "percent_distribution": {
            class_name: f"{(count / total_images) * 100:.2f}%"
            for class_name, count in session['predictions'].items()
        }
    }

    return jsonify(summary_metrics)


if __name__ == '__main__':
    app.run(debug=True)
