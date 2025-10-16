
# Step 1: Use the specified PyTorch base image
FROM pytorch/pytorch:2.7.0-cuda12.8-cudnn9-devel

# Step 2: System Dependencies & Basic Setup
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    git \
    wget \
    cmake \
    python3-pip \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install uv for better dependency management
RUN python3 -m pip install --no-cache-dir --upgrade pip
RUN pip install uv

# Step 3: Environment Variables
ENV MAX_JOBS=4
ENV HF_HOME=/workspace/.cache/huggingface
ENV TRANSFORMERS_CACHE=/workspace/.cache/huggingface/models
ENV PATH="/root/.local/bin:${PATH}"

# Step 4: Install Axolotl first (it will install compatible versions of dependencies)
WORKDIR /app
RUN git clone https://github.com/OpenAccess-AI-Collective/axolotl.git
WORKDIR /app/axolotl
RUN pip install --no-build-isolation -e .[flash-attn,deepspeed]

# Step 5: Install additional packages (will upgrade if needed)
RUN cat <<EOF > /tmp/requirements.txt
transformers==4.43.2
peft==0.15.2
huggingface_hub
datasets==2.20.0
accelerate==0.32.1
bitsandbytes==0.43.1
sentencepiece==0.2.0
protobuf==4.25.3
packaging==24.1
ninja==1.11.1.1
EOF

# Install packages with cache
RUN --mount=type=cache,target=/root/.cache/pip pip install --no-cache-dir -r /tmp/requirements.txt && rm /tmp/requirements.txt

# Step 7: Set up Workspace
WORKDIR /workspace
RUN mkdir -p /workspace/.cache/huggingface && \
    mkdir -p /data && \
    mkdir -p /config

# Step 8: Verify installation
RUN python3 -c "import torch; print(f'PyTorch version: {torch.__version__}'); print(f'CUDA available: {torch.cuda.is_available()}'); print(f'CUDA version from torch: {torch.version.cuda}'); print(f'cuDNN version from torch: {torch.backends.cudnn.version()}')"
RUN python3 -c "import transformers; import peft; import datasets; import accelerate; print('HF libs imported OK (bitsandbytes requires GPU at runtime)')"
RUN accelerate --version && axolotl --version || echo "Axolotl CLI not found or failed"

# Set default working directory
WORKDIR /workspace

# Default command
CMD ["bash"]
