import { useQuery } from "@tanstack/react-query";
import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import { dashboardApi } from "../api/client";
import { StatCard } from "../components/StatCard";

export default function DashboardPage() {
  const { data, isLoading } = useQuery({
    queryKey: ["dashboard"],
    queryFn: () => dashboardApi.get().then((r) => r.data),
    refetchInterval: 30000,
  });

  if (isLoading || !data) {
    return <div>Loading dashboard...</div>;
  }

  const s = data.stats;

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">
        Infrastructure Overview
      </h1>

      <div className="grid grid-cols-2 md:grid-cols-6 gap-4 mb-8">
        <StatCard
          label="Devices"
          value={s.total_devices}
          color="border-blue-500"
        />

        <StatCard
          label="Online"
          value={s.online}
          color="border-green-500"
        />

        <StatCard
          label="Offline"
          value={s.offline}
          color="border-red-500"
        />

        <StatCard
          label="Open Alerts"
          value={s.open_alerts}
          color="border-yellow-500"
        />

        <StatCard
          label="Critical"
          value={s.critical_alerts}
          color="border-red-600"
        />

        <StatCard
          label="Warnings"
          value={s.warning_alerts}
          color="border-yellow-400"
        />
      </div>

      <div className="bg-slate-900 rounded-lg p-4">
        <h2 className="text-lg font-semibold mb-4">
          Average Latency — Last 24h
        </h2>

        <ResponsiveContainer width="100%" height={280}>
          <LineChart data={data.latency_trend}>
            <CartesianGrid
              strokeDasharray="3 3"
              stroke="#334155"
            />

            <XAxis
              dataKey="hour"
              stroke="#94a3b8"
            />

            <YAxis stroke="#94a3b8" />

            <Tooltip
              contentStyle={{
                background: "#1e293b",
                border: "none",
              }}
            />

            <Line
              type="monotone"
              dataKey="avg_latency_ms"
              stroke="#3b82f6"
              strokeWidth={2}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}