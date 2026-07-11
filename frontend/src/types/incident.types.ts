export type IncidentStatus = "NEW" | "ASSIGNED" | "IN_PROGRESS" | "RESOLVED" | "CLOSED";
export type IncidentPriority = "CRITICAL" | "HIGH" | "MEDIUM" | "LOW";
export type ImpactLevel = "HIGH" | "MEDIUM" | "LOW";
export type UrgencyLevel = "HIGH" | "MEDIUM" | "LOW";

export interface Incident {
  id: string;
  title: string;
  description: string;
  priority: IncidentPriority;
  status: IncidentStatus;
  impactLevel: ImpactLevel;
  urgencyLevel: UrgencyLevel;
  assignedTo?: string;
  createdBy: string;
  createdAt: string;
  updatedAt: string;
  resolvedAt?: string;
  closedAt?: string;
  slaInfo?: SLAInfo;
}

export interface SLAInfo {
  responseTimeRemaining: number;
  resolutionTimeRemaining: number;
  status: "on-track" | "warning" | "breached";
}

export interface WorkNote {
  id: string;
  incidentId: string;
  content: string;
  author: string;
  createdAt: string;
}

export interface IncidentFilters {
  status?: IncidentStatus[];
  priority?: IncidentPriority[];
  assignedTo?: string;
  createdBy?: string;
  dateRange?: {
    from: string;
    to: string;
  };
  search?: string;
}

export interface IncidentListState {
  incidents: Incident[];
  loading: boolean;
  error: string | null;
  filters: IncidentFilters;
  pagination: {
    currentPage: number;
    pageSize: number;
    total: number;
  };
}

export interface IncidentDetailState {
  incident: Incident | null;
  loading: boolean;
  error: string | null;
  workNotes: WorkNote[];
}

export interface IncidentFormState {
  formData: Partial<Incident>;
  validationErrors: Record<string, string>;
  isSubmitting: boolean;
}
