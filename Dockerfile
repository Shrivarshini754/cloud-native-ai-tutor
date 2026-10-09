FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Force Uvicorn to bind to 0.0.0.0 so Render can route external traffic
CMD ["uvicorn", "backend:app", "--host", "0.0.0.0", "--port", "8000"]