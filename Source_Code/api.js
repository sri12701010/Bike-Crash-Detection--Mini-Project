import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8001/api",
});

export const uploadSensorData = (payload) => api.post("/sensor/upload", payload);
export const predictCrash = (payload) => api.post("/predict", payload);
export const sendAlert = (payload) => api.post("/alert", payload);
export const getRecentSensorData = (limit = 8) => api.get(`/sensor/recent?limit=${limit}`);

export default api;
