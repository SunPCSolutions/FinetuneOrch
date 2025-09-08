# Implementation Plan: Build `llama.cpp` with CUDA 12.8

## 1. Objective

To build a custom `llama.cpp` Docker image that utilizes the same CUDA version as the `llama-factory` service (CUDA 12.8) and to integrate it correctly into the `docker-compose` stack.

## 2. Diagnosis

- **Core Requirement:** The `llama.cpp` container must use CUDA 12.8.
- **Confirmation:** The root `Dockerfile` correctly uses `pytorch/pytorch:2.7.0-cuda12.8-cudnn9-devel` as its base image. This means the correct CUDA version is already specified at the foundational layer.
- **Primary Blocker:** The build process is failing silently due to a missing dependency. The `Dockerfile` lacks the `build-essential` package, which provides the C++ compiler (`g++`) required by `cmake` to compile the `llama.cpp` source code.
- **Secondary Blocker:** The `docker-compose.yml` file is pointing the `llama-cpp` service to a pre-built public image, completely bypassing the local `Dockerfile` where the correct CUDA version is defined.

## 3. Implementation Steps

The following steps will resolve both blockers, enabling a successful build with the correct CUDA version.

### Step 1: Update `Dockerfile` to Include Compiler

Add the `build-essential` package to the `apt-get install` command. This will provide the necessary C++ compiler for the build.

**File to Edit:** `Dockerfile`

**Change:**
```diff
--- a/Dockerfile
+++ b/Dockerfile
@@ -6,8 +6,9 @@
 ENV DEBIAN_FRONTEND=noninteractive
 RUN apt-get update && \
     apt-get install -y --no-install-recommends \
+    build-essential \
     git \
     wget \
     cmake \
     python3-pip \
     && apt-get clean && rm -rf /var/lib/apt/lists/*
```

### Step 2: Update `docker-compose.yml` to Use Local Build

Modify the `llama-cpp` service to build from the local root `Dockerfile`. This ensures our custom, CUDA 12.8-based image is used.

**File to Edit:** `docker-compose.yml`

**Change:**
```diff
--- a/docker-compose.yml
+++ b/docker-compose.yml
@@ -68,8 +68,10 @@
       - docknet
 
   llama-cpp:
-    image: ghcr.io/ggml-org/llama.cpp:full-cuda
+    build:
+      context: .
+      dockerfile: Dockerfile
     deploy:
       resources:
         reservations:
```

## 4. Execution and Verification

1.  Apply the changes detailed above to `Dockerfile` and `docker-compose.yml`.
2.  From the project root, run the following command to build and start the `llama-cpp` service:
    ```bash
    docker compose up --build -d llama-cpp
    ```
3.  Verify the container is running using `docker ps`. The `finetune-llama-cpp-1` container should now be up and stable, having been built with the correct CUDA 12.8 environment.