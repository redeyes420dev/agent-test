import React, { useState } from 'react';
import './App.css';

function App() {
  const [requirements, setRequirements] = useState('');
  const [code, setCode] = useState('');
  const [documentation, setDocumentation] = useState('');
  const [tests, setTests] = useState('');

  const handleGenerateCode = async () => {
    const response = await fetch('http://localhost:8000/generate_code', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ requirements }),
    });

    const data = await response.json();
    setCode(data.code);
    setDocumentation(data.documentation);
    setTests(data.tests);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Coding Agent</h1>
        <textarea
          value={requirements}
          onChange={(e) => setRequirements(e.target.value)}
          placeholder="Enter requirements here"
          rows="10"
          cols="50"
        />
        <button onClick={handleGenerateCode}>Generate Code</button>
        {code && (
          <div>
            <h2>Generated Code</h2>
            <pre>{code}</pre>
          </div>
        )}
        {documentation && (
          <div>
            <h2>Documentation</h2>
            <pre>{documentation}</pre>
          </div>
        )}
        {tests && (
          <div>
            <h2>Tests</h2>
            <pre>{tests}</pre>
          </div>
        )}
      </header>
    </div>
  );
}

export default App;
