import type { Metadata } from "next";
import Link from "next/link";
import Image from "next/image";
import "./globals.css";
import { AuthNav } from "./components/AuthNav";

export const metadata: Metadata = {
  title: "RupixAI",
  description: "AI image wrapper",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-neutral-950 text-neutral-100">
        <nav className="border-b border-neutral-800 sticky top-0 z-10 bg-neutral-950/80 backdrop-blur">
          <div className="max-w-5xl mx-auto px-4 py-3 flex items-center gap-4">
            <Link href="/" className="flex items-center gap-2 font-semibold">
              <Image
                src="/rupixlogo.png"
                alt="RupixAI Logo"
                width={32}
                height={32}
                className="rounded"
              />
              RupixAI
            </Link>
            <div className="flex-1" />
            <AuthNav />
          </div>
        </nav>
        <main className="max-w-5xl mx-auto px-4 py-6">{children}</main>
      </body>
    </html>
  );
}
