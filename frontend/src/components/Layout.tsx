import { Link, Outlet } from "react-router-dom";

import { useAuth } from "../context/AuthContext";

export default function Layout() {
  const { user, logout } = useAuth();

  return (
    <div>
      <nav className="bg-slate-900 border-b border-blue-500 px-6 py-3 flex items-center gap-6">
        <span className="text-blue-400 font-bold text-xl">
          🛰 NetWatch
        </span>

        <Link
          to="/dashboard"
          className="hover:text-blue-400"
        >
          Dashboard
        </Link>

        <Link
          to="/devices"
          className="hover:text-blue-400"
        >
          Devices
        </Link>

        <Link
          to="/alerts"
          className="hover:text-blue-400"
        >
          Alerts
        </Link>

        <span className="ml-auto text-sm text-slate-400">
          {user?.username}
        </span>

        <button
          onClick={logout}
          className="text-sm text-red-400 hover:underline"
        >
          Logout
        </button>
      </nav>

      <main className="p-6">
        <Outlet />
      </main>
    </div>
  );
}