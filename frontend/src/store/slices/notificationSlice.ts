import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { Notification, NotificationState, NotificationPreferences } from "@/types";

const initialState: NotificationState = {
  notifications: [],
  unreadCount: 0,
  loading: false,
  error: null,
  preferences: {
    emailNotifications: true,
    inAppNotifications: true,
    smsNotifications: false,
    incidentNotifications: true,
    changeNotifications: true,
    requestNotifications: true,
  },
};

const notificationSlice = createSlice({
  name: "notifications",
  initialState,
  reducers: {
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.loading = action.payload;
    },
    setError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload;
    },
    setNotifications: (state, action: PayloadAction<Notification[]>) => {
      state.notifications = action.payload;
      state.unreadCount = action.payload.filter((n) => n.status === "UNREAD").length;
      state.loading = false;
      state.error = null;
    },
    addNotification: (state, action: PayloadAction<Notification>) => {
      state.notifications.unshift(action.payload);
      if (action.payload.status === "UNREAD") {
        state.unreadCount += 1;
      }
    },
    markAsRead: (state, action: PayloadAction<string>) => {
      const notification = state.notifications.find((n) => n.id === action.payload);
      if (notification && notification.status === "UNREAD") {
        notification.status = "READ";
        state.unreadCount -= 1;
      }
    },
    markAllAsRead: (state) => {
      state.notifications.forEach((n) => {
        if (n.status === "UNREAD") {
          n.status = "READ";
        }
      });
      state.unreadCount = 0;
    },
    deleteNotification: (state, action: PayloadAction<string>) => {
      const notification = state.notifications.find((n) => n.id === action.payload);
      if (notification && notification.status === "UNREAD") {
        state.unreadCount -= 1;
      }
      state.notifications = state.notifications.filter((n) => n.id !== action.payload);
    },
    setPreferences: (state, action: PayloadAction<NotificationPreferences>) => {
      state.preferences = action.payload;
    },
  },
});

export const {
  setLoading,
  setError,
  setNotifications,
  addNotification,
  markAsRead,
  markAllAsRead,
  deleteNotification,
  setPreferences,
} = notificationSlice.actions;
export default notificationSlice.reducer;
