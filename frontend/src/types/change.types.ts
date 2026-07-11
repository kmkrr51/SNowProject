export type ChangeStatus =
  | "DRAFT"
  | "SUBMITTED"
  | "APPROVED"
  | "REJECTED"
  | "IMPLEMENTED"
  | "CLOSED";
export type ChangeType = "STANDARD" | "EMERGENCY" | "NORMAL";
export type RiskLevel = "HIGH" | "MEDIUM" | "LOW";
export type ApprovalStatus = "PENDING" | "APPROVED" | "REJECTED";

export interface Change {
  id: string;
  title: string;
  description: string;
  type: ChangeType;
  status: ChangeStatus;
  riskLevel: RiskLevel;
  impactAssessment?: string;
  rollbackPlan?: string;
  implementationSchedule?: string;
  createdBy: string;
  createdAt: string;
  updatedAt: string;
  implementedAt?: string;
}

export interface ChangeApproval {
  id: string;
  changeId: string;
  approverId: string;
  status: ApprovalStatus;
  comments?: string;
  approvedAt?: string;
}

export interface ChangeImplementation {
  id: string;
  changeId: string;
  startTime?: string;
  endTime?: string;
  status: "SCHEDULED" | "IN_PROGRESS" | "COMPLETED" | "ROLLED_BACK";
}

export interface ChangeFilters {
  status?: ChangeStatus[];
  riskLevel?: RiskLevel[];
  type?: ChangeType[];
  dateRange?: {
    from: string;
    to: string;
  };
  search?: string;
}

export interface ChangeListState {
  changes: Change[];
  loading: boolean;
  error: string | null;
  filters: ChangeFilters;
  pagination: {
    currentPage: number;
    pageSize: number;
    total: number;
  };
}

export interface ChangeDetailState {
  change: Change | null;
  loading: boolean;
  error: string | null;
  approvals: ChangeApproval[];
  implementation?: ChangeImplementation;
}

export interface ChangeFormState {
  formData: Partial<Change>;
  validationErrors: Record<string, string>;
  isSubmitting: boolean;
}
