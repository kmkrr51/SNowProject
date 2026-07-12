import React, { useState } from "react";
import { useSelector, useDispatch } from "react-redux";
import { Plus, Filter } from "lucide-react";
import { RootState } from "@/store";
import { setPage } from "@/store/slices/changeSlice";
import { Change, ChangeStatus, RiskLevel } from "@/types";
import Button from "@/components/common/Button";
import Card from "@/components/common/Card";
import Table from "@/components/common/Table";
import Badge from "@/components/common/Badge";
import CreateChangeModal from "@/components/change/CreateChangeModal";
import { useChangesData } from "@/hooks/useChangesData";
import { formatDate } from "@/utils/dateFormatter";

const ChangePage: React.FC = () => {
  useChangesData();
  const dispatch = useDispatch();
  const { changes, loading, pagination } = useSelector(
    (state: RootState) => state.changes,
  );
  const [showFilters, setShowFilters] = useState(false);
  const [selectedChange, setSelectedChange] = useState<Change | null>(null);
  const [showCreateModal, setShowCreateModal] = useState(false);

  const statusColors: Record<ChangeStatus, "danger" | "warning" | "success" | "primary" | "default"> = {
    DRAFT: "default",
    SUBMITTED: "primary",
    APPROVED: "success",
    REJECTED: "danger",
    IMPLEMENTED: "success",
    CLOSED: "default",
  };

  const riskColors: Record<RiskLevel, "danger" | "warning" | "success"> = {
    HIGH: "danger",
    MEDIUM: "warning",
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
      render: (value: ChangeStatus) => (
        <Badge variant={statusColors[value]} size="sm">
          {value}
        </Badge>
      ),
    },
    {
      key: "riskLevel",
      header: "Risk",
      render: (value: RiskLevel) => (
        <Badge variant={riskColors[value]} size="sm">
          {value}
        </Badge>
      ),
    },
    {
      key: "type",
      header: "Type",
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
        <h1 className="text-3xl font-bold text-secondary-900">Change Management</h1>
        <p className="text-secondary-600 mt-2">Plan, approve, and implement changes safely</p>
      </div>

      <Card>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-secondary-900">Changes</h2>
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
              New Change
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
                  <option value="DRAFT">Draft</option>
                  <option value="SUBMITTED">Submitted</option>
                  <option value="APPROVED">Approved</option>
                  <option value="REJECTED">Rejected</option>
                  <option value="IMPLEMENTED">Implemented</option>
                  <option value="CLOSED">Closed</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-secondary-700 mb-1">
                  Risk Level
                </label>
                <select className="w-full px-3 py-2 border border-secondary-300 rounded-md">
                  <option value="">All</option>
                  <option value="HIGH">High</option>
                  <option value="MEDIUM">Medium</option>
                  <option value="LOW">Low</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-secondary-700 mb-1">
                  Type
                </label>
                <select className="w-full px-3 py-2 border border-secondary-300 rounded-md">
                  <option value="">All</option>
                  <option value="STANDARD">Standard</option>
                  <option value="EMERGENCY">Emergency</option>
                  <option value="NORMAL">Normal</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-secondary-700 mb-1">
                  Search
                </label>
                <input
                  type="text"
                  placeholder="Search changes..."
                  className="w-full px-3 py-2 border border-secondary-300 rounded-md"
                />
              </div>
            </div>
          </div>
        )}

        <Table
          columns={columns}
          data={changes}
          loading={loading}
          onRowClick={setSelectedChange}
          pagination={{
            currentPage: pagination.currentPage,
            pageSize: pagination.pageSize,
            total: pagination.total,
            onPageChange: (page) => dispatch(setPage(page)),
          }}
        />
      </Card>

      <CreateChangeModal
        isOpen={showCreateModal}
        onClose={() => setShowCreateModal(false)}
      />

      {selectedChange && (
        <div className="mt-6 p-6 bg-white rounded-lg shadow-md border border-secondary-200">
          <h2 className="text-xl font-semibold text-secondary-900 mb-4">
            {selectedChange.title}
          </h2>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <p className="text-sm text-secondary-600">ID</p>
              <p className="font-medium text-secondary-900">{selectedChange.id}</p>
            </div>
            <div>
              <p className="text-sm text-secondary-600">Status</p>
              <p className="font-medium text-secondary-900">{selectedChange.status}</p>
            </div>
            <div>
              <p className="text-sm text-secondary-600">Risk Level</p>
              <p className="font-medium text-secondary-900">{selectedChange.riskLevel}</p>
            </div>
            <div>
              <p className="text-sm text-secondary-600">Type</p>
              <p className="font-medium text-secondary-900">{selectedChange.type}</p>
            </div>
          </div>
          <div className="mt-4">
            <p className="text-sm text-secondary-600">Description</p>
            <p className="text-secondary-900">{selectedChange.description}</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default ChangePage;
