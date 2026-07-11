import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import { useSelector } from "react-redux";
import { RootState } from "@/store";
import Header from "@/components/layout/Header";
import Sidebar from "@/components/layout/Sidebar";
import ErrorBoundary from "@/components/common/ErrorBoundary";
import LoginPage from "@/pages/LoginPage";
import DashboardPage from "@/pages/DashboardPage";
import IncidentPage from "@/pages/IncidentPage";
import ProblemPage from "@/pages/ProblemPage";
import ChangePage from "@/pages/ChangePage";
import RequestPage from "@/pages/RequestPage";
import NotificationCenterPage from "@/pages/NotificationCenterPage";
import AuditTrailPage from "@/pages/AuditTrailPage";

const App: React.FC = () => {
  const { isAuthenticated } = useSelector((state: RootState) => state.auth);

  if (!isAuthenticated) {
    return (
      <Router>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="*" element={<Navigate to="/login" replace />} />
        </Routes>
      </Router>
    );
  }

  return (
    <ErrorBoundary>
      <Router>
        <div className="flex flex-col h-screen bg-secondary-50">
          <Header />
          <div className="flex flex-1 overflow-hidden">
            <Sidebar />
            <main className="flex-1 overflow-auto">
              <Routes>
                <Route path="/dashboard" element={<DashboardPage />} />
                <Route path="/incidents" element={<IncidentPage />} />
                <Route path="/problems" element={<ProblemPage />} />
                <Route path="/changes" element={<ChangePage />} />
                <Route path="/requests" element={<RequestPage />} />
                <Route path="/notifications" element={<NotificationCenterPage />} />
                <Route path="/audit" element={<AuditTrailPage />} />
                <Route path="/" element={<Navigate to="/dashboard" replace />} />
              </Routes>
            </main>
          </div>
        </div>
      </Router>
    </ErrorBoundary>
  );
};

export default App;
