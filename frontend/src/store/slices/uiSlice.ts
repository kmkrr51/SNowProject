import { createSlice, PayloadAction } from "@reduxjs/toolkit";

interface UIState {
  theme: "light" | "dark";
  sidebarOpen: boolean;
  modals: Record<string, { isOpen: boolean; data?: any }>;
  notifications: Array<{ id: string; message: string; type: string }>;
}

const initialState: UIState = {
  theme: localStorage.getItem("theme") === "dark" ? "dark" : "light",
  sidebarOpen: true,
  modals: {},
  notifications: [],
};

const uiSlice = createSlice({
  name: "ui",
  initialState,
  reducers: {
    setTheme: (state, action: PayloadAction<"light" | "dark">) => {
      state.theme = action.payload;
      localStorage.setItem("theme", action.payload);
    },
    toggleSidebar: (state) => {
      state.sidebarOpen = !state.sidebarOpen;
    },
    setSidebarOpen: (state, action: PayloadAction<boolean>) => {
      state.sidebarOpen = action.payload;
    },
    openModal: (
      state,
      action: PayloadAction<{ name: string; data?: any }>,
    ) => {
      state.modals[action.payload.name] = {
        isOpen: true,
        data: action.payload.data,
      };
    },
    closeModal: (state, action: PayloadAction<string>) => {
      state.modals[action.payload] = { isOpen: false };
    },
    addNotification: (
      state,
      action: PayloadAction<{ message: string; type: string }>,
    ) => {
      const id = Date.now().toString();
      state.notifications.push({ id, ...action.payload });
    },
    removeNotification: (state, action: PayloadAction<string>) => {
      state.notifications = state.notifications.filter(
        (n) => n.id !== action.payload,
      );
    },
  },
});

export const {
  setTheme,
  toggleSidebar,
  setSidebarOpen,
  openModal,
  closeModal,
  addNotification,
  removeNotification,
} = uiSlice.actions;
export default uiSlice.reducer;
