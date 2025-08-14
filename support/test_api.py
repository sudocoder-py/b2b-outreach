#!/usr/bin/env python3
"""
Simple test script for the Support Chat API.
Run this after setting up the system to verify everything works.

Usage:
    python support/test_api.py
"""

import requests
import json
import sys
from django.conf import settings

# Configuration
API_BASE_URL = "http://localhost:8000"
USERNAME = "your_username"  # Change this
PASSWORD = "your_password"  # Change this


def get_auth_token():
    """Get JWT token for authentication"""
    login_url = f"{API_BASE_URL}/auth/api/login/"
    data = {
        "username": USERNAME,
        "password": PASSWORD
    }
    
    response = requests.post(login_url, json=data)
    if response.status_code == 200:
        return response.json().get('access')
    else:
        print(f"Login failed: {response.status_code} - {response.text}")
        return None


def test_create_message(token):
    """Test creating a new support message"""
    url = f"{API_BASE_URL}/support/api/messages/"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "content": "Hello, this is a test message from the API test script!",
        "message_type": "text",
        "page_url": "http://localhost:8000/test",
        "subject": "API Test"
    }
    
    response = requests.post(url, json=data, headers=headers)
    print(f"Create Message: {response.status_code}")
    if response.status_code == 201:
        result = response.json()
        print(f"Session ID: {result['session_id']}")
        return result['session_id']
    else:
        print(f"Error: {response.text}")
        return None


def test_list_sessions(token):
    """Test listing chat sessions"""
    url = f"{API_BASE_URL}/support/api/sessions/"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers)
    print(f"List Sessions: {response.status_code}")
    if response.status_code == 200:
        sessions = response.json()
        print(f"Found {len(sessions)} sessions")
        return sessions
    else:
        print(f"Error: {response.text}")
        return []


def test_get_session_messages(token, session_id):
    """Test getting messages for a session"""
    url = f"{API_BASE_URL}/support/api/sessions/{session_id}/messages/"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers)
    print(f"Get Session Messages: {response.status_code}")
    if response.status_code == 200:
        messages = response.json()
        print(f"Found {len(messages)} messages")
        for msg in messages:
            print(f"  - {msg['sender']}: {msg['content'][:50]}...")
    else:
        print(f"Error: {response.text}")


def test_webhook(session_id):
    """Test the webhook endpoint (simulating Telegram bot)"""
    url = f"{API_BASE_URL}/support/webhook/telegram/"
    headers = {
        "X-API-Key": "your-secret-key-change-this",  # Default key from settings
        "Content-Type": "application/json"
    }
    data = {
        "session_id": session_id,
        "content": "This is a test reply from the support team!",
        "support_agent_name": "Test Agent",
        "telegram_user_id": 123456789,
        "message_type": "text"
    }
    
    response = requests.post(url, json=data, headers=headers)
    print(f"Webhook Test: {response.status_code}")
    if response.status_code == 201:
        print("Webhook test successful!")
    else:
        print(f"Webhook Error: {response.text}")


def main():
    print("Testing Support Chat API...")
    print("=" * 40)
    
    # Get authentication token
    print("1. Getting authentication token...")
    token = get_auth_token()
    if not token:
        print("Failed to get authentication token. Please check your credentials.")
        sys.exit(1)
    
    # Test creating a message
    print("\n2. Testing message creation...")
    session_id = test_create_message(token)
    if not session_id:
        print("Failed to create message.")
        sys.exit(1)
    
    # Test listing sessions
    print("\n3. Testing session listing...")
    sessions = test_list_sessions(token)
    
    # Test getting session messages
    print("\n4. Testing session messages...")
    test_get_session_messages(token, session_id)
    
    # Test webhook
    print("\n5. Testing webhook...")
    test_webhook(session_id)
    
    # Test getting messages again to see the support reply
    print("\n6. Testing session messages after webhook...")
    test_get_session_messages(token, session_id)
    
    print("\n" + "=" * 40)
    print("API testing completed!")


if __name__ == "__main__":
    main()
