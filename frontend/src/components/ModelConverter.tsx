import React, { useState } from 'react';
import ModelSelector from './ModelSelector';
import ConversionForm from './ConversionForm';

const ModelConverter: React.FC = () => {
    const [selectedModel, setSelectedModel] = useState<string>('');

    return (
        <div>
            <h2>Model Converter and Loader</h2>
            <ModelSelector selectedModel={selectedModel} setSelectedModel={setSelectedModel} />
            {selectedModel && <ConversionForm selectedModel={selectedModel} />}
        </div>
    );
};

export default ModelConverter;