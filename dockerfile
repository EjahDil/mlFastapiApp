# Use an official lightweight Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install system dependencies (for some Python packages)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first (to leverage Docker cache)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Make a directory for models inside the container
RUN mkdir -p /models

# # Set environment variable
# ENV API_KEY="secretkey123"

# --- INSECURE: bake secret into a file inside the image ---
# RUN echo "secretkey123" > /app/secret_key.txt && \
# chmod 600 /app/secret_key.txt && \
# ls -l /app/secret_key.txt

# Create a non-root user and switch to it
RUN useradd -m -u 1000 mlappuser && chown -R mlappuser:mlappuser /app 
USER mlappuser

# Expose FastAPI default port
EXPOSE 8000

# Run the FastAPI app with uvicorn
CMD ["uvicorn", "mainls:appls", "--host", "0.0.0.0", "--port", "8000"]


