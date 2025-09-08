# System Patterns: End-to-End Fine-Tuning Workflow

## 1. Overall Architecture

The system is designed as a simple, service-oriented architecture where a Caddy reverse proxy directs traffic to the appropriate backend service. This provides a single entry point for the user and simplifies the overall network configuration.

```mermaid
graph TD
    subgraph "User's Browser"
        A[React Dashboard UI]
    end

    subgraph "Application Server (Docker Compose)"
        B[Caddy Reverse Proxy]
        C[Frontend Service (Vite)]
        D[Backend Service (FastAPI)]
        E[easy-dataset Service]
        F[LLaMA-Factory Service]
        G[llama.cpp Service]
        H[Ollama Service]
        I[TensorBoard Service]
    end

    A -- HTTPS --> B
    B -- /api/* --> D
    B -- /* --> C
    
    A -- Direct Link --> E[easy-dataset UI]
    A -- Direct Link --> F[LLaMA-Factory UI]
    A -- Direct Link --> I[TensorBoard UI]
    D -- Orchestrates --> F
    F -- Merges LoRA --> G
    G -- Converts to GGUF --> H
    H -- Serves Model --> A

    style A fill:#cde4ff
    style B fill:#d5e8d4
    style C fill:#ffe6cc
    style D fill:#f8cecc
    style E fill:#e1d5e7
    style F fill:#e1d5e7
    style I fill:#dae8fc
```

## 2. Core Components

-   **Caddy Reverse Proxy:** The single entry point for all traffic. It routes API requests to the backend and all other requests to the frontend service.
-   **Frontend Service (Vite):** A Single Page Application (SPA) that serves as the main orchestration dashboard. It is served by the Vite development server.
-   **Backend Service (FastAPI):** A lightweight proxy and status monitor. Its primary role is to expose an API that the frontend can poll for service status and logs. It also orchestrates the model merging, conversion, and loading processes.
-   **easy-dataset Service:** A standalone, containerized Gradio application for dataset preparation. The user interacts with its UI directly.
-   **LLaMA-Factory Service:** A standalone, containerized Gradio application for model fine-tuning. The user interacts with its UI directly. It is also used by the backend to merge LoRA adapters into base models.
-   **llama.cpp Service:** A containerized "toolbox" service. It remains in a waiting state until the Backend Service executes a command within it (e.g., `docker exec`) to perform on-demand tasks like converting models to GGUF format.
-   **Ollama Service:** A service for running large language models. Orchestrated by the Backend Service for loading GGUF models.
-   **TensorBoard Service:** A standalone service for visualizing training metrics. It reads logs from the `./saves` directory, which is shared with the `LLaMA-Factory` service.

## 3. Key Technical Decisions & Patterns

-   **Reverse Proxy Architecture:** Using Caddy as a reverse proxy simplifies the system by providing a single entry point and abstracting the internal service addresses.
-   **Service Orchestration over Abstraction:** The dashboard does not abstract the functionality of the core tools. Instead, it orchestrates their deployment and provides a centralized view, preserving the power and flexibility of the underlying applications.
-   **Containerization:** Using Docker and Docker Compose remains critical. It ensures that the specific environments and dependencies for the dashboard, `easy-dataset`, and `LLaMA-Factory` are managed consistently and reliably.
-   **Robust Model Workflow:** The system now includes robust steps for merging LoRA adapters, converting to GGUF, and loading into Ollama, addressing various pathing and dependency challenges.
