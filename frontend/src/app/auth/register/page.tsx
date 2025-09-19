"use client";
import { useState } from "react";
import { apiFetch } from "@/lib/api";
import { useRouter } from "next/navigation";
import Link from "next/link";
import SocialLogin from "@/app/components/SocialLogin";

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

  const handleSocialSuccess = () => {
    router.push("/");
  };

  const handleSocialError = (error: string) => {
    setError(error);
  };

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
      
      <SocialLogin onSuccess={handleSocialSuccess} onError={handleSocialError} />
      
      <div className="mt-3 text-center">
        <p className="text-sm text-neutral-400">Already have an account? <Link className="underline" href="/auth/login">Login</Link></p>
      </div>
    </div>
  );
}
