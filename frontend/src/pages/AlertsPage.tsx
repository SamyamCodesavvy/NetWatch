import {
  useMutation,
  useQuery,
  useQueryClient,
} from "@tanstack/react-query";

import { alertApi } from "../api/client";

export default function AlertsPage() {
  const qc = useQueryClient();

  const { data: alerts } = useQuery({
    queryKey: ["alerts"],
    queryFn: () => alertApi.list().then((r) => r.data),
    refetchInterval: 15000,
  });

  const resolveMutation = useMutation({
    mutationFn: (id: number) => alertApi.resolve(id),

    onSuccess: () =>
      qc.invalidateQueries({
        queryKey: ["alerts"],
      }),
  });

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">
        Alerts
      </h1>

      <div className="space-y-2">
        {alerts?.map((a) => (
          <div
            key={a.id}
            className={`p-4 rounded border-l-4 bg-slate-900 ${
              a.severity === "critical"
                ? "border-red-500"
                : "border-yellow-500"
            }`}
          >
            <div className="flex justify-between">
              <span className="font-semibold">
                {a.rule_name} — {a.hostname}
              </span>

              <span className="text-xs text-slate-400">
                {a.status}
              </span>
            </div>

            <p className="text-sm text-slate-300 mt-1">
              {a.message}
            </p>

            {a.status !== "resolved" && (
              <button
                onClick={() =>
                  resolveMutation.mutate(a.id)
                }
                className="text-xs text-blue-400 hover:underline mt-2"
              >
                Mark Resolved
              </button>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}