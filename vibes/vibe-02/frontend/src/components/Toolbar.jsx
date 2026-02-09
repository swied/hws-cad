// frontend/src/components/Toolbar.jsx
import React from 'react';
import axios from 'axios';
import useBoardStore from '../store/boardStore';

const Toolbar = () => {
  const { boardData } = useBoardStore();

  const handleExportGCode = async () => {
    try {
      const response = await axios.post(
        'http://localhost:8000/api/cam/generate/outline',
        { cutter_diameter: 12.7, feed_rate: 1500 },
        { responseType: 'blob' }
      );
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `${boardData.name || 'board'}_outline.cnc`);
      document.body.appendChild(link);
      link.click();
    } catch (err) {
      console.error("Export failed", err);
    }
  };

  return (
    <div className="toolbar" style={{ height: '50px', background: '#333', color: 'white', display: 'flex', alignItems: 'center', padding: '0 20px' }}>
      <span style={{ marginRight: '20px', fontWeight: 'bold' }}>BoardCAD Web</span>
      <button onClick={() => alert('New Board')}>New</button>
      <button onClick={() => alert('Open...')}>Open</button>
      <button onClick={() => alert('Save')}>Save</button>
      <div style={{ flex: 1 }}></div>
      <button onClick={handleExportGCode} style={{ background: 'orange', border: 'none', padding: '5px 15px' }}>
        Export G-Code
      </button>
    </div>
  );
};

export default Toolbar;