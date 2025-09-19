from django.shortcuts import get_object_or_404
from django.db import transaction
from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiResponse
from .models import PaymentTransaction, Profile
from .payment_serializers import (
    PaymentTransactionSerializer,
    CreatePaymentSerializer,
    VerifyPaymentSerializer,
)
from .payment_services import get_payment_service


@extend_schema(tags=['Payments'], summary='List user payment transactions', responses={200: PaymentTransactionSerializer(many=True)})
class PaymentTransactionListView(generics.ListAPIView):
    serializer_class = PaymentTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PaymentTransaction.objects.filter(user=self.request.user).order_by('-created_at')


@extend_schema(tags=['Payments'], summary='Create payment for credits', responses={201: OpenApiResponse(description='Payment created')})
class CreatePaymentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = CreatePaymentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        gateway = serializer.validated_data['gateway']
        amount = serializer.validated_data['amount']
        credits = serializer.validated_data['credits']
        
        try:
            # Create payment with gateway
            service = get_payment_service(gateway)
            payment_data = service.create_payment(
                amount=amount,
                credits_purchased=credits,
                user=request.user,
                return_url=request.data.get('return_url')
            )
            
            # Create transaction record
            transaction_obj = PaymentTransaction.objects.create(
                user=request.user,
                gateway=gateway,
                transaction_id=payment_data['transaction_id'],
                amount=amount,
                credits_purchased=credits,
                status='pending',
                gateway_data=payment_data.get('gateway_data', {})
            )
            
            return Response({
                'transaction_id': transaction_obj.transaction_id,
                'payment_data': payment_data,
                'status': 'pending'
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Payments'], summary='Verify payment completion', responses={200: OpenApiResponse(description='Payment verified')})
class VerifyPaymentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = VerifyPaymentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        transaction_id = serializer.validated_data['transaction_id']
        gateway_data = serializer.validated_data['gateway_data']
        
        try:
            # Get transaction
            transaction_obj = get_object_or_404(
                PaymentTransaction,
                transaction_id=transaction_id,
                user=request.user
            )
            
            if transaction_obj.status != 'pending':
                return Response({'error': 'Transaction already processed'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Verify with gateway
            service = get_payment_service(transaction_obj.gateway)
            is_verified, verification_data = service.verify_payment(transaction_id, gateway_data)
            
            if is_verified:
                # Add credits to user
                with transaction.atomic():
                    profile = request.user.profile
                    profile.credits += transaction_obj.credits
                    profile.save(update_fields=['credits'])
                    
                    transaction_obj.status = 'completed'
                    transaction_obj.completed_at = timezone.now()
                    transaction_obj.gateway_data.update(verification_data)
                    transaction_obj.save()
                
                return Response({
                    'status': 'completed',
                    'credits_added': transaction_obj.credits,
                    'total_credits': request.user.profile.credits
                })
            else:
                transaction_obj.status = 'failed'
                transaction_obj.gateway_data.update({'verification_error': verification_data})
                transaction_obj.save()
                
                return Response({'error': 'Payment verification failed'}, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Payments'], summary='Get payment transaction details', responses={200: PaymentTransactionSerializer})
class PaymentTransactionDetailView(generics.RetrieveAPIView):
    serializer_class = PaymentTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'transaction_id'

    def get_queryset(self):
        return PaymentTransaction.objects.filter(user=self.request.user)
