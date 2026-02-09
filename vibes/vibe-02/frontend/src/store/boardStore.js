// frontend/src/store/boardStore.js
import { create } from 'zustand';
import axios from 'axios';

const useBoardStore = create((set, get) => ({
  boardData: null,
  loading: false,
  
  fetchBoard: async () => {
    set({ loading: true });
    try {
      // Connects to Python Backend
      const response = await axios.get('http://localhost:8000/api/board/');
      set({ boardData: response.data, loading: false });
    } catch (error) {
      console.error("Failed to fetch board", error);
      set({ loading: false });
    }
  },

  updateDimensions: async (newDims) => {
    const current = get().boardData;
    const updated = { ...current, dimensions: { ...current.dimensions, ...newDims } };
    set({ boardData: updated });
    // Sync with backend
    await axios.post('http://localhost:8000/api/board/update', updated);
  }
}));

export default useBoardStore;