# Product Context: Fine-Tuning Orchestration Dashboard

## 1. Problem Space

While powerful, standalone fine-tuning tools like `LLaMA-Factory` and `easy-dataset` present a fragmented user experience. The user must manage separate processes, terminals, and logs, making the end-to-end workflow cumbersome and difficult to monitor. There is a need for a simple orchestration layer that unifies these tools into a single, observable system.

## 2. Solution Vision

This application provides a "mission control" dashboard for the fine-tuning process. It does not replace the core functionality of `easy-dataset` or `LLaMA-Factory`; instead, it wraps them in a simple, unified UI. The goal is to provide a seamless user experience by handling the lifecycle of these services, presenting their status and output in one place, and orchestrating the conversion and loading of fine-tuned models.

## 3. User Experience Goals

-   **Simplicity:** The user should be able to start the entire system with a single command.
-   **Centralized Control:** The dashboard should be the single source of truth for the status of all services.
-   **Clear Navigation:** The user should be easily able to navigate to the UIs of the underlying services (`easy-dataset`, `LLaMA-Factory`) to perform their tasks.
-   **Immediate Feedback:** The dashboard must provide real-time (or near-real-time) log streaming and status updates.

## 4. Key Assumptions

-   Users are familiar with the basic concepts of fine-tuning and the purpose of `LLaMA-Factory` and `easy-dataset`.
-   The primary value is in orchestration and monitoring, not in abstracting away the core tools themselves.
-   A containerized, `docker-compose`-based deployment is the most effective way to manage the multi-service environment.
