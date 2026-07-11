import { createSlice, PayloadAction } from "@reduxjs/toolkit";

interface SearchState {
  results: any[];
  query: string;
  loading: boolean;
  error: string | null;
  filters: {
    entityType?: string;
    dateRange?: { from: string; to: string };
  };
}

const initialState: SearchState = {
  results: [],
  query: "",
  loading: false,
  error: null,
  filters: {},
};

const searchSlice = createSlice({
  name: "search",
  initialState,
  reducers: {
    setQuery: (state, action: PayloadAction<string>) => {
      state.query = action.payload;
    },
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.loading = action.payload;
    },
    setError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload;
    },
    setResults: (state, action: PayloadAction<any[]>) => {
      state.results = action.payload;
      state.loading = false;
      state.error = null;
    },
    setFilters: (state, action: PayloadAction<SearchState["filters"]>) => {
      state.filters = action.payload;
    },
    clearResults: (state) => {
      state.results = [];
      state.query = "";
      state.filters = {};
    },
  },
});

export const { setQuery, setLoading, setError, setResults, setFilters, clearResults } =
  searchSlice.actions;
export default searchSlice.reducer;
