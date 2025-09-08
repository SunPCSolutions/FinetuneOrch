import React, { useState } from 'react';
import { convertAndLoadModel } from '../services/api';

interface ConversionFormProps {
    selectedModel: string;
}

const ConversionForm: React.FC<ConversionFormProps> = ({ selectedModel }) => {
    const [useLegacyFormat, setUseLegacyFormat] = useState<boolean>(true);
    const [newModelName, setNewModelName] = useState<string>('');
    const [systemPrompt, setSystemPrompt] = useState<string>('You are a helpful assistant.');
    const [baseModelPath, setBaseModelPath] = useState<string>('');
    const [conversionStatus, setConversionStatus] = useState<string>('');

    const handleConvertAndLoad = async () => {
        if (selectedModel) {
            setConversionStatus(`Converting and loading ${selectedModel}...`);
            try {
                const response = await convertAndLoadModel(
                    selectedModel,
                    baseModelPath,
                    useLegacyFormat,
                    newModelName,
                    systemPrompt
                );
                setConversionStatus(response.message);
            } catch (error: any) {
                setConversionStatus(`Error: ${error.response?.data?.detail || error.message}`);
            }
        }
    };

    return (
        <div>
            <div>
                <label>New Ollama Model Name:</label>
                <input
                    type="text"
                    value={newModelName}
                    onChange={(e) => setNewModelName(e.target.value)}
                    placeholder="e.g., llama3.2:new"
                />
            </div>
            <div>
                <label>Base Model Path:</label>
                <input
                    type="text"
                    value={baseModelPath}
                    onChange={(e) => setBaseModelPath(e.target.value)}
                    placeholder="e.g., unsloth/llama-3.2-3b-instruct"
                />
            </div>
            <div>
                <input
                    type="checkbox"
                    checked={useLegacyFormat}
                    onChange={(e: React.ChangeEvent<HTMLInputElement>) => setUseLegacyFormat(e.target.checked)}
                />
                <label>Use Legacy Format</label>
            </div>
            <div>
                <label>System Prompt:</label>
                <textarea
                    value={systemPrompt}
                    onChange={(e) => setSystemPrompt(e.target.value)}
                    rows={4}
                    style={{ width: '100%', marginTop: '5px' }}
                />
            </div>
            <button onClick={handleConvertAndLoad} disabled={!selectedModel}>Convert and Load</button>
            {conversionStatus && <p>{conversionStatus}</p>}
        </div>
    );
};

export default ConversionForm;