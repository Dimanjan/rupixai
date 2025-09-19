from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Auth
    path('auth/register/', views.RegisterView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # User/Profile
    path('me/', views.MeView.as_view(), name='me'),
    path('me/credits/add/', views.AddCreditsView.as_view(), name='add_credits'),

    # Chat
    path('chat/threads/', views.ChatThreadListCreateView.as_view(), name='chat_thread_list_create'),
    path('chat/threads/<int:thread_id>/', views.ChatThreadDetailView.as_view(), name='chat_thread_detail'),
    path('chat/threads/<int:thread_id>/messages/', views.ChatMessageCreateView.as_view(), name='chat_message_create'),

    # Image Jobs (stub for generation to be implemented next)
    path('image-jobs/', views.ImageJobListCreateView.as_view(), name='image_job_list_create'),
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