export type NotificationType =
  | "INCIDENT_CREATED"
  | "INCIDENT_ASSIGNED"
  | "CHANGE_APPROVED"
  | "REQUEST_FULFILLED"
  | "SLA_WARNING"
  | "SLA_BREACHED"
  | "SYSTEM_ALERT";

export type NotificationStatus = "UNREAD" | "READ";

export interface Notification {
  id: string;
  recipientId: string;
  subject: string;
  message: string;
  type: NotificationType;
  relatedEntityId?: string;
  relatedEntityType?: string;
  status: NotificationStatus;
  createdAt: string;
  readAt?: string;
}

export interface NotificationPreferences {
  emailNotifications: boolean;
  inAppNotifications: boolean;
  smsNotifications: boolean;
  incidentNotifications: boolean;
  changeNotifications: boolean;
  requestNotifications: boolean;
}

export interface NotificationState {
  notifications: Notification[];
  unreadCount: number;
  loading: boolean;
  error: string | null;
  preferences: NotificationPreferences;
}
