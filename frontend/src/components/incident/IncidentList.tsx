import React, { useState } from "react";
import { useSelector, useDispatch } from "react-redux";
import { Plus, Filter } from "lucide-react";
import { RootState } from "@/store";
import { setFilters, setPage } from "@/store/slices/incidentSlice";
import { Incident, IncidentPriority, IncidentStatus } from "@/types";
import Button from "@/components/common/Button";
import Card from "@/components/common/Card";
import Table from "@/components/common/Table";
import Badge from "@/components/common/Badge";
import { formatDate } from "@/utils/dateFormatter";

interface IncidentListProps {
  onCreateClick: () => void;
  onIncidentClick?: (incident: Incident) => void;
}

const IncidentList: React.FC<IncidentListProps> = ({ onCreateClick, onIncidentClick }) => {
  const dispatch = useDispatch();
  const { incidents, loading, pagination } = useSelector(
    (state: RootState) => state.incidents,
  );
  const [showFilters, setShowFilters] = useState(false);

  const priorityColors: Record<IncidentPriority, "danger" | "warning" | "success" | "primary"> = {
    CRITICAL: "danger",
    HIGH: "warning",
    MEDIUM: "primary",
    LOW: "success",
  };

  const statusColors: Record<
    IncidentStatus,
    "danger" | "warning" | "success" | "primary" | "default"
  > = {
    NEW: "primary",
    ASSIGNED: "warning",
    IN_PROGRESS: "warning",
    RESOLVED: "success",
    CLOSED: "default",
  };

  const columns = [
    {
      key: "id",
      header: "ID",
      sortable: true,
    },
    {
      key: "title",
      header: "Title",
      sortable: true,
    },
    {
      key: "priority",
      header: "Priority",
      sortable: true,
      render: (value: IncidentPriority) => (
        <Badge variant={priorityColors[value]} size="sm">
          {value}
        </Badge>
      ),
    },
    {
      key: "status",
      header: "Status",
      sortable: true,
      render: (value: IncidentStatus) => (
        <Badge variant={statusColors[value]} size="sm">
          {value}
        </Badge>
      ),
    },
    {
      key: "assignedTo",
      header: "Assigned To",
      render: (value: string | undefined) => value || "Unassigned",
    },
    {
      key: "createdAt",
      header: "Created",
      render: (value: string) => formatDate(value),
    },
  ];

  return (
    <div className="space-y-4">
      <Card>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-secondary-900">Incidents</h2>
          <div className="flex gap-2">
            <Button
              variant="secondary"
              size="sm"
              icon={<Filter size={16} />}
              onClick={() => setShowFilters(!showFilters)}
            >
              Filters
            </Button>
            <Button
              variant="primary"
              size="sm"
              icon={<Plus size={16} />}
              onClick={onCreateClick}
            >
              New Incident
            </Button>
          </div>
        </div>

        {showFilters && (
          <div className="mb-4 p-4 bg-secondary-50 rounded-md border border-secondary-200">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div>
                <label className="block text-sm font-medium text-secondary-700 mb-1">
                  Status
                </label>
                <select className="w-full px-3 py-2 border border-secondary-300 rounded-md">
                  <option value="">All</option>
                  <option value="NEW">New</option>
                  <option value="ASSIGNED">Assigned</option>
                  <option value="IN_PROGRESS">In Progress</option>
                  <option value="RESOLVED">Resolved</option>
                  <option value="CLOSED">Closed</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-secondary-700 mb-1">
                  Priority
                </label>
                <select className="w-full px-3 py-2 border border-secondary-300 rounded-md">
                  <option value="">All</option>
                  <option value="CRITICAL">Critical</option>
                  <option value="HIGH">High</option>
                  <option value="MEDIUM">Medium</option>
                  <option value="LOW">Low</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-secondary-700 mb-1">
                  Assigned To
                </label>
                <input
                  type="text"
                  placeholder="Technician name"
                  className="w-full px-3 py-2 border border-secondary-300 rounded-md"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-secondary-700 mb-1">
                  Search
                </label>
                <input
                  type="text"
                  placeholder="Search incidents..."
                  className="w-full px-3 py-2 border border-secondary-300 rounded-md"
                />
              </div>
            </div>
          </div>
        )}

        <Table
          columns={columns}
          data={incidents}
          loading={loading}
          onRowClick={onIncidentClick}
          pagination={{
            currentPage: pagination.currentPage,
            pageSize: pagination.pageSize,
            total: pagination.total,
            onPageChange: (page) => dispatch(setPage(page)),
          }}
        />
      </Card>
    </div>
  );
};

export default IncidentList;
