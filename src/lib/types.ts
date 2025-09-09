export type JobStatus =
  | "COMPLETED"
  | "RUNNING"
  | "QUEUED"
  | "ERROR"
  | "CANCELLED";

export interface Job {
  id: string;
  status: JobStatus;
  backend: string;
  submitted: string; // ISO timestamp or human-readable
  elapsed_time: number;
  user: string;
  qpu_seconds: number;
  logs: string[];
  results: Record<string, any> | null;
  status_history: { status: JobStatus; timestamp: string }[];
}

export interface Backend {
  name: string;
  status: "active" | "inactive" | "maintenance";
  qubit_count: number;
  queue_depth: number;
  error_rate: number;
}

export interface Metrics {
  live_jobs: number;      // jobs currently running/queued
  avg_wait_time: number;  // in seconds
  success_rate: number;   // percentage (0–100)
  open_sessions: number;  // active user sessions
}

/**
 * ChartData format:
 * - `time`: timestamp label (string)
 * - job counts by status at that time
 */
export interface ChartData {
  time: string;
  COMPLETED: number;
  RUNNING: number;
  QUEUED: number;
  ERROR: number;
}

export interface Anomaly {
  jobId: string;
  anomalyDescription: string;
  severity: "low" | "medium" | "high";
}
