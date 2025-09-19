from django.shortcuts import get_object_or_404
from django.db import transaction
from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiResponse
from .models import Profile, ChatThread, ChatMessage, ImageJob
from .serializers import (
    RegisterSerializer,
    UserSerializer,
    ChatThreadSerializer,
    ChatMessageSerializer,
    ImageJobSerializer,
)
from .services import select_service


@extend_schema(tags=['Auth'], summary='Register a new user', responses={201: OpenApiResponse(description='User created')})
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


@extend_schema(tags=['Users'], summary='Get current user profile', responses={200: UserSerializer})
class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)


@extend_schema(tags=['Credits'], summary='Add credits to a user (admin only)')
class AddCreditsView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        user_id = request.data.get("user_id")
        amount = int(request.data.get("amount", 0))
        if not user_id or amount <= 0:
            return Response({"detail": "user_id and positive amount required"}, status=400)
        profile = get_object_or_404(Profile, user_id=user_id)
        profile.credits += amount
        profile.save(update_fields=["credits"])
        return Response({"user_id": user_id, "credits": profile.credits})


@extend_schema(tags=['Chat'], summary='List or create chat threads', responses={200: ChatThreadSerializer})
class ChatThreadListCreateView(generics.ListCreateAPIView):
    serializer_class = ChatThreadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ChatThread.objects.filter(user=self.request.user).order_by("-updated_at")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema(tags=['Chat'], summary='Retrieve or delete a chat thread', responses={200: ChatThreadSerializer})
class ChatThreadDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = ChatThreadSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_url_kwarg = 'thread_id'

    def get_queryset(self):
        return ChatThread.objects.filter(user=self.request.user)


@extend_schema(tags=['Chat'], summary='Create a message in a thread', responses={201: ChatThreadSerializer})
class ChatMessageCreateView(generics.CreateAPIView):
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        thread = get_object_or_404(ChatThread, id=kwargs.get('thread_id'), user=request.user)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ChatMessage.objects.create(
            thread=thread,
            role=serializer.validated_data.get('role', 'user'),
            content=serializer.validated_data['content'],
        )
        thread.save(update_fields=["updated_at"])  # touch
        return Response(ChatThreadSerializer(thread).data, status=status.HTTP_201_CREATED)


def build_thread_context(thread: ChatThread) -> str:
    history = []
    for msg in thread.messages.order_by('created_at')[:50]:
        prefix = 'User' if msg.role == 'user' else 'Assistant'
        history.append(f"{prefix}: {msg.content}")
    return "\n".join(history)


@extend_schema(tags=['Images'], summary='List or create image jobs (multipart for uploads)', responses={200: ImageJobSerializer})
class ImageJobListCreateView(generics.ListCreateAPIView):
    serializer_class = ImageJobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ImageJob.objects.filter(user=self.request.user).order_by("-created_at")

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        provider = request.data.get("provider")
        model = request.data.get("model")
        prompt = request.data.get("prompt", "")
        thread_id = request.data.get("thread") or request.data.get("thread_id")
        thread = None
        if thread_id:
            thread = get_object_or_404(ChatThread, id=thread_id, user=request.user)

        # Prepare context-aware prompt if a thread is provided
        final_prompt = prompt
        if thread:
            context = build_thread_context(thread)
            if context:
                final_prompt = f"Context from conversation so far:\n{context}\n\nCurrent request: {prompt}"

        # Collect uploaded files (multiple)
        upload_files = request.FILES.getlist('images')
        input_images = [f.read() for f in upload_files][:10]

        profile = request.user.profile
        required_credits = 1
        if profile.credits < required_credits:
            return Response({"detail": "Insufficient credits"}, status=402)

        # Create job as queued
        job = ImageJob.objects.create(
            user=request.user,
            thread=thread,
            provider=provider,
            model=model or "auto",
            prompt=prompt,
            input_images=[],
            status='queued',
            credits_spent=required_credits,
        )

        # Deduct credits up-front
        profile.credits -= required_credits
        profile.save(update_fields=["credits"])

        # Call provider service synchronously for now
        try:
            service = select_service(provider)
            outputs_b64 = service.generate(prompt=final_prompt, input_images=input_images)
            job.output_images = outputs_b64
            job.status = 'completed'
            job.completed_at = timezone.now()
            job.save(update_fields=["output_images", "status", "completed_at"]) 

            # usage counter
            profile.total_images_generated += len(outputs_b64) if outputs_b64 else 1
            profile.save(update_fields=["total_images_generated"]) 

            # Persist chat messages to history within thread if provided
            if thread:
                ChatMessage.objects.create(thread=thread, role='user', content=prompt)
                ChatMessage.objects.create(thread=thread, role='assistant', content=f"Generated {len(outputs_b64) if outputs_b64 else 1} image(s)")
                thread.save(update_fields=["updated_at"]) 
        except Exception as e:
            job.status = 'failed'
            job.save(update_fields=["status"]) 
            return Response({"detail": str(e)}, status=400)

        return Response(ImageJobSerializer(job).data, status=201)


@extend_schema(tags=['Images'], summary='Get image job details', responses={200: ImageJobSerializer})
class ImageJobDetailView(generics.RetrieveAPIView):
    serializer_class = ImageJobSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_url_kwarg = 'job_id'

    def get_queryset(self):
        return ImageJob.objects.filter(user=self.request.user)
from .payment_views import *
from .webhook_views import *
