# Use Python 3.11 slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    gcc \
    python3-dev \
    musl-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create startup script that handles everything at runtime
RUN echo '#!/bin/bash\n\
set -e\n\
echo "Collecting static files..."\n\
python manage.py collectstatic --noinput || echo "Static files collection failed, continuing..."\n\
echo "Running migrations..."\n\
python manage.py migrate --noinput || echo "Migrations failed, continuing..."\n\
echo "Starting server on port ${PORT:-8000}..."\n\
exec gunicorn esports_platform.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 3 --timeout 120 --log-file - --access-logfile - --error-logfile -\n\
' > /app/start.sh && chmod +x /app/start.sh

# Expose port
EXPOSE $PORT

# Start the application
CMD ["/bin/bash", "/app/start.sh"]
