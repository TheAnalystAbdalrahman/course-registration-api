FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Make startup script executable
RUN chmod +x start.sh

# Expose port
EXPOSE 8000

# Run migrations and start server using startup script
# PORT is provided by Railway, defaults to 8000 for local
# Use shell form to ensure proper error handling
CMD ["/bin/bash", "-c", "./start.sh"]

