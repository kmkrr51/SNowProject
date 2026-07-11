import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { Change, ChangeListState, ChangeFilters } from "@/types";
import { fetchChanges, createChange, updateChangeThunk } from "../thunks/changeThunks";

const initialState: ChangeListState = {
  changes: [],
  loading: false,
  error: null,
  filters: {},
  pagination: {
    currentPage: 1,
    pageSize: 10,
    total: 0,
  },
};

const changeSlice = createSlice({
  name: "changes",
  initialState,
  reducers: {
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.loading = action.payload;
    },
    setError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload;
    },
    setChanges: (state, action: PayloadAction<Change[]>) => {
      state.changes = action.payload;
      state.loading = false;
      state.error = null;
    },
    addChange: (state, action: PayloadAction<Change>) => {
      state.changes.unshift(action.payload);
    },
    updateChange: (state, action: PayloadAction<Change>) => {
      const index = state.changes.findIndex((c) => c.id === action.payload.id);
      if (index !== -1) {
        state.changes[index] = action.payload;
      }
    },
    deleteChange: (state, action: PayloadAction<string>) => {
      state.changes = state.changes.filter((c) => c.id !== action.payload);
    },
    setFilters: (state, action: PayloadAction<ChangeFilters>) => {
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
      .addCase(fetchChanges.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchChanges.fulfilled, (state, action) => {
        state.changes = action.payload;
        state.loading = false;
      })
      .addCase(fetchChanges.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      .addCase(createChange.pending, (state) => {
        state.loading = true;
      })
      .addCase(createChange.fulfilled, (state, action) => {
        state.changes.unshift(action.payload);
        state.loading = false;
      })
      .addCase(createChange.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      .addCase(updateChangeThunk.pending, (state) => {
        state.loading = true;
      })
      .addCase(updateChangeThunk.fulfilled, (state, action) => {
        const index = state.changes.findIndex((c) => c.id === action.payload.id);
        if (index !== -1) {
          state.changes[index] = action.payload;
        }
        state.loading = false;
      })
      .addCase(updateChangeThunk.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      });
  },
});

export const {
  setLoading,
  setError,
  setChanges,
  addChange,
  updateChange,
  deleteChange,
  setFilters,
  setPage,
  setPagination,
} = changeSlice.actions;
export default changeSlice.reducer;
