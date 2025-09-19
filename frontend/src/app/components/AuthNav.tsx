"use client";
import Link from "next/link";
import { useEffect, useState } from "react";
import { isAuthenticated, clearTokens } from "@/lib/api";

function AuthNav() {
  const [authenticated, setAuthenticated] = useState(false);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    setAuthenticated(isAuthenticated());
  }, []);

  const handleLogout = () => {
    clearTokens();
    setAuthenticated(false);
    window.location.href = '/auth/login';
  };

  // Always render the same structure to prevent hydration mismatch
  return (
    <div className="flex items-center gap-4">
      {!mounted ? (
        // Loading state - same structure as authenticated state
        <>
          <div className="w-16 h-4 bg-neutral-800 rounded animate-pulse"></div>
          <div className="w-16 h-4 bg-neutral-800 rounded animate-pulse"></div>
          <div className="w-16 h-4 bg-neutral-800 rounded animate-pulse"></div>
        </>
      ) : authenticated ? (
        // Authenticated state
        <>
          <Link href="/history" className="hover:underline">History</Link>
          <Link href="/profile" className="hover:underline">Profile</Link>
          <button onClick={handleLogout} className="hover:underline">Logout</button>
        </>
      ) : (
        // Not authenticated state
        <>
          <Link href="/auth/register" className="hover:underline">Register</Link>
          <Link href="/auth/login" className="hover:underline">Login</Link>
        </>
      )}
    </div>
  );
}

export default AuthNav;
