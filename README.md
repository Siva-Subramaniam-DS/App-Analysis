# App-Analysis

## Table of Content















---

### **Purpose of the Image Classification**
This Flask application is designed for image classification. It allows users to upload images, which are then processed and classified into one of three categories: "Good," "Bad," or "Neutral." The app also maintains a session to track the overall classification summary.

---

### **Key Components -  Image Classification**

#### **1. Imports**
- **Flask**: Framework to create the web application.
  - `render_template`: Renders HTML templates.
  - `request`: Handles HTTP requests (e.g., form data, file uploads).
  - `jsonify`: Converts Python objects into JSON responses.
  - `session`: Stores user-specific data across requests.
- **TensorFlow and Keras**: Used for loading the model and preprocessing images.
  - `load_model`: Loads a pre-trained Keras model.
  - `load_img`, `img_to_array`: Prepares images for model prediction.
- **NumPy**: Used for numerical computations.
- **os**: Handles file system operations (e.g., saving and deleting files).

#### **2. Flask App Initialization**
- `UPLOAD_FOLDER`: Directory for saving uploaded images temporarily.
- `IMG_SIZE`: The target size of the images for the model (`224x224` pixels).
- `CLASS_NAMES`: Defines the possible output classes (`Good`, `Bad`, `Neutral`).
- `app.config['UPLOAD_FOLDER']`: Configures the folder to store uploaded files.
- `app.secret_key`: A key to enable Flask session storage.

---

### **Routes and Functions**

#### **1. Loading the Model**
```python
try:
    model = load_model(MODEL_PATH)
    print(f"Model loaded successfully from {MODEL_PATH}")
except Exception as e:
    print(f"Failed to load model: {e}")
    model = None
```
- Tries to load the pre-trained model from `model.h5`.
- If successful, the model is loaded and ready for predictions.
- If an error occurs (e.g., file not found), it logs the error and sets `model = None`.

---

#### **2. Session Initialization**
```python
@app.before_request
def init_session():
    if 'predictions' not in session:
        session['predictions'] = {"Good": 0, "Bad": 0, "Neutral": 0}
```
- A Flask `@before_request` hook ensures that the session contains a `predictions` dictionary before every request.
- This dictionary tracks the count of classifications for each class.

---

#### **3. Render Image Classification Page**
```python
@app.route('/imageclassify', methods=['GET'])
def imageclassify():
    return render_template("image_Classifier.html")
```
- Renders the HTML page `image_Classifier.html` for the image classification interface.

---

#### **4. Image Upload and Classification**
```python
@app.route('/upload', methods=['POST'])
def upload():
```
Handles the following steps:
1. **Check for File in Request**:
   ```python
   if 'file' not in request.files:
       return jsonify({"error": "No file uploaded"}), 400
   ```

2. **Save Uploaded File**:
   ```python
   file = request.files['file']
   file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
   os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
   file.save(file_path)
   ```

3. **Preprocess the Image**:
   ```python
   image = load_img(file_path, target_size=(IMG_SIZE, IMG_SIZE))
   img_array = img_to_array(image)
   img_array = np.expand_dims(img_array, axis=0)
   img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)
   ```

4. **Model Prediction**:
   ```python
   predictions = model.predict(img_array)
   predicted_class = CLASS_NAMES[np.argmax(predictions)]
   confidence = np.max(predictions)
   ```

5. **Update Session**:
   ```python
   session['predictions'][predicted_class] += 1
   ```

6. **Return Results**:
   ```python
   return jsonify({
       "prediction": predicted_class,
       "confidence": f"{confidence:.2f}"
   })
   ```

7. **Error Handling**:
   - If any exception occurs, it returns a JSON error response.

8. **Cleanup**:
   ```python
   os.remove(file_path)
   ```

---

#### **5. Summary Metrics**
```python
@app.route('/summary', methods=['GET'])
def summary():
```
- Computes and returns a summary of all classifications.

1. **Check if Images Have Been Uploaded**:
   ```python
   total_images = sum(session['predictions'].values())
   if total_images == 0:
       return jsonify({"error": "No images uploaded yet"}), 400
   ```

2. **Calculate Metrics**:
   ```python
   summary_metrics = {
       "total_images": total_images,
       "class_distribution": session['predictions'],
       "percent_distribution": {
           class_name: f"{(count / total_images) * 100:.2f}%"
           for class_name, count in session['predictions'].items()
       }
   }
   ```

3. **Return Results**:
   ```python
   return jsonify(summary_metrics)
   ```

---

### **App Execution**
```python
if __name__ == '__main__':
    app.run(debug=True)
```
- Starts the Flask development server in debug mode for easier testing and error reporting.

---

### **Expected File Structure**
- `app.py`: This script.
- `uploads/`: Temporary directory for uploaded images.
- `templates/image_Classifier.html`: HTML template for the UI.
- `model.h5`: The pre-trained Keras model.

---

### Example Output
Prediction: Good ✅
Confidence: 95.67% 🎯

---

### **Summary of Features**
1. **File Upload**: Users can upload images for classification.
2. **Real-Time Predictions**: Classifies images using a pre-trained TensorFlow model.
3. **Session Tracking**: Maintains a count of classifications for summary metrics.
4. **Dynamic JSON Responses**: Provides feedback to the user via JSON API.
5. **Summary Metrics**: Displays overall classification results and distributions.

This app is modular, robust, and well-structured for real-world use cases in image classification tasks.
