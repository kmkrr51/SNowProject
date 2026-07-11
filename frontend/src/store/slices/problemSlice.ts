import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { Problem, ProblemListState, ProblemFilters } from "@/types";
import { fetchProblems, createProblem, updateProblemThunk } from "../thunks/problemThunks";

const initialState: ProblemListState = {
  problems: [],
  loading: false,
  error: null,
  filters: {},
  pagination: {
    currentPage: 1,
    pageSize: 10,
    total: 0,
  },
};

const problemSlice = createSlice({
  name: "problems",
  initialState,
  reducers: {
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.loading = action.payload;
    },
    setError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload;
    },
    setProblems: (state, action: PayloadAction<Problem[]>) => {
      state.problems = action.payload;
      state.loading = false;
      state.error = null;
    },
    addProblem: (state, action: PayloadAction<Problem>) => {
      state.problems.unshift(action.payload);
    },
    updateProblem: (state, action: PayloadAction<Problem>) => {
      const index = state.problems.findIndex((p) => p.id === action.payload.id);
      if (index !== -1) {
        state.problems[index] = action.payload;
      }
    },
    deleteProblem: (state, action: PayloadAction<string>) => {
      state.problems = state.problems.filter((p) => p.id !== action.payload);
    },
    setFilters: (state, action: PayloadAction<ProblemFilters>) => {
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
      .addCase(fetchProblems.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchProblems.fulfilled, (state, action) => {
        state.problems = action.payload;
        state.loading = false;
      })
      .addCase(fetchProblems.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      .addCase(createProblem.pending, (state) => {
        state.loading = true;
      })
      .addCase(createProblem.fulfilled, (state, action) => {
        state.problems.unshift(action.payload);
        state.loading = false;
      })
      .addCase(createProblem.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      .addCase(updateProblemThunk.pending, (state) => {
        state.loading = true;
      })
      .addCase(updateProblemThunk.fulfilled, (state, action) => {
        const index = state.problems.findIndex((p) => p.id === action.payload.id);
        if (index !== -1) {
          state.problems[index] = action.payload;
        }
        state.loading = false;
      })
      .addCase(updateProblemThunk.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      });
  },
});

export const {
  setLoading,
  setError,
  setProblems,
  addProblem,
  updateProblem,
  deleteProblem,
  setFilters,
  setPage,
  setPagination,
} = problemSlice.actions;
export default problemSlice.reducer;
