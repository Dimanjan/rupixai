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

# Import webhook views
from .webhook_views import (
    KhaltiWebhookView,
    eSewaWebhookView,
    StripeWebhookView,
    RazorpayWebhookView,
    BinanceWebhookView,
)
from .payment_views import (
    PaymentTransactionListView,
    CreatePaymentView,
    VerifyPaymentView,
    PaymentTransactionDetailView,
)


@extend_schema(tags=['Auth'], summary='Register a new user', responses={201: OpenApiResponse(description='User created')})
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        # Profile is created automatically via signals
        return user


@extend_schema(tags=['Auth'], summary='Get current user profile', responses={200: UserSerializer})
class MeView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


@extend_schema(tags=['Credits'], summary='Add credits to user account', responses={200: OpenApiResponse(description='Credits added')})
class AddCreditsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        amount = request.data.get('amount', 0)
        try:
            amount = int(amount)
            if amount <= 0:
                return Response({'error': 'Amount must be positive'}, status=status.HTTP_400_BAD_REQUEST)
            
            profile = request.user.profile
            profile.credits += amount
            profile.save()
            
            return Response({
                'message': f'Added {amount} credits',
                'total_credits': profile.credits
            })
        except (ValueError, TypeError):
            return Response({'error': 'Invalid amount'}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Chat'], summary='List and create chat threads', responses={200: ChatThreadSerializer(many=True)})
class ChatThreadListCreateView(generics.ListCreateAPIView):
    serializer_class = ChatThreadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ChatThread.objects.filter(user=self.request.user).order_by('-updated_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema(tags=['Chat'], summary='Get chat thread details', responses={200: ChatThreadSerializer})
class ChatThreadDetailView(generics.RetrieveAPIView):
    serializer_class = ChatThreadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ChatThread.objects.filter(user=self.request.user)


@extend_schema(tags=['Chat'], summary='Add message to chat thread', responses={201: OpenApiResponse(description='Message added')})
class ChatMessageCreateView(generics.CreateAPIView):
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        thread_id = self.kwargs['thread_id']
        thread = get_object_or_404(ChatThread, id=thread_id, user=self.request.user)
        serializer.save(thread=thread)


@extend_schema(tags=['Images'], summary='List and create image generation jobs', responses={200: ImageJobSerializer(many=True)})
class ImageJobListCreateView(generics.ListCreateAPIView):
    serializer_class = ImageJobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ImageJob.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        # Check if user has enough credits
        profile = self.request.user.profile
        if profile.credits < 1:
            return Response({'error': 'Insufficient credits'}, status=status.HTTP_402_PAYMENT_REQUIRED)
        
        # Deduct credits
        profile.credits -= 1
        profile.save()
        
        # Create the job
        job = serializer.save(user=self.request.user, status='pending', credits_spent=1)
        
        # Generate images asynchronously (in a real app, use Celery)
        try:
            service = select_service(job.provider)
            images = service.generate(job.prompt, job.input_images)
            job.output_images = images
            job.status = 'completed'
            job.completed_at = timezone.now()
            job.save()
            
            # Add message to thread if specified
            if job.thread:
                thread = job.thread
                ChatMessage.objects.create(
                    thread=thread,
                    role='user',
                    content=f"Generate image: {job.prompt}"
                )
                ChatMessage.objects.create(
                    thread=thread,
                    role='assistant',
                    content=f"Generated {len(images)} image(s) using {job.provider} {job.model}"
                )
                
        except Exception as e:
            job.status = 'failed'
            job.save()
            # Refund credits on failure
            profile.credits += 1
            profile.save()
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(tags=['Images'], summary='Get image job details', responses={200: ImageJobSerializer})
class ImageJobDetailView(generics.RetrieveAPIView):
    serializer_class = ImageJobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ImageJob.objects.filter(user=self.request.user)


def build_thread_context(thread: ChatThread) -> str:
    """Build context string from chat thread history"""
    messages = thread.messages.all().order_by('created_at')
    context_parts = []
    
    for msg in messages:
        role = "User" if msg.role == "user" else "Assistant"
        context_parts.append(f"{role}: {msg.content}")
    
    return "\n".join(context_parts)
