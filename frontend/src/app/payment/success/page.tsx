"use client";
import { useEffect, useState } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import { apiFetch } from "@/lib/api";

export default function PaymentSuccessPage() {
  const [status, setStatus] = useState<'loading' | 'success' | 'error'>('loading');
  const [message, setMessage] = useState('');
  const searchParams = useSearchParams();
  const router = useRouter();

  useEffect(() => {
    const verifyPayment = async () => {
      try {
        const transactionId = searchParams.get('transaction_id');
        const gatewayData = searchParams.get('gateway_data');
        
        if (!transactionId) {
          setStatus('error');
          setMessage('No transaction ID found');
          return;
        }

        const response = await apiFetch('/payments/verify/', {
          method: 'POST',
          body: JSON.stringify({
            transaction_id: transactionId,
            gateway_data: gatewayData ? JSON.parse(gatewayData) : {}
          })
        });

        if (response.status === 'completed') {
          setStatus('success');
          setMessage(`Payment successful! ${response.credits_added} credits added to your account.`);
        } else {
          setStatus('error');
          setMessage('Payment verification failed');
        }
      } catch (error: any) {
        setStatus('error');
        setMessage(error.message || 'Payment verification failed');
      }
    };

    verifyPayment();
  }, [searchParams]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-neutral-900">
      <div className="max-w-md w-full mx-4">
        <div className="bg-neutral-800 border border-neutral-700 rounded-lg p-8 text-center">
          {status === 'loading' && (
            <>
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
              <h1 className="text-xl font-semibold mb-2">Verifying Payment...</h1>
              <p className="text-neutral-400">Please wait while we verify your payment.</p>
            </>
          )}
          
          {status === 'success' && (
            <>
              <div className="text-green-500 text-6xl mb-4">✓</div>
              <h1 className="text-xl font-semibold mb-2 text-green-400">Payment Successful!</h1>
              <p className="text-neutral-300 mb-6">{message}</p>
              <button
                onClick={() => router.push('/profile')}
                className="bg-blue-600 hover:bg-blue-700 text-white py-2 px-6 rounded transition-colors"
              >
                Go to Profile
              </button>
            </>
          )}
          
          {status === 'error' && (
            <>
              <div className="text-red-500 text-6xl mb-4">✗</div>
              <h1 className="text-xl font-semibold mb-2 text-red-400">Payment Failed</h1>
              <p className="text-neutral-300 mb-6">{message}</p>
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
            </>
          )}
        </div>
      </div>
    </div>
  );
}
