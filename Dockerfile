FROM python:3.10-slim

WORKDIR /app

# Copy files first
COPY requirements.txt .
COPY app.py .
COPY templates/ templates/
# COPY database.db .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
