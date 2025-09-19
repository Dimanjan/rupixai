from django.contrib import admin
from .models import Profile, ChatThread, ChatMessage, ImageJob, PaymentTransaction


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "credits", "total_images_generated")
    search_fields = ("user__username",)


class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 0


@admin.register(ChatThread)
class ChatThreadAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "title", "created_at", "updated_at")
    search_fields = ("title", "user__username")
    inlines = [ChatMessageInline]


@admin.register(ImageJob)
class ImageJobAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "provider", "model", "status", "credits_spent", "created_at")
    list_filter = ("provider", "status")
    search_fields = ("user__username", "model")

@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "gateway", "transaction_id", "amount", "credits", "status", "created_at")
    list_filter = ("gateway", "status")
    search_fields = ("user__username", "transaction_id")
