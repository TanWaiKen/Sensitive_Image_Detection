import requests
import base64
import json

def test_base64_api(image_path, api_url):
    """Test API with base64 encoded image"""
    
    # Encode image to base64
    with open(image_path, 'rb') as f:
        image_data = base64.b64encode(f.read()).decode('utf-8')
    
    # Send POST request with base64 data
    payload = {'image_base64': image_data}
    response = requests.post(f"{api_url}/predict", json=payload)
    
    if response.status_code == 200:
        result = response.json()
        print(f"Prediction: {result['predicted_class']}")
        print(f"Confidence: {result['confidence']:.4f}")
    else:
        print(f"Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    API_URL = "http://127.0.0.1:8080"
    IMAGE_PATH = r"C:\Users\tanwa\source\repos\Huawei ML\pavilion_kl.png"
    
    test_base64_api(IMAGE_PATH, API_URL)