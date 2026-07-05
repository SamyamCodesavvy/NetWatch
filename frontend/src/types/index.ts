export interface User {
  id: number;
  username: string;
  email: string;
  role: "admin" | "operator" | "viewer";
  is_active: boolean;
  created_at: string;
}

export interface Device {
  id: number;
  hostname: string;
  ip_address: string | null;
  domain_name: string | null;
  operating_system: string | null;
  environment: "dev" | "staging" | "prod";
  owner: string | null;
  ssh_port: number;
  http_port: number;
  https_port: number;
  monitoring_enabled: boolean;
  created_at: string;
}

export interface Alert {
  id: number;
  device_id: number;
  hostname: string | null;
  rule_name: string;
  severity: "warning" | "critical";
  message: string | null;
  status: "open" | "acknowledged" | "resolved";
  triggered_at: string;
  resolved_at: string | null;
}

export interface DashboardStats {
  stats: {
    total_devices: number;
    online: number;
    offline: number;
    open_alerts: number;
    critical_alerts: number;
    warning_alerts: number;
  };
  latency_trend: {
    hour: number;
    avg_latency_ms: number;
  }[];
  latest_alerts: Alert[];
}