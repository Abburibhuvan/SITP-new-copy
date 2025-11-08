FROM python:3.11-slim

LABEL "language"="python"
LABEL "framework"="django"

WORKDIR /src

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy project files
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput || true

EXPOSE 8080

# Run gunicorn
CMD ["gunicorn", "TAU.wsgi:application", "--bind", "0.0.0.0:8080", "--log-file", "-", "--access-logfile", "-", "--workers", "2"]
