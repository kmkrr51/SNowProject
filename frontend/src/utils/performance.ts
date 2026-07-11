export interface PerformanceMetrics {
  name: string;
  duration: number;
  timestamp: number;
}

const metrics: PerformanceMetrics[] = [];

export const startMeasure = (name: string) => {
  if (typeof window !== "undefined" && window.performance) {
    window.performance.mark(`${name}-start`);
  }
};

export const endMeasure = (name: string) => {
  if (typeof window !== "undefined" && window.performance) {
    window.performance.mark(`${name}-end`);
    try {
      window.performance.measure(name, `${name}-start`, `${name}-end`);
      const measure = window.performance.getEntriesByName(name)[0];
      if (measure) {
        metrics.push({
          name,
          duration: measure.duration,
          timestamp: Date.now(),
        });

        if (process.env.NODE_ENV === "development") {
          console.log(`[Performance] ${name}: ${measure.duration.toFixed(2)}ms`);
        }
      }
    } catch (e) {
      console.error("Performance measurement error:", e);
    }
  }
};

export const getMetrics = (): PerformanceMetrics[] => {
  return [...metrics];
};

export const clearMetrics = () => {
  metrics.length = 0;
};

export const reportMetrics = () => {
  if (process.env.NODE_ENV === "production" && metrics.length > 0) {
    const avgDuration = metrics.reduce((sum, m) => sum + m.duration, 0) / metrics.length;
    console.log(`[Performance Report] Average duration: ${avgDuration.toFixed(2)}ms`);
  }
};
