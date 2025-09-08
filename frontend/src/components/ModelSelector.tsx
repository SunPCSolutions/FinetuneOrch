import React, { useState, useEffect } from 'react';
import { getFinetunedModels } from '../services/api';

interface ModelSelectorProps {
    selectedModel: string;
    setSelectedModel: (model: string) => void;
}

const ModelSelector: React.FC<ModelSelectorProps> = ({ selectedModel, setSelectedModel }) => {
    const [models, setModels] = useState<string[]>([]);
    const [loading, setLoading] = useState<boolean>(true);

    useEffect(() => {
        const fetchModels = async () => {
            try {
                const finetunedModels = await getFinetunedModels();
                setModels(finetunedModels);
            } catch (error) {
                // The error is already logged in the api service
            } finally {
                setLoading(false);
            }
        };
        fetchModels();
    }, []);

    if (loading) {
        return <div>Loading models...</div>;
    }

    return (
        <select onChange={(e: React.ChangeEvent<HTMLSelectElement>) => setSelectedModel(e.target.value)} value={selectedModel}>
            <option value="">Select a model</option>
            {models && models.map((model: string) => (
                <option key={model} value={model}>{model.replace("::", " / ")}</option>
            ))}
        </select>
    );
};

export default ModelSelector;