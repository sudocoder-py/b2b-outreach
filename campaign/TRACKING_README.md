# Email Tracking Implementation with PyTracking

This document explains how email open and click tracking has been implemented using the `pytracking` library.

## Overview

The tracking system provides:
- **Open Tracking**: Invisible pixel tracking to detect when emails are opened
- **Click Tracking**: URL rewriting to track link clicks
- **Integration**: Seamless integration with existing `MessageAssignment` and `Link` models
- **Analytics**: Automatic updates to `CampaignStats` for tracking metrics

## Components

### 1. Tracking Configuration (`campaign/tracking.py`)

- `get_pytracking_configuration()`: Creates pytracking config using `SITE_URL` from Django settings
- `add_tracking_to_email()`: Adds tracking pixels and rewrites links in HTML content
- `CustomOpenTrackingView`: Handles open tracking events and updates `MessageAssignment.opened`
- `CustomClickTrackingView`: Handles click tracking events and updates `Link.visit_count`

### 2. Email Sender Integration (`campaign/email_sender.py`)

- Modified `format_email_as_html()` to accept `message_assignment` parameter
- Automatic tracking injection when sending emails
- Respects campaign options (`open_tracking_enabled`, `link_tracking_enabled`)

### 3. URL Configuration (`campaign/urls.py`)

New tracking endpoints:
- `/campaign/tracking/open/<path>` - Open tracking pixel endpoint
- `/campaign/tracking/click/<path>` - Click tracking redirect endpoint

## Setup Instructions

### 1. Install Dependencies

```bash
pip install pytracking
```

### 2. Update Django Settings

Add to `INSTALLED_APPS`:
```python
INSTALLED_APPS = [
    # ... other apps
    'pytracking',
    # ... rest of apps
]
```

Ensure `SITE_URL` is configured:
```python
SITE_URL = 'https://yourdomain.com'  # or http://localhost:8000 for development
```

### 3. Run Migrations

```bash
python manage.py migrate
```

### 4. Enable Tracking for Campaigns

Use the management command to enable tracking:

```bash
# Enable tracking for all campaigns
python manage.py enable_tracking --all

# Enable tracking for specific campaign
python manage.py enable_tracking --campaign-id 1

# Enable only open tracking
python manage.py enable_tracking --all --open-tracking

# Preview changes without applying
python manage.py enable_tracking --all --dry-run
```

## How It Works

### Open Tracking

1. When an email is sent, a tracking pixel is automatically inserted into the HTML
2. The pixel URL contains encrypted metadata about the `MessageAssignment`
3. When the email is opened, the pixel is loaded, triggering the tracking endpoint
4. The system updates `MessageAssignment.opened = True` and `opened_at = timezone.now()`
5. Campaign statistics are automatically updated

### Click Tracking

1. All links in the email HTML are automatically rewritten to go through tracking URLs
2. When a link is clicked, it goes to the tracking endpoint first
3. The system records the click and updates relevant `Link` objects
4. The user is then redirected to the original destination
5. Campaign statistics are automatically updated

### Integration with Existing Models

The tracking system integrates seamlessly with your existing models:

- **MessageAssignment**: `opened` and `opened_at` fields are automatically updated
- **Link**: `visit_count` and `visited_at` fields are automatically updated  
- **CampaignStats**: `opened_count` and `clicked_count` are automatically incremented
- **CampaignOptions**: `open_tracking_enabled` and `link_tracking_enabled` control tracking

## Testing

Run the test script to verify tracking is working:

```bash
python campaign/test_tracking.py
```

This will test:
- Pytracking configuration
- Campaign options setup
- HTML modification with tracking

## Monitoring

### Check Tracking Status

View campaign options in Django admin or use the management command:

```bash
python manage.py enable_tracking  # Shows current status
```

### View Tracking Data

- **Opens**: Check `MessageAssignment.opened` and `opened_at` fields
- **Clicks**: Check `Link.visit_count` and `visited_at` fields  
- **Analytics**: View `CampaignStats` for aggregated metrics

## Troubleshooting

### Common Issues

1. **Tracking not working**:
   - Verify `SITE_URL` is correctly configured
   - Check that tracking is enabled in campaign options
   - Ensure pytracking is in `INSTALLED_APPS`

2. **URLs not being tracked**:
   - Verify `link_tracking_enabled = True` in campaign options
   - Check that HTML content contains valid `<a>` tags

3. **Opens not being tracked**:
   - Verify `open_tracking_enabled = True` in campaign options
   - Check that emails are being sent as HTML (not text-only)
   - Note: Some email clients block tracking pixels

### Debug Mode

Enable debug logging to see tracking events:

```python
LOGGING = {
    'loggers': {
        'campaign.tracking': {
            'level': 'DEBUG',
            'handlers': ['console'],
        },
    },
}
```

## Security Considerations

- Tracking URLs contain encrypted metadata, not plain IDs
- The system uses Django's `SECRET_KEY` for encryption
- No sensitive data is exposed in tracking URLs
- Tracking respects campaign-level settings (can be disabled)

## Performance

- Tracking pixels are small (1x1 transparent images)
- Click tracking adds minimal redirect overhead
- Database updates are efficient (single queries per event)
- No impact on email sending performance

## Privacy Compliance

- Tracking can be disabled per campaign via `CampaignOptions`
- Consider adding unsubscribe links and privacy notices
- Tracking data is stored securely in your database
- No third-party tracking services are used
