import React, { ReactNode, ErrorInfo } from "react";
import { AlertCircle } from "lucide-react";
import Button from "./Button";

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

class ErrorBoundary extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error("Error caught by boundary:", error, errorInfo);
  }

  handleReset = () => {
    this.setState({ hasError: false, error: null });
  };

  render() {
    if (this.state.hasError) {
      return (
        this.props.fallback || (
          <div className="flex items-center justify-center min-h-screen bg-secondary-50">
            <div className="bg-white rounded-lg shadow-lg p-8 max-w-md">
              <div className="flex items-center justify-center mb-4">
                <AlertCircle size={48} className="text-danger-600" />
              </div>
              <h1 className="text-2xl font-bold text-secondary-900 mb-2 text-center">
                Oops! Something went wrong
              </h1>
              <p className="text-secondary-600 mb-4 text-center">
                {this.state.error?.message || "An unexpected error occurred"}
              </p>
              <div className="flex gap-2">
                <Button variant="secondary" fullWidth onClick={this.handleReset}>
                  Try Again
                </Button>
                <Button
                  variant="primary"
                  fullWidth
                  onClick={() => (window.location.href = "/")}
                >
                  Go Home
                </Button>
              </div>
              {process.env.NODE_ENV === "development" && (
                <details className="mt-4 p-2 bg-secondary-100 rounded text-xs">
                  <summary className="cursor-pointer font-semibold">Error Details</summary>
                  <pre className="mt-2 overflow-auto text-danger-600">
                    {this.state.error?.stack}
                  </pre>
                </details>
              )}
            </div>
          </div>
        )
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
