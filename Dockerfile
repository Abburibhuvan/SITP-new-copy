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

# Make start script executable
RUN chmod +x start.sh

EXPOSE 8080

# Run startup script
CMD ["./start.sh"]
