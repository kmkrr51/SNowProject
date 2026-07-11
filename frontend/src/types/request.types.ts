export type RequestStatus = "NEW" | "ASSIGNED" | "IN_PROGRESS" | "FULFILLED" | "CLOSED";
export type RequestType = "STANDARD" | "URGENT" | "ROUTINE";
export type RequestPriority = "CRITICAL" | "HIGH" | "MEDIUM" | "LOW";

export interface Task {
  id: string;
  name: string;
  description?: string;
  completed: boolean;
  completedAt?: string;
  completedBy?: string;
}

export interface ServiceRequest {
  id: string;
  requestType: RequestType;
  title: string;
  description: string;
  status: RequestStatus;
  priority: RequestPriority;
  requester: string;
  requestedService: string;
  assignedTo?: string;
  tasks: Task[];
  fulfillmentDetails?: string;
  createdAt: string;
  updatedAt: string;
  fulfilledAt?: string;
  closedAt?: string;
}

export interface RequestFilters {
  status?: RequestStatus[];
  priority?: RequestPriority[];
  type?: RequestType[];
  assignedTo?: string;
  requester?: string;
  dateRange?: {
    from: string;
    to: string;
  };
  search?: string;
}

export interface RequestListState {
  requests: ServiceRequest[];
  loading: boolean;
  error: string | null;
  filters: RequestFilters;
  pagination: {
    currentPage: number;
    pageSize: number;
    total: number;
  };
}

export interface RequestDetailState {
  request: ServiceRequest | null;
  loading: boolean;
  error: string | null;
}

export interface RequestFormState {
  formData: Partial<ServiceRequest>;
  validationErrors: Record<string, string>;
  isSubmitting: boolean;
}
