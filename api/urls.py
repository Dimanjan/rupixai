from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    # Authentication
    path('auth/register/', views.RegisterView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='refresh'),
    
    # Password Reset
    path('auth/forgot-password/', views.ForgotPasswordView.as_view(), name='forgot_password'),
    path('auth/reset-password/', views.ResetPasswordView.as_view(), name='reset_password'),
    path('auth/verify-reset-token/<uuid:token>/', views.VerifyResetTokenView.as_view(), name='verify_reset_token'),
    
    # Social Auth
    path('social/urls/', views.SocialLoginUrlsView.as_view(), name='social_login_urls'),
    path('social/callback/', views.SocialLoginCallbackView.as_view(), name='social_login_callback'),
    
    # User Profile
    path('me/', views.MeView.as_view(), name='me'),
    path('me/credits/add/', views.AddCreditsView.as_view(), name='add_credits'),
    
    # Chat/History
    path('chat/threads/', views.ChatThreadListCreateView.as_view(), name='chat_threads'),
    path('chat/threads/<int:thread_id>/', views.ChatThreadDetailView.as_view(), name='chat_thread_detail'),
    path('chat/threads/<int:thread_id>/messages/', views.ChatMessageCreateView.as_view(), name='chat_messages'),
    
    # Image Jobs
    path('image-jobs/', views.ImageJobListCreateView.as_view(), name='image_jobs'),
    path('image-jobs/<int:job_id>/', views.ImageJobDetailView.as_view(), name='image_job_detail'),
    
    # Payments
    path('payments/', views.PaymentTransactionListView.as_view(), name='payment_list'),
    path('payments/create/', views.CreatePaymentView.as_view(), name='create_payment'),
    path('payments/verify/', views.VerifyPaymentView.as_view(), name='verify_payment'),
    path('payments/<str:transaction_id>/', views.PaymentTransactionDetailView.as_view(), name='payment_detail'),
    
    # Payment Webhooks
    path('webhooks/khalti/', views.KhaltiWebhookView.as_view(), name='khalti_webhook'),
    path('webhooks/esewa/', views.ESewaWebhookView.as_view(), name='esewa_webhook'),
    path('webhooks/stripe/', views.StripeWebhookView.as_view(), name='stripe_webhook'),
    path('webhooks/razorpay/', views.RazorpayWebhookView.as_view(), name='razorpay_webhook'),
    path('webhooks/binance/', views.BinanceWebhookView.as_view(), name='binance_webhook'),
]
