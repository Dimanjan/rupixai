from django.contrib import admin
from .models import Profile, ChatThread, ChatMessage, ImageJob, PaymentTransaction, PasswordResetToken


class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 0


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'credits', 'total_images_generated']
    search_fields = ['user__username', 'user__email']


@admin.register(ChatThread)
class ChatThreadAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['title', 'user__username']
    inlines = [ChatMessageInline]


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['thread', 'role', 'content_preview', 'created_at']
    list_filter = ['role', 'created_at']
    search_fields = ['content', 'thread__title', 'thread__user__username']
    
    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'


@admin.register(ImageJob)
class ImageJobAdmin(admin.ModelAdmin):
    list_display = ['user', 'provider', 'model', 'status', 'created_at', 'credits_spent']
    list_filter = ['provider', 'model', 'status', 'created_at']
    search_fields = ['prompt', 'user__username']
    readonly_fields = ['created_at', 'completed_at']


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'gateway', 'transaction_id', 'amount', 'credits_purchased', 'status', 'created_at']
    list_filter = ['gateway', 'status', 'created_at']
    search_fields = ['transaction_id', 'user__username', 'user__email']
    readonly_fields = ['created_at', 'completed_at']


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ['user', 'token', 'created_at', 'expires_at', 'used']
    list_filter = ['used', 'created_at']
    search_fields = ['user__username', 'user__email', 'token']
    readonly_fields = ['token', 'created_at']
