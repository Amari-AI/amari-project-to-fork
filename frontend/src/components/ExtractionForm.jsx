import React, { useState, useEffect } from 'react';

const ExtractionForm = ({ data }) => {
  const [formData, setFormData] = useState({});

  useEffect(() => {
    if (data) {
      try {
        const parsedData = typeof data === 'string' ? JSON.parse(data) : data;
        setFormData(parsedData);
      } catch (e) {
        console.error("Failed to parse data", e);
        setFormData({ raw_text: data });
      }
    }
  }, [data]);

  const handleChange = (key, value) => {
    setFormData({ ...formData, [key]: value });
  };

  return (
    <div className="p-4 bg-white shadow rounded-lg h-full overflow-auto">
      <h2 className="text-xl font-bold mb-4">Extracted Data</h2>
      <form>
        {Object.entries(formData).map(([key, value]) => (
          <div key={key} className="mb-4">
            <label className="block text-gray-700 text-sm font-bold mb-2 capitalize">
              {key.replace(/_/g, ' ')}
            </label>
            <input
              type="text"
              value={value || ''}
              onChange={(e) => handleChange(key, e.target.value)}
              className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            />
          </div>
        ))}
      </form>
    </div>
  );
};

export default ExtractionForm;
