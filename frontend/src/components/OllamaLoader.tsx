import React, { useState, useEffect } from 'react';
import { getOllamaModels } from '../services/api';

const OllamaLoader: React.FC = () => {
    const [ollamaModels, setOllamaModels] = useState<string[]>([]);

    useEffect(() => {
        const fetchOllamaModels = async () => {
            try {
                const models = await getOllamaModels();
                setOllamaModels(models);
            } catch (error) {
                // The error is already logged in the api service
            }
        };

        fetchOllamaModels();
        const interval = setInterval(fetchOllamaModels, 5000); // Refresh every 5 seconds

        return () => clearInterval(interval); // Cleanup on component unmount
    }, []);

    return (
        <div>
            <h2>Loaded Ollama Models</h2>
            {ollamaModels.length > 0 ? (
                <ul>
                    {ollamaModels.map(model => (
                        <li key={model}>{model}</li>
                    ))}
                </ul>
            ) : (
                <p>No models loaded in Ollama.</p>
            )}
        </div>
    );
};

export default OllamaLoader;