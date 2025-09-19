"use client";
import { useState } from "react";
import { apiFetch } from "@/lib/api";
import { useRouter } from "next/navigation";

export default function RegisterPage() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    try {
      await apiFetch("/auth/register/", { method: "POST", body: { username, email, password } });
      router.push("/auth/login");
    } catch (err: any) {
      setError(err.message);
    }
  }

  return (
    <div className="max-w-sm mx-auto">
      <h1 className="text-xl font-semibold mb-4">Create account</h1>
      <form onSubmit={onSubmit} className="space-y-3">
        <input className="w-full px-3 py-2 bg-neutral-900 border border-neutral-800 rounded" placeholder="Username" value={username} onChange={e=>setUsername(e.target.value)} />
        <input className="w-full px-3 py-2 bg-neutral-900 border border-neutral-800 rounded" placeholder="Email (optional)" value={email} onChange={e=>setEmail(e.target.value)} />
        <input type="password" className="w-full px-3 py-2 bg-neutral-900 border border-neutral-800 rounded" placeholder="Password" value={password} onChange={e=>setPassword(e.target.value)} />
        {error && <p className="text-red-400 text-sm">{error}</p>}
        <button className="w-full bg-white text-black py-2 rounded">Sign up</button>
      </form>
    </div>
  );
} 