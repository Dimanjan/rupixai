# RupixAI Mobile App

A Flutter mobile application for the RupixAI platform - AI-powered image generation.

## Features

- �� **AI Image Generation**: Generate images using OpenAI DALL-E 3 and Google Gemini
- 🔐 **Authentication**: Secure login/register with JWT tokens
- 💳 **Credit System**: Purchase credits through multiple payment gateways
- 📱 **Modern UI**: Beautiful, responsive design with Material 3
- 🔄 **Real-time Updates**: Live status updates for image generation
- 📸 **Image Upload**: Support for multiple image inputs
- 📊 **History Tracking**: View all your generated images
- 👤 **User Profile**: Manage your account and view statistics

## Tech Stack

- **Framework**: Flutter 3.35.2
- **State Management**: Riverpod
- **Navigation**: GoRouter
- **HTTP Client**: Dio
- **Local Storage**: Flutter Secure Storage
- **Image Handling**: Image Picker, Cached Network Image
- **UI Components**: Material 3 Design

## Getting Started

### Prerequisites

- Flutter SDK (3.0.0 or higher)
- Dart SDK (3.0.0 or higher)
- Android Studio / VS Code
- Android device or emulator

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd rupixai_mobile
   ```

2. **Install dependencies**
   ```bash
   flutter pub get
   ```

3. **Configure API endpoint**
   - Update the `_baseUrl` in `lib/services/api_service.dart`
   - Default: `http://localhost:8000/api`
   - For production: `https://your-api-domain.com/api`

4. **Run the app**
   ```bash
   flutter run
   ```

### Configuration

#### API Configuration
Update the API base URL in `lib/services/api_service.dart`:

```dart
static const String _baseUrl = 'https://your-api-domain.com/api';
```

#### Payment Gateways
The app supports multiple payment gateways:
- Stripe
- Khalti (Nepal)
- eSewa (Nepal)
- Razorpay (India)
- Binance (Crypto)

#### Social Login
Configure social login providers in your backend and update the app accordingly.

## Project Structure

```
lib/
├── models/           # Data models
│   ├── user.dart
│   ├── image_job.dart
│   ├── chat.dart
│   └── payment.dart
├── services/         # API services
│   └── api_service.dart
├── providers/        # State management
│   ├── auth_provider.dart
│   └── image_provider.dart
├── screens/          # UI screens
│   ├── auth/
│   ├── home/
│   ├── profile/
│   ├── history/
│   └── payment/
├── widgets/          # Reusable widgets
├── utils/            # Utilities
│   └── app_theme.dart
└── main.dart         # App entry point
```

## Features Overview

### Authentication
- User registration and login
- JWT token management
- Secure token storage
- Social login support (Google, Facebook, etc.)

### Image Generation
- Multiple AI providers (OpenAI, Gemini)
- Custom prompts
- Image upload support
- Real-time generation status
- Credit-based pricing

### Payment System
- Multiple payment gateways
- Credit packages
- Transaction history
- Secure payment processing

### User Experience
- Modern Material 3 design
- Dark/Light theme support
- Responsive layout
- Smooth animations
- Offline support (cached images)

## API Integration

The app communicates with the Django backend through REST APIs:

- **Authentication**: `/api/auth/`
- **Image Generation**: `/api/image-jobs/`
- **User Profile**: `/api/me/`
- **Payments**: `/api/payments/`
- **Chat History**: `/api/chat/`

## Building for Production

### Android
```bash
flutter build apk --release
# or
flutter build appbundle --release
```

### iOS
```bash
flutter build ios --release
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions:
- Create an issue on GitHub
- Contact the development team
- Check the documentation

## Roadmap

- [ ] Push notifications
- [ ] Offline mode
- [ ] Advanced image editing
- [ ] Batch image generation
- [ ] AI model comparison
- [ ] Social sharing
- [ ] Advanced user analytics
