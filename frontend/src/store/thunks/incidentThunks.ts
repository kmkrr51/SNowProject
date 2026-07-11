import { createAsyncThunk } from "@reduxjs/toolkit";
import apiClient from "@/services/api";
import { Incident } from "@/types";

export const fetchIncidents = createAsyncThunk(
  "incidents/fetchIncidents",
  async (_, { rejectWithValue }) => {
    try {
      const response = await apiClient.get<{ incidents: Incident[] }>(
        "/incidents",
      );
      return response.data.incidents || [];
    } catch (error: any) {
      return rejectWithValue(
        error.message || "Failed to fetch incidents",
      );
    }
  },
);

export const fetchIncidentById = createAsyncThunk(
  "incidents/fetchIncidentById",
  async (id: string, { rejectWithValue }) => {
    try {
      const response = await apiClient.get<Incident>(
        `/incidents/${id}`,
      );
      return response.data;
    } catch (error: any) {
      return rejectWithValue(
        error.message || "Failed to fetch incident",
      );
    }
  },
);

export const createIncident = createAsyncThunk(
  "incidents/createIncident",
  async (data: any, { rejectWithValue }) => {
    try {
      const response = await apiClient.post<Incident>(
        "/incidents",
        data,
      );
      return response.data;
    } catch (error: any) {
      return rejectWithValue(
        error.message || "Failed to create incident",
      );
    }
  },
);

export const updateIncidentThunk = createAsyncThunk(
  "incidents/updateIncident",
  async (
    { id, data }: { id: string; data: any },
    { rejectWithValue },
  ) => {
    try {
      const response = await apiClient.patch<Incident>(
        `/incidents/${id}`,
        data,
      );
      return response.data;
    } catch (error: any) {
      return rejectWithValue(
        error.message || "Failed to update incident",
      );
    }
  },
);
