# Implementation Plan: End-to-End Fine-Tuning Workflow

## 1. Objective

To create a seamless, end-to-end workflow for fine-tuning language models, from dataset creation to a GGUF-converted model ready for use in Ollama, all orchestrated through a unified frontend.

## 2. Architectural Changes

### 2.1. Shared Volume Consolidation

The `docker-compose.yml` file will be modified to use a single, shared volume for `data`, `output`, and `saves`. This will eliminate the need to copy files between the `easy-dataset`, `llama-factory`, and `llama-cpp` containers.

**File to Edit:** `docker-compose.yml`

**Changes:**

```diff
--- a/docker-compose.yml
+++ b/docker-compose.yml
@@ -48,11 +48,11 @@
       - "7002:7860"
       - "7003:6006"
     volumes:
-      - ./data:/app/shared_data
+      - shared_data:/app/shared_data
       - ./hf_cache:/root/.cache/huggingface
-      - ./output:/app/output
-      - ./saves:/app/saves
+      - shared_data:/app/output
+      - shared_data:/app/saves
       - llama_factory_cache:/app/cache
     environment:
       - HF_TOKEN=${HF_TOKEN}
@@ -65,7 +65,7 @@
     ports:
       - "7001:1717"
     volumes:
-      - ./data:/app/local-db
+      - shared_data:/app/local-db
     restart: unless-stopped
     networks:
       - docknet
@@ -85,7 +85,7 @@
               count: all
               capabilities: [gpu]
     volumes:
-      - ./output:/models
+      - shared_data:/models
     command: --server -m /models/your-model.gguf
     networks:
       - docknet
@@ -95,6 +95,7 @@
   uploads:
   caddy_data:
   llama_factory_cache:
+  shared_data:

 networks:
   docknet:
```

### 2.2. Frontend UI Enhancements

A new section will be added to the frontend UI to manage the GGUF conversion and Ollama integration. This will involve creating new React components and updating the existing UI.

**New Components:**

*   `src/components/ModelConverter.tsx`: A new component to list fine-tuned models, trigger GGUF conversion, and display the status.
*   `src/components/OllamaLoader.tsx`: A new component to list GGUF models, create a Modelfile, and load the model into Ollama.

**UI Changes:**

*   The main `App.tsx` file will be updated to include the new `ModelConverter` and `OllamaLoader` components.

### 2.3. Backend API Extension

New API endpoints will be added to the backend to support the new frontend features.

**File to Edit:** `backend/main.py`

**New Endpoints:**

*   `GET /api/models/finetuned`: List all fine-tuned models in the `output` directory.
*   `POST /api/models/convert`: Trigger the GGUF conversion process for a selected model.
*   `GET /api/models/gguf`: List all GGUF-converted models.
*   `POST /api/models/load`: Create a Modelfile and load the selected GGUF model into Ollama.

## 3. Implementation Steps

1.  **Apply the `docker-compose.yml` changes** to consolidate the shared volumes.
2.  **Implement the new frontend components** (`ModelConverter.tsx` and `OllamaLoader.tsx`) and update the main `App.tsx` file.
3.  **Implement the new backend API endpoints** in `backend/main.py`.
4.  **Test the end-to-end workflow** to ensure that a model can be fine-tuned, converted to GGUF, and loaded into Ollama through the UI.