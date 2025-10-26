# Sensitive Image Detection

A PyTorch-based document classification model that detects sensitive documents (ID cards, passports, driver licenses, bank cards) deployed on Google Cloud Platform.

## Model Classes
- Bank Card
- Driver License  
- ID Card
- Non-sensitive
- Passport

## Quick Start

### Local Testing
```bash
pip install -r requirements.txt
python app.py
```

### Deploy to GCP
```bash
# Update PROJECT_ID in deploy.sh
chmod +x deploy.sh
./deploy.sh
```

## API Usage

**Health Check:**
```bash
curl https://your-service-url/health
```

**Prediction:**
```bash
curl -X POST -F "image=@test.jpg" https://your-service-url/predict
```

**Response:**
```json
{
  "predicted_class": "id_card",
  "confidence": 0.9542,
  "all_probabilities": {
    "bank_card": 0.0123,
    "drvlic": 0.0089,
    "id_card": 0.9542,
    "non_sensitive": 0.0156,
    "passport": 0.0090
  }
}
```

## Files
- `app.py` - Flask API server
- `Dockerfile` - Container configuration
- `requirements.txt` - Python dependencies
- `deploy.sh` - GCP deployment script
- `class_names.json` - Model class definitions
- `model_best.pt` - Trained PyTorch model