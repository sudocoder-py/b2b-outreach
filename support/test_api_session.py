#!/usr/bin/env python3
"""
Test script for Support Chat API using Django session authentication.
Make sure you're logged into Django admin first, then run this script.

Usage:
    python support/test_api_session.py
"""

import requests
import json

# Configuration
API_BASE_URL = "http://localhost:8000"
USERNAME = "your_username"  # Change this to your Django admin username
PASSWORD = "your_password"  # Change this to your Django admin password


def login_and_get_session():
    """Login to Django and get session cookies"""
    session = requests.Session()
    
    # Get login page to get CSRF token
    login_page = session.get(f"{API_BASE_URL}/admin/login/")
    if login_page.status_code != 200:
        print(f"Failed to get login page: {login_page.status_code}")
        return None
    
    # Extract CSRF token
    csrf_token = None
    for line in login_page.text.split('\n'):
        if 'csrfmiddlewaretoken' in line and 'value=' in line:
            csrf_token = line.split('value="')[1].split('"')[0]
            break
    
    if not csrf_token:
        print("Could not find CSRF token")
        return None
    
    # Login
    login_data = {
        'username': USERNAME,
        'password': PASSWORD,
        'csrfmiddlewaretoken': csrf_token,
        'next': '/admin/'
    }
    
    login_response = session.post(f"{API_BASE_URL}/admin/login/", data=login_data)
    
    # Check if login was successful
    if login_response.status_code == 200 and '/admin/' in login_response.url:
        print("✅ Successfully logged in!")
        return session
    else:
        print(f"❌ Login failed: {login_response.status_code}")
        return None


def test_create_message(session):
    """Test creating a new support message"""
    # Get CSRF token for API calls
    csrf_response = session.get(f"{API_BASE_URL}/admin/")
    csrf_token = None
    for cookie in session.cookies:
        if cookie.name == 'csrftoken':
            csrf_token = cookie.value
            break
    
    url = f"{API_BASE_URL}/support/api/messages/"
    headers = {
        "Content-Type": "application/json",
        "X-CSRFToken": csrf_token,
        "Referer": API_BASE_URL  # Required for CSRF
    }
    data = {
        "content": "Hello, this is a test message using Django session auth!",
        "message_type": "text",
        "page_url": "http://localhost:8000/test",
        "subject": "Session Auth Test"
    }
    
    response = session.post(url, json=data, headers=headers)
    print(f"Create Message: {response.status_code}")
    if response.status_code == 201:
        result = response.json()
        print(f"Session ID: {result['session_id']}")
        return result['session_id']
    else:
        print(f"Error: {response.text}")
        return None


def test_list_sessions(session):
    """Test listing chat sessions"""
    url = f"{API_BASE_URL}/support/api/sessions/"
    
    response = session.get(url)
    print(f"List Sessions: {response.status_code}")
    if response.status_code == 200:
        sessions = response.json()
        print(f"Found {len(sessions)} sessions")
        return sessions
    else:
        print(f"Error: {response.text}")
        return []


def test_get_session_messages(session, session_id):
    """Test getting messages for a session"""
    url = f"{API_BASE_URL}/support/api/sessions/{session_id}/messages/"
    
    response = session.get(url)
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
        "content": "This is a test reply from the support team via webhook!",
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
    print("Testing Support Chat API with Django Session Authentication...")
    print("=" * 60)
    
    # Login and get session
    print("1. Logging into Django admin...")
    session = login_and_get_session()
    if not session:
        print("Failed to login. Please check your credentials.")
        print("Make sure you have a Django superuser account created.")
        return
    
    # Test creating a message
    print("\n2. Testing message creation...")
    session_id = test_create_message(session)
    if not session_id:
        print("Failed to create message.")
        return
    
    # Test listing sessions
    print("\n3. Testing session listing...")
    sessions = test_list_sessions(session)
    
    # Test getting session messages
    print("\n4. Testing session messages...")
    test_get_session_messages(session, session_id)
    
    # Test webhook
    print("\n5. Testing webhook...")
    test_webhook(session_id)
    
    # Test getting messages again to see the support reply
    print("\n6. Testing session messages after webhook...")
    test_get_session_messages(session, session_id)
    
    print("\n" + "=" * 60)
    print("API testing completed!")
    print("\nNow check your Telegram group - you should see the test message!")


if __name__ == "__main__":
    main()
