import React, { useState } from "react";
import { useSelector, useDispatch } from "react-redux";
import { Plus, Filter } from "lucide-react";
import { RootState } from "@/store";
import { setPage } from "@/store/slices/problemSlice";
import { Problem, ProblemStatus } from "@/types";
import Button from "@/components/common/Button";
import Card from "@/components/common/Card";
import Table from "@/components/common/Table";
import Badge from "@/components/common/Badge";
import { formatDate } from "@/utils/dateFormatter";

interface ProblemListProps {
  onCreateClick: () => void;
  onProblemClick?: (problem: Problem) => void;
}

const ProblemList: React.FC<ProblemListProps> = ({ onCreateClick, onProblemClick }) => {
  const dispatch = useDispatch();
  const { problems, loading, pagination } = useSelector(
    (state: RootState) => state.problems,
  );
  const [showFilters, setShowFilters] = useState(false);

  const statusColors: Record<ProblemStatus, "danger" | "warning" | "success" | "primary" | "default"> = {
    IDENTIFIED: "primary",
    INVESTIGATING: "warning",
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
      key: "status",
      header: "Status",
      sortable: true,
      render: (value: ProblemStatus) => (
        <Badge variant={statusColors[value]} size="sm">
          {value}
        </Badge>
      ),
    },
    {
      key: "relatedIncidents",
      header: "Related Incidents",
      render: (value: string[]) => value?.length || 0,
    },
    {
      key: "impactedServices",
      header: "Impacted Services",
      render: (value: string[]) => value?.length || 0,
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
          <h2 className="text-lg font-semibold text-secondary-900">Problems</h2>
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
              New Problem
            </Button>
          </div>
        </div>

        {showFilters && (
          <div className="mb-4 p-4 bg-secondary-50 rounded-md border border-secondary-200">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium text-secondary-700 mb-1">
                  Status
                </label>
                <select className="w-full px-3 py-2 border border-secondary-300 rounded-md">
                  <option value="">All</option>
                  <option value="IDENTIFIED">Identified</option>
                  <option value="INVESTIGATING">Investigating</option>
                  <option value="RESOLVED">Resolved</option>
                  <option value="CLOSED">Closed</option>
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
                  Search
                </label>
                <input
                  type="text"
                  placeholder="Search problems..."
                  className="w-full px-3 py-2 border border-secondary-300 rounded-md"
                />
              </div>
            </div>
          </div>
        )}

        <Table
          columns={columns}
          data={problems}
          loading={loading}
          onRowClick={onProblemClick}
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

export default ProblemList;
