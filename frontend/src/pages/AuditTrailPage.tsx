import React, { useState } from "react";
import { useSelector, useDispatch } from "react-redux";
import { Filter } from "lucide-react";
import { RootState } from "@/store";
import { setPage } from "@/store/slices/auditSlice";
import Card from "@/components/common/Card";
import Table from "@/components/common/Table";
import Button from "@/components/common/Button";

const AuditTrailPage: React.FC = () => {
  const dispatch = useDispatch();
  const { logs, pagination } = useSelector((state: RootState) => state.audit);
  const [showFilters, setShowFilters] = useState(false);

  const columns = [
    {
      key: "timestamp",
      header: "Timestamp",
      sortable: true,
      render: (value: string) => new Date(value).toLocaleString(),
    },
    {
      key: "entityType",
      header: "Entity Type",
      sortable: true,
    },
    {
      key: "entityId",
      header: "Entity ID",
    },
    {
      key: "action",
      header: "Action",
      sortable: true,
    },
    {
      key: "actor",
      header: "Actor",
      sortable: true,
    },
  ];

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-secondary-900">Audit Trail</h1>
        <p className="text-secondary-600 mt-2">
          Track all changes and activities in the system
        </p>
      </div>

      <Card>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-secondary-900">Activity Log</h2>
          <Button
            variant="secondary"
            size="sm"
            icon={<Filter size={16} />}
            onClick={() => setShowFilters(!showFilters)}
          >
            Filters
          </Button>
        </div>

        {showFilters && (
          <div className="mb-4 p-4 bg-secondary-50 rounded-md border border-secondary-200">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div>
                <label className="block text-sm font-medium text-secondary-700 mb-1">
                  Entity Type
                </label>
                <select className="w-full px-3 py-2 border border-secondary-300 rounded-md">
                  <option value="">All</option>
                  <option value="INCIDENT">Incident</option>
                  <option value="PROBLEM">Problem</option>
                  <option value="CHANGE">Change</option>
                  <option value="REQUEST">Request</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-secondary-700 mb-1">
                  Action
                </label>
                <select className="w-full px-3 py-2 border border-secondary-300 rounded-md">
                  <option value="">All</option>
                  <option value="CREATE">Create</option>
                  <option value="UPDATE">Update</option>
                  <option value="DELETE">Delete</option>
                  <option value="ASSIGN">Assign</option>
                  <option value="CLOSE">Close</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-secondary-700 mb-1">
                  Date Range
                </label>
                <input
                  type="date"
                  className="w-full px-3 py-2 border border-secondary-300 rounded-md"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-secondary-700 mb-1">
                  Actor
                </label>
                <input
                  type="text"
                  placeholder="User name"
                  className="w-full px-3 py-2 border border-secondary-300 rounded-md"
                />
              </div>
            </div>
          </div>
        )}

        <Table
          columns={columns}
          data={logs}
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

export default AuditTrailPage;
