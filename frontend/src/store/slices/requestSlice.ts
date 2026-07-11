import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { ServiceRequest, RequestListState, RequestFilters } from "@/types";
import { fetchRequests, createRequest, updateRequestThunk } from "../thunks/requestThunks";

const initialState: RequestListState = {
  requests: [],
  loading: false,
  error: null,
  filters: {},
  pagination: {
    currentPage: 1,
    pageSize: 10,
    total: 0,
  },
};

const requestSlice = createSlice({
  name: "requests",
  initialState,
  reducers: {
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.loading = action.payload;
    },
    setError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload;
    },
    setRequests: (state, action: PayloadAction<ServiceRequest[]>) => {
      state.requests = action.payload;
      state.loading = false;
      state.error = null;
    },
    addRequest: (state, action: PayloadAction<ServiceRequest>) => {
      state.requests.unshift(action.payload);
    },
    updateRequest: (state, action: PayloadAction<ServiceRequest>) => {
      const index = state.requests.findIndex((r) => r.id === action.payload.id);
      if (index !== -1) {
        state.requests[index] = action.payload;
      }
    },
    deleteRequest: (state, action: PayloadAction<string>) => {
      state.requests = state.requests.filter((r) => r.id !== action.payload);
    },
    setFilters: (state, action: PayloadAction<RequestFilters>) => {
      state.filters = action.payload;
      state.pagination.currentPage = 1;
    },
    setPage: (state, action: PayloadAction<number>) => {
      state.pagination.currentPage = action.payload;
    },
    setPagination: (
      state,
      action: PayloadAction<{ total: number; pageSize: number }>,
    ) => {
      state.pagination.total = action.payload.total;
      state.pagination.pageSize = action.payload.pageSize;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchRequests.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchRequests.fulfilled, (state, action) => {
        state.requests = action.payload;
        state.loading = false;
      })
      .addCase(fetchRequests.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      .addCase(createRequest.pending, (state) => {
        state.loading = true;
      })
      .addCase(createRequest.fulfilled, (state, action) => {
        state.requests.unshift(action.payload);
        state.loading = false;
      })
      .addCase(createRequest.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      .addCase(updateRequestThunk.pending, (state) => {
        state.loading = true;
      })
      .addCase(updateRequestThunk.fulfilled, (state, action) => {
        const index = state.requests.findIndex((r) => r.id === action.payload.id);
        if (index !== -1) {
          state.requests[index] = action.payload;
        }
        state.loading = false;
      })
      .addCase(updateRequestThunk.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      });
  },
});

export const {
  setLoading,
  setError,
  setRequests,
  addRequest,
  updateRequest,
  deleteRequest,
  setFilters,
  setPage,
  setPagination,
} = requestSlice.actions;
export default requestSlice.reducer;
