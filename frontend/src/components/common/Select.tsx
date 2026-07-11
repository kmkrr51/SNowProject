import React from "react";
import clsx from "clsx";
import { ChevronDown } from "lucide-react";

interface SelectOption {
  value: string;
  label: string;
}

interface SelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  label?: string;
  options: SelectOption[];
  error?: string;
  helpText?: string;
  placeholder?: string;
}

const Select = React.forwardRef<HTMLSelectElement, SelectProps>(
  ({ label, options, error, helpText, placeholder, className, ...props }, ref) => {
    return (
      <div className="w-full">
        {label && (
          <label className="block text-sm font-medium text-secondary-700 mb-1">
            {label}
            {props.required && <span className="text-danger-600 ml-1">*</span>}
          </label>
        )}
        <div className="relative">
          <select
            ref={ref}
            className={clsx(
              "w-full px-3 py-2 border rounded-md text-secondary-900 bg-white appearance-none",
              "focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent",
              "transition-colors duration-200 cursor-pointer",
              error
                ? "border-danger-500 focus:ring-danger-500"
                : "border-secondary-300 focus:ring-primary-500",
              className,
            )}
            {...props}
          >
            {placeholder && <option value="">{placeholder}</option>}
            {options.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
          <ChevronDown
            size={20}
            className="absolute right-3 top-2.5 text-secondary-400 pointer-events-none"
          />
        </div>
        {error && <p className="mt-1 text-sm text-danger-600">{error}</p>}
        {helpText && !error && <p className="mt-1 text-sm text-secondary-500">{helpText}</p>}
      </div>
    );
  },
);

Select.displayName = "Select";

export default Select;
