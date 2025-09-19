"use client";
import Link from "next/link";
import { useEffect, useState } from "react";
import { apiFetch, isAuthenticated } from "@/lib/api";
import { useRouter } from "next/navigation";

type Thread = { id: number; title: string; updated_at: string };

export default function HistoryPage() {
  const router = useRouter();
  const [threads, setThreads] = useState<Thread[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!isAuthenticated()) {
      router.push('/auth/login');
      return;
    }
    (async () => {
      try { setThreads(await apiFetch<Thread[]>("/chat/threads/")); } catch (e:any) { setError(e.message); }
    })();
  }, []);

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-semibold">History</h1>
      {error && <p className="text-red-400 text-sm">{error}</p>}
      <div className="space-y-2">
        {threads.map(t => (
          <Link key={t.id} href={`/history/${t.id}`} className="block border border-neutral-800 rounded p-3 hover:bg-neutral-900">
            <div className="font-medium">{t.title}</div>
            <div className="text-xs text-neutral-400">{new Date(t.updated_at).toLocaleString()}</div>
          </Link>
        ))}
        {threads.length===0 && !error && <div className="text-neutral-400">No threads yet.</div>}
      </div>
    </div>
  );
} 