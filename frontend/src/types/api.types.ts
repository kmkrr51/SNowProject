export interface ApiResponse<T> {
  data: T;
  message: string;
  status: number;
}

export interface ApiErrorResponse {
  message: string;
  status: number;
  errors?: Record<string, string[]>;
  timestamp: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  pageSize: number;
  totalPages: number;
}

export interface ApiError extends Error {
  status: number;
  data?: ApiErrorResponse;
}
