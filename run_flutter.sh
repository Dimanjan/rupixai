#!/bin/bash

echo "🚀 Starting RupixAI Flutter Mobile App..."

# Check if Flutter is installed
if ! command -v flutter &> /dev/null; then
    echo "❌ Flutter is not installed. Please install Flutter first."
    echo "Visit: https://flutter.dev/docs/get-started/install"
    exit 1
fi

# Navigate to Flutter app directory
cd rupixai_mobile || { echo "❌ Flutter app directory not found."; exit 1; }

# Check if dependencies are installed
if [ ! -d "build" ] && [ ! -f "pubspec.lock" ]; then
    echo "📦 Installing Flutter dependencies..."
    flutter pub get
fi

# Check for available devices
echo "📱 Checking for available devices..."
flutter devices

echo ""
echo "🎯 Available options:"
echo "1. Run on Android device/emulator"
echo "2. Run on iOS simulator (macOS only)"
echo "3. Run on web browser"
echo "4. Run on desktop (macOS/Windows/Linux)"
echo ""

read -p "Choose an option (1-4): " choice

case $choice in
    1)
        echo "🤖 Starting Android app..."
        flutter run -d android
        ;;
    2)
        echo "🍎 Starting iOS app..."
        flutter run -d ios
        ;;
    3)
        echo "🌐 Starting web app..."
        flutter run -d chrome
        ;;
    4)
        echo "🖥️ Starting desktop app..."
        flutter run -d macos
        ;;
    *)
        echo "❌ Invalid option. Starting with default device..."
        flutter run
        ;;
esac
