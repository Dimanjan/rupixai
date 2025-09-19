"use client";
import { useState } from "react";
import { apiFetch, saveTokens } from "@/lib/api";
import { useRouter } from "next/navigation";

interface SocialLoginProps {
  onSuccess?: () => void;
  onError?: (error: string) => void;
}

export default function SocialLogin({ onSuccess, onError }: SocialLoginProps) {
  const [loading, setLoading] = useState<string | null>(null);
  const router = useRouter();

  const handleSocialLogin = async (provider: string) => {
    setLoading(provider);
    
    try {
      // For development, we'll use a mock approach
      // In production, you would integrate with the actual OAuth flows
      
      // Mock access token for testing
      const mockTokens = {
        google: "mock_google_token",
        facebook: "mock_facebook_token",
        instagram: "mock_instagram_token",
        github: "mock_github_token",
        twitter: "mock_twitter_token",
      };
      
      const response = await apiFetch<{
        access: string;
        refresh: string;
        user: {
          id: number;
          username: string;
          email: string;
          first_name: string;
          last_name: string;
        };
      }>("/social/callback/", {
        method: "POST",
        body: {
          provider,
          access_token: mockTokens[provider as keyof typeof mockTokens],
        },
      });
      
      saveTokens(response.access, response.refresh);
      
      if (onSuccess) {
        onSuccess();
      } else {
        router.push("/");
      }
    } catch (err: any) {
      const errorMessage = err.message || "Social login failed";
      if (onError) {
        onError(errorMessage);
      } else {
        console.error("Social login error:", errorMessage);
      }
    } finally {
      setLoading(null);
    }
  };

  const socialProviders = [
    {
      name: "Google",
      provider: "google",
      icon: "🔍",
      color: "bg-red-500 hover:bg-red-600",
    },
    {
      name: "Facebook",
      provider: "facebook",
      icon: "📘",
      color: "bg-blue-600 hover:bg-blue-700",
    },
    {
      name: "Instagram",
      provider: "instagram",
      icon: "📷",
      color: "bg-pink-500 hover:bg-pink-600",
    },
    {
      name: "GitHub",
      provider: "github",
      icon: "🐙",
      color: "bg-gray-800 hover:bg-gray-900",
    },
    {
      name: "Twitter",
      provider: "twitter",
      icon: "🐦",
      color: "bg-sky-500 hover:bg-sky-600",
    },
  ];

  return (
    <div className="space-y-3">
      <div className="relative">
        <div className="absolute inset-0 flex items-center">
          <div className="w-full border-t border-neutral-700" />
        </div>
        <div className="relative flex justify-center text-sm">
          <span className="px-2 bg-neutral-950 text-neutral-400">Or continue with</span>
        </div>
      </div>
      
      <div className="grid grid-cols-2 gap-3">
        {socialProviders.map((social) => (
          <button
            key={social.provider}
            onClick={() => handleSocialLogin(social.provider)}
            disabled={loading === social.provider}
            className={`${social.color} text-white py-2 px-4 rounded transition-colors flex items-center justify-center gap-2 disabled:opacity-50`}
          >
            {loading === social.provider ? (
              <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
            ) : (
              <span className="text-lg">{social.icon}</span>
            )}
            <span className="text-sm font-medium">{social.name}</span>
          </button>
        ))}
      </div>
    </div>
  );
}
