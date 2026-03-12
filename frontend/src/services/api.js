import axios from "axios";

const API = axios.create({
  baseURL: import.meta.env.VITE_API_URL
});

API.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
  }, (error) => {
  return Promise.reject(error);
});

export const getToken = () => localStorage.getItem("token");


export const logout = () => {
  localStorage.removeItem("token");
  localStorage.removeItem("currentUser");
};

export default API;