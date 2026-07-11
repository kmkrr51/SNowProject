import { createAsyncThunk } from "@reduxjs/toolkit";
import apiClient from "@/services/api";
import { Problem } from "@/types";

export const fetchProblems = createAsyncThunk(
  "problems/fetchProblems",
  async (_, { rejectWithValue }) => {
    try {
      const response = await apiClient.get<{ problems: Problem[] }>(
        "/problems",
      );
      return response.data.problems || [];
    } catch (error: any) {
      return rejectWithValue(
        error.message || "Failed to fetch problems",
      );
    }
  },
);

export const fetchProblemById = createAsyncThunk(
  "problems/fetchProblemById",
  async (id: string, { rejectWithValue }) => {
    try {
      const response = await apiClient.get<Problem>(
        `/problems/${id}`,
      );
      return response.data;
    } catch (error: any) {
      return rejectWithValue(
        error.message || "Failed to fetch problem",
      );
    }
  },
);

export const createProblem = createAsyncThunk(
  "problems/createProblem",
  async (data: any, { rejectWithValue }) => {
    try {
      const response = await apiClient.post<Problem>(
        "/problems",
        data,
      );
      return response.data;
    } catch (error: any) {
      return rejectWithValue(
        error.message || "Failed to create problem",
      );
    }
  },
);

export const updateProblemThunk = createAsyncThunk(
  "problems/updateProblem",
  async (
    { id, data }: { id: string; data: any },
    { rejectWithValue },
  ) => {
    try {
      const response = await apiClient.patch<Problem>(
        `/problems/${id}`,
        data,
      );
      return response.data;
    } catch (error: any) {
      return rejectWithValue(
        error.message || "Failed to update problem",
      );
    }
  },
);
