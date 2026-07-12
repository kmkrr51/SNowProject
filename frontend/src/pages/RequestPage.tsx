import React, { useState } from "react";
import { useSelector, useDispatch } from "react-redux";
import { Plus, Filter } from "lucide-react";
import { RootState } from "@/store";
import { setPage } from "@/store/slices/requestSlice";
import { ServiceRequest, RequestStatus, RequestPriority } from "@/types";
import Button from "@/components/common/Button";
import Card from "@/components/common/Card";
import Table from "@/components/common/Table";
import Badge from "@/components/common/Badge";
import CreateRequestModal from "@/components/request/CreateRequestModal";
import { useRequestsData } from "@/hooks/useRequestsData";
import { formatDate } from "@/utils/dateFormatter";

const RequestPage: React.FC = () => {
  useRequestsData();
  const dispatch = useDispatch();
  const { requests, loading, pagination } = useSelector(
    (state: RootState) => state.requests,
  );
  const [showFilters, setShowFilters] = useState(false);
  const [selectedRequest, setSelectedRequest] = useState<ServiceRequest | null>(null);
  const [showCreateModal, setShowCreateModal] = useState(false);

  const statusColors: Record<RequestStatus, "danger" | "warning" | "success" | "primary" | "default"> = {
    NEW: "primary",
    ASSIGNED: "warning",
    IN_PROGRESS: "warning",
    FULFILLED: "success",
    CLOSED: "default",
  };

  const priorityColors: Record<RequestPriority, "danger" | "warning" | "success" | "primary"> = {
    CRITICAL: "danger",
    HIGH: "warning",
    MEDIUM: "primary",
    LOW: "success",
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
      key: "status",
      header: "Status",
      sortable: true,
      render: (value: RequestStatus) => (
        <Badge variant={statusColors[value]} size="sm">
          {value}
        </Badge>
      ),
    },
    {
      key: "priority",
      header: "Priority",
      render: (value: RequestPriority) => (
        <Badge variant={priorityColors[value]} size="sm">
          {value}
        </Badge>
      ),
    },
    {
      key: "requestedService",
      header: "Service",
    },
    {
      key: "createdAt",
      header: "Created",
      render: (value: string) => formatDate(value),
    },
  ];

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-secondary-900">Service Requests</h1>
        <p className="text-secondary-600 mt-2">Manage and fulfill service requests</p>
      </div>

      <Card>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-secondary-900">Requests</h2>
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
              onClick={() => setShowCreateModal(true)}
            >
              New Request
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
                  <option value="FULFILLED">Fulfilled</option>
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
                  Service
                </label>
                <input
                  type="text"
                  placeholder="Service name"
                  className="w-full px-3 py-2 border border-secondary-300 rounded-md"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-secondary-700 mb-1">
                  Search
                </label>
                <input
                  type="text"
                  placeholder="Search requests..."
                  className="w-full px-3 py-2 border border-secondary-300 rounded-md"
                />
              </div>
            </div>
          </div>
        )}

        <Table
          columns={columns}
          data={requests}
          loading={loading}
          onRowClick={setSelectedRequest}
          pagination={{
            currentPage: pagination.currentPage,
            pageSize: pagination.pageSize,
            total: pagination.total,
            onPageChange: (page) => dispatch(setPage(page)),
          }}
        />
      </Card>

      <CreateRequestModal
        isOpen={showCreateModal}
        onClose={() => setShowCreateModal(false)}
      />

      {selectedRequest && (
        <div className="mt-6 p-6 bg-white rounded-lg shadow-md border border-secondary-200">
          <h2 className="text-xl font-semibold text-secondary-900 mb-4">
            {selectedRequest.title}
          </h2>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <p className="text-sm text-secondary-600">ID</p>
              <p className="font-medium text-secondary-900">{selectedRequest.id}</p>
            </div>
            <div>
              <p className="text-sm text-secondary-600">Status</p>
              <p className="font-medium text-secondary-900">{selectedRequest.status}</p>
            </div>
            <div>
              <p className="text-sm text-secondary-600">Priority</p>
              <p className="font-medium text-secondary-900">{selectedRequest.priority}</p>
            </div>
            <div>
              <p className="text-sm text-secondary-600">Service</p>
              <p className="font-medium text-secondary-900">{selectedRequest.requestedService}</p>
            </div>
            <div>
              <p className="text-sm text-secondary-600">Requester</p>
              <p className="font-medium text-secondary-900">{selectedRequest.requester}</p>
            </div>
            <div>
              <p className="text-sm text-secondary-600">Assigned To</p>
              <p className="font-medium text-secondary-900">
                {selectedRequest.assignedTo || "Unassigned"}
              </p>
            </div>
          </div>
          <div className="mt-4">
            <p className="text-sm text-secondary-600">Description</p>
            <p className="text-secondary-900">{selectedRequest.description}</p>
          </div>
          {selectedRequest.tasks && selectedRequest.tasks.length > 0 && (
            <div className="mt-4">
              <p className="text-sm font-medium text-secondary-700 mb-2">Tasks</p>
              <ul className="space-y-1">
                {selectedRequest.tasks.map((task, idx) => (
                  <li key={idx} className="text-sm text-secondary-600">
                    {task.completed ? "✓" : "○"} {task.name}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default RequestPage;
