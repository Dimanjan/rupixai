from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile, ChatThread, ChatMessage, ImageJob


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["credits", "total_images_generated"]


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "profile"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["username", "email", "password"]
        extra_kwargs = {
            "email": {"required": False, "allow_blank": True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
        )
        return user


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ["id", "role", "content", "created_at"]


class ChatThreadSerializer(serializers.ModelSerializer):
    messages = ChatMessageSerializer(many=True, read_only=True)

    class Meta:
        model = ChatThread
        fields = ["id", "title", "created_at", "updated_at", "messages"]


class ImageJobSerializer(serializers.ModelSerializer):
    thread = serializers.PrimaryKeyRelatedField(queryset=ChatThread.objects.all(), required=False, allow_null=True)

    class Meta:
        model = ImageJob
        fields = [
            "id",
            "thread",
            "provider",
            "model",
            "prompt",
            "input_images",
            "output_images",
            "status",
            "credits_spent",
            "created_at",
            "completed_at",
        ]
        read_only_fields = ["output_images", "status", "credits_spent", "created_at", "completed_at"] 