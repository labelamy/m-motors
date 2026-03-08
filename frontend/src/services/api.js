import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8000",
});

API.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const getToken = () => {
  const token = localStorage.getItem("token");
  if (!token) return null;

  // On peut aussi décoder le token pour vérifier sa validité (optionnel)
  // Ici on se contente de vérifier qu'il existe
  return token;
};

export const logout = () => {
  localStorage.removeItem("token");
  localStorage.removeItem("currentUser");
};

export default API;