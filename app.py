import torch
import torchvision.transforms as transforms
from PIL import Image
from flask import Flask, request, jsonify
import json
import io
import os

app = Flask(__name__)

# Load model and class names
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = torch.load('model_best.pt', map_location=device)
model.eval()

with open('class_names.json', 'r') as f:
    class_data = json.load(f)
    class_names = class_data['class_names']

# Image preprocessing
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        
        file = request.files['image']
        image = Image.open(io.BytesIO(file.read())).convert('RGB')
        
        # Preprocess image
        input_tensor = transform(image).unsqueeze(0).to(device)
        
        # Make prediction
        with torch.no_grad():
            outputs = model(input_tensor)
            probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
            predicted_class = torch.argmax(probabilities).item()
            confidence = probabilities[predicted_class].item()
        
        return jsonify({
            'predicted_class': class_names[predicted_class],
            'confidence': float(confidence),
            'all_probabilities': {class_names[i]: float(probabilities[i]) for i in range(len(class_names))}
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)