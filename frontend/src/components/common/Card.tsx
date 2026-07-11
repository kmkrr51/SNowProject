import React from "react";
import clsx from "clsx";

interface CardProps {
  title?: string;
  subtitle?: string;
  children: React.ReactNode;
  footer?: React.ReactNode;
  padding?: "sm" | "md" | "lg";
  bordered?: boolean;
  hoverable?: boolean;
  className?: string;
}

const Card: React.FC<CardProps> = ({
  title,
  subtitle,
  children,
  footer,
  padding = "md",
  bordered = true,
  hoverable = false,
  className,
}) => {
  const paddingStyles = {
    sm: "p-3",
    md: "p-4",
    lg: "p-6",
  };

  return (
    <div
      className={clsx(
        "bg-white rounded-lg shadow-md",
        bordered && "border border-secondary-200",
        hoverable && "hover:shadow-lg transition-shadow duration-200 cursor-pointer",
        className,
      )}
    >
      {(title || subtitle) && (
        <div className={clsx(paddingStyles[padding], "border-b border-secondary-200")}>
          {title && <h3 className="text-lg font-semibold text-secondary-900">{title}</h3>}
          {subtitle && <p className="text-sm text-secondary-500 mt-1">{subtitle}</p>}
        </div>
      )}
      <div className={paddingStyles[padding]}>{children}</div>
      {footer && (
        <div className={clsx(paddingStyles[padding], "border-t border-secondary-200")}>
          {footer}
        </div>
      )}
    </div>
  );
};

export default Card;
