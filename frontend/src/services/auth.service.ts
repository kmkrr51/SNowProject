import apiClient from "./api";
import { LoginRequest, LoginResponse, RegisterRequest, User } from "@/types";

export const authService = {
  login: async (credentials: LoginRequest): Promise<LoginResponse> => {
    const response = await apiClient.post<LoginResponse>("/auth/login", credentials);
    return response.data;
  },

  register: async (data: RegisterRequest): Promise<User> => {
    const response = await apiClient.post<User>("/auth/register", data);
    return response.data;
  },

  logout: async (): Promise<void> => {
    await apiClient.post("/auth/logout");
  },

  getCurrentUser: async (): Promise<User> => {
    const response = await apiClient.get<User>("/auth/me");
    return response.data;
  },

  refreshToken: async (): Promise<LoginResponse> => {
    const refreshToken = localStorage.getItem("refreshToken");
    const response = await apiClient.post<LoginResponse>("/auth/refresh", {
      refreshToken,
    });
    return response.data;
  },
};
