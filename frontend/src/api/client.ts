import axios from "axios";

import type { Alert, DashboardStats, Device } from "../types";

const API_BASE_URL =
  import.meta.env.VITE_API_URL || "http://localhost:8000";

export const api = axios.create({
  baseURL: API_BASE_URL,
});

// Attach the JWT token (if present) to every outgoing request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

// If a token expires, kick the user back to /login
api.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401) {
      localStorage.removeItem("access_token");
      window.location.href = "/login";
    }

    return Promise.reject(err);
  }
);

export const authApi = {
  login: (username: string, password: string) =>
    api.post("/auth/login", { username, password }),

  register: (username: string, email: string, password: string) =>
    api.post("/auth/register", { username, email, password }),

  me: () => api.get("/auth/me"),
};

export const deviceApi = {
  list: () => api.get<Device[]>("/devices/"),

  create: (data: Partial<Device>) =>
    api.post<Device>("/devices/", data),

  delete: (id: number) => api.delete(`/devices/${id}`),
};

export const alertApi = {
  list: () => api.get<Alert[]>("/alerts/"),

  resolve: (id: number) =>
    api.put(`/alerts/${id}`, { status: "resolved" }),
};

export const dashboardApi = {
  get: () => api.get<DashboardStats>("/dashboard/"),
};