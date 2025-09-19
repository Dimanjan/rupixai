from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    credits = models.PositiveIntegerField(default=0)
    total_images_generated = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.user.username}'s profile"


class ChatThread(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_threads')
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.title} ({self.user.username})"


class ChatMessage(models.Model):
    thread = models.ForeignKey(ChatThread, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=20, choices=[('user', 'User'), ('assistant', 'Assistant')])
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.role}: {self.content[:50]}..."


class ImageJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='image_jobs')
    thread = models.ForeignKey(ChatThread, on_delete=models.SET_NULL, null=True, blank=True)
    provider = models.CharField(max_length=50)  # 'openai', 'gemini'
    model = models.CharField(max_length=100)  # 'dall-e-3', 'gemini-2.5-flash-image-preview'
    prompt = models.TextField()
    input_images = models.JSONField(default=list, blank=True)  # List of base64 images
    output_images = models.JSONField(default=list, blank=True)  # List of generated image URLs
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    credits_spent = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.provider} - {self.prompt[:50]}..."


class PaymentTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_transactions')
    gateway = models.CharField(max_length=50)  # 'khalti', 'esewa', 'stripe', 'razorpay', 'binance'
    transaction_id = models.CharField(max_length=255, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    credits_purchased = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled')
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    gateway_data = models.JSONField(default=dict, blank=True)  # Store gateway-specific data

    def __str__(self) -> str:
        return f"{self.gateway} - {self.transaction_id}"


# Password Reset Model
class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)
    
    def is_valid(self):
        return not self.used and timezone.now() < self.expires_at
    
    def mark_as_used(self):
        self.used = True
        self.save()
    
    class Meta:
        ordering = ['-created_at']
