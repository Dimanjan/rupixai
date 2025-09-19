from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiResponse
from django.contrib.auth.models import User
from .models import PasswordResetToken


@extend_schema(
    tags=['Password Reset'],
    summary='Request password reset',
    responses={200: OpenApiResponse(description='Password reset email sent')}
)
class ForgotPasswordView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=email)
            
            # Create password reset token (expires in 1 hour)
            token_obj = PasswordResetToken.objects.create(
                user=user,
                expires_at=timezone.now() + timezone.timedelta(hours=1)
            )
            
            # Send password reset email
            reset_url = f"{settings.FRONTEND_URL}/auth/reset-password?token={token_obj.token}"
            
            # In a real application, you would send an actual email
            # For now, we'll just log it or return the URL for testing
            print(f"Password reset email for {email}: {reset_url}")
            
            # If you have email configured, uncomment this:
            # send_mail(
            #     'Password Reset Request',
            #     f'Click the link to reset your password: {reset_url}',
            #     settings.DEFAULT_FROM_EMAIL,
            #     [email],
            #     fail_silently=False,
            # )
            
            return Response({
                'message': 'Password reset email sent',
                'reset_url': reset_url  # Remove this in production
            })
            
        except User.DoesNotExist:
            # Don't reveal if email exists or not
            return Response({
                'message': 'If the email exists, a password reset link has been sent'
            })


@extend_schema(
    tags=['Password Reset'],
    summary='Reset password with token',
    responses={200: OpenApiResponse(description='Password reset successfully')}
)
class ResetPasswordView(APIView):
    def post(self, request):
        token = request.data.get('token')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')
        
        if not all([token, new_password, confirm_password]):
            return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        if new_password != confirm_password:
            return Response({'error': "Passwords don't match"}, status=status.HTTP_400_BAD_REQUEST)
        
        if len(new_password) < 8:
            return Response({'error': 'Password must be at least 8 characters long'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            token_obj = PasswordResetToken.objects.get(token=token)
            
            if not token_obj.is_valid():
                return Response(
                    {'error': 'Invalid or expired token'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Update user password
            user = token_obj.user
            user.set_password(new_password)
            user.save()
            
            # Mark token as used
            token_obj.mark_as_used()
            
            return Response({'message': 'Password reset successfully'})
            
        except PasswordResetToken.DoesNotExist:
            return Response(
                {'error': 'Invalid token'},
                status=status.HTTP_400_BAD_REQUEST
            )


@extend_schema(
    tags=['Password Reset'],
    summary='Verify password reset token',
    responses={200: OpenApiResponse(description='Token verification result')}
)
class VerifyResetTokenView(APIView):
    def get(self, request, token):
        try:
            token_obj = PasswordResetToken.objects.get(token=token)
            
            if token_obj.is_valid():
                return Response({
                    'valid': True,
                    'token': {
                        'token': str(token_obj.token),
                        'created_at': token_obj.created_at,
                        'expires_at': token_obj.expires_at,
                        'used': token_obj.used
                    }
                })
            else:
                return Response({
                    'valid': False,
                    'error': 'Token expired or already used'
                })
                
        except PasswordResetToken.DoesNotExist:
            return Response({
                'valid': False,
                'error': 'Invalid token'
            })
