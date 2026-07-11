import React from "react";
import { useSelector, useDispatch } from "react-redux";
import { Bell, Trash2 } from "lucide-react";
import { RootState } from "@/store";
import { markAsRead, markAllAsRead, deleteNotification } from "@/store/slices/notificationSlice";
import Card from "@/components/common/Card";
import Button from "@/components/common/Button";
import Badge from "@/components/common/Badge";

const NotificationCenterPage: React.FC = () => {
  const dispatch = useDispatch();
  const { notifications, unreadCount } = useSelector(
    (state: RootState) => state.notifications,
  );

  const getNotificationColor = (type: string) => {
    switch (type) {
      case "INCIDENT":
        return "danger";
      case "CHANGE":
        return "warning";
      case "REQUEST":
        return "primary";
      case "PROBLEM":
        return "danger";
      default:
        return "primary";
    }
  };

  return (
    <div className="p-6">
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-secondary-900">Notifications</h1>
          <p className="text-secondary-600 mt-2">
            {unreadCount} unread notification{unreadCount !== 1 ? "s" : ""}
          </p>
        </div>
        {unreadCount > 0 && (
          <Button
            variant="secondary"
            size="sm"
            onClick={() => dispatch(markAllAsRead())}
          >
            Mark all as read
          </Button>
        )}
      </div>

      <Card>
        <div className="space-y-2">
          {notifications.length > 0 ? (
            notifications.map((notification) => (
              <div
                key={notification.id}
                className={`p-4 rounded-lg border-l-4 transition-colors ${
                  notification.status === "UNREAD"
                    ? "bg-primary-50 border-primary-500"
                    : "bg-secondary-50 border-secondary-300"
                }`}
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-1">
                      <Bell size={16} className="text-primary-600" />
                      <h3 className="font-semibold text-secondary-900">
                        {notification.subject}
                      </h3>
                      <Badge
                        variant={getNotificationColor(notification.type)}
                        size="sm"
                      >
                        {notification.type}
                      </Badge>
                      {notification.status === "UNREAD" && (
                        <div className="w-2 h-2 bg-primary-600 rounded-full"></div>
                      )}
                    </div>
                    <p className="text-secondary-700 mb-2">{notification.message}</p>
                    <p className="text-xs text-secondary-500">
                      {new Date(notification.createdAt).toLocaleString()}
                    </p>
                  </div>
                  <div className="flex gap-2 ml-4">
                    {notification.status === "UNREAD" && (
                      <Button
                        variant="secondary"
                        size="sm"
                        onClick={() => dispatch(markAsRead(notification.id))}
                      >
                        Mark as read
                      </Button>
                    )}
                    <button
                      onClick={() => dispatch(deleteNotification(notification.id))}
                      className="p-2 hover:bg-secondary-200 rounded-md transition-colors"
                    >
                      <Trash2 size={16} className="text-secondary-600" />
                    </button>
                  </div>
                </div>
              </div>
            ))
          ) : (
            <div className="text-center py-8">
              <Bell size={32} className="mx-auto text-secondary-400 mb-2" />
              <p className="text-secondary-600">No notifications</p>
            </div>
          )}
        </div>
      </Card>
    </div>
  );
};

export default NotificationCenterPage;
