// frontend/src/components/Controls.jsx
import React from 'react';
import useBoardStore from '../store/boardStore';

const Controls = () => {
  const { boardData, updateDimensions } = useBoardStore();

  if (!boardData) return <div>Loading...</div>;

  const handleChange = (e) => {
    const { name, value } = e.target;
    updateDimensions({ [name]: parseFloat(value) });
  };

  return (
    <div className="controls">
      <h3>Dimensions</h3>
      <div className="input-group">
        <label>Length (cm)</label>
        <input 
          type="number" 
          name="length" 
          value={boardData.dimensions.length} 
          onChange={handleChange} 
        />
      </div>
      <div className="input-group">
        <label>Width (cm)</label>
        <input 
          type="number" 
          name="width" 
          value={boardData.dimensions.width} 
          onChange={handleChange} 
        />
      </div>
      <div className="input-group">
        <label>Thickness (cm)</label>
        <input 
          type="number" 
          name="thickness" 
          value={boardData.dimensions.thickness} 
          onChange={handleChange} 
        />
      </div>
    </div>
  );
};

export default Controls;