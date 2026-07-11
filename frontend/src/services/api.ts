import axios, { AxiosInstance, AxiosError } from "axios";
import { ApiError, ApiErrorResponse } from "@/types";

// In development, use the proxy; in production, use the full URL
const getApiBaseUrl = () => {
  const isDev = import.meta.url.includes("localhost") || import.meta.url.includes("127.0.0.1");
  if (isDev) {
    return "/api/v1"; // Use Vite proxy
  }
  return "http://localhost:8000/api/v1";
};

const API_BASE_URL = getApiBaseUrl();

const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error),
);

apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError<ApiErrorResponse>) => {
    const apiError: ApiError = new Error(
      error.response?.data?.message || error.message,
    ) as ApiError;
    apiError.status = error.response?.status || 500;
    apiError.data = error.response?.data;

    if (error.response?.status === 401) {
      localStorage.removeItem("token");
      localStorage.removeItem("refreshToken");
      window.location.href = "/login";
    }

    return Promise.reject(apiError);
  },
);

export default apiClient;

