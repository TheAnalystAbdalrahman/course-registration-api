FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Make scripts executable
RUN chmod +x start.sh entrypoint.py

# Expose port
EXPOSE 8000

# Run migrations and start server using Python entrypoint
# PORT is provided by Railway, defaults to 8000 for local
# Python entrypoint is more reliable than bash script on Railway
CMD ["python", "entrypoint.py"]

