import React from "react";
import { useSelector } from "react-redux";
import { AlertCircle, CheckCircle, Clock, TrendingUp } from "lucide-react";
import { RootState } from "@/store";
import Card from "@/components/common/Card";
import Badge from "@/components/common/Badge";
import { useDashboardData } from "@/hooks/useDashboardData";

const DashboardPage: React.FC = () => {
  useDashboardData();
  
  const { incidents } = useSelector((state: RootState) => state.incidents);
  const { problems } = useSelector((state: RootState) => state.problems);
  const { changes } = useSelector((state: RootState) => state.changes);
  const { requests } = useSelector((state: RootState) => state.requests);
  const { unreadCount } = useSelector((state: RootState) => state.notifications);

  const metrics = [
    {
      title: "Active Incidents",
      value: incidents.filter((i) => i.status !== "CLOSED").length,
      icon: AlertCircle,
      color: "danger",
      trend: "+12%",
    },
    {
      title: "Resolved This Week",
      value: incidents.filter((i) => i.status === "RESOLVED").length,
      icon: CheckCircle,
      color: "success",
      trend: "+8%",
    },
    {
      title: "Avg Resolution Time",
      value: "4.2h",
      icon: Clock,
      color: "primary",
      trend: "-5%",
    },
    {
      title: "System Health",
      value: "98.5%",
      icon: TrendingUp,
      color: "success",
      trend: "+2%",
    },
  ];

  const recentIncidents = incidents.slice(0, 5);
  const pendingChanges = changes.filter((c) => c.status === "SUBMITTED").length;
  const openRequests = requests.filter((r) => r.status !== "FULFILLED").length;

  return (
    <div className="p-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-secondary-900">Dashboard</h1>
        <p className="text-secondary-600 mt-2">Welcome back! Here's your system overview</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        {metrics.map((metric) => {
          const Icon = metric.icon;
          return (
            <Card key={metric.title} className="hover:shadow-lg transition-shadow">
              <div className="flex items-start justify-between">
                <div>
                  <p className="text-sm text-secondary-600 mb-1">{metric.title}</p>
                  <p className="text-3xl font-bold text-secondary-900">{metric.value}</p>
                </div>
                <Icon size={24} className="text-primary-500" />
              </div>
              <div className="mt-4 flex items-center justify-between">
                <span className="text-xs text-secondary-500">vs last week</span>
                <Badge
                  variant={metric.trend.startsWith("+") ? "danger" : "success"}
                  size="sm"
                >
                  {metric.trend}
                </Badge>
              </div>
            </Card>
          );
        })}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card className="lg:col-span-2">
          <h2 className="text-lg font-semibold text-secondary-900 mb-4">Recent Incidents</h2>
          <div className="space-y-3">
            {recentIncidents.length > 0 ? (
              recentIncidents.map((incident) => (
                <div
                  key={incident.id}
                  className="flex items-start justify-between p-3 bg-secondary-50 rounded-lg hover:bg-secondary-100 transition-colors cursor-pointer"
                >
                  <div className="flex-1">
                    <p className="font-medium text-secondary-900">{incident.title}</p>
                    <p className="text-sm text-secondary-600">ID: {incident.id}</p>
                  </div>
                  <Badge
                    variant={
                      incident.priority === "CRITICAL"
                        ? "danger"
                        : incident.priority === "HIGH"
                          ? "warning"
                          : "success"
                    }
                    size="sm"
                  >
                    {incident.priority}
                  </Badge>
                </div>
              ))
            ) : (
              <p className="text-secondary-500 text-center py-4">No recent incidents</p>
            )}
          </div>
        </Card>

        <div className="space-y-6">
          <Card>
            <h3 className="text-lg font-semibold text-secondary-900 mb-4">Quick Stats</h3>
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-secondary-600">Pending Changes</span>
                <Badge variant="warning" size="sm">
                  {pendingChanges}
                </Badge>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-secondary-600">Open Requests</span>
                <Badge variant="primary" size="sm">
                  {openRequests}
                </Badge>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-secondary-600">Active Problems</span>
                <Badge variant="danger" size="sm">
                  {problems.filter((p) => p.status !== "CLOSED").length}
                </Badge>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-secondary-600">Notifications</span>
                <Badge variant="primary" size="sm">
                  {unreadCount}
                </Badge>
              </div>
            </div>
          </Card>

          <Card>
            <h3 className="text-lg font-semibold text-secondary-900 mb-4">System Status</h3>
            <div className="space-y-2">
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-success-500 rounded-full"></div>
                <span className="text-sm text-secondary-600">All systems operational</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-success-500 rounded-full"></div>
                <span className="text-sm text-secondary-600">API responding normally</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-success-500 rounded-full"></div>
                <span className="text-sm text-secondary-600">Database healthy</span>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;
