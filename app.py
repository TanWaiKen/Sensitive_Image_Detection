from ultralytics import YOLO
from flask import Flask, request, jsonify
import json
import os
import base64
import io
from PIL import Image

app = Flask(__name__)

# Load YOLO model
try:
    model = YOLO('best.pt')
except:
    model = None  # Handle missing model file

with open('class_names.json', 'r') as f:
    class_data = json.load(f)
    class_names = class_data['class_names']

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if model is None:
            return jsonify({'error': 'Model not loaded'}), 500
            
        if 'image_base64' not in request.json:
            return jsonify({'error': 'image_base64 required'}), 400
        
        # Decode base64 image
        image_data = base64.b64decode(request.json['image_base64'])
        image = Image.open(io.BytesIO(image_data))
        if image.mode in ('RGBA', 'LA', 'P'):
            image = image.convert('RGB')
        temp_path = f"temp_image_{os.getpid()}.jpg"
        image.save(temp_path)
        
        try:
            # Make prediction with YOLO
            results = model.predict(temp_path, imgsz=224, verbose=False)
            
            # Extract probabilities
            probs = results[0].probs.data.cpu().numpy()
            predicted_class = probs.argmax()
            confidence = float(probs[predicted_class])
            
            return jsonify({
                'predicted_class': class_names[predicted_class],
                'confidence': confidence,
                'all_probabilities': {class_names[i]: float(probs[i]) for i in range(len(class_names))}
            })
        finally:
            # Clean up temp file
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)