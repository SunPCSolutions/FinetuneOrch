import os
import tarfile
import logging
import time
from io import BytesIO
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import docker

# --- Configuration Constants ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Fine-Tuning Orchestration API",
    description="An API for orchestrating the fine-tuning, conversion, and loading of language models.",
    version="0.2.0",
)

SAVES_DIR = "/app/saves"
LLAMA_FACTORY_CONTAINER = os.getenv("LLAMA_FACTORY_CONTAINER", "finetune-llama-factory-1")
LLAMA_CPP_CONTAINER = os.getenv("LLAMA_CPP_CONTAINER", "finetune-llama-cpp-1")
OLLAMA_CONTAINER = os.getenv("OLLAMA_CONTAINER", "ollama")

# --- Pydantic Models ---
class ConvertAndLoadRequest(BaseModel):
    base_model_path: str
    use_legacy_format: bool
    new_model_name: str
    system_prompt: str

# --- Helper Functions ---
def _put_file_in_container(container, src_path, dest_path):
    """Helper to copy a file into a container, creating a tar archive in memory."""
    stream = BytesIO()
    with tarfile.open(fileobj=stream, mode='w') as tar:
        tar.add(src_path, arcname=os.path.basename(dest_path))
    stream.seek(0)
    container.put_archive(os.path.dirname(dest_path), stream)

def _get_container(client, container_name):
    """Gets a Docker container by name, raising an HTTPException if not found."""
    try:
        return client.containers.get(container_name)
    except docker.errors.NotFound:
        logger.error(f"Container not found: {container_name}")
        raise HTTPException(status_code=500, detail=f"Container '{container_name}' not found.")

def _merge_lora_adapter(client, base_model_path, container_adapter_path, container_merged_model_path):
    """Merges the LoRA adapter into the base model using llamafactory-cli."""
    logger.info("Step 1: Merging LoRA adapter...")
    llama_factory = _get_container(client, LLAMA_FACTORY_CONTAINER)
    merge_cmd = [
        "llamafactory-cli", "export",
        "--model_name_or_path", base_model_path,
        "--adapter_name_or_path", container_adapter_path,
        "--template", "default",
        "--export_dir", container_merged_model_path,
        "--export_size", "2",
        "--export_legacy_format", "False"
    ]
    exit_code, output = llama_factory.exec_run(merge_cmd)
    if exit_code != 0:
        error_message = f"Failed to merge LoRA adapter: {output.decode('utf-8')}"
        logger.error(error_message)
        raise RuntimeError(error_message)
    logger.info("Successfully merged LoRA adapter.")

def _convert_to_gguf(client, container_merged_model_path, container_gguf_path):
    """Converts the merged model to GGUF format."""
    logger.info("Step 2: Converting merged model to GGUF...")
    llama_cpp = _get_container(client, LLAMA_CPP_CONTAINER)
    base_model_for_conversion = container_merged_model_path.replace("/app/saves", "/saves")
    convert_cmd = [
        "python3", "convert_hf_to_gguf.py",
        base_model_for_conversion,
        "--outfile", container_gguf_path,
        "--outtype", "f16"
    ]
    exit_code, output = llama_cpp.exec_run(convert_cmd)
    if exit_code != 0:
        error_message = f"GGUF conversion failed: {output.decode('utf-8')}"
        logger.error(error_message)
        raise RuntimeError(error_message)
    logger.info("GGUF conversion successful.")

def _wait_for_gguf_file(host_gguf_model_path):
    """Waits for the GGUF file to become available on the host."""
    logger.info(f"Waiting for GGUF file at {host_gguf_model_path}...")
    max_wait_time = 30
    start_time = time.time()
    while not os.path.exists(host_gguf_model_path):
        if time.time() - start_time > max_wait_time:
            error_message = f"GGUF file not found at {host_gguf_model_path} after waiting."
            logger.error(error_message)
            raise FileNotFoundError(error_message)
        time.sleep(1)
    logger.info("GGUF file found.")

def _create_modelfile(host_modelfile_path, ollama_gguf_dest_path, system_prompt):
    """Creates the Modelfile for Ollama."""
    logger.info("Step 3: Creating Modelfile...")
    modelfile_content = f"""FROM ./{os.path.basename(ollama_gguf_dest_path)}
TEMPLATE \"\"\"
{{{{- if .System }}}}<|begin_of_text|><|start_header_id|>system<|end_header_id|>
{{{{ .System }}}}<|eot_id|>{{{{- end }}}}
<|start_header_id|>user<|end_header_id|>
{{{{ .Prompt }}}}<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>
{{{{ .Response }}}}<|eot_id|>
\"\"\"
SYSTEM \"\"\"{system_prompt}\"\"\"
"""
    with open(host_modelfile_path, "w") as f:
        f.write(modelfile_content)
    logger.info(f"Modelfile created at {host_modelfile_path}")

def _load_model_into_ollama(client, new_model_name, host_gguf_model_path, ollama_gguf_dest_path, host_modelfile_path, ollama_modelfile_dest_path):
    """Copies files to and creates the model in the Ollama container."""
    logger.info("Step 4: Loading model into Ollama...")
    ollama = _get_container(client, OLLAMA_CONTAINER)
    _put_file_in_container(ollama, host_gguf_model_path, ollama_gguf_dest_path)
    _put_file_in_container(ollama, host_modelfile_path, ollama_modelfile_dest_path)
    create_cmd = ["ollama", "create", new_model_name, "-f", ollama_modelfile_dest_path]
    exit_code, output = ollama.exec_run(create_cmd)
    if exit_code != 0:
        error_message = f"Ollama model creation failed: {output.decode('utf-8')}"
        logger.error(error_message)
        raise RuntimeError(error_message)
    logger.info(f"Successfully created Ollama model: {new_model_name}")

# --- Main Orchestration Logic ---
def _convert_and_load_model_sync(training_run_id: str, base_model_path: str, use_legacy_format: bool, new_model_name: str, system_prompt: str):
    """Main orchestration function to convert and load a single model."""
    client = docker.from_env()
    logger.info(f"Starting conversion for {training_run_id}")

    model_name, training_run = training_run_id.split("::")
    
    # Define paths
    host_model_path = os.path.join(SAVES_DIR, model_name)
    host_adapter_path = os.path.join(host_model_path, "lora", training_run)
    host_merged_model_path = os.path.join(host_model_path, "merged_model")
    host_gguf_model_path = os.path.join(SAVES_DIR, f"{new_model_name}.gguf")
    host_modelfile_path = os.path.join(SAVES_DIR, f"Modelfile.{new_model_name}")

    container_adapter_path = f"/app/saves/{model_name}/lora/{training_run}"
    container_merged_model_path = f"/app/saves/{model_name}/merged_model"
    container_gguf_path = f"/saves/{new_model_name}.gguf"
    ollama_modelfile_dest_path = f"/Modelfile.{new_model_name}"
    ollama_gguf_dest_path = f"/{new_model_name}.gguf"

    if not os.path.isdir(host_adapter_path):
        raise FileNotFoundError(f"Adapter not found at {host_adapter_path}")

    _merge_lora_adapter(client, base_model_path, container_adapter_path, container_merged_model_path)
    _convert_to_gguf(client, container_merged_model_path, container_gguf_path)
    _wait_for_gguf_file(host_gguf_model_path)
    _create_modelfile(host_modelfile_path, ollama_gguf_dest_path, system_prompt)
    _load_model_into_ollama(client, new_model_name, host_gguf_model_path, ollama_gguf_dest_path, host_modelfile_path, ollama_modelfile_dest_path)

# --- API Endpoints ---
@app.on_event("startup")
async def startup_event():
    """Ensure the saves directory exists on startup."""
    os.makedirs(SAVES_DIR, exist_ok=True)

@app.get("/")
async def root():
    return {"message": "Welcome to the Fine-Tuning Orchestration API"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/models/finetuned")
async def get_finetuned_models():
    """Lists valid, fine-tuned LoRA adapters from the saves directory."""
    valid_training_runs = []
    if not os.path.isdir(SAVES_DIR):
        return {"models": []}
    for model_folder in os.listdir(SAVES_DIR):
        model_path = os.path.join(SAVES_DIR, model_folder)
        if os.path.isdir(model_path):
            lora_dir = os.path.join(model_path, "lora")
            if os.path.isdir(lora_dir):
                for training_run in os.listdir(lora_dir):
                    run_path = os.path.join(lora_dir, training_run)
                    if os.path.isdir(run_path) and "adapter_config.json" in os.listdir(run_path):
                        valid_training_runs.append(f"{model_folder}::{training_run}")
    return {"models": valid_training_runs}

@app.get("/models/gguf")
async def get_gguf_models():
    """Lists all available GGUF models in the saves directory."""
    gguf_models = []
    if not os.path.isdir(SAVES_DIR):
        return {"models": []}
    for f in os.listdir(SAVES_DIR):
        if f.endswith(".gguf"):
            gguf_models.append({
                "filename": f,
                "model_name": f.replace(".gguf", "")
            })
    return {"models": gguf_models}

@app.get("/models/ollama")
async def get_ollama_models():
    """Lists all models currently available in Ollama."""
    try:
        client = docker.from_env()
        ollama = _get_container(client, OLLAMA_CONTAINER)
        exit_code, output = ollama.exec_run("ollama list")
        if exit_code != 0:
            raise RuntimeError(f"Failed to list Ollama models: {output.decode('utf-8')}")
        
        lines = output.decode('utf-8').strip().split('\n')
        model_lines = lines[1:]
        models = [line.split() for line in model_lines]
        return {"models": models}
    except Exception as e:
        logger.error(f"An unexpected error occurred in get_ollama_models: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An internal server error occurred.")

@app.post("/models/convert-and-load/{model_name}")
async def convert_and_load_model(model_name: str, request: ConvertAndLoadRequest):
    """Orchestrates the conversion and loading of a fine-tuned model."""
    try:
        _convert_and_load_model_sync(
            model_name, 
            request.base_model_path, 
            request.use_legacy_format, 
            request.new_model_name, 
            request.system_prompt
        )
        return {"message": f"Successfully converted and loaded model: {model_name}"}
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during conversion: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred in convert_and_load_model: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An internal server error occurred.")