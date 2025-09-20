# RupixAI Mobile App

A Flutter mobile application for AI-powered image generation, connecting to the RupixAI Django backend.

## 🚀 Features

- **AI Image Generation**: Generate images using OpenAI DALL-E 3 and Google Gemini models
- **User Authentication**: Secure login/register with JWT tokens
- **Credit System**: Purchase and manage credits for image generation
- **Chat History**: View and manage your image generation history
- **Profile Management**: View account details and usage statistics
- **Payment Integration**: Support for multiple payment gateways (Khalti, eSewa, Stripe, Razorpay, Binance)
- **Social Login**: Login with Google, Facebook, GitHub, Twitter, and Instagram
- **Cross-Platform**: Works on Android, iOS, and Web

## 📱 Screenshots

The app includes the following screens:
- **Splash Screen**: Loading screen with app branding
- **Login/Register**: Authentication screens with social login options
- **Home**: Main image generation interface
- **Profile**: User account and credit management
- **History**: View generated images and chat threads
- **Payment**: Credit purchase with multiple payment options

## 🛠️ Tech Stack

- **Framework**: Flutter 3.x
- **State Management**: Riverpod
- **Navigation**: GoRouter
- **HTTP Client**: Dio
- **Storage**: Flutter Secure Storage (mobile) / localStorage (web)
- **UI**: Material 3 Design System
- **Backend**: Django REST API

## 📋 Prerequisites

- Flutter SDK (3.0 or higher)
- Dart SDK (3.0 or higher)
- Android Studio / Xcode (for mobile development)
- Chrome (for web development)
- RupixAI Django backend running on `http://127.0.0.1:8000`

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone <repository-url>
cd rupixai/rupixai_mobile
```

### 2. Install Dependencies

```bash
flutter pub get
```

### 3. Configure API Endpoint

The app is configured to connect to `http://127.0.0.1:8000/api` by default. To change this, update the `_baseUrl` in `lib/services/api_service.dart`:

```dart
static const String _baseUrl = 'http://your-backend-url/api';
```

### 4. Run the App

#### For Web Development:
```bash
flutter run -d chrome
```

#### For Android:
```bash
flutter run -d android
```

#### For iOS:
```bash
flutter run -d ios
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Backend API URL
API_BASE_URL=http://127.0.0.1:8000/api

# Optional: Firebase configuration (if using Firebase features)
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_API_KEY=your-api-key
```

### API Configuration

The app uses a web-compatible API service that automatically handles:
- Token storage (localStorage for web, secure storage for mobile)
- JWT token refresh
- Error handling and retry logic
- CORS support

## 📱 Platform Support

### Web
- ✅ Chrome (tested)
- ✅ Firefox (compatible)
- ✅ Safari (compatible)
- ✅ Edge (compatible)

### Mobile
- ✅ Android (API 21+)
- ✅ iOS (iOS 11+)

## 🔐 Authentication

The app supports multiple authentication methods:

### Standard Login
- Username/Password authentication
- JWT token-based sessions
- Automatic token refresh

### Social Login
- Google OAuth
- Facebook Login
- GitHub OAuth
- Twitter OAuth
- Instagram OAuth

### Test Credentials
For testing purposes, use:
- **Username**: `demo`
- **Password**: `demo123`
- **Credits**: 100 (pre-loaded)

## 💳 Payment Integration

The app supports multiple payment gateways:

- **Khalti**: Nepal's popular payment gateway
- **eSewa**: Nepal's digital wallet
- **Stripe**: International payment processing
- **Razorpay**: Indian payment gateway
- **Binance**: Cryptocurrency payments

## 🎨 UI/UX Features

- **Material 3 Design**: Modern, adaptive UI components
- **Dark/Light Theme**: Automatic theme switching based on system preferences
- **Responsive Design**: Optimized for different screen sizes
- **Loading States**: Smooth loading animations and skeleton screens
- **Error Handling**: User-friendly error messages and retry mechanisms

## 📊 State Management

The app uses Riverpod for state management with the following providers:

- **AuthProvider**: User authentication state
- **ApiServiceProvider**: HTTP client and API communication
- **UserProvider**: Current user data and profile information

## 🔄 API Integration

### Endpoints Used

- `POST /auth/login/` - User login
- `POST /auth/register/` - User registration
- `GET /me/` - Get current user profile
- `POST /image-jobs/` - Create image generation job
- `GET /image-jobs/` - List user's image jobs
- `GET /chat/threads/` - List chat threads
- `POST /payments/create/` - Create payment
- `POST /payments/verify/` - Verify payment

### Error Handling

The app includes comprehensive error handling:
- Network connectivity issues
- Authentication failures
- API rate limiting
- Server errors
- Validation errors

## 🧪 Testing

### Running Tests

```bash
# Run all tests
flutter test

# Run tests with coverage
flutter test --coverage

# Run integration tests
flutter test integration_test/
```

### Test Structure

- **Unit Tests**: Individual widget and service tests
- **Widget Tests**: UI component testing
- **Integration Tests**: End-to-end user flow testing

## 🚀 Building for Production

### Web Build

```bash
flutter build web --release
```

### Android Build

```bash
flutter build apk --release
# or
flutter build appbundle --release
```

### iOS Build

```bash
flutter build ios --release
```

## 📦 Dependencies

### Core Dependencies

- `flutter_riverpod`: State management
- `go_router`: Navigation
- `dio`: HTTP client
- `flutter_secure_storage`: Secure token storage

### UI Dependencies

- `material_color_utilities`: Material 3 color utilities
- `cached_network_image`: Image caching
- `image_picker`: Image selection

### Development Dependencies

- `flutter_lints`: Linting rules
- `build_runner`: Code generation
- `freezed`: Immutable classes
- `json_annotation`: JSON serialization

## 🔧 Development

### Code Structure

```
lib/
├── main.dart                 # App entry point
├── models/                   # Data models
├── providers/                # Riverpod providers
├── screens/                  # UI screens
│   ├── auth/                # Authentication screens
│   ├── home/                # Home screen
│   ├── profile/             # Profile screen
│   ├── history/             # History screens
│   └── payment/             # Payment screens
├── services/                 # API and business logic
├── utils/                    # Utilities and helpers
└── widgets/                  # Reusable widgets
```

### Code Style

The project follows Flutter's official style guide:
- Use `flutter_lints` for consistent code style
- Follow Material 3 design principles
- Implement proper error handling
- Use meaningful variable and function names

## 🐛 Troubleshooting

### Common Issues

1. **API Connection Failed**
   - Ensure the Django backend is running on `http://127.0.0.1:8000`
   - Check CORS settings in Django
   - Verify network connectivity

2. **Authentication Issues**
   - Clear app data and try logging in again
   - Check if tokens are being stored properly
   - Verify backend authentication endpoints

3. **Build Issues**
   - Run `flutter clean` and `flutter pub get`
   - Check Flutter and Dart SDK versions
   - Ensure all dependencies are compatible

### Debug Mode

Enable debug mode for detailed logging:

```dart
// In main.dart
void main() {
  runApp(
    ProviderScope(
      child: RupixAIApp(),
    ),
  );
}
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

## 🔄 Version History

- **v1.0.0** - Initial release with basic image generation
- **v1.1.0** - Added social login and payment integration
- **v1.2.0** - Web compatibility and improved UI

---

**Built with ❤️ using Flutter**
