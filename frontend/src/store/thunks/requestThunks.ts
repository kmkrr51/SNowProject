import { createAsyncThunk } from "@reduxjs/toolkit";
import apiClient from "@/services/api";
import { ServiceRequest } from "@/types";

export const fetchRequests = createAsyncThunk(
  "requests/fetchRequests",
  async (_, { rejectWithValue }) => {
    try {
      const response = await apiClient.get<{ requests: ServiceRequest[] }>(
        "/requests",
      );
      return response.data.requests || [];
    } catch (error: any) {
      return rejectWithValue(
        error.message || "Failed to fetch requests",
      );
    }
  },
);

export const fetchRequestById = createAsyncThunk(
  "requests/fetchRequestById",
  async (id: string, { rejectWithValue }) => {
    try {
      const response = await apiClient.get<ServiceRequest>(
        `/requests/${id}`,
      );
      return response.data;
    } catch (error: any) {
      return rejectWithValue(
        error.message || "Failed to fetch request",
      );
    }
  },
);

export const createRequest = createAsyncThunk(
  "requests/createRequest",
  async (data: any, { rejectWithValue }) => {
    try {
      const response = await apiClient.post<ServiceRequest>(
        "/requests",
        data,
      );
      return response.data;
    } catch (error: any) {
      return rejectWithValue(
        error.message || "Failed to create request",
      );
    }
  },
);

export const updateRequestThunk = createAsyncThunk(
  "requests/updateRequest",
  async (
    { id, data }: { id: string; data: any },
    { rejectWithValue },
  ) => {
    try {
      const response = await apiClient.patch<ServiceRequest>(
        `/requests/${id}`,
        data,
      );
      return response.data;
    } catch (error: any) {
      return rejectWithValue(
        error.message || "Failed to update request",
      );
    }
  },
);
