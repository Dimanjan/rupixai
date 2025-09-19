#!/usr/bin/env python3
"""
Simple test script to verify social login endpoints
"""
import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_social_login_urls():
    """Test the social login URLs endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/social/urls/")
        print(f"Social URLs Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("Available social login URLs:")
            for provider, url in data.items():
                print(f"  {provider}: {url}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error testing social URLs: {e}")

def test_social_callback():
    """Test the social login callback endpoint"""
    try:
        # Test with mock data
        test_data = {
            "provider": "google",
            "access_token": "mock_google_token"
        }
        
        response = requests.post(
            f"{BASE_URL}/social/callback/",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Social Callback Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("Social login successful!")
            print(f"Access token: {data.get('access', 'N/A')[:20]}...")
            print(f"User: {data.get('user', {}).get('username', 'N/A')}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error testing social callback: {e}")

if __name__ == "__main__":
    print("Testing Social Login Endpoints...")
    print("=" * 40)
    
    test_social_login_urls()
    print()
    test_social_callback()
    
    print("\nNote: These are mock tests. For real OAuth integration,")
    print("you need to set up OAuth apps with each provider and")
    print("configure the credentials in your .env file.")
