import React, { useState } from 'react';
import './App.css';
import ModelConverter from './components/ModelConverter';
import OllamaLoader from './components/OllamaLoader';
 
 function App() {
   return (
     <div className="App">
       <header className="App-header">
         <h1>Orchestration Dashboard</h1>
       </header>
       <main>
         <section className="card">
           <h2>Service UIs</h2>
           <div className="button-container">
             <a href={import.meta.env.VITE_EASY_DATASET_URL} target="_blank" rel="noopener noreferrer">
               <button>Easy Dataset</button>
             </a>
             <a href={import.meta.env.VITE_LLAMA_FACTORY_URL} target="_blank" rel="noopener noreferrer">
               <button>LLaMA Factory</button>
             </a>
           </div>
         </section>
         <section className="card">
           <h2>TensorBoard Monitoring</h2>
           <iframe
             src={import.meta.env.VITE_TENSORBOARD_URL}
             title="TensorBoard"
             width="100%"
             height="600px"
             style={{ border: '1px solid #ccc' }}
           />
         </section>
         <section className="card">
           <ModelConverter />
         </section>
         <section className="card">
           <OllamaLoader />
         </section>
       </main>
     </div>
   );
 }

export default App;
