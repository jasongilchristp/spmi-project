# Stage 1: Build
FROM python:3.9-slim as build

# Set the working directory
WORKDIR /app

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Copy the current directory contents into the container at /app
COPY . /app

# Create a virtual environment
RUN python -m venv venv

# Activate the virtual environment and install dependencies
RUN . venv/bin/activate && pip install --no-cache-dir -r requirements.txt

# Stage 2: Final
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the virtual environment from the build stage
COPY --from=build /app/venv /app/venv
COPY . /app

# Ensure the virtual environment is activated
ENV PATH="/app/venv/bin:$PATH"

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "app.py"]
# Allocate Swap Space
RUN fallocate -l 2G /swapfile && \
    chmod 600 /swapfile && \
    mkswap /swapfile && \
    swapon /swapfile