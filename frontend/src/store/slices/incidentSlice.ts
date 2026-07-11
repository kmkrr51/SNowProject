import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { Incident, IncidentListState, IncidentFilters } from "@/types";
import { fetchIncidents, createIncident, updateIncidentThunk } from "../thunks/incidentThunks";

const initialState: IncidentListState = {
  incidents: [],
  loading: false,
  error: null,
  filters: {},
  pagination: {
    currentPage: 1,
    pageSize: 10,
    total: 0,
  },
};

const incidentSlice = createSlice({
  name: "incidents",
  initialState,
  reducers: {
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.loading = action.payload;
    },
    setError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload;
    },
    setIncidents: (state, action: PayloadAction<Incident[]>) => {
      state.incidents = action.payload;
      state.loading = false;
      state.error = null;
    },
    addIncident: (state, action: PayloadAction<Incident>) => {
      state.incidents.unshift(action.payload);
    },
    updateIncident: (state, action: PayloadAction<Incident>) => {
      const index = state.incidents.findIndex((i) => i.id === action.payload.id);
      if (index !== -1) {
        state.incidents[index] = action.payload;
      }
    },
    deleteIncident: (state, action: PayloadAction<string>) => {
      state.incidents = state.incidents.filter((i) => i.id !== action.payload);
    },
    setFilters: (state, action: PayloadAction<IncidentFilters>) => {
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
      .addCase(fetchIncidents.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchIncidents.fulfilled, (state, action) => {
        state.incidents = action.payload;
        state.loading = false;
      })
      .addCase(fetchIncidents.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      .addCase(createIncident.pending, (state) => {
        state.loading = true;
      })
      .addCase(createIncident.fulfilled, (state, action) => {
        state.incidents.unshift(action.payload);
        state.loading = false;
      })
      .addCase(createIncident.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      .addCase(updateIncidentThunk.pending, (state) => {
        state.loading = true;
      })
      .addCase(updateIncidentThunk.fulfilled, (state, action) => {
        const index = state.incidents.findIndex((i) => i.id === action.payload.id);
        if (index !== -1) {
          state.incidents[index] = action.payload;
        }
        state.loading = false;
      })
      .addCase(updateIncidentThunk.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      });
  },
});

export const {
  setLoading,
  setError,
  setIncidents,
  addIncident,
  updateIncident,
  deleteIncident,
  setFilters,
  setPage,
  setPagination,
} = incidentSlice.actions;
export default incidentSlice.reducer;
