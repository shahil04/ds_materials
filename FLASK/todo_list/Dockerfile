# Use Python base image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port
EXPOSE 8080

# Run Flask in production using Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
