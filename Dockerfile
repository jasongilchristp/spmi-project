# Stage 1: Build
FROM python:3.9-slim as build

# Set the working directory
WORKDIR /app

# Install dependencies needed to build the application
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Final
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy only necessary files from the build stage
COPY --from=build /root/.local /root/.local
COPY . /app

# Ensure the venv is active and application can run
ENV PATH="/root/.local/bin:$PATH"

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "app.py"]
