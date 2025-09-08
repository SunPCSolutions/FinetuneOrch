# Tech Context: End-to-End Fine-Tuning Workflow

## 1. Core Technologies

-   **Backend Framework:** Python with FastAPI.
-   **Frontend Framework:** Vite with React and TypeScript.
-   **Reverse Proxy:** Caddy.
-   **Dataset Management:** `easy-dataset` (Gradio-based application).
-   **Model Fine-Tuning:** `LLaMA-Factory` (Gradio-based application).
-   **Containerization:** Docker and Docker Compose.
-   **Model Conversion:** `llama.cpp`
-   **Model Serving:** Ollama

## 2. Development Environment

-   **Languages:** Python, TypeScript/JavaScript.
-   **Package Management:** `pip` for Python, `npm` for Node.js.
-   **Key Python Libraries (Backend):**
    -   `fastapi`
    -   `uvicorn`
    -   `python-dotenv`
    -   `docker` (for interacting with the Docker daemon)
-   **Key Frontend Libraries:**
    -   `react`, `react-dom`
    -   `axios` (for API calls)
-   **GPU:** A CUDA-enabled GPU is required for the `LLaMA-Factory` service.

## 3. Data Formats

-   **API Communication:** JSON is used for all API requests and responses between the React frontend and the FastAPI backend.
-   **Dataset/Model Formats:** Handled internally by `easy-dataset` and `LLaMA-Factory`.

## 4. Version Control

-   Git / GitHub will be used for source code management.

## 5. LangChain Chat Prompt Structure

-   **ChatPromptTemplate:** LangChain uses a `ChatPromptTemplate` to structure the input for chat models. This template typically includes placeholders for a `system` message and a `human` message.
-   **System Prompt:** The `system` message is used to provide instructions to the model (e.g., "You are a helpful assistant.").
-   **Human Prompt:** The `human` message is used to provide the user's input.
