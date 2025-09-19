from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple
import uuid
import os


class PaymentService(ABC):
    """Base class for payment gateway services"""
    
    @abstractmethod
    def create_payment(self, amount: float, credits: int, user, return_url: str = None) -> Dict[str, Any]:
        """Create a payment and return payment data"""
        pass
    
    @abstractmethod
    def verify_payment(self, transaction_id: str, gateway_data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """Verify payment completion"""
        pass
    
    @abstractmethod
    def refund_payment(self, transaction_id: str, amount: float) -> Dict[str, Any]:
        """Refund a payment"""
        pass


class KhaltiService(PaymentService):
    """Khalti payment gateway service"""
    
    def __init__(self):
        self.secret_key = os.getenv('KHALTI_SECRET_KEY', 'test_secret_key')
        self.public_key = os.getenv('KHALTI_PUBLIC_KEY', 'test_public_key')
        self.base_url = os.getenv('KHALTI_BASE_URL', 'https://a.khalti.com/api/v2')
    
    def create_payment(self, amount: float, credits: int, user, return_url: str = None) -> Dict[str, Any]:
        transaction_id = f"khalti_{uuid.uuid4().hex[:16]}"
        
        # In a real implementation, you would make API calls to Khalti
        payment_data = {
            'transaction_id': transaction_id,
            'payment_url': f"https://khalti.com/pay/{transaction_id}",
            'gateway_data': {
                'public_key': self.public_key,
                'amount': int(amount * 100),  # Khalti expects amount in paisa
                'currency': 'NPR',
                'return_url': return_url or 'http://localhost:3000/payment/success',
                'website_url': 'http://localhost:3000',
                'purchase_order_id': transaction_id,
                'purchase_order_name': f'Credits Purchase - {credits} credits',
            }
        }
        
        return payment_data
    
    def verify_payment(self, transaction_id: str, gateway_data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        # In a real implementation, you would verify with Khalti API
        # For now, we'll simulate a successful verification
        return True, {'khalti_transaction_id': f'khalti_{transaction_id}', 'status': 'completed'}
    
    def refund_payment(self, transaction_id: str, amount: float) -> Dict[str, Any]:
        # In a real implementation, you would call Khalti refund API
        return {'refund_id': f'refund_{transaction_id}', 'status': 'processed'}


class ESewaService(PaymentService):
    """eSewa payment gateway service"""
    
    def __init__(self):
        self.merchant_id = os.getenv('ESEWA_MERCHANT_ID', 'test_merchant_id')
        self.secret_key = os.getenv('ESEWA_SECRET_KEY', 'test_secret_key')
        self.base_url = os.getenv('ESEWA_BASE_URL', 'https://uat.esewa.com.np')
    
    def create_payment(self, amount: float, credits: int, user, return_url: str = None) -> Dict[str, Any]:
        transaction_id = f"esewa_{uuid.uuid4().hex[:16]}"
        
        payment_data = {
            'transaction_id': transaction_id,
            'payment_url': f"{self.base_url}/epay/main",
            'gateway_data': {
                'amt': amount,
                'pdc': 0,
                'psc': 0,
                'txAmt': 0,
                'tAmt': amount,
                'pid': transaction_id,
                'scd': self.merchant_id,
                'su': return_url or 'http://localhost:3000/payment/success',
                'fu': 'http://localhost:3000/payment/failure',
            }
        }
        
        return payment_data
    
    def verify_payment(self, transaction_id: str, gateway_data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        # In a real implementation, you would verify with eSewa API
        return True, {'esewa_transaction_id': f'esewa_{transaction_id}', 'status': 'completed'}
    
    def refund_payment(self, transaction_id: str, amount: float) -> Dict[str, Any]:
        return {'refund_id': f'refund_{transaction_id}', 'status': 'processed'}


class StripeService(PaymentService):
    """Stripe payment gateway service"""
    
    def __init__(self):
        self.secret_key = os.getenv('STRIPE_SECRET_KEY', 'sk_test_...')
        self.publishable_key = os.getenv('STRIPE_PUBLISHABLE_KEY', 'pk_test_...')
    
    def create_payment(self, amount: float, credits: int, user, return_url: str = None) -> Dict[str, Any]:
        transaction_id = f"stripe_{uuid.uuid4().hex[:16]}"
        
        payment_data = {
            'transaction_id': transaction_id,
            'gateway_data': {
                'publishable_key': self.publishable_key,
                'amount': int(amount * 100),  # Stripe expects amount in cents
                'currency': 'usd',
                'payment_intent_id': f'pi_{transaction_id}',
                'client_secret': f'pi_{transaction_id}_secret',
                'return_url': return_url or 'http://localhost:3000/payment/success',
            }
        }
        
        return payment_data
    
    def verify_payment(self, transaction_id: str, gateway_data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        # In a real implementation, you would verify with Stripe API
        return True, {'stripe_payment_intent_id': f'pi_{transaction_id}', 'status': 'succeeded'}
    
    def refund_payment(self, transaction_id: str, amount: float) -> Dict[str, Any]:
        return {'refund_id': f're_{transaction_id}', 'status': 'succeeded'}


class RazorpayService(PaymentService):
    """Razorpay payment gateway service"""
    
    def __init__(self):
        self.key_id = os.getenv('RAZORPAY_KEY_ID', 'rzp_test_...')
        self.key_secret = os.getenv('RAZORPAY_KEY_SECRET', 'test_secret')
    
    def create_payment(self, amount: float, credits: int, user, return_url: str = None) -> Dict[str, Any]:
        transaction_id = f"razorpay_{uuid.uuid4().hex[:16]}"
        
        payment_data = {
            'transaction_id': transaction_id,
            'gateway_data': {
                'key': self.key_id,
                'amount': int(amount * 100),  # Razorpay expects amount in paise
                'currency': 'INR',
                'order_id': f'order_{transaction_id}',
                'name': 'Credits Purchase',
                'description': f'Purchase {credits} credits',
                'prefill': {
                    'name': user.username,
                    'email': user.email or '',
                },
                'return_url': return_url or 'http://localhost:3000/payment/success',
            }
        }
        
        return payment_data
    
    def verify_payment(self, transaction_id: str, gateway_data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        # In a real implementation, you would verify with Razorpay API
        return True, {'razorpay_payment_id': f'pay_{transaction_id}', 'status': 'captured'}
    
    def refund_payment(self, transaction_id: str, amount: float) -> Dict[str, Any]:
        return {'refund_id': f'rfd_{transaction_id}', 'status': 'processed'}


class BinanceService(PaymentService):
    """Binance Pay service"""
    
    def __init__(self):
        self.api_key = os.getenv('BINANCE_API_KEY', 'test_api_key')
        self.secret_key = os.getenv('BINANCE_SECRET_KEY', 'test_secret_key')
    
    def create_payment(self, amount: float, credits: int, user, return_url: str = None) -> Dict[str, Any]:
        transaction_id = f"binance_{uuid.uuid4().hex[:16]}"
        
        payment_data = {
            'transaction_id': transaction_id,
            'gateway_data': {
                'merchant_id': 'test_merchant',
                'amount': amount,
                'currency': 'USDT',
                'order_id': transaction_id,
                'description': f'Purchase {credits} credits',
                'return_url': return_url or 'http://localhost:3000/payment/success',
            }
        }
        
        return payment_data
    
    def verify_payment(self, transaction_id: str, gateway_data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        # In a real implementation, you would verify with Binance Pay API
        return True, {'binance_transaction_id': f'binance_{transaction_id}', 'status': 'completed'}
    
    def refund_payment(self, transaction_id: str, amount: float) -> Dict[str, Any]:
        return {'refund_id': f'refund_{transaction_id}', 'status': 'processed'}


def get_payment_service(gateway: str) -> PaymentService:
    """Factory function to get the appropriate payment service"""
    services = {
        'khalti': KhaltiService,
        'esewa': ESewaService,
        'stripe': StripeService,
        'razorpay': RazorpayService,
        'binance': BinanceService,
    }
    
    service_class = services.get(gateway.lower())
    if not service_class:
        raise ValueError(f"Unsupported payment gateway: {gateway}")
    
    return service_class()
