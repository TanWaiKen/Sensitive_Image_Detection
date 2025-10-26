FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY model_best.pt .
COPY HMS_ML/class_names.json .
COPY app.py .

EXPOSE 8080

CMD ["python", "app.py"]