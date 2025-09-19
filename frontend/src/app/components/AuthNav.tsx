"use client";
import Link from "next/link";
import { useEffect, useState } from "react";
import { isAuthenticated, clearTokens } from "@/lib/api";

export function AuthNav() {
  const [authenticated, setAuthenticated] = useState(false);

  useEffect(() => {
    setAuthenticated(isAuthenticated());
  }, []);

  const handleLogout = () => {
    clearTokens();
    setAuthenticated(false);
    window.location.href = '/auth/login';
  };

  if (authenticated) {
    return (
      <>
        <Link href="/history" className="hover:underline">History</Link>
        <Link href="/profile" className="hover:underline">Profile</Link>
        <button onClick={handleLogout} className="hover:underline">Logout</button>
      </>
    );
  }

  return (
    <>
      <Link href="/auth/register" className="hover:underline">Register</Link>
      <Link href="/auth/login" className="hover:underline">Login</Link>
    </>
  );
}
