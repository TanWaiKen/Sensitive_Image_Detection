#!/bin/bash

# Set your GCP project ID and region
PROJECT_ID="your-project-id"
REGION="us-central1"
SERVICE_NAME="document-detection-api"

# Build and push Docker image to Google Container Registry
docker build -t gcr.io/$PROJECT_ID/$SERVICE_NAME .
docker push gcr.io/$PROJECT_ID/$SERVICE_NAME

# Deploy to Cloud Run
gcloud run deploy $SERVICE_NAME \
    --image gcr.io/$PROJECT_ID/$SERVICE_NAME \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --memory 2Gi \
    --cpu 2 \
    --timeout 300