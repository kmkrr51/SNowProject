import React from "react";
import clsx from "clsx";

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  helpText?: string;
  icon?: React.ReactNode;
}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, helpText, icon, className, ...props }, ref) => {
    return (
      <div className="w-full">
        {label && (
          <label className="block text-sm font-medium text-secondary-700 mb-1">
            {label}
            {props.required && <span className="text-danger-600 ml-1">*</span>}
          </label>
        )}
        <div className="relative">
          {icon && <div className="absolute left-3 top-3 text-secondary-400">{icon}</div>}
          <input
            ref={ref}
            className={clsx(
              "w-full px-3 py-2 border rounded-md text-secondary-900 placeholder-secondary-400",
              "focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent",
              "transition-colors duration-200",
              icon && "pl-10",
              error
                ? "border-danger-500 focus:ring-danger-500"
                : "border-secondary-300 focus:ring-primary-500",
              className,
            )}
            {...props}
          />
        </div>
        {error && <p className="mt-1 text-sm text-danger-600">{error}</p>}
        {helpText && !error && <p className="mt-1 text-sm text-secondary-500">{helpText}</p>}
      </div>
    );
  },
);

Input.displayName = "Input";

export default Input;
