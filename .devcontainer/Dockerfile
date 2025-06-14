FROM python:3.11

# Install Node.js
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /workspace

# Copy and install Python dependencies
COPY api/requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy and install Node.js dependencies
COPY frontend/package*.json frontend/.npmrc /tmp/frontend/
WORKDIR /tmp/frontend
RUN npm install --legacy-peer-deps

# Go back to workspace
WORKDIR /workspace

# Keep container running
CMD ["sleep", "infinity"]
