# RupixAI - AI Image Generation Platform

A comprehensive AI image generation platform with Django backend and Next.js frontend, supporting multiple AI providers and payment gateways.

## Features

- **AI Image Generation**: Support for OpenAI DALL-E 3 and Google Gemini
- **User Authentication**: JWT-based authentication system
- **Credit System**: User credits with multiple payment gateways
- **Chat History**: Thread-based conversation management
- **Payment Integration**: Khalti, eSewa, Stripe, Razorpay, Binance
- **Modern UI**: Responsive design with Tailwind CSS
- **API Documentation**: OpenAPI/Swagger documentation

## Tech Stack

### Backend
- Django 5.2.6
- Django REST Framework
- JWT Authentication
- SQLite Database
- OpenAI API Integration
- Google Gemini API Integration

### Frontend
- Next.js 15.5.3
- TypeScript
- Tailwind CSS
- React Hooks

## Quick Start

### Prerequisites
- Python 3.12+
- Node.js 18+
- OpenAI API Key
- (Optional) Google Gemini API Key

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Dimanjan/rupixai.git
   cd rupixai
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment setup**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

5. **Database setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Run the server**
   ```bash
   python manage.py runserver
   ```

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Run the development server**
   ```bash
   npm run dev
   ```

4. **Open your browser**
   ```
   http://localhost:3000
   ```

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```bash
# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# CORS Settings
CORS_ALLOW_ALL_ORIGINS=True
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# API Keys
OPENAI_API_KEY=your-openai-api-key-here
GEMINI_API_KEY=your-gemini-api-key-here

# Payment Gateway API Keys (Optional)
KHALTI_SECRET_KEY=your-khalti-secret-key
KHALTI_PUBLIC_KEY=your-khalti-public-key
ESEWA_MERCHANT_ID=your-esewa-merchant-id
ESEWA_SECRET_KEY=your-esewa-secret-key
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
RAZORPAY_KEY_ID=rzp_test_...
RAZORPAY_KEY_SECRET=your-razorpay-secret
BINANCE_API_KEY=your-binance-api-key
BINANCE_SECRET_KEY=your-binance-secret-key
```

## API Documentation

Once the backend is running, you can access the API documentation at:

- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/
- **OpenAPI Schema**: http://localhost:8000/api/schema/

## API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/refresh/` - Refresh JWT token

### User Profile
- `GET /api/me/` - Get current user profile
- `POST /api/me/credits/add/` - Add credits (admin only)

### Image Generation
- `GET /api/image-jobs/` - List user's image jobs
- `POST /api/image-jobs/` - Create new image generation job
- `GET /api/image-jobs/<id>/` - Get specific image job

### Chat/History
- `GET /api/chat/threads/` - List chat threads
- `POST /api/chat/threads/` - Create new thread
- `GET /api/chat/threads/<id>/` - Get thread details
- `POST /api/chat/threads/<id>/messages/` - Add message to thread

### Payments
- `GET /api/payments/` - List payment transactions
- `POST /api/payments/create/` - Create payment
- `POST /api/payments/verify/` - Verify payment
- `GET /api/payments/<id>/` - Get payment details

## Payment Gateways

The platform supports multiple payment gateways:

1. **Khalti** - Nepal's leading payment gateway
2. **eSewa** - Digital wallet and payment service
3. **Stripe** - Global payment processing
4. **Razorpay** - Indian payment gateway
5. **Binance Pay** - Cryptocurrency payments

## Credit Packages

- 50 credits for $5
- 100 credits for $10
- 250 credits for $25
- 500 credits for $50
- 1000 credits for $100

## AI Models

### OpenAI DALL-E 3
- **Cost**: $0.040 per image (1024x1024)
- **Quality**: High-quality, photorealistic images
- **Best for**: Professional use, detailed prompts

### Google Gemini 2.5 Flash
- **Cost**: Free tier available
- **Quality**: Good quality, experimental
- **Best for**: Testing, development

## Development

### Running Tests
```bash
# Backend tests
python manage.py test

# Frontend tests
cd frontend
npm test
```

### Code Quality
```bash
# Backend linting
flake8 .
black .

# Frontend linting
cd frontend
npm run lint
```

## Deployment

### Backend Deployment
1. Set up a production database (PostgreSQL recommended)
2. Configure environment variables for production
3. Set up a WSGI server (Gunicorn)
4. Configure reverse proxy (Nginx)

### Frontend Deployment
1. Build the production version
   ```bash
   cd frontend
   npm run build
   ```
2. Deploy to Vercel, Netlify, or your preferred platform

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support, please open an issue on GitHub or contact the development team.

## Changelog

### v1.0.0
- Initial release
- OpenAI DALL-E 3 integration
- User authentication system
- Credit system with payment gateways
- Chat history management
- Modern responsive UI

## Social Login Integration

RupixAI now supports social login with multiple providers using Django Allauth. Users can sign in with their existing social media accounts.

### Supported Providers

- **Google** - OAuth2 with profile and email access
- **Facebook** - OAuth2 with profile and email access  
- **Instagram** - OAuth2 with profile access
- **GitHub** - OAuth2 with user and repository access
- **Twitter** - OAuth2 with read access

### Backend Configuration

The social login system is built on Django Allauth and integrates seamlessly with the existing JWT authentication system.

#### API Endpoints

- `GET /api/social/urls/` - Get social login URLs for all providers
- `POST /api/social/callback/` - Handle social login callback with access token

#### OAuth App Setup

To enable social login, you need to create OAuth applications with each provider:

**Google OAuth2:**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Add authorized redirect URIs: `http://localhost:8000/accounts/google/login/callback/`

**Facebook OAuth2:**
1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Create a new app
3. Add Facebook Login product
4. Set valid OAuth redirect URIs: `http://localhost:8000/accounts/facebook/login/callback/`

**Instagram OAuth2:**
1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Create a new app
3. Add Instagram Basic Display product
4. Set valid OAuth redirect URIs: `http://localhost:8000/accounts/instagram/login/callback/`

**GitHub OAuth2:**
1. Go to GitHub Settings > Developer settings > OAuth Apps
2. Create a new OAuth App
3. Set Authorization callback URL: `http://localhost:8000/accounts/github/login/callback/`

**Twitter OAuth2:**
1. Go to [Twitter Developer Portal](https://developer.twitter.com/)
2. Create a new app
3. Enable OAuth 2.0
4. Set callback URL: `http://localhost:8000/accounts/twitter/login/callback/`

### Environment Variables

Add these to your `.env` file:

```bash
# Google OAuth2
GOOGLE_OAUTH2_CLIENT_ID=your-google-client-id
GOOGLE_OAUTH2_CLIENT_SECRET=your-google-client-secret

# Facebook OAuth2
FACEBOOK_APP_ID=your-facebook-app-id
FACEBOOK_APP_SECRET=your-facebook-app-secret

# Instagram OAuth2
INSTAGRAM_CLIENT_ID=your-instagram-client-id
INSTAGRAM_CLIENT_SECRET=your-instagram-client-secret

# GitHub OAuth2
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret

# Twitter OAuth2
TWITTER_CLIENT_ID=your-twitter-client-id
TWITTER_CLIENT_SECRET=your-twitter-client-secret
```

### Frontend Integration

The frontend includes a `SocialLogin` component that provides buttons for all supported providers. The component handles the OAuth flow and integrates with the existing JWT authentication system.

#### Usage

```tsx
import SocialLogin from "@/app/components/SocialLogin";

<SocialLogin 
  onSuccess={() => router.push("/")}
  onError={(error) => setError(error)}
/>
```

### Testing

Run the test script to verify social login endpoints:

```bash
python test_social_login.py
```

### Security Features

- **JWT Integration**: Social logins generate JWT tokens compatible with the existing auth system
- **User Linking**: Existing users can link social accounts to their profiles
- **Unique Usernames**: Automatic username generation for social users
- **Email Verification**: Optional email verification for social accounts
- **Token Expiration**: Social login tokens follow the same expiration rules as regular JWT tokens

### Production Considerations

1. **HTTPS Required**: OAuth providers require HTTPS in production
2. **Domain Verification**: Update OAuth app settings with production domains
3. **Rate Limiting**: Implement rate limiting for social login endpoints
4. **Error Handling**: Comprehensive error handling for OAuth failures
5. **User Data Privacy**: Ensure compliance with privacy regulations

### Troubleshooting

**Common Issues:**

1. **"Invalid redirect URI"**: Check OAuth app settings match your domain
2. **"App not verified"**: Complete OAuth app verification process
3. **"Scope not granted"**: Ensure requested scopes are approved
4. **"Token expired"**: Implement proper token refresh logic

**Debug Mode:**
Set `DEBUG=True` in your `.env` file to see detailed OAuth flow logs.
