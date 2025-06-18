# Multi-stage build for Next.js and Python app
FROM node:18-alpine AS nextjs-build

# Set working directory for Next.js
WORKDIR /frontend

# Copy Next.js package files
COPY frontend/package*.json ./
RUN npm ci --only=production

# Copy Next.js source code
COPY frontend/ .

# Build Next.js application
RUN npm run build

# Main application image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies including Node.js for running Next.js
RUN apt-get update && apt-get install -y \
    curl \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY api/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY api/ .
COPY dataset/ ./dataset/

# Copy built Next.js application from build stage
COPY --from=nextjs-build /frontend/.next ./frontend/.next
COPY --from=nextjs-build /frontend/public ./frontend/public
COPY --from=nextjs-build /frontend/package*.json ./frontend/
COPY --from=nextjs-build /frontend/node_modules ./frontend/node_modules
COPY frontend/next.config.ts ./frontend/

# Create a non-root user
RUN useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app
USER app

# Expose ports
EXPOSE 8000 3000

# Health check for both services
HEALTHCHECK --interval=30s --timeout=30s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health && curl -f http://localhost:3000 || exit 1

# Create startup script
USER root
RUN echo '#!/bin/bash\n\
cd /app\n\
uvicorn main:app --host 0.0.0.0 --port 8000 &\n\
cd /app/frontend\n\
npm start -- --port 3000 --hostname 0.0.0.0 &\n\
wait' > /app/start.sh && chmod +x /app/start.sh

USER app

# Run both applications
CMD ["/app/start.sh"]
