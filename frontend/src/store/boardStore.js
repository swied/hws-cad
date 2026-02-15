// frontend/src/store/boardStore.js
import { create } from 'zustand';
import axios from 'axios';

// Use the environment variable defined in docker-compose.yml, 
// falling back to localhost if not defined.
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
// const response = await axios.get(`${API_BASE_URL}/api/board/`);

const useBoardStore = create((set, get) => ({
  boardData: null,
  loading: false,
  
  fetchBoard: async () => {
    set({ loading: true });
    try {
      // Connects to Python Backend using the dynamic URL
      const response = await axios.get(`${API_BASE_URL}/api/board/`);
      set({ boardData: response.data, loading: false });
    } catch (error) {
      console.error("Failed to fetch board", error);
      set({ loading: false });
    }
  },

  updateDimensions: async (newDims) => {
    const current = get().boardData;
    if (!current) return;

    const updated = { 
      ...current, 
      dimensions: { ...current.dimensions, ...newDims } 
    };
    
    set({ boardData: updated });
    
    try {
      // Sync with backend using the dynamic URL
      await axios.post(`${API_BASE_URL}/api/board/update`, updated);
    } catch (error) {
      console.error("Failed to sync dimensions with backend", error);
    }
  }
}));

export default useBoardStore;