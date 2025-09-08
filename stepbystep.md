# Step-by-Step Guide to Fine-Tuning a Model

This guide will walk you through the complete process of preparing a dataset, fine-tuning a language model using LLaMA-Factory, and making it available for use with Ollama, all orchestrated through the main dashboard.

---

### Step 1: Prepare Your Dataset and Model

Before you can fine-tune, you need a dataset in the correct format and the base model.

**A. Create Your JSONL Dataset**

LLaMA-Factory requires datasets to be in JSONL format, where each line is a separate JSON object.

*   **Option 1: Use `easy-dataset` (Recommended for new datasets)**
    1.  Launch the services (`docker compose up`).
    2.  Open the main dashboard and click the link to the `easy-dataset` UI.
    3.  Use its interface to create, label, and export your dataset. Ensure it is saved in the `shared_data` directory.

**B. Register Your Dataset**

To make your dataset visible in the LLaMA-Factory UI, you must add an entry for it in the `data/dataset_info.json` file.

1.  Open the `data/dataset_info.json` file.
2.  Add a new JSON object for your dataset. The key will be the name that appears in the UI.

**C. Obtain the Base Model**

You have two options to get the base model:

*   **Option 1: Direct Download in LLaMA-Factory (Recommended)**
    1.  Launch the services (`docker compose up`).
    2.  Open the LLaMA-Factory UI.
    3.  In the "Model name" field, enter the full Hugging Face repository ID (e.g., `unsloth/llama-3-8b-instruct-bnb-4bit`).
    4.  LLaMA-Factory will attempt to download the model directly.
    5.  **If this fails** due to network issues or repository access problems, proceed to Option 2.

*   **Option 2: Manual `git clone` (Fallback)**
    To ensure a reliable workflow and avoid network issues, you can manually download the model.
    1.  Open a terminal in the project's root directory.
    2.  Run the following `git` command to clone the model into the `./models` directory:
        ```bash
        git clone https://huggingface.co/unsloth/llama-3-8b-instruct-bnb-4bit models/unsloth/llama-3-8b-instruct-bnb-4bit
        ```

---

### Step 2: Launch the Services

With the data and model ready, start the entire application stack.

1.  In your terminal, run:
    ```bash
    docker compose up --build -d
    ```
2.  Open your web browser and navigate to the main orchestration dashboard (usually `http://localhost:3000`).

---

### Step 3: Configure the Fine-Tuning Job

1.  From the main dashboard, click the link to open the **LLaMA-Factory UI**.
2.  Set the following parameters carefully:
    *   **Model name**: If you used **Option 1 (Direct Download)**, select the downloaded model from the dropdown. If you used **Option 2 (Manual `git clone`)**, select **`Custom`** from the dropdown menu.
    *   **Model path**: If you selected **`Custom`**, enter the path to the model *inside the container*:
        ```
        /app/models/unsloth/llama-3-8b-instruct-bnb-4bit
        ```
    *   **Dataset**: Select your dataset from the dropdown.
    *   **Finetuning method**: `lora`
    *   **Extra configurations**: Select `TensorBoard` from the dropdown menu to enable monitoring.

---

### Step 4: Start and Monitor Fine-Tuning

1.  Once all parameters are set, click the **Start** button.
2.  The fine-tuning process will begin. You can monitor the progress in two ways:
    *   **LLaMA-Factory UI:** Watch the logs and the **Loss graph**. A downward-trending loss curve indicates that the model is learning successfully.
    *   **TensorBoard:** Return to the main dashboard and view the **TensorBoard Monitoring** section for more detailed metrics.

---

### Step 5: Convert and Load the Model into Ollama

After the fine-tuning job is complete, the final step is to convert the model and load it into Ollama.

1.  Return to the main **Orchestration Dashboard**.
2.  Navigate to the **Model Converter** section.
3.  Select your newly fine-tuned model from the list.
4.  In the **Base Model Path** field, enter the **Hugging Face repository ID** of the base model (e.g., `unsloth/Llama-3.2-3B-Instruct`). **Do not use the local file path.**
5.  Give your new model a name and a system prompt.
6.  Click the **Convert and Load Model** button. The backend will handle merging the adapter, converting the model to GGUF, and loading it into Ollama.