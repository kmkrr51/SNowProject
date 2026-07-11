# React Frontend - Component Specifications

**Status:** PLANNING PHASE
**Date:** 2026-07-10

---

## 1. Common Components Specification

### 1.1 Button Component

**Props:**
```typescript
interface ButtonProps {
  variant: 'primary' | 'secondary' | 'danger' | 'success' | 'warning';
  size: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  loading?: boolean;
  icon?: ReactNode;
  onClick?: () => void;
  children: ReactNode;
  className?: string;
  type?: 'button' | 'submit' | 'reset';
  fullWidth?: boolean;
}
```

**Variants:**
- Primary (blue background)
- Secondary (gray background)
- Danger (red background)
- Success (green background)
- Warning (orange background)

**States:**
- Normal
- Hover
- Active
- Disabled
- Loading (with spinner)

---

### 1.2 Input Component

**Props:**
```typescript
interface InputProps {
  type: 'text' | 'email' | 'password' | 'number' | 'date' | 'time';
  label?: string;
  placeholder?: string;
  value?: string;
  onChange?: (value: string) => void;
  error?: string;
  disabled?: boolean;
  required?: boolean;
  icon?: ReactNode;
  helpText?: string;
  className?: string;
}
```

**Features:**
- Label with required indicator
- Error message display
- Helper text
- Icon support
- Disabled state
- Focus state styling

---

### 1.3 Select Component

**Props:**
```typescript
interface SelectProps {
  label?: string;
  options: Array<{ value: string; label: string }>;
  value?: string;
  onChange?: (value: string) => void;
  error?: string;
  disabled?: boolean;
  searchable?: boolean;
  clearable?: boolean;
  placeholder?: string;
  required?: boolean;
}
```

**Features:**
- Dropdown with options
- Search functionality
- Clear button
- Disabled state
- Error display
- Custom option rendering

---

### 1.4 Table Component

**Props:**
```typescript
interface TableProps {
  columns: Array<{
    key: string;
    header: string;
    sortable?: boolean;
    render?: (value: any, row: any) => ReactNode;
  }>;
  data: any[];
  loading?: boolean;
  error?: string;
  onSort?: (key: string, direction: 'asc' | 'desc') => void;
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
```

**Features:**
- Sortable columns
- Row selection
- Pagination
- Loading state
- Error state
- Custom cell rendering
- Hover effects

---

### 1.5 Modal Component

**Props:**
```typescript
interface ModalProps {
  isOpen: boolean;
  title: string;
  children: ReactNode;
  onClose: () => void;
  actions?: Array<{
    label: string;
    onClick: () => void;
    variant: 'primary' | 'secondary' | 'danger';
  }>;
  size?: 'sm' | 'md' | 'lg';
  closeButton?: boolean;
}
```

**Features:**
- Overlay backdrop
- Close button
- Action buttons
- Size variants
- Keyboard support (ESC to close)
- Focus trap

---

### 1.6 Badge Component

**Props:**
```typescript
interface BadgeProps {
  variant: 'default' | 'primary' | 'success' | 'warning' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  children: ReactNode;
  icon?: ReactNode;
  className?: string;
}
```

**Variants:**
- Default (gray)
- Primary (blue)
- Success (green)
- Warning (orange)
- Danger (red)

---

### 1.7 Card Component

**Props:**
```typescript
interface CardProps {
  title?: string;
  subtitle?: string;
  children: ReactNode;
  footer?: ReactNode;
  padding?: 'sm' | 'md' | 'lg';
  bordered?: boolean;
  hoverable?: boolean;
  className?: string;
}
```

**Features:**
- Title and subtitle
- Padding options
- Border option
- Hover effect
- Footer section

---

### 1.8 Loading Component

**Props:**
```typescript
interface LoadingProps {
  type: 'spinner' | 'skeleton' | 'dots' | 'bar';
  size?: 'sm' | 'md' | 'lg';
  message?: string;
  fullScreen?: boolean;
}
```

**Types:**
- Spinner (rotating circle)
- Skeleton (placeholder)
- Dots (animated dots)
- Progress bar

---

### 1.9 Pagination Component

**Props:**
```typescript
interface PaginationProps {
  currentPage: number;
  totalPages: number;
  pageSize: number;
  total: number;
  onPageChange: (page: number) => void;
  onPageSizeChange?: (size: number) => void;
  pageSizeOptions?: number[];
}
```

**Features:**
- Previous/Next buttons
- Page number buttons
- Go to page input
- Page size selector
- Total count display

---

## 2. Domain-Specific Components

### 2.1 Incident Components

#### IncidentList Component
**Props:**
```typescript
interface IncidentListProps {
  incidents: Incident[];
  loading: boolean;
  error?: string;
  filters: IncidentFilters;
  onFilterChange: (filters: IncidentFilters) => void;
  onIncidentClick: (incident: Incident) => void;
  onCreateClick: () => void;
}
```

**Features:**
- Searchable table
- Filter panel
- Bulk actions
- Create button
- Pagination

---

#### IncidentDetail Component
**Props:**
```typescript
interface IncidentDetailProps {
  incident: Incident;
  loading: boolean;
  error?: string;
  onAssign: (technicianId: string) => void;
  onStatusChange: (status: string) => void;
  onResolve: () => void;
  onClose: () => void;
  onAddWorkNote: (content: string) => void;
}
```

**Sections:**
- Basic information
- Status timeline
- SLA status
- Work notes
- Related problems
- Action buttons

---

#### SLAStatus Component
**Props:**
```typescript
interface SLAStatusProps {
  responseTimeRemaining: number; // in minutes
  resolutionTimeRemaining: number; // in minutes
  status: 'on-track' | 'warning' | 'breached';
  priority: 'critical' | 'high' | 'medium' | 'low';
}
```

**Features:**
- Countdown timers
- Color-coded status
- Warning indicators
- Progress bars

---

### 2.2 Problem Components

#### ProblemList Component
**Props:**
```typescript
interface ProblemListProps {
  problems: Problem[];
  loading: boolean;
  filters: ProblemFilters;
  onFilterChange: (filters: ProblemFilters) => void;
  onProblemClick: (problem: Problem) => void;
  onCreateClick: () => void;
}
```

---

#### RCAWorkflow Component
**Props:**
```typescript
interface RCAWorkflowProps {
  problem: Problem;
  onStartRCA: () => void;
  onCompleteRCA: (rootCause: string) => void;
  onCreateKnownError: (error: KnownError) => void;
}
```

**Sections:**
- RCA status
- Start RCA button
- RCA details form
- Root cause input
- Known errors list

---

### 2.3 Change Components

#### ChangeList Component
**Props:**
```typescript
interface ChangeListProps {
  changes: Change[];
  loading: boolean;
  filters: ChangeFilters;
  onFilterChange: (filters: ChangeFilters) => void;
  onChangeClick: (change: Change) => void;
  onCreateClick: () => void;
}
```

---

#### ChangeApprovalWorkflow Component
**Props:**
```typescript
interface ChangeApprovalWorkflowProps {
  change: Change;
  canApprove: boolean;
  onApprove: (comments?: string) => void;
  onReject: (reason: string) => void;
  onImplement: () => void;
  onRollback: () => void;
}
```

**Sections:**
- Approval status
- Approver comments
- Approve/Reject buttons
- Implementation section
- Rollback option

---

### 2.4 Request Components

#### RequestList Component
**Props:**
```typescript
interface RequestListProps {
  requests: ServiceRequest[];
  loading: boolean;
  filters: RequestFilters;
  onFilterChange: (filters: RequestFilters) => void;
  onRequestClick: (request: ServiceRequest) => void;
  onCreateClick: () => void;
}
```

---

#### TaskList Component
**Props:**
```typescript
interface TaskListProps {
  tasks: Task[];
  onAddTask: (task: Task) => void;
  onCompleteTask: (taskIndex: number) => void;
  onDeleteTask: (taskIndex: number) => void;
  progress: number;
}
```

**Features:**
- Add task form
- Task list with checkboxes
- Delete button
- Progress bar
- Completion percentage

---

## 3. Layout Components

### 3.1 Header Component
**Features:**
- Logo
- Search bar
- Notification bell
- User menu
- Responsive hamburger menu

---

### 3.2 Sidebar Component
**Features:**
- Navigation menu
- Collapsible sections
- Active link highlighting
- Collapse/expand toggle
- Responsive behavior

---

### 3.3 Footer Component
**Features:**
- Copyright info
- Links
- Version info
- Support contact

---

## 4. Form Components

### 4.1 IncidentForm Component
**Fields:**
- Title (required)
- Description (required)
- Priority (dropdown)
- Impact Level (dropdown)
- Urgency Level (dropdown)
- Submit/Cancel buttons

---

### 4.2 ProblemForm Component
**Fields:**
- Title (required)
- Description (required)
- Related Incidents (multi-select)
- Submit/Cancel buttons

---

### 4.3 ChangeForm Component
**Fields:**
- Title (required)
- Description (required)
- Change Type (dropdown)
- Risk Level (dropdown)
- Impact Assessment (textarea)
- Rollback Plan (textarea)
- Submit/Cancel buttons

---

### 4.4 RequestForm Component
**Fields:**
- Request Type (dropdown)
- Title (required)
- Description (required)
- Requested Service (dropdown)
- Priority (dropdown)
- Submit/Cancel buttons

---

## 5. Filter Components

### 5.1 IncidentFilters Component
**Filters:**
- Status (multi-select)
- Priority (multi-select)
- Assigned To (dropdown)
- Date Range
- Search (text)

---

### 5.2 ProblemFilters Component
**Filters:**
- Status (multi-select)
- Date Range
- Search (text)

---

### 5.3 ChangeFilters Component
**Filters:**
- Status (multi-select)
- Risk Level (multi-select)
- Change Type (multi-select)
- Date Range
- Search (text)

---

### 5.4 RequestFilters Component
**Filters:**
- Status (multi-select)
- Priority (multi-select)
- Request Type (multi-select)
- Date Range
- Search (text)

---

## 6. Dashboard Components

### 6.1 MetricsCard Component
**Props:**
```typescript
interface MetricsCardProps {
  title: string;
  value: number | string;
  unit?: string;
  trend?: 'up' | 'down' | 'stable';
  trendValue?: number;
  icon?: ReactNode;
  onClick?: () => void;
}
```

---

### 6.2 Chart Component
**Props:**
```typescript
interface ChartProps {
  type: 'line' | 'bar' | 'pie' | 'doughnut';
  title: string;
  data: any;
  options?: any;
  height?: number;
}
```

---

### 6.3 RecentActivity Component
**Props:**
```typescript
interface RecentActivityProps {
  activities: Activity[];
  loading: boolean;
  onActivityClick: (activity: Activity) => void;
}
```

---

## 7. Search Components

### 7.1 SearchBar Component
**Props:**
```typescript
interface SearchBarProps {
  onSearch: (query: string) => void;
  placeholder?: string;
  loading?: boolean;
  suggestions?: string[];
}
```

---

### 7.2 SearchResults Component
**Props:**
```typescript
interface SearchResultsProps {
  results: SearchResult[];
  query: string;
  loading: boolean;
  error?: string;
  onResultClick: (result: SearchResult) => void;
  filters: SearchFilters;
  onFilterChange: (filters: SearchFilters) => void;
}
```

---

## 8. Notification Components

### 8.1 NotificationCenter Component
**Props:**
```typescript
interface NotificationCenterProps {
  notifications: Notification[];
  unreadCount: number;
  onMarkAsRead: (notificationId: string) => void;
  onNotificationClick: (notification: Notification) => void;
}
```

---

### 8.2 NotificationItem Component
**Props:**
```typescript
interface NotificationItemProps {
  notification: Notification;
  onMarkAsRead: () => void;
  onClick: () => void;
}
```

---

## 9. Audit Components

### 9.1 AuditTrail Component
**Props:**
```typescript
interface AuditTrailProps {
  entityType: string;
  entityId: string;
  logs: AuditLog[];
  loading: boolean;
  filters: AuditFilters;
  onFilterChange: (filters: AuditFilters) => void;
}
```

---

### 9.2 AuditLog Component
**Props:**
```typescript
interface AuditLogProps {
  log: AuditLog;
  onExpand?: () => void;
}
```

**Displays:**
- Timestamp
- Action
- Actor
- Changes
- Details (expandable)

---

## 10. Page Components

### 10.1 IncidentPage
**Layout:**
- Header with create button
- Filter panel
- Incident list
- Detail modal/drawer

---

### 10.2 DashboardPage
**Layout:**
- Metrics cards
- Charts
- Recent activity
- Quick actions

---

### 10.3 SearchPage
**Layout:**
- Search bar
- Filter panel
- Results list
- Pagination

---

## 11. Accessibility Features

### All Components Should Include:
- ARIA labels
- Keyboard navigation
- Focus management
- Color contrast compliance
- Screen reader support
- Semantic HTML

---

## 12. Responsive Design

### Breakpoints:
- Mobile: < 640px
- Tablet: 640px - 1024px
- Desktop: > 1024px

### Component Behavior:
- Stack vertically on mobile
- Collapse sidebar on mobile
- Hide non-essential columns on tablet
- Full layout on desktop

---

## 13. Styling Approach

### Tailwind CSS Classes:
- Use utility classes
- Create component-specific classes
- Maintain consistent spacing
- Use color variables
- Support dark mode

---

## 14. State Management Integration

### Redux Integration:
- Connect components to Redux store
- Use selectors for data
- Dispatch actions for mutations
- Use thunks for async operations

---

## 15. Error Handling

### Error Display:
- Error boundaries
- Toast notifications
- Error messages in forms
- Error pages (404, 500)

---

## 16. Loading States

### Loading Indicators:
- Skeleton loaders
- Spinners
- Progress bars
- Disabled buttons

---

## 17. Animation & Transitions

### Animations:
- Page transitions
- Modal animations
- Hover effects
- Loading animations
- Status change animations

---

## 18. Performance Considerations

### Optimization:
- Memoization (React.memo)
- Code splitting
- Lazy loading
- Image optimization
- Debouncing/Throttling

---

## Conclusion

This specification provides detailed guidelines for building all React components. Each component should follow these specifications for consistency, maintainability, and user experience.

---

**Document Version:** 1.0
**Last Updated:** 2026-07-10
