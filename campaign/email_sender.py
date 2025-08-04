from django.core.mail import send_mail, EmailMultiAlternatives
from django.core.mail.backends.smtp import EmailBackend
from django.conf import settings
from django.utils import timezone
from django.db import transaction
from clients.models import EmailAccount
import logging
import html
import smtplib
import random
from datetime import date

logger = logging.getLogger(__name__)


class CustomEmailBackend(EmailBackend):
    """
    Custom email backend that uses EmailAccount settings instead of Django settings
    """
    def __init__(self, email_account, **kwargs):
        self.email_account = email_account

        # Set SMTP settings from EmailAccount
        kwargs.update({
            'host': email_account.smtp_host,
            'port': email_account.smtp_port,
            'username': email_account.smtp_username,
            'password': email_account.smtp_password,
            'use_tls': email_account.smtp_use_tls,
            'use_ssl': email_account.smtp_use_ssl,
        })

        super().__init__(**kwargs)


def get_available_email_account(campaign):
    """
    Get an available email account for sending emails based on campaign options
    and daily limits.

    Args:
        campaign: Campaign object

    Returns:
        EmailAccount object or None if no account is available
    """
    try:
        # Get campaign options to find assigned email accounts
        campaign_options = campaign.campaign_options.first()
        if not campaign_options:
            logger.error(f"No campaign options found for campaign {campaign.id}")
            return None

        # Get email accounts assigned to this campaign
        email_accounts = campaign_options.email_accounts.filter(
            status='active'
        ).order_by('?')  # Random order for load balancing

        if not email_accounts.exists():
            logger.error(f"No active email accounts found for campaign {campaign.id}")
            return None

        # Check daily limits and find available account
        today = date.today()

        for account in email_accounts:
            # Check if account has reached daily limit
            if account.emails_sent < account.daily_limit:
                logger.info(f"Selected email account: {account.email} (sent: {account.emails_sent}/{account.daily_limit})")
                return account

        logger.warning(f"All email accounts for campaign {campaign.id} have reached their daily limits")
        return None

    except Exception as e:
        logger.error(f"Error getting available email account: {str(e)}")
        return None


def update_email_account_usage(email_account):
    """
    Update the email account usage counter

    Args:
        email_account: EmailAccount object
    """
    try:
        with transaction.atomic():
            # Refresh from database to avoid race conditions
            account = EmailAccount.objects.select_for_update().get(id=email_account.id)
            account.emails_sent += 1
            account.save(update_fields=['emails_sent'])
            logger.info(f"Updated email count for {account.email}: {account.emails_sent}/{account.daily_limit}")
    except Exception as e:
        logger.error(f"Error updating email account usage: {str(e)}")


def reset_daily_email_counts():
    """
    Reset daily email counts for all email accounts.
    This should be called daily via a cron job or scheduled task.
    """
    try:
        updated_count = EmailAccount.objects.filter(emails_sent__gt=0).update(emails_sent=0)
        logger.info(f"Reset daily email counts for {updated_count} email accounts")
        return updated_count
    except Exception as e:
        logger.error(f"Error resetting daily email counts: {str(e)}")
        return 0


def test_email_account_connection(email_account):
    """
    Test the connection for an email account

    Args:
        email_account: EmailAccount object

    Returns:
        dict: {'success': bool, 'message': str}
    """
    try:
        if email_account.is_smtp():
            # Test SMTP connection
            backend = CustomEmailBackend(email_account)
            connection = backend.open()

            if connection:
                backend.close()
                return {
                    'success': True,
                    'message': f'SMTP connection successful for {email_account.email}'
                }
            else:
                return {
                    'success': False,
                    'message': f'SMTP connection failed for {email_account.email}'
                }

        elif email_account.requires_oauth():
            # Test OAuth2 connection (placeholder for future implementation)
            return {
                'success': False,
                'message': f'OAuth2 testing not yet implemented for {email_account.connection_type}'
            }
        else:
            return {
                'success': False,
                'message': f'Unknown connection type: {email_account.connection_type}'
            }

    except Exception as e:
        logger.error(f"Error testing email account connection: {str(e)}")
        return {
            'success': False,
            'message': f'Connection test failed: {str(e)}'
        }


def send_campaign_email(message_assignment, campaign):
    """
    Send an email for a message assignment with tracking using database-stored email accounts

    Args:
        message_assignment: MessageAssignment object to send

    Returns:
        bool: True if successful, False otherwise, or "already sent" if already sent
    """
    try:
        if message_assignment.sent == True:
            return "already sent"

        # Get an available email account
        email_account = get_available_email_account(campaign)
        if not email_account:
            logger.error(f"No available email account for campaign {campaign.id}")
            return False

        # Get personalized content with tracking URL
        subject = message_assignment.message.subject

        # Use personalized content if available, otherwise get default personalized content
        if message_assignment.personlized_msg_to_send:
            content = message_assignment.personlized_msg_to_send
        else:
            content = message_assignment.get_personalized_content()

        # Get recipient email
        recipient_email = message_assignment.campaign_lead.lead.email
        recipient_name = message_assignment.campaign_lead.lead.full_name

        # Determine sender information
        sender_name = email_account.sender_name or email_account.email.split('@')[0]
        from_email = f"{sender_name} <{email_account.email}>"

        # Log the email details for debugging
        logger.info(f"Preparing to send email to {recipient_name} <{recipient_email}>")
        logger.info(f"From: {from_email}")
        logger.info(f"Subject: {subject}")
        logger.info(f"Content: {content[:100]}...")  # Log first 100 chars of content

        # Create plain text version (for email clients that don't support HTML)
        plain_text = content

        # Create HTML version with proper formatting
        html_content = format_email_as_html(content)

        # Create custom email backend for this account
        if email_account.is_smtp():
            backend = CustomEmailBackend(email_account)

            # Create email message with both HTML and plain text versions
            email = EmailMultiAlternatives(
                subject=subject,
                body=plain_text,  # Plain text version
                from_email=from_email,
                to=[f"{recipient_name} <{recipient_email}>"],
                connection=backend
            )

            # Add HTML version
            email.attach_alternative(html_content, "text/html")

            # Send the email
            sent = email.send(fail_silently=False)

        else:
            # Handle OAuth2 accounts (Gmail, Outlook, Yahoo)
            from .email_oauth import send_oauth2_email
            sent = send_oauth2_email(
                email_account,
                subject,
                html_content,
                recipient_email,
                recipient_name
            )

        # Record that the email was sent if successful
        if sent:
            logger.info(f"Successfully sent email to {recipient_email} from {email_account.email}")

            # Update message assignment
            message_assignment.sent = True
            message_assignment.sent_at = timezone.now()
            message_assignment.save(update_fields=['sent', 'sent_at'])

            # Update email account usage
            update_email_account_usage(email_account)

            # 🔥 Update analytics efficiently
            from .services import AnalyticsService
            AnalyticsService.handle_email_sent(message_assignment)

            return True
        else:
            logger.error(f"Failed to send email to {recipient_email} from {email_account.email}")
            return False

    except Exception as e:
        logger.error(f"Error sending email: {str(e)}")
        return False

def format_email_as_html(content):
    """
    Format plain text content as HTML with proper line breaks and paragraphs
    
    Args:
        content: Plain text content to format
        
    Returns:
        str: HTML formatted content
    """
    # Replace newlines with HTML line breaks
    
    # Wrap in HTML structure
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333333;
                margin: 0;
                padding: 20px;
            }}
            p {{
                margin-bottom: 16px;
                font-size: 16px;
            }}
            a {{
                color: #0066cc;
                text-decoration: none;
            }}
            a:hover {{
                text-decoration: underline;
            }}
            .signature {{
                margin-top: 30px;
                border-top: 1px solid #eeeeee;
                padding-top: 10px;
                color: #666666;
            }}
            ul {{
                padding-left: 20px;
                margin-bottom: 16px;
            }}
            li {{
                margin-bottom: 8px;
                font-size: 16px;
            }}
        </style>
    </head>
    <body>
        <div>{content}</div>
    </body>
    </html>
    """
    
    return html_content