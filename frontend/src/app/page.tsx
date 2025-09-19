"use client";
import { useEffect, useState } from "react";
import { apiFetch, isAuthenticated } from "@/lib/api";
import { useRouter } from "next/navigation";

type ImageJob = {
  id: number;
  thread?: number | null;
  provider: string;
  model: string;
  prompt: string;
  output_images: string[];
  status: string;
  created_at: string;
};

type Thread = { id: number; title: string; updated_at: string };

export default function Dashboard() {
  const router = useRouter();
  const [provider, setProvider] = useState("openai");
  const [model, setModel] = useState("dall-e-3");
  const [prompt, setPrompt] = useState("");
  const [files, setFiles] = useState<File[]>([]);
  const [jobs, setJobs] = useState<ImageJob[]>([]);
  const [threads, setThreads] = useState<Thread[]>([]);
  const [selectedThread, setSelectedThread] = useState<number | "new" | null>(null);
  const [newTitle, setNewTitle] = useState("");
  const [error, setError] = useState<string| null>(null);
  const [loading, setLoading] = useState(false);

  async function loadJobs() {
    try { setJobs(await apiFetch<ImageJob[]>("/image-jobs/")); } catch (e:any) { setError(e.message); }
  }
  async function loadThreads() {
    try { setThreads(await apiFetch<Thread[]>("/chat/threads/")); } catch (e:any) { setError(e.message); }
  }

  useEffect(() => { 
    if (!isAuthenticated()) {
      router.push('/auth/login');
      return;
    }
    loadJobs(); 
    loadThreads(); 
  }, [router]);

  async function ensureThread(): Promise<number | null> {
    if (selectedThread === "new") {
      const title = newTitle || `Thread ${new Date().toLocaleString()}`;
      const thread = await apiFetch<Thread>("/chat/threads/", { method: "POST", body: { title } });
      await loadThreads();
      setSelectedThread(thread.id);
      setNewTitle("");
      return thread.id;
    }
    return typeof selectedThread === "number" ? selectedThread : null;
  }

  async function submitJob(e: React.FormEvent) {
    e.preventDefault();
    if (!prompt.trim()) return;
    setLoading(true); setError(null);
    try {
      const threadId = await ensureThread();
      const form = new FormData();
      form.append("provider", provider);
      form.append("model", model);
      form.append("prompt", prompt);
      if (threadId) form.append("thread", String(threadId));
      files.forEach(f => form.append("images", f));
      await apiFetch("/image-jobs/", { method: "POST", formData: form });
      setPrompt(""); setFiles([]);
      await loadJobs();
    } catch (e: any) { setError(e.message); }
    finally { setLoading(false); }
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold">Generate images</h1>
      <form onSubmit={submitJob} className="space-y-3">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-3">
          <select value={provider} onChange={e=>{setProvider(e.target.value); setModel(e.target.value==="openai"?"dall-e-3":"gemini-2.5-flash-image-preview");}} className="px-3 py-2 bg-neutral-900 border border-neutral-800 rounded">
            <option value="openai">OpenAI DALL-E 3 ($0.040/image)</option>
            <option value="gemini">Google Gemini 2.5 Flash (Free tier)</option>
          </select>
          <input value={model} onChange={e=>setModel(e.target.value)} className="px-3 py-2 bg-neutral-900 border border-neutral-800 rounded" placeholder="Model" />
          <select value={selectedThread ?? ''} onChange={e=> setSelectedThread(e.target.value === 'new' ? 'new' : (e.target.value ? Number(e.target.value) : null))} className="px-3 py-2 bg-neutral-900 border border-neutral-800 rounded">
            <option value="">No thread (fresh, history ignored)</option>
            <option value="new">+ New chat thread</option>
            {threads.map(t => (
              <option key={t.id} value={t.id}>{t.title}</option>
            ))}
          </select>
          {selectedThread === "new" && (
            <input value={newTitle} onChange={e=>setNewTitle(e.target.value)} placeholder="New thread title" className="px-3 py-2 bg-neutral-900 border border-neutral-800 rounded" />
          )}
          <input type="file" multiple onChange={e=> setFiles(Array.from(e.target.files||[]))} className="px-3 py-2 bg-neutral-900 border border-neutral-800 rounded" />
        </div>
        <textarea value={prompt} onChange={e=>setPrompt(e.target.value)} className="w-full h-28 px-3 py-2 bg-neutral-900 border border-neutral-800 rounded" placeholder="Write your prompt..." />
        {error && <p className="text-red-400 text-sm">{error}</p>}
        <button disabled={loading} className="bg-white text-black px-4 py-2 rounded">{loading?"Generating...":"Generate"}</button>
      </form>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {jobs.map(job => (
          <div key={job.id} className="border border-neutral-800 rounded p-3">
            <div className="text-sm text-neutral-400">{job.provider} • {job.model} • {new Date(job.created_at).toLocaleString()}</div>
            <div className="font-medium mt-1">{job.prompt}</div>
            <div className="mt-2 grid grid-cols-2 gap-2">
              {(job.output_images||[]).map((imageUrl, i) => {
                // Check if it's a URL or base64 data
                const isUrl = imageUrl.startsWith('http');
                const src = isUrl ? imageUrl : `data:image/png;base64,${imageUrl}`;
                return (
                  <img key={i} src={src} alt="result" className="rounded" />
                );
              })}
            </div>
            <div className="mt-2 text-sm">Status: {job.status} {job.thread ? `• Thread #${job.thread}` : ''}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
