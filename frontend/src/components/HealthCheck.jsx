import React, { useState } from 'react';
import axios from 'axios';

const HealthCheck = () => {
  const [checking, setChecking] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleHealthCheck = async () => {
    setChecking(true);
    setError(null);
    setResult(null);

    try {
      const response = await axios.get('http://localhost:8000/health-check/openai');
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to connect to OpenAI API');
      console.error(err);
    } finally {
      setChecking(false);
    }
  };

  return (
    <div className="p-4 bg-white shadow rounded-lg">
      <h2 className="text-xl font-bold mb-4">OpenAI Health Check</h2>
      <button
        onClick={handleHealthCheck}
        disabled={checking}
        className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 disabled:bg-gray-400 transition-colors"
      >
        {checking ? 'Checking...' : 'Test OpenAI Connection'}
      </button>
      
      {result && (
        <div className="mt-4 p-3 bg-green-50 border border-green-200 rounded">
          <p className="text-green-800 font-semibold">✓ {result.message}</p>
          <p className="text-sm text-green-700 mt-1">Model: {result.model}</p>
          <p className="text-sm text-green-700">Response: {result.response}</p>
        </div>
      )}
      
      {error && (
        <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded">
          <p className="text-red-800 font-semibold">✗ Connection Failed</p>
          <p className="text-sm text-red-700 mt-1">
            {typeof error === 'object' ? error.message : error}
          </p>
          {typeof error === 'object' && error.error && (
            <p className="text-xs text-red-600 mt-1 font-mono">{error.error}</p>
          )}
        </div>
      )}
    </div>
  );
};

export default HealthCheck;
