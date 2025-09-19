from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from allauth.socialaccount.models import SocialAccount
from drf_spectacular.utils import extend_schema, OpenApiResponse
import requests
import json

User = get_user_model()


@extend_schema(
    tags=['Social Auth'],
    summary='Get social login URLs',
    responses={200: OpenApiResponse(description='Social login URLs')}
)
class SocialLoginUrlsView(APIView):
    def get(self, request):
        base_url = request.build_absolute_uri('/accounts/')
        
        urls = {
            'google': f"{base_url}google/login/",
            'facebook': f"{base_url}facebook/login/",
            'instagram': f"{base_url}instagram/login/",
            'github': f"{base_url}github/login/",
            'twitter': f"{base_url}twitter/login/",
        }
        
        return Response(urls)


@extend_schema(
    tags=['Social Auth'],
    summary='Handle social login callback',
    responses={200: OpenApiResponse(description='Login successful')}
)
class SocialLoginCallbackView(APIView):
    def post(self, request):
        provider = request.data.get('provider')
        access_token = request.data.get('access_token')
        
        if not provider or not access_token:
            return Response(
                {'error': 'Provider and access_token are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Get user info from the provider
            user_info = self.get_user_info(provider, access_token)
            
            if not user_info:
                return Response(
                    {'error': 'Failed to get user info from provider'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Get or create user
            user = self.get_or_create_user(provider, user_info)
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            
            return Response({
                'access': str(access_token),
                'refresh': str(refresh),
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                }
            })
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def get_user_info(self, provider, access_token):
        """Get user information from the social provider"""
        if provider == 'google':
            response = requests.get(
                'https://www.googleapis.com/oauth2/v2/userinfo',
                headers={'Authorization': f'Bearer {access_token}'}
            )
            if response.status_code == 200:
                data = response.json()
                return {
                    'id': data.get('id'),
                    'email': data.get('email'),
                    'first_name': data.get('given_name'),
                    'last_name': data.get('family_name'),
                    'username': data.get('email', '').split('@')[0],
                    'picture': data.get('picture'),
                }
        
        elif provider == 'facebook':
            response = requests.get(
                f'https://graph.facebook.com/me?fields=id,name,email,first_name,last_name,picture&access_token={access_token}'
            )
            if response.status_code == 200:
                data = response.json()
                return {
                    'id': data.get('id'),
                    'email': data.get('email'),
                    'first_name': data.get('first_name'),
                    'last_name': data.get('last_name'),
                    'username': data.get('email', '').split('@')[0] if data.get('email') else data.get('name', '').replace(' ', '_'),
                    'picture': data.get('picture', {}).get('data', {}).get('url') if data.get('picture') else None,
                }
        
        elif provider == 'instagram':
            response = requests.get(
                f'https://graph.instagram.com/me?fields=id,username,account_type,media_count&access_token={access_token}'
            )
            if response.status_code == 200:
                data = response.json()
                return {
                    'id': data.get('id'),
                    'email': None,  # Instagram doesn't provide email
                    'first_name': None,
                    'last_name': None,
                    'username': data.get('username'),
                    'picture': None,
                }
        
        elif provider == 'github':
            response = requests.get(
                'https://api.github.com/user',
                headers={'Authorization': f'token {access_token}'}
            )
            if response.status_code == 200:
                data = response.json()
                return {
                    'id': data.get('id'),
                    'email': data.get('email'),
                    'first_name': data.get('name', '').split(' ')[0] if data.get('name') else None,
                    'last_name': ' '.join(data.get('name', '').split(' ')[1:]) if data.get('name') and len(data.get('name', '').split(' ')) > 1 else None,
                    'username': data.get('login'),
                    'picture': data.get('avatar_url'),
                }
        
        elif provider == 'twitter':
            # Twitter API v2 requires different handling
            response = requests.get(
                'https://api.twitter.com/2/users/me?user.fields=profile_image_url',
                headers={'Authorization': f'Bearer {access_token}'}
            )
            if response.status_code == 200:
                data = response.json().get('data', {})
                return {
                    'id': data.get('id'),
                    'email': None,  # Twitter doesn't provide email in v2
                    'first_name': None,
                    'last_name': None,
                    'username': data.get('username'),
                    'picture': data.get('profile_image_url'),
                }
        
        return None
    
    def get_or_create_user(self, provider, user_info):
        """Get or create user from social provider info"""
        # Try to find existing social account
        try:
            social_account = SocialAccount.objects.get(
                provider=provider,
                uid=user_info['id']
            )
            return social_account.user
        except SocialAccount.DoesNotExist:
            pass
        
        # Try to find user by email if available
        if user_info.get('email'):
            try:
                user = User.objects.get(email=user_info['email'])
                # Create social account for existing user
                SocialAccount.objects.create(
                    user=user,
                    provider=provider,
                    uid=user_info['id'],
                    extra_data=user_info
                )
                return user
            except User.DoesNotExist:
                pass
        
        # Create new user
        username = user_info['username']
        # Ensure username is unique
        original_username = username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{original_username}_{counter}"
            counter += 1
        
        user = User.objects.create_user(
            username=username,
            email=user_info.get('email', ''),
            first_name=user_info.get('first_name', ''),
            last_name=user_info.get('last_name', ''),
        )
        
        # Create social account
        SocialAccount.objects.create(
            user=user,
            provider=provider,
            uid=user_info['id'],
            extra_data=user_info
        )
        
        return user
