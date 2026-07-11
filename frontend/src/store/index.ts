import { configureStore } from "@reduxjs/toolkit";
import authReducer from "./slices/authSlice";
import uiReducer from "./slices/uiSlice";
import incidentReducer from "./slices/incidentSlice";
import problemReducer from "./slices/problemSlice";
import changeReducer from "./slices/changeSlice";
import requestReducer from "./slices/requestSlice";
import notificationReducer from "./slices/notificationSlice";
import searchReducer from "./slices/searchSlice";
import auditReducer from "./slices/auditSlice";

export const store = configureStore({
  reducer: {
    auth: authReducer,
    ui: uiReducer,
    incidents: incidentReducer,
    problems: problemReducer,
    changes: changeReducer,
    requests: requestReducer,
    notifications: notificationReducer,
    search: searchReducer,
    audit: auditReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
