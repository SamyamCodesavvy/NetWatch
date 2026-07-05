import { useState, type FormEvent } from "react";
import { useNavigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext";

export default function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const { login } = useAuth();
  const navigate = useNavigate();

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError("");

    try {
      await login(username, password);
      navigate("/dashboard");
    } catch {
      setError("Invalid username or password");
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center">
      <form
        onSubmit={handleSubmit}
        className="bg-slate-900 p-8 rounded-lg w-80 border border-blue-500"
      >
        <h1 className="text-2xl font-bold text-blue-400 mb-6">
          🛰 NetWatch
        </h1>

        {error && (
          <p className="text-red-400 text-sm mb-3">
            {error}
          </p>
        )}

        <input
          className="w-full mb-3 p-2 rounded bg-slate-800 border border-slate-700"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />

        <input
          className="w-full mb-4 p-2 rounded bg-slate-800 border border-slate-700"
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <button className="w-full bg-blue-600 hover:bg-blue-500 rounded p-2 font-semibold">
          Log In
        </button>
      </form>
    </div>
  );
}