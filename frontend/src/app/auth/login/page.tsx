"use client";
import { useState } from "react";
import { apiFetch, saveTokens } from "@/lib/api";
import { useRouter } from "next/navigation";
import Link from "next/link";

export default function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    try {
      const data = await apiFetch<{ access: string; refresh: string }>("/auth/login/", {
        method: "POST",
        body: { username, password },
      });
      saveTokens(data.access, data.refresh);
      router.push("/");
    } catch (err: any) {
      setError(err.message);
    }
  }

  return (
    <div className="max-w-sm mx-auto">
      <h1 className="text-xl font-semibold mb-4">Login</h1>
      <form onSubmit={onSubmit} className="space-y-3">
        <input className="w-full px-3 py-2 bg-neutral-900 border border-neutral-800 rounded" placeholder="Username" value={username} onChange={e=>setUsername(e.target.value)} />
        <input type="password" className="w-full px-3 py-2 bg-neutral-900 border border-neutral-800 rounded" placeholder="Password" value={password} onChange={e=>setPassword(e.target.value)} />
        {error && <p className="text-red-400 text-sm">{error}</p>}
        <button className="w-full bg-white text-black py-2 rounded">Sign in</button>
      </form>
      <div className="mt-3 space-y-2">
        <p className="text-sm text-neutral-400">No account? <Link className="underline" href="/auth/register">Register</Link></p>
        <p className="text-sm text-neutral-400">Forgot password? <Link className="underline" href="/auth/forgot-password">Reset it</Link></p>
      </div>
    </div>
  );
}
