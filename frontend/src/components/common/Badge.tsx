import React from "react";
import clsx from "clsx";

interface BadgeProps {
  variant?: "default" | "primary" | "success" | "warning" | "danger";
  size?: "sm" | "md" | "lg";
  children: React.ReactNode;
  icon?: React.ReactNode;
  className?: string;
}

const Badge: React.FC<BadgeProps> = ({
  variant = "default",
  size = "md",
  children,
  icon,
  className,
}) => {
  const variantStyles = {
    default: "bg-secondary-200 text-secondary-800",
    primary: "bg-primary-200 text-primary-800",
    success: "bg-success-200 text-success-800",
    warning: "bg-warning-200 text-warning-800",
    danger: "bg-danger-200 text-danger-800",
  };

  const sizeStyles = {
    sm: "px-2 py-0.5 text-xs",
    md: "px-3 py-1 text-sm",
    lg: "px-4 py-1.5 text-base",
  };

  return (
    <span
      className={clsx(
        "inline-flex items-center font-medium rounded-full",
        variantStyles[variant],
        sizeStyles[size],
        className,
      )}
    >
      {icon && <span className="mr-1">{icon}</span>}
      {children}
    </span>
  );
};

export default Badge;
