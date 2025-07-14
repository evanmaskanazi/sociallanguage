FROM python:3.11-slim

# Install system dependencies for WeasyPrint and dos2unix
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-cffi \
    python3-brotli \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libharfbuzz0b \
    libpangocairo-1.0-0 \
    fonts-noto \
    fonts-noto-cjk \
    dos2unix \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application files
COPY . .

# Convert line endings and make startup script executable
RUN dos2unix startup.sh && chmod +x startup.sh

# Use startup script
CMD ["./startup.sh"]
