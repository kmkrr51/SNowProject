export type ProblemStatus = "IDENTIFIED" | "INVESTIGATING" | "RESOLVED" | "CLOSED";

export interface Problem {
  id: string;
  title: string;
  description: string;
  status: ProblemStatus;
  rootCause?: string;
  relatedIncidents: string[];
  impactedServices: string[];
  createdBy: string;
  createdAt: string;
  updatedAt: string;
  resolvedAt?: string;
}

export interface RCARecord {
  id: string;
  problemId: string;
  analysisDetails: string;
  contributingFactors: string[];
  timeline: string;
  createdAt: string;
}

export interface KnownError {
  id: string;
  problemId: string;
  workaround?: string;
  temporaryFix?: string;
  permanentFix?: string;
  status: "ACTIVE" | "RESOLVED";
  createdAt: string;
}

export interface ProblemFilters {
  status?: ProblemStatus[];
  dateRange?: {
    from: string;
    to: string;
  };
  search?: string;
}

export interface ProblemListState {
  problems: Problem[];
  loading: boolean;
  error: string | null;
  filters: ProblemFilters;
  pagination: {
    currentPage: number;
    pageSize: number;
    total: number;
  };
}

export interface ProblemDetailState {
  problem: Problem | null;
  loading: boolean;
  error: string | null;
  rcaRecords: RCARecord[];
  knownErrors: KnownError[];
}

export interface ProblemFormState {
  formData: Partial<Problem>;
  validationErrors: Record<string, string>;
  isSubmitting: boolean;
}
