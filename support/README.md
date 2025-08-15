# Support Chat System with Telegram Bot

This system provides a complete support chat integration using Telegram Bot API and Django REST Framework.

## Setup Instructions

### 1. Telegram Bot Setup

#### Create a Telegram Bot:
1. Open Telegram and search for `@BotFather`
2. Send `/newbot` command
3. Follow the instructions to create your bot
4. Save the `BOT_TOKEN` you receive

#### Create Support Group:
1. Create a private Telegram group for your support team
2. Add your bot to the group
3. Make the bot an admin (required for sending messages)
4. Get the group chat ID:
   - Add `@userinfobot` to your group temporarily
   - The bot will show the group ID (negative number)
   - Remove `@userinfobot` after getting the ID

### 2. Environment Variables

Add these to your `.env` file:

```env
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_SUPPORT_CHAT_ID=-1001234567890  # Your group chat ID (negative number)
TELEGRAM_WEBHOOK_API_KEY=your-secret-webhook-key-here
DJANGO_API_URL=http://localhost:8000  # Your Django API URL
```

### 3. Install Dependencies

```bash
pip install python-telegram-bot==21.9
```

### 4. Database Migration

```bash
python manage.py makemigrations support
python manage.py migrate
```

### 5. Running the Bot

#### Option A: Polling Mode (Development)
```bash
python manage.py run_telegram_bot
```

#### Option B: Webhook Mode (Production)
```bash
python manage.py set_telegram_webhook https://yourdomain.com/support/webhook/telegram/
```

## API Endpoints

### Authentication
All user endpoints require authentication. Include the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

### User Endpoints

#### 1. Create Message (Start Chat)
```http
POST /support/api/messages/
Content-Type: application/json

{
    "content": "Hello, I need help with my account",
    "message_type": "text",
    "page_url": "https://example.com/dashboard",
    "subject": "Account Issue"
}
```

Response:
```json
{
    "message": {
        "id": "uuid",
        "sender": "user",
        "message_type": "text",
        "content": "Hello, I need help with my account",
        "created_at": "2024-01-01T12:00:00Z",
        "support_agent_name": "",
        "is_read": false
    },
    "session_id": "session-uuid",
    "session_url": "http://localhost:8000/support/chat/session-uuid/"
}
```

#### 2. Continue Existing Chat
```http
POST /support/api/messages/
Content-Type: application/json

{
    "session_id": "existing-session-uuid",
    "content": "Thanks for the help!",
    "message_type": "text"
}
```

#### 3. List User's Chat Sessions
```http
GET /support/api/sessions/
```

Response:
```json
[
    {
        "id": "session-uuid",
        "created_at": "2024-01-01T12:00:00Z",
        "updated_at": "2024-01-01T12:30:00Z",
        "is_active": true,
        "page_url": "https://example.com/dashboard",
        "subject": "Account Issue",
        "message_count": 5,
        "messages": [...]
    }
]
```

#### 4. Get Specific Chat Session
```http
GET /support/api/sessions/{session_id}/
```

#### 5. Get Messages for Session
```http
GET /support/api/sessions/{session_id}/messages/
```

### Webhook Endpoint (Internal)

#### Telegram Bot Webhook
```http
POST /support/webhook/telegram/
X-API-Key: your-webhook-api-key
Content-Type: application/json

{
    "session_id": "session-uuid",
    "content": "Hello! How can I help you?",
    "support_agent_name": "John Doe",
    "telegram_user_id": 123456789,
    "message_type": "text"
}
```

## Support Team Usage

### In Telegram Group

When a user sends a message, the bot will post to your support group:

```
🆘 New Support Message

👤 User: john@example.com (john_doe)
🆔 Session ID: `abc123-def456-ghi789`
🔗 Session URL: http://localhost:8000/support/chat/abc123-def456-ghi789/
📄 Page: https://example.com/dashboard
📝 Subject: Account Issue

💬 Message:
Hello, I need help with my account

---
Reply with: /reply abc123-def456-ghi789 <your response>
```

### Replying to Users

#### Method 1: Using /reply command
```
/reply abc123-def456-ghi789 Hello! I can help you with your account. What specific issue are you experiencing?
```

#### Method 2: Reply to bot message
Simply reply to the bot's message in the group chat. The bot will automatically extract the session ID.

## Error Handling

- Invalid session IDs will return 404 errors
- Missing authentication will return 401 errors
- Malformed requests will return 400 errors
- Bot configuration errors are logged to Django logs

## Security Notes

- The webhook endpoint uses API key authentication
- Change the default `TELEGRAM_WEBHOOK_API_KEY` in production
- User endpoints require proper Django authentication
- Bot token should be kept secret and not committed to version control
