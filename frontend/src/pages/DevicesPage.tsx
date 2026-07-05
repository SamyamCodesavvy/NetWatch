// frontend/src/pages/DevicesPage.tsx

import { useState } from "react";

import {
  useMutation,
  useQuery,
  useQueryClient,
} from "@tanstack/react-query";

import { deviceApi } from "../api/client";

export default function DevicesPage() {
  const qc = useQueryClient();

  const [hostname, setHostname] = useState("");
  const [ip, setIp] = useState("");

  const { data: devices } = useQuery({
    queryKey: ["devices"],
    queryFn: () => deviceApi.list().then((r) => r.data),
  });

  const createMutation = useMutation({
    mutationFn: () =>
      deviceApi.create({
        hostname,
        ip_address: ip,
      }),

    onSuccess: () => {
      qc.invalidateQueries({
        queryKey: ["devices"],
      });

      setHostname("");
      setIp("");
    },
  });

  const deleteMutation = useMutation({
    mutationFn: (id: number) => deviceApi.delete(id),

    onSuccess: () =>
      qc.invalidateQueries({
        queryKey: ["devices"],
      }),
  });

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">
        Device Inventory
      </h1>

      <div className="flex gap-2 mb-6">
        <input
          className="p-2 rounded bg-slate-800 border border-slate-700"
          placeholder="Hostname"
          value={hostname}
          onChange={(e) => setHostname(e.target.value)}
        />

        <input
          className="p-2 rounded bg-slate-800 border border-slate-700"
          placeholder="IP Address"
          value={ip}
          onChange={(e) => setIp(e.target.value)}
        />

        <button
          onClick={() => createMutation.mutate()}
          className="bg-blue-600 hover:bg-blue-500 px-4 rounded"
        >
          Add Device
        </button>
      </div>

      <table className="w-full text-sm">
        <thead className="bg-slate-900">
          <tr>
            <th className="p-3 text-left">
              Hostname
            </th>

            <th className="p-3 text-left">
              IP
            </th>

            <th className="p-3 text-left">
              Env
            </th>

            <th className="p-3 text-left"></th>
          </tr>
        </thead>

        <tbody>
          {devices?.map((d) => (
            <tr
              key={d.id}
              className="border-t border-slate-800"
            >
              <td className="p-3">
                {d.hostname}
              </td>

              <td className="p-3 font-mono text-xs">
                {d.ip_address}
              </td>

              <td className="p-3">
                {d.environment}
              </td>

              <td className="p-3">
                <button
                  onClick={() => deleteMutation.mutate(d.id)}
                  className="text-red-400 hover:underline text-xs"
                >
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}