import requests
import json

def test_api(image_path, api_url):
    """Test the deployed API with an image"""
    
    # Health check
    health_response = requests.get(f"{api_url}/health")
    print(f"Health check: {health_response.json()}")
    
    # Prediction
    with open(image_path, 'rb') as f:
        files = {'image': f}
        response = requests.post(f"{api_url}/predict", files=files)
    
    if response.status_code == 200:
        result = response.json()
        print(f"Prediction: {result['predicted_class']}")
        print(f"Confidence: {result['confidence']:.4f}")
        print("All probabilities:")
        for class_name, prob in result['all_probabilities'].items():
            print(f"  {class_name}: {prob:.4f}")
    else:
        print(f"Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    # Replace with your deployed API URL and test image path
    API_URL = "https://your-service-url"
    IMAGE_PATH = "path/to/test/image.jpg"
    
    test_api(IMAGE_PATH, API_URL)