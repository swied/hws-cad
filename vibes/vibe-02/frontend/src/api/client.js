// frontend/src/api/client.js
import axios from 'axios';

const apiClient = axios.create({
  // Use the env variable from docker-compose, fallback to localhost
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

export default apiClient;