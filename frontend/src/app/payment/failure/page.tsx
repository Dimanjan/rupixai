"use client";
import { useRouter } from "next/navigation";

export default function PaymentFailurePage() {
  const router = useRouter();

  return (
    <div className="min-h-screen flex items-center justify-center bg-neutral-900">
      <div className="max-w-md w-full mx-4">
        <div className="bg-neutral-800 border border-neutral-700 rounded-lg p-8 text-center">
          <div className="text-red-500 text-6xl mb-4">✗</div>
          <h1 className="text-xl font-semibold mb-2 text-red-400">Payment Failed</h1>
          <p className="text-neutral-300 mb-6">
            Your payment could not be processed. Please try again or contact support if the problem persists.
          </p>
          <div className="flex gap-3">
            <button
              onClick={() => router.push('/profile')}
              className="flex-1 bg-neutral-700 hover:bg-neutral-600 text-white py-2 px-4 rounded transition-colors"
            >
              Back to Profile
            </button>
            <button
              onClick={() => router.push('/')}
              className="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded transition-colors"
            >
              Go Home
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
