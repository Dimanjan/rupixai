# RupixAI Mobile App

A Flutter mobile application for AI-powered image generation.

## 🚀 Quick Start

### Prerequisites
- Flutter SDK 3.0+
- Dart SDK 3.0+
- RupixAI backend running on `http://127.0.0.1:8000`

### Installation

```bash
# Install dependencies
flutter pub get

# Run on web
flutter run -d chrome

# Run on Android
flutter run -d android

# Run on iOS
flutter run -d ios
```

### Test Login
- **Username**: `demo`
- **Password**: `demo123`
- **Credits**: 100

## 📱 Features

- ✅ AI Image Generation (OpenAI DALL-E 3, Google Gemini)
- ✅ User Authentication & Registration
- ✅ Credit System & Payment Integration
- ✅ Chat History & Image Management
- ✅ Social Login (Google, Facebook, GitHub, etc.)
- ✅ Cross-Platform (Web, Android, iOS)
- ✅ Material 3 Design

## 🛠️ Tech Stack

- **Flutter** - Cross-platform framework
- **Riverpod** - State management
- **GoRouter** - Navigation
- **Dio** - HTTP client
- **Material 3** - UI design system

## 📁 Project Structure

```
lib/
├── main.dart              # App entry point
├── models/               # Data models
├── providers/            # Riverpod providers
├── screens/              # UI screens
│   ├── auth/            # Login/Register
│   ├── home/            # Image generation
│   ├── profile/         # User profile
│   ├── history/         # Chat history
│   └── payment/         # Credit purchase
├── services/            # API services
├── utils/               # Utilities
└── widgets/             # Reusable widgets
```

## 🔧 Configuration

Update API endpoint in `lib/services/api_service.dart`:

```dart
static const String _baseUrl = 'http://your-backend-url/api';
```

## 🚀 Building

```bash
# Web
flutter build web --release

# Android
flutter build apk --release

# iOS
flutter build ios --release
```

## 📄 License

MIT License - see LICENSE file for details.
