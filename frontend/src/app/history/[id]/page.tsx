"use client";
import Link from "next/link";
import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";

interface Params { params: { id: string } }

type Message = { id: number; role: string; content: string; created_at: string };
type Thread = { id: number; title: string; created_at: string; updated_at: string; messages: Message[] };

export default function ThreadDetail({ params }: Params) {
  const threadId = Number(params.id);
  const [thread, setThread] = useState<Thread | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    (async () => {
      try { setThread(await apiFetch<Thread>(`/chat/threads/${threadId}/`)); } catch (e:any) { setError(e.message); }
    })();
  }, [threadId]);

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-3">
        <Link href="/history" className="text-sm underline">← Back to History</Link>
      </div>
      {error && <p className="text-red-400 text-sm">{error}</p>}
      {thread && (
        <div className="space-y-3">
          <h1 className="text-2xl font-semibold">{thread.title}</h1>
          <div className="space-y-2">
            {thread.messages.map(m => (
              <div key={m.id} className="rounded border border-neutral-800 p-2">
                <div className="text-xs text-neutral-400">{m.role} • {new Date(m.created_at).toLocaleString()}</div>
                <div>{m.content}</div>
              </div>
            ))}
            {thread.messages.length===0 && <div className="text-neutral-400">No messages yet.</div>}
          </div>
        </div>
      )}
    </div>
  );
} 