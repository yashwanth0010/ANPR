FROM python:3.11-slim

WORKDIR /app

RUN apt-get update

# Copy dependencies first
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy app code
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Start FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
