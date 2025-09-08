import axios from 'axios';

const apiClient = axios.create({
  baseURL: '/', // All requests are proxied by Caddy
});

export const getFinetunedModels = async () => {
  try {
    const response = await apiClient.get('/models/finetuned');
    return response.data.models || [];
  } catch (error) {
    console.error('Error fetching fine-tuned models:', error);
    throw error;
  }
};

export const getOllamaModels = async () => {
  try {
    const response = await apiClient.get('/models/ollama');
    return response.data.models || [];
  } catch (error) {
    console.error('Error fetching Ollama models:', error);
    throw error;
  }
};

export const convertAndLoadModel = async (
  selectedModel: string,
  baseModelPath: string,
  useLegacyFormat: boolean,
  newModelName: string,
  systemPrompt: string
) => {
  try {
    const response = await apiClient.post(`/models/convert-and-load/${selectedModel}`, {
      base_model_path: baseModelPath,
      use_legacy_format: useLegacyFormat,
      new_model_name: newModelName || `${selectedModel}-finetuned`,
      system_prompt: systemPrompt,
    });
    return response.data;
  } catch (error) {
    console.error('Error converting and loading model:', error);
    throw error;
  }
};