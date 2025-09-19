"use client";
import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";

type Message = { id: number; role: string; content: string; created_at: string };
type Thread = { id: number; title: string; created_at: string; updated_at: string; messages: Message[] };

export default function ChatPage() {
  const [threads, setThreads] = useState<Thread[]>([]);
  const [selected, setSelected] = useState<Thread | null>(null);
  const [newTitle, setNewTitle] = useState("");
  const [newMessage, setNewMessage] = useState("");
  const [error, setError] = useState<string| null>(null);

  async function loadThreads() {
    try { setThreads(await apiFetch<Thread[]>("/chat/threads/")); } catch (e:any) { setError(e.message); }
  }
  useEffect(()=>{ loadThreads(); }, []);

  async function createThread() {
    try {
      await apiFetch("/chat/threads/", { method: "POST", body: { title: newTitle || "New chat" } });
      setNewTitle("");
      await loadThreads();
    } catch (e:any) { setError(e.message); }
  }

  async function sendMessage() {
    if (!selected) return;
    try {
      const updated = await apiFetch<Thread>(`/chat/threads/${selected.id}/messages/`, { method: "POST", body: { role: "user", content: newMessage } });
      setSelected(updated);
      setNewMessage("");
      await loadThreads();
    } catch (e:any) { setError(e.message); }
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      <div className="space-y-3">
        <div className="flex gap-2">
          <input value={newTitle} onChange={e=>setNewTitle(e.target.value)} placeholder="New chat title" className="flex-1 px-3 py-2 bg-neutral-900 border border-neutral-800 rounded" />
          <button onClick={createThread} className="bg-white text-black px-3 rounded">New</button>
        </div>
        <div className="space-y-2">
          {threads.map(t => (
            <button key={t.id} onClick={()=>setSelected(t)} className={`w-full text-left border border-neutral-800 rounded p-2 ${selected?.id===t.id?"bg-neutral-900":""}`}>
              <div className="font-medium truncate">{t.title}</div>
              <div className="text-xs text-neutral-400">{new Date(t.updated_at).toLocaleString()}</div>
            </button>
          ))}
        </div>
      </div>
      <div className="md:col-span-2 border border-neutral-800 rounded p-3">
        {selected ? (
          <div className="flex flex-col h-full">
            <div className="flex-1 space-y-3 overflow-auto max-h-[60vh] pr-2">
              {selected.messages.map(m => (
                <div key={m.id} className="rounded border border-neutral-800 p-2">
                  <div className="text-xs text-neutral-400">{m.role} • {new Date(m.created_at).toLocaleString()}</div>
                  <div>{m.content}</div>
                </div>
              ))}
            </div>
            <div className="mt-3 flex gap-2">
              <input value={newMessage} onChange={e=>setNewMessage(e.target.value)} placeholder="Type a message" className="flex-1 px-3 py-2 bg-neutral-900 border border-neutral-800 rounded" />
              <button onClick={sendMessage} className="bg-white text-black px-3 rounded">Send</button>
            </div>
          </div>
        ) : (
          <div className="text-neutral-400">Select a thread to view messages.</div>
        )}
        {error && <p className="text-red-400 text-sm mt-2">{error}</p>}
      </div>
    </div>
  );
} 