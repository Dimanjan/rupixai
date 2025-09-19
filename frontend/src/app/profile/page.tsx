"use client";
import { useEffect, useState } from "react";
import { apiFetch, isAuthenticated } from "@/lib/api";
import { useRouter } from "next/navigation";

type Me = { id: number; username: string; email: string; profile: { credits: number; total_images_generated: number } };

type PaymentGateway = 'khalti' | 'esewa' | 'stripe' | 'razorpay' | 'binance';

interface PaymentRequest {
  gateway: PaymentGateway;
  amount: number;
  credits: number;
}

interface PaymentResponse {
  transaction_id: string;
  payment_url?: string;
  gateway_data?: any;
}

export default function ProfilePage() {
  const router = useRouter();
  const [me, setMe] = useState<Me | null>(null);
  const [error, setError] = useState<string| null>(null);
  const [showBuyCredits, setShowBuyCredits] = useState(false);
  const [selectedGateway, setSelectedGateway] = useState<PaymentGateway>('khalti');
  const [amount, setAmount] = useState(10);
  const [isProcessing, setIsProcessing] = useState(false);
  const [paymentError, setPaymentError] = useState<string | null>(null);

  const creditPackages = [
    { amount: 5, credits: 50, price: 5 },
    { amount: 10, credits: 100, price: 10 },
    { amount: 25, credits: 250, price: 25 },
    { amount: 50, credits: 500, price: 50 },
    { amount: 100, credits: 1000, price: 100 },
  ];

  const gateways = [
    { id: 'khalti', name: 'Khalti', icon: '💳', description: 'Nepal\'s leading payment gateway' },
    { id: 'esewa', name: 'eSewa', icon: '📱', description: 'Digital wallet and payment service' },
    { id: 'stripe', name: 'Stripe', icon: '💎', description: 'Global payment processing' },
    { id: 'razorpay', name: 'Razorpay', icon: '🔷', description: 'Indian payment gateway' },
    { id: 'binance', name: 'Binance Pay', icon: '₿', description: 'Cryptocurrency payments' },
  ] as const;

  useEffect(() => {
    if (!isAuthenticated()) {
      router.push('/auth/login');
      return;
    }
    (async () => {
      try { setMe(await apiFetch<Me>("/me/")); } catch (e:any) { setError(e.message); }
    })();
  }, []);

  const handleBuyCredits = async () => {
    setIsProcessing(true);
    setPaymentError(null);
    
    try {
      const selectedPackage = creditPackages.find(pkg => pkg.amount === amount);
      if (!selectedPackage) throw new Error('Invalid package selected');

      const paymentData: PaymentRequest = {
        return_url: `${window.location.origin}/payment/success`,
        gateway: selectedGateway,
        amount: selectedPackage.price,
        credits: selectedPackage.credits,
      };

      const response = await apiFetch<PaymentResponse>('/payments/create/', {
        method: 'POST',
        body: JSON.stringify(paymentData),
      });

      // Handle different gateway responses
      if (response.payment_url) {
        // Redirect to payment gateway
        window.open(response.payment_url, '_blank');
      } else if (response.gateway_data) {
        // Handle gateway-specific data (e.g., Stripe elements, Razorpay checkout)
        handleGatewaySpecificPayment(response.gateway_data);
      } else {
        throw new Error('No payment URL or gateway data received');
      }

    } catch (e: any) {
      setPaymentError(e.message || 'Payment initiation failed');
    } finally {
      setIsProcessing(false);
    }
  };

  const handleGatewaySpecificPayment = (gatewayData: any) => {
    switch (selectedGateway) {
      case 'stripe':
        // Initialize Stripe Elements
        console.log('Stripe payment data:', gatewayData);
        // In a real implementation, you'd initialize Stripe Elements here
        break;
      case 'razorpay':
        // Initialize Razorpay checkout
        console.log('Razorpay payment data:', gatewayData);
        // In a real implementation, you'd initialize Razorpay checkout here
        break;
      case 'binance':
        // Handle Binance Pay
        console.log('Binance payment data:', gatewayData);
        break;
      default:
        console.log('Gateway data:', gatewayData);
    }
  };

  const refreshProfile = async () => {
    try { setMe(await apiFetch<Me>("/me/")); } catch (e:any) { setError(e.message); }
  };

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-semibold">Profile</h1>
      {error && <p className="text-red-400 text-sm">{error}</p>}
      {me && (
        <div className="space-y-2">
          <div className="text-lg">{me.username}</div>
          <div className="text-neutral-400">{me.email}</div>
          <div className="mt-4 grid grid-cols-2 gap-3">
            <div className="border border-neutral-800 rounded p-3">
              <div className="text-sm text-neutral-400">Credits</div>
              <div className="text-2xl font-semibold">{me.profile.credits}</div>
            </div>
            <div className="border border-neutral-800 rounded p-3">
              <div className="text-sm text-neutral-400">Images Generated</div>
              <div className="text-2xl font-semibold">{me.profile.total_images_generated}</div>
            </div>
          </div>
          
          <button
            onClick={() => setShowBuyCredits(true)}
            className="mt-4 w-full bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded transition-colors"
          >
            Buy Credits
          </button>
        </div>
      )}

      {/* Buy Credits Modal */}
      {showBuyCredits && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-neutral-900 border border-neutral-800 rounded-lg p-6 w-full max-w-md mx-4">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-semibold">Buy Credits</h2>
              <button
                onClick={() => setShowBuyCredits(false)}
                className="text-neutral-400 hover:text-white"
              >
                ✕
              </button>
            </div>

            {paymentError && (
              <div className="mb-4 p-3 bg-red-900/20 border border-red-800 rounded text-red-400 text-sm">
                {paymentError}
              </div>
            )}

            {/* Credit Package Selection */}
            <div className="mb-6">
              <label className="block text-sm font-medium mb-2">Credit Package</label>
              <div className="grid grid-cols-2 gap-2">
                {creditPackages.map((pkg) => (
                  <button
                    key={pkg.amount}
                    onClick={() => setAmount(pkg.amount)}
                    className={`p-3 border rounded text-left transition-colors ${
                      amount === pkg.amount
                        ? 'border-blue-500 bg-blue-500/10'
                        : 'border-neutral-700 hover:border-neutral-600'
                    }`}
                  >
                    <div className="font-semibold">{pkg.credits} credits</div>
                    <div className="text-sm text-neutral-400">${pkg.price}</div>
                  </button>
                ))}
              </div>
            </div>

            {/* Payment Gateway Selection */}
            <div className="mb-6">
              <label className="block text-sm font-medium mb-2">Payment Method</label>
              <div className="space-y-2">
                {gateways.map((gateway) => (
                  <button
                    key={gateway.id}
                    onClick={() => setSelectedGateway(gateway.id)}
                    className={`w-full p-3 border rounded text-left transition-colors ${
                      selectedGateway === gateway.id
                        ? 'border-blue-500 bg-blue-500/10'
                        : 'border-neutral-700 hover:border-neutral-600'
                    }`}
                  >
                    <div className="flex items-center gap-3">
                      <span className="text-xl">{gateway.icon}</span>
                      <div>
                        <div className="font-medium">{gateway.name}</div>
                        <div className="text-sm text-neutral-400">{gateway.description}</div>
                      </div>
                    </div>
                  </button>
                ))}
              </div>
            </div>

            {/* Payment Summary */}
            <div className="mb-6 p-4 bg-neutral-800 rounded">
              <div className="flex justify-between items-center">
                <span>Total Credits:</span>
                <span className="font-semibold">{creditPackages.find(pkg => pkg.amount === amount)?.credits}</span>
              </div>
              <div className="flex justify-between items-center mt-1">
                <span>Amount:</span>
                <span className="font-semibold">${creditPackages.find(pkg => pkg.amount === amount)?.price}</span>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="flex gap-3">
              <button
                onClick={() => setShowBuyCredits(false)}
                className="flex-1 py-2 px-4 border border-neutral-700 rounded hover:border-neutral-600 transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={handleBuyCredits}
                disabled={isProcessing}
                className="flex-1 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-800 disabled:cursor-not-allowed text-white py-2 px-4 rounded transition-colors"
              >
                {isProcessing ? 'Processing...' : 'Pay Now'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
