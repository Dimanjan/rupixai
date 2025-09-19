from django.shortcuts import get_object_or_404
from django.db import transaction
from django.utils import timezone
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
import logging
from .models import PaymentTransaction, Profile
from .payment_services import get_payment_service

logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name='dispatch')
class KhaltiWebhookView(APIView):
    """Handle Khalti payment webhooks"""
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            transaction_id = data.get('transaction_id')
            status = data.get('status')
            
            if not transaction_id:
                return Response({'error': 'Missing transaction_id'}, status=400)
            
            # Find the transaction
            payment_transaction = get_object_or_404(
                PaymentTransaction,
                transaction_id=transaction_id,
                gateway='khalti'
            )
            
            if status == 'completed':
                # Verify with Khalti service
                service = get_payment_service('khalti')
                is_verified, verification_data = service.verify_payment(transaction_id, data)
                
                if is_verified:
                    with transaction.atomic():
                        profile = payment_transaction.user.profile
                        profile.credits += payment_transaction.credits_purchased
                        profile.save(update_fields=['credits'])
                        
                        payment_transaction.status = 'completed'
                        payment_transaction.completed_at = timezone.now()
                        payment_transaction.gateway_data.update(verification_data)
                        payment_transaction.save()
                    
                    logger.info(f"Khalti payment completed: {transaction_id}")
                    return Response({'status': 'success'})
                else:
                    payment_transaction.status = 'failed'
                    payment_transaction.gateway_data.update({'verification_error': verification_data})
                    payment_transaction.save()
                    return Response({'error': 'Verification failed'}, status=400)
            else:
                payment_transaction.status = 'failed'
                payment_transaction.save()
                return Response({'status': 'failed'})
                
        except Exception as e:
            logger.error(f"Khalti webhook error: {str(e)}")
            return Response({'error': str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class ESewaWebhookView(APIView):
    """Handle eSewa payment webhooks"""
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            transaction_id = data.get('transaction_id')
            status = data.get('status')
            
            if not transaction_id:
                return Response({'error': 'Missing transaction_id'}, status=400)
            
            payment_transaction = get_object_or_404(
                PaymentTransaction,
                transaction_id=transaction_id,
                gateway='esewa'
            )
            
            if status == 'completed':
                service = get_payment_service('esewa')
                is_verified, verification_data = service.verify_payment(transaction_id, data)
                
                if is_verified:
                    with transaction.atomic():
                        profile = payment_transaction.user.profile
                        profile.credits += payment_transaction.credits_purchased
                        profile.save(update_fields=['credits'])
                        
                        payment_transaction.status = 'completed'
                        payment_transaction.completed_at = timezone.now()
                        payment_transaction.gateway_data.update(verification_data)
                        payment_transaction.save()
                    
                    return Response({'status': 'success'})
                else:
                    payment_transaction.status = 'failed'
                    payment_transaction.save()
                    return Response({'error': 'Verification failed'}, status=400)
            else:
                payment_transaction.status = 'failed'
                payment_transaction.save()
                return Response({'status': 'failed'})
                
        except Exception as e:
            logger.error(f"eSewa webhook error: {str(e)}")
            return Response({'error': str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhookView(APIView):
    """Handle Stripe payment webhooks"""
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            event_type = data.get('type')
            
            if event_type == 'payment_intent.succeeded':
                payment_intent = data.get('data', {}).get('object', {})
                transaction_id = payment_intent.get('metadata', {}).get('transaction_id')
                
                if transaction_id:
                    payment_transaction = get_object_or_404(
                        PaymentTransaction,
                        transaction_id=transaction_id,
                        gateway='stripe'
                    )
                    
                    with transaction.atomic():
                        profile = payment_transaction.user.profile
                        profile.credits += payment_transaction.credits_purchased
                        profile.save(update_fields=['credits'])
                        
                        payment_transaction.status = 'completed'
                        payment_transaction.completed_at = timezone.now()
                        payment_transaction.gateway_data.update({
                            'stripe_payment_intent_id': payment_intent.get('id'),
                            'webhook_data': data
                        })
                        payment_transaction.save()
                    
                    return Response({'status': 'success'})
            
            return Response({'status': 'ignored'})
                
        except Exception as e:
            logger.error(f"Stripe webhook error: {str(e)}")
            return Response({'error': str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class RazorpayWebhookView(APIView):
    """Handle Razorpay payment webhooks"""
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            event = data.get('event')
            
            if event == 'payment.captured':
                payment = data.get('payload', {}).get('payment', {}).get('entity', {})
                transaction_id = payment.get('notes', {}).get('transaction_id')
                
                if transaction_id:
                    payment_transaction = get_object_or_404(
                        PaymentTransaction,
                        transaction_id=transaction_id,
                        gateway='razorpay'
                    )
                    
                    with transaction.atomic():
                        profile = payment_transaction.user.profile
                        profile.credits += payment_transaction.credits_purchased
                        profile.save(update_fields=['credits'])
                        
                        payment_transaction.status = 'completed'
                        payment_transaction.completed_at = timezone.now()
                        payment_transaction.gateway_data.update({
                            'razorpay_payment_id': payment.get('id'),
                            'webhook_data': data
                        })
                        payment_transaction.save()
                    
                    return Response({'status': 'success'})
            
            return Response({'status': 'ignored'})
                
        except Exception as e:
            logger.error(f"Razorpay webhook error: {str(e)}")
            return Response({'error': str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class BinanceWebhookView(APIView):
    """Handle Binance Pay webhooks"""
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            status = data.get('status')
            transaction_id = data.get('transaction_id')
            
            if status == 'SUCCESS' and transaction_id:
                payment_transaction = get_object_or_404(
                    PaymentTransaction,
                    transaction_id=transaction_id,
                    gateway='binance'
                )
                
                with transaction.atomic():
                    profile = payment_transaction.user.profile
                    profile.credits += payment_transaction.credits_purchased
                    profile.save(update_fields=['credits'])
                    
                    payment_transaction.status = 'completed'
                    payment_transaction.completed_at = timezone.now()
                    payment_transaction.gateway_data.update(data)
                    payment_transaction.save()
                
                return Response({'status': 'success'})
            
            return Response({'status': 'ignored'})
                
        except Exception as e:
            logger.error(f"Binance webhook error: {str(e)}")
            return Response({'error': str(e)}, status=500)
