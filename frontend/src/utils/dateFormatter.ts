export const formatDate = (dateValue: string | Date | null | undefined): string => {
  if (!dateValue) {
    return "";
  }

  try {
    const date = typeof dateValue === "string" ? new Date(dateValue) : dateValue;

    if (isNaN(date.getTime())) {
      return "Invalid Date";
    }

    return date.toLocaleDateString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
    });
  } catch (error) {
    return "Invalid Date";
  }
};

export const formatDateTime = (dateValue: string | Date | null | undefined): string => {
  if (!dateValue) {
    return "";
  }

  try {
    const date = typeof dateValue === "string" ? new Date(dateValue) : dateValue;

    if (isNaN(date.getTime())) {
      return "Invalid Date";
    }

    return date.toLocaleDateString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  } catch (error) {
    return "Invalid Date";
  }
};
