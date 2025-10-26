FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY class_names.json .
COPY app.py .

# Create placeholder for model file
RUN echo "Model file should be mounted or copied separately" > best.pt

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]