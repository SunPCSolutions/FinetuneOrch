# Base image with PyTorch and CUDA support
FROM pytorch/pytorch:2.7.1-cuda12.8-cudnn9-runtime

# Set environment variables to prevent interactive prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# Update package lists and install git
RUN apt-get update && \
    apt-get install -y git build-essential && \
    rm -rf /var/lib/apt/lists/*

# Upgrade torch and torchvision
RUN pip install --upgrade torch torchvision

# Set the working directory
WORKDIR /app

# Clone the LLaMA-Factory repository from GitHub
# Using --depth 1 for a shallow clone to reduce image size
RUN git clone --depth 1 https://github.com/hiyouga/LLaMA-Factory.git .

# Install the Python dependencies using pip
# Using --no-cache-dir to keep the image layer smaller
RUN pip install --no-cache-dir -r requirements.txt tensorboard


# Install LLaMA-Factory from source
RUN pip install .

# Install bitsandbytes for quantization
RUN pip install bitsandbytes>=0.39.0

# Force upgrade peft and huggingface_hub at the end to override any version conflicts
RUN pip install --upgrade huggingface_hub && pip install "peft>=0.14.0,<=0.15.2"

# Create and set permissions for the cache and saves directories
RUN mkdir -p /app/cache /app/saves && \
    chown -R 1000:1000 /app/cache /app/saves

# Define data volumes for caching, datasets, and outputs
VOLUME [ "/root/.cache/huggingface", "/app/shared_data", "/app/output", "/app/cache" ]

# Expose the default port for the Gradio web UI
EXPOSE 7860

# Set a default command to launch the web UI
# This can be overridden in docker-compose.yml if needed
# Set a default command to launch the web UI
# Set a default command to launch the web UI
CMD ["llamafactory-cli", "webui"]