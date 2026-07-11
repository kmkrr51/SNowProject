import React from "react";
import clsx from "clsx";
import { ChevronUp, ChevronDown } from "lucide-react";

interface TableColumn {
  key: string;
  header: string;
  sortable?: boolean;
  render?: (value: any, row: any) => React.ReactNode;
}

interface TableProps {
  columns: TableColumn[];
  data: any[];
  loading?: boolean;
  error?: string;
  onSort?: (key: string, direction: "asc" | "desc") => void;
  onRowClick?: (row: any) => void;
  selectable?: boolean;
  onSelect?: (selectedRows: any[]) => void;
  pagination?: {
    currentPage: number;
    pageSize: number;
    total: number;
    onPageChange: (page: number) => void;
  };
}

const Table: React.FC<TableProps> = ({
  columns,
  data,
  loading = false,
  error,
  onSort,
  onRowClick,
  selectable = false,
  onSelect,
  pagination,
}) => {
  const [sortKey, setSortKey] = React.useState<string | null>(null);
  const [sortDirection, setSortDirection] = React.useState<"asc" | "desc">("asc");
  const [selectedRows, setSelectedRows] = React.useState<Set<string>>(new Set());

  const handleSort = (key: string) => {
    if (!onSort) return;

    if (sortKey === key) {
      const newDirection = sortDirection === "asc" ? "desc" : "asc";
      setSortDirection(newDirection);
      onSort(key, newDirection);
    } else {
      setSortKey(key);
      setSortDirection("asc");
      onSort(key, "asc");
    }
  };

  const handleSelectAll = (checked: boolean) => {
    if (checked) {
      const newSelected = new Set(data.map((row) => row.id));
      setSelectedRows(newSelected);
      onSelect?.(data);
    } else {
      setSelectedRows(new Set());
      onSelect?.([]);
    }
  };

  const handleSelectRow = (rowId: string, row: any) => {
    const newSelected = new Set(selectedRows);
    if (newSelected.has(rowId)) {
      newSelected.delete(rowId);
    } else {
      newSelected.add(rowId);
    }
    setSelectedRows(newSelected);
    onSelect?.(data.filter((r) => newSelected.has(r.id)));
  };

  if (error) {
    return (
      <div className="p-4 bg-danger-50 border border-danger-200 rounded-md">
        <p className="text-danger-800">{error}</p>
      </div>
    );
  }

  return (
    <div className="overflow-x-auto">
      <table className="w-full">
        <thead>
          <tr className="border-b border-secondary-200 bg-secondary-50">
            {selectable && (
              <th className="px-4 py-3 text-left">
                <input
                  type="checkbox"
                  checked={selectedRows.size === data.length && data.length > 0}
                  onChange={(e) => handleSelectAll(e.target.checked)}
                  className="rounded"
                />
              </th>
            )}
            {columns.map((column) => (
              <th
                key={column.key}
                className={clsx(
                  "px-4 py-3 text-left text-sm font-semibold text-secondary-700",
                  column.sortable && "cursor-pointer hover:bg-secondary-100",
                )}
                onClick={() => column.sortable && handleSort(column.key)}
              >
                <div className="flex items-center gap-2">
                  {column.header}
                  {column.sortable && sortKey === column.key && (
                    <>
                      {sortDirection === "asc" ? (
                        <ChevronUp size={16} />
                      ) : (
                        <ChevronDown size={16} />
                      )}
                    </>
                  )}
                </div>
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {loading ? (
            <tr>
              <td colSpan={columns.length + (selectable ? 1 : 0)} className="px-4 py-8 text-center">
                <div className="flex justify-center">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600" />
                </div>
              </td>
            </tr>
          ) : data.length === 0 ? (
            <tr>
              <td
                colSpan={columns.length + (selectable ? 1 : 0)}
                className="px-4 py-8 text-center text-secondary-500"
              >
                No data available
              </td>
            </tr>
          ) : (
            data.map((row) => (
              <tr
                key={row.id}
                className={clsx(
                  "border-b border-secondary-200 hover:bg-secondary-50 transition-colors",
                  onRowClick && "cursor-pointer",
                )}
                onClick={() => onRowClick?.(row)}
              >
                {selectable && (
                  <td className="px-4 py-3" onClick={(e) => e.stopPropagation()}>
                    <input
                      type="checkbox"
                      checked={selectedRows.has(row.id)}
                      onChange={() => handleSelectRow(row.id, row)}
                      className="rounded"
                    />
                  </td>
                )}
                {columns.map((column) => (
                  <td key={column.key} className="px-4 py-3 text-sm text-secondary-900">
                    {column.render ? column.render(row[column.key], row) : row[column.key]}
                  </td>
                ))}
              </tr>
            ))
          )}
        </tbody>
      </table>
      {pagination && (
        <div className="flex items-center justify-between px-4 py-3 border-t border-secondary-200 bg-secondary-50">
          <p className="text-sm text-secondary-600">
            Showing {(pagination.currentPage - 1) * pagination.pageSize + 1} to{" "}
            {Math.min(pagination.currentPage * pagination.pageSize, pagination.total)} of{" "}
            {pagination.total}
          </p>
          <div className="flex gap-2">
            <button
              onClick={() => pagination.onPageChange(pagination.currentPage - 1)}
              disabled={pagination.currentPage === 1}
              className="px-3 py-1 border border-secondary-300 rounded-md disabled:opacity-50 disabled:cursor-not-allowed hover:bg-secondary-100"
            >
              Previous
            </button>
            <button
              onClick={() => pagination.onPageChange(pagination.currentPage + 1)}
              disabled={pagination.currentPage * pagination.pageSize >= pagination.total}
              className="px-3 py-1 border border-secondary-300 rounded-md disabled:opacity-50 disabled:cursor-not-allowed hover:bg-secondary-100"
            >
              Next
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Table;
