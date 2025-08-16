# Support Chat - Production Deployment Guide

## 🚀 Production Configuration

### 1. Environment Variables

Update your production `.env` file:

```env
# Django API URL - MUST be your actual domain
DJANGO_API_URL=https://vibereach.gatara.org

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_SUPPORT_CHAT_ID=your_chat_id_here
TELEGRAM_WEBHOOK_API_KEY=UpppKXgmTR8Jc+eelW7ncFLcAoIl11AMVa4tbhNfWWor

# Your existing domain config (keep these)
ALLOWED_HOSTS=localhost,127.0.0.1,vibereach.gatara.org
CSRF_TRUSTED_ORIGINS=https://vibereach.gatara.org
SITE_URL=https://vibereach.gatara.org
```

### 2. Deployment Options

#### Option A: Polling Mode (Simple)
The docker-compose.yml has been updated to include a separate `telegram-bot` service that runs in polling mode.

**Deploy:**
```bash
docker-compose up -d
```

**Pros:**
- Simple setup
- Works behind firewalls
- No additional configuration needed

**Cons:**
- Uses more resources (constant polling)
- Slight delay in message processing

#### Option B: Webhook Mode (Recommended for Production)

**Step 1:** Remove the telegram-bot service from docker-compose.yml:
```yaml
# Comment out or remove the telegram-bot service
# telegram-bot:
#   build: .
#   ...
```

**Step 2:** Deploy your main application:
```bash
docker-compose up -d
```

**Step 3:** Set up the webhook (run once after deployment):
```bash
# SSH into your server and run:
docker-compose exec web python manage.py set_telegram_webhook
```

This will automatically set the webhook to: `https://vibereach.gatara.org/support/webhook/telegram/`

**Pros:**
- More efficient (event-driven)
- Instant message processing
- Better for high-traffic applications

**Cons:**
- Requires HTTPS (which you have)
- Webhook URL must be accessible from internet

### 3. Security Considerations

#### Webhook Security
The webhook endpoint is protected by:
- API key authentication (`TELEGRAM_WEBHOOK_API_KEY`)
- HTTPS encryption
- Django CSRF protection (for user endpoints)

#### Recommended Security Settings
```env
# Use a strong, unique webhook API key
TELEGRAM_WEBHOOK_API_KEY=your-very-long-random-secure-key-here

# Ensure HTTPS is enforced
SECURE_SSL_REDIRECT=True
```

### 4. Monitoring & Logging

#### Check Bot Status
```bash
# Check if bot is running (polling mode)
docker-compose logs telegram-bot

# Check webhook status (webhook mode)
curl -X GET "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getWebhookInfo"
```

#### Django Logs
The support system logs to Django's logging system. Check logs for:
- Message forwarding status
- API errors
- Webhook calls

```bash
docker-compose logs web | grep support
```

### 5. Testing in Production

#### Test the Complete Flow:
1. Visit: `https://vibereach.gatara.org/support/test/`
2. Open the chat widget
3. Send a test message
4. Check your Telegram group
5. Reply in Telegram
6. Verify reply appears in chat widget

#### API Health Check:
```bash
# Test API endpoint
curl -X GET https://vibereach.gatara.org/support/api/sessions/ \
  -H "Cookie: sessionid=your_session_id"
```

### 6. Troubleshooting

#### Common Issues:

**1. Messages not forwarding to Telegram:**
- Check `TELEGRAM_BOT_TOKEN` is correct
- Verify `TELEGRAM_SUPPORT_CHAT_ID` is correct (negative number)
- Ensure bot is admin in the group
- Check Django logs for errors

**2. Webhook not receiving replies:**
- Verify `DJANGO_API_URL` uses HTTPS
- Check webhook is set: `python manage.py set_telegram_webhook`
- Verify `TELEGRAM_WEBHOOK_API_KEY` matches in both places

**3. CSRF errors:**
- Ensure `CSRF_TRUSTED_ORIGINS` includes your domain
- Check that frontend is sending CSRF tokens

#### Debug Commands:
```bash
# Check webhook info
python manage.py shell -c "
from support.client import TelegramBotClient
import asyncio
client = TelegramBotClient()
# Check webhook status via Telegram API
"

# Test bot connection
python manage.py test_telegram_send

# Check database
python manage.py shell -c "
from support.models import ChatSession, Message
print(f'Sessions: {ChatSession.objects.count()}')
print(f'Messages: {Message.objects.count()}')
"
```

### 7. Scaling Considerations

For high-traffic applications:

1. **Use webhook mode** instead of polling
2. **Consider Redis** for message queuing
3. **Database indexing** on frequently queried fields
4. **Rate limiting** on API endpoints
5. **Monitoring** with tools like Sentry

### 8. Backup & Recovery

Important data to backup:
- Chat sessions (`ChatSession` model)
- Messages (`Message` model)
- Telegram bot configuration

```bash
# Backup support data
python manage.py dumpdata support > support_backup.json

# Restore support data
python manage.py loaddata support_backup.json
```

## 🎯 Quick Production Checklist

- [ ] Update `DJANGO_API_URL` to your domain
- [ ] Set strong `TELEGRAM_WEBHOOK_API_KEY`
- [ ] Choose polling or webhook mode
- [ ] Deploy with `docker-compose up -d`
- [ ] Set webhook (if using webhook mode)
- [ ] Test complete flow on production
- [ ] Monitor logs for errors
- [ ] Set up backup strategy

## 🆘 Support

If you encounter issues:
1. Check the logs: `docker-compose logs`
2. Test individual components
3. Verify environment variables
4. Check Telegram bot permissions
