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
from .tracking import add_tracking_to_email

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

        logger.info(f"🔧 Initializing CustomEmailBackend:")
        logger.info(f"   Host: {kwargs['host']}")
        logger.info(f"   Port: {kwargs['port']}")
        logger.info(f"   Username: {kwargs['username']}")
        logger.info(f"   Use TLS: {kwargs['use_tls']}")
        logger.info(f"   Use SSL: {kwargs['use_ssl']}")

        super().__init__(**kwargs)

    def open(self):
        """
        Override open method to provide better error logging
        """
        try:
            logger.info(f"🔄 Opening SMTP connection to {self.host}:{self.port}")
            result = super().open()
            if result:
                logger.info("✅ SMTP connection opened successfully")
            else:
                logger.error("❌ SMTP connection failed to open")
            return result
        except Exception as e:
            logger.error(f"💥 SMTP connection error: {str(e)}")
            logger.error(f"💥 Error type: {type(e).__name__}")
            raise e


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
        logger.info(f"📧 Finding available email account for campaign: {campaign.name} (ID: {campaign.id})")

        # Get campaign options to find assigned email accounts
        campaign_options = campaign.campaign_options.first()
        if not campaign_options:
            logger.error(f"❌ No campaign options found for campaign {campaign.id}")
            return None

        logger.info(f"✅ Campaign options found (ID: {campaign_options.id})")

        # Get email accounts assigned to this campaign
        email_accounts = campaign_options.email_accounts.filter(
            status='active'
        ).order_by('?')  # Random order for load balancing

        if not email_accounts.exists():
            logger.error(f"❌ No active email accounts found for campaign {campaign.id}")
            return None

        logger.info(f"✅ Found {email_accounts.count()} active email accounts for campaign {campaign.id}")

        # Check daily limits and find available account
        today = date.today()

        for account in email_accounts:
            logger.info(f"🔍 Checking account: {account.email} (sent: {account.emails_sent}/{account.daily_limit})")
            # Check if account has reached daily limit
            if account.emails_sent < account.daily_limit:
                logger.info(f"✅ Selected email account: {account.email} (sent: {account.emails_sent}/{account.daily_limit})")
                return account
            else:
                logger.warning(f"⚠️ Account {account.email} has reached daily limit ({account.emails_sent}/{account.daily_limit})")

        logger.warning(f"❌ All email accounts for campaign {campaign.id} have reached their daily limits")
        return None

    except Exception as e:
        logger.error(f"💥 Error getting available email account for campaign {campaign.id}: {str(e)}")
        import traceback
        logger.error(f"💥 Full traceback:\n{traceback.format_exc()}")
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
        campaign: Campaign object (for email account selection)

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

        # Create HTML version with proper formatting and tracking
        html_content = format_email_as_html(content, message_assignment)

        # Create custom email backend for this account
        if email_account.is_smtp():
            logger.info(f"📧 Using SMTP backend for {email_account.email}")
            logger.info(f"🔧 SMTP Config: {email_account.smtp_host}:{email_account.smtp_port}")
            logger.info(f"🔧 TLS: {email_account.smtp_use_tls}, SSL: {email_account.smtp_use_ssl}")
            logger.info(f"🔧 Username: {email_account.smtp_username}")

            try:
                backend = CustomEmailBackend(email_account)
                logger.info("✅ SMTP backend created successfully")

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
                logger.info("✅ Email message created successfully")

                # Test connection first
                logger.info("🔄 Testing SMTP connection...")
                try:
                    connection = backend.open()
                    if connection:
                        logger.info("✅ SMTP connection test successful")
                        backend.close()
                    else:
                        logger.error("❌ SMTP connection test failed")
                        return False
                except Exception as conn_error:
                    logger.error(f"❌ SMTP connection test failed: {str(conn_error)}")
                    logger.error(f"❌ Connection error type: {type(conn_error).__name__}")

                    # Provide specific SSL/TLS troubleshooting
                    if "SSL" in str(conn_error) or "TLS" in str(conn_error):
                        logger.error("🔧 SSL/TLS Configuration Issue Detected:")
                        logger.error(f"   Current settings: TLS={email_account.smtp_use_tls}, SSL={email_account.smtp_use_ssl}")
                        logger.error(f"   Port: {email_account.smtp_port}")
                        logger.error("   💡 Common fixes:")
                        logger.error("      - Port 587 usually requires TLS=True, SSL=False")
                        logger.error("      - Port 465 usually requires TLS=False, SSL=True")
                        logger.error("      - Port 25 usually requires TLS=False, SSL=False")

                        # Suggest alternative configurations
                        if email_account.smtp_port == 587 and not email_account.smtp_use_tls:
                            logger.error("   🔧 Try: TLS=True, SSL=False for port 587")
                        elif email_account.smtp_port == 465 and not email_account.smtp_use_ssl:
                            logger.error("   🔧 Try: TLS=False, SSL=True for port 465")

                    return False

                # Send the email
                logger.info("🔄 Sending email...")
                sent = email.send(fail_silently=False)

                if sent:
                    logger.info("✅ Email sent successfully via SMTP")
                else:
                    logger.error("❌ Email sending failed (no exception thrown)")

            except Exception as smtp_error:
                logger.error(f"💥 SMTP Error: {str(smtp_error)}")
                logger.error(f"💥 Error type: {type(smtp_error).__name__}")

                # Enhanced SSL/TLS error analysis
                error_str = str(smtp_error).lower()
                if "ssl" in error_str or "tls" in error_str:
                    logger.error("🔧 SSL/TLS Error Analysis:")
                    logger.error(f"   Host: {email_account.smtp_host}")
                    logger.error(f"   Port: {email_account.smtp_port}")
                    logger.error(f"   TLS: {email_account.smtp_use_tls}")
                    logger.error(f"   SSL: {email_account.smtp_use_ssl}")

                    if "wrong version number" in error_str:
                        logger.error("   🚨 Wrong SSL/TLS version error detected!")
                        logger.error("   💡 This usually means:")
                        logger.error("      1. Using SSL=True on a TLS-only port (like 587)")
                        logger.error("      2. Using TLS=True on an SSL-only port (like 465)")
                        logger.error("      3. Server doesn't support the SSL/TLS version")

                        # Provide specific recommendations based on common providers
                        host_lower = email_account.smtp_host.lower()
                        if "gmail" in host_lower:
                            logger.error("   🔧 Gmail recommendations:")
                            logger.error("      - Port 587: TLS=True, SSL=False")
                            logger.error("      - Port 465: TLS=False, SSL=True")
                        elif "outlook" in host_lower or "hotmail" in host_lower:
                            logger.error("   🔧 Outlook recommendations:")
                            logger.error("      - Port 587: TLS=True, SSL=False")
                        elif "yahoo" in host_lower:
                            logger.error("   🔧 Yahoo recommendations:")
                            logger.error("      - Port 587: TLS=True, SSL=False")
                            logger.error("      - Port 465: TLS=False, SSL=True")

                return False

        else:
            # Handle OAuth2 accounts (Gmail, Outlook, Yahoo)
            logger.info(f"📧 Using OAuth2 for {email_account.connection_type}")
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


def send_campaign_email_with_account(message_assignment, campaign, email_account):
    """
    Send an email for a message assignment using a specific email account.
    This function is used by the rate-limited scheduling system.

    Args:
        message_assignment: MessageAssignment object to send
        campaign: Campaign object
        email_account: Specific EmailAccount object to use for sending

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        if message_assignment.sent:
            logger.info(f"Email already sent for assignment {message_assignment.id}")
            return True

        # Check if account is active and has capacity
        if email_account.status != 'active':
            logger.error(f"Email account {email_account.email} is not active")
            return False

        if email_account.emails_sent >= email_account.daily_limit:
            logger.error(f"Email account {email_account.email} has reached daily limit ({email_account.emails_sent}/{email_account.daily_limit})")
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
        logger.info(f"📧 Sending via {email_account.email} to {recipient_name} <{recipient_email}>")
        logger.info(f"📧 Subject: {subject}")

        # Create plain text version
        plain_text = content

        # Create HTML version with proper formatting and tracking
        html_content = format_email_as_html(content, message_assignment)

        # Send email based on account type
        sent = False

        if email_account.is_smtp():
            logger.info(f"📧 Using SMTP backend for {email_account.email}")

            try:
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

                if sent:
                    logger.info(f"✅ Email sent successfully via SMTP from {email_account.email}")
                else:
                    logger.error(f"❌ Email sending failed from {email_account.email}")

            except Exception as smtp_error:
                logger.error(f"💥 SMTP Error from {email_account.email}: {str(smtp_error)}")
                return False

        else:
            # Handle OAuth2 accounts (Gmail, Outlook, Yahoo)
            logger.info(f"📧 Using OAuth2 for {email_account.connection_type}")
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
            logger.info(f"✅ Successfully sent email to {recipient_email} from {email_account.email}")

            # Update message assignment
            message_assignment.sent = True
            message_assignment.sent_at = timezone.now()
            message_assignment.save(update_fields=['sent', 'sent_at'])

            # Update email account usage
            update_email_account_usage(email_account)

            # Update analytics efficiently
            from .services import AnalyticsService
            AnalyticsService.handle_email_sent(message_assignment)

            return True
        else:
            logger.error(f"❌ Failed to send email to {recipient_email} from {email_account.email}")
            return False

    except Exception as e:
        logger.error(f"💥 Error sending email with specific account {email_account.email}: {str(e)}")
        return False


def format_email_as_html(content, message_assignment=None):
    """
    Format plain text content as HTML with proper line breaks and paragraphs

    Args:
        content: Plain text content to format
        message_assignment: MessageAssignment object for tracking (optional)

    Returns:
        str: HTML formatted content with tracking if enabled
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

    # Add tracking if message_assignment is provided
    if message_assignment:
        try:
            html_content = add_tracking_to_email(html_content, message_assignment)
        except Exception as e:
            logger.error(f"Error adding tracking to email: {str(e)}")
            # Continue with original content if tracking fails

    return html_content