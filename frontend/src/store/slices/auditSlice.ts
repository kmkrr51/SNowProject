import { createSlice, PayloadAction } from "@reduxjs/toolkit";

interface AuditLog {
  id: string;
  entityType: string;
  entityId: string;
  action: string;
  actor: string;
  changes: Record<string, any>;
  timestamp: string;
}

interface AuditState {
  logs: AuditLog[];
  loading: boolean;
  error: string | null;
  filters: {
    entityType?: string;
    actor?: string;
    dateRange?: { from: string; to: string };
  };
  pagination: {
    currentPage: number;
    pageSize: number;
    total: number;
  };
}

const initialState: AuditState = {
  logs: [],
  loading: false,
  error: null,
  filters: {},
  pagination: {
    currentPage: 1,
    pageSize: 10,
    total: 0,
  },
};

const auditSlice = createSlice({
  name: "audit",
  initialState,
  reducers: {
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.loading = action.payload;
    },
    setError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload;
    },
    setLogs: (state, action: PayloadAction<AuditLog[]>) => {
      state.logs = action.payload;
      state.loading = false;
      state.error = null;
    },
    setFilters: (state, action: PayloadAction<AuditState["filters"]>) => {
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
});

export const { setLoading, setError, setLogs, setFilters, setPage, setPagination } =
  auditSlice.actions;
export default auditSlice.reducer;
