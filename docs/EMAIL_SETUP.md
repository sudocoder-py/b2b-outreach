# Email Account Setup Guide

This guide explains how to set up and use the database-driven email system for sending campaign emails.

## Overview

The system now uses database-stored email accounts instead of Django's default SMTP settings. This allows:

- Multiple email accounts per company
- Individual daily limits for each account
- Load balancing across accounts
- Support for both SMTP and OAuth2 accounts
- Per-campaign email account assignment

## Email Account Model

Each email account has the following key fields:

- `email`: The email address
- `connection_type`: 'gmail', 'outlook', 'yahoo', or 'imap/smtp'
- `status`: 'active', 'inactive', 'error', or 'pending'
- `daily_limit`: Maximum emails per day (default: 30)
- `emails_sent`: Current daily count (resets daily)
- `min_wait_time`: Minimum seconds between emails (default: 1)

### SMTP Accounts

For SMTP accounts, configure:
- `smtp_host`: SMTP server hostname
- `smtp_port`: SMTP port (usually 587 or 465)
- `smtp_use_tls`: Use TLS encryption
- `smtp_use_ssl`: Use SSL encryption
- `smtp_username`: SMTP username
- `smtp_password`: SMTP password

### OAuth2 Accounts (Future)

OAuth2 accounts (Gmail, Outlook, Yahoo) will use:
- `access_token`: OAuth2 access token
- `refresh_token`: OAuth2 refresh token
- `token_expiry`: Token expiration date

## Setting Up Email Accounts

### 1. Create Email Accounts

Add email accounts through Django admin or API:

```python
from clients.models import EmailAccount, SubscribedCompany

# Get your company
company = SubscribedCompany.objects.get(id=1)

# Create SMTP email account
account = EmailAccount.objects.create(
    subscribed_company=company,
    email='your-email@domain.com',
    connection_type='imap/smtp',
    status='active',
    smtp_host='smtp.your-provider.com',
    smtp_port=587,
    smtp_use_tls=True,
    smtp_username='your-email@domain.com',
    smtp_password='your-password',
    sender_name='Your Name',
    daily_limit=50
)
```

### 2. Assign Accounts to Campaigns

In your campaign options, assign email accounts:

```python
from campaign.models import CampaignOptions

# Get campaign options
options = CampaignOptions.objects.get(campaign_id=1)

# Assign email accounts
options.email_accounts.add(account)
```

### 3. Test Connections

Test email account connections:

```bash
# Test all active accounts
python manage.py test_email_accounts

# Test specific account by ID
python manage.py test_email_accounts --account-id 1

# Test specific account by email
python manage.py test_email_accounts --email your-email@domain.com
```

## Daily Limits and Reset

### Automatic Reset

Set up a daily cron job to reset email counts:

```bash
# Add to crontab (runs daily at midnight)
0 0 * * * cd /path/to/your/project && python manage.py reset_daily_email_counts
```

### Manual Reset

Reset counts manually:

```bash
python manage.py reset_daily_email_counts
```

## API Endpoints

### Test Connection

```bash
POST /api/email-accounts/{id}/test-connection/
```

Returns:
```json
{
    "success": true,
    "message": "SMTP connection successful for your-email@domain.com",
    "account_email": "your-email@domain.com"
}
```

## How It Works

1. **Email Selection**: When sending a campaign email, the system:
   - Gets email accounts assigned to the campaign
   - Filters for active accounts
   - Checks daily limits
   - Selects an available account randomly for load balancing

2. **Sending Process**: 
   - Creates a custom SMTP backend for the selected account
   - Sends the email using the account's SMTP settings
   - Updates the account's daily usage counter
   - Records the sent status in the message assignment

3. **Error Handling**:
   - If no accounts are available, the email is not sent
   - Connection errors are logged and returned
   - Failed sends don't increment usage counters

## Common SMTP Settings

### Gmail
- Host: `smtp.gmail.com`
- Port: `587`
- TLS: `True`
- Note: Use App Passwords, not regular passwords

### Outlook/Hotmail
- Host: `smtp-mail.outlook.com`
- Port: `587`
- TLS: `True`

### Yahoo
- Host: `smtp.mail.yahoo.com`
- Port: `587` or `465`
- TLS: `True` (port 587) or SSL: `True` (port 465)

### Zoho
- Host: `smtp.zoho.com`
- Port: `587` or `465`
- TLS: `True` (port 587) or SSL: `True` (port 465)

## Troubleshooting

### Connection Issues
1. Verify SMTP settings are correct
2. Check if the email provider requires app passwords
3. Ensure firewall allows SMTP connections
4. Test with the management command

### Daily Limits
1. Check if accounts have reached daily limits
2. Increase daily limits if needed
3. Add more email accounts for higher volume
4. Ensure daily reset cron job is running

### OAuth2 (Future)
OAuth2 implementation is planned for future releases and will provide:
- Better security (no password storage)
- Higher sending limits
- Automatic token refresh
- Native API integration
