from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    credits = models.PositiveIntegerField(default=0)
    total_images_generated = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return f"Profile({self.user.username})"


class ChatThread(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_threads')
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"ChatThread({self.id}) - {self.title}"


class ChatMessage(models.Model):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('assistant', 'Assistant'),
        ('system', 'System'),
    )
    thread = models.ForeignKey(ChatThread, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=16, choices=ROLE_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"ChatMessage({self.id}) {self.role}"


class ImageJob(models.Model):
    PROVIDER_CHOICES = (
        ('openai', 'OpenAI'),
        ('gemini', 'Gemini'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='image_jobs')
    thread = models.ForeignKey(ChatThread, null=True, blank=True, on_delete=models.SET_NULL, related_name='image_jobs')
    provider = models.CharField(max_length=16, choices=PROVIDER_CHOICES)
    model = models.CharField(max_length=128)
    prompt = models.TextField()
    input_images = models.JSONField(default=list, blank=True)
    output_images = models.JSONField(default=list, blank=True)
    status = models.CharField(max_length=32, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    credits_spent = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return f"ImageJob({self.id}) {self.provider} {self.status}"


class PaymentTransaction(models.Model):
    GATEWAY_CHOICES = (
        ('khalti', 'Khalti'),
        ('esewa', 'eSewa'),
        ('stripe', 'Stripe'),
        ('razorpay', 'Razorpay'),
        ('binance', 'Binance'),
    )
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_transactions')
    gateway = models.CharField(max_length=16, choices=GATEWAY_CHOICES)
    transaction_id = models.CharField(max_length=255, unique=True)  # Gateway's transaction ID
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Amount in local currency
    credits = models.PositiveIntegerField()  # Credits to be added
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default='pending')
    gateway_response = models.JSONField(default=dict, blank=True)  # Store gateway response
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return f"Payment({self.id}) {self.gateway} {self.status}"
