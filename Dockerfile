# ==========================================
# Stage 1: Build Vue Frontend
# ==========================================
FROM node:18-alpine AS frontend-builder
WORKDIR /app/frontend

# Install dependencies
COPY frontend/package*.json ./
RUN npm ci

# Copy source and build
COPY frontend/ ./
RUN npm run build

# ==========================================
# Stage 2: Final Production Container
# ==========================================
FROM python:3.11-slim
WORKDIR /app

# Install Redis Server and required packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    redis-server \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy compiled frontend from Stage 1
COPY --from=frontend-builder /app/frontend/dist /app/frontend/dist

# Copy backend files
COPY backend /app/backend

# Install python dependencies + production server (gunicorn)
WORKDIR /app/backend
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn

# Copy entrypoint startup script
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Set environment variables for production
ENV FLASK_ENV=production
ENV PORT=7860
ENV PYTHONUNBUFFERED=1

EXPOSE 7860

CMD ["/app/entrypoint.sh"]
