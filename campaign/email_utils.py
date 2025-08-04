"""
Email utility functions for campaign management
"""

from clients.models import EmailAccount
from django.db.models import Q, F
from django.db import models
import logging

logger = logging.getLogger(__name__)


def get_email_account_stats(company=None):
    """
    Get statistics about email accounts
    
    Args:
        company: SubscribedCompany object (optional)
        
    Returns:
        dict: Statistics about email accounts
    """
    queryset = EmailAccount.objects.all()
    
    if company:
        queryset = queryset.filter(subscribed_company=company)
    
    stats = {
        'total_accounts': queryset.count(),
        'active_accounts': queryset.filter(status='active').count(),
        'inactive_accounts': queryset.filter(status='inactive').count(),
        'error_accounts': queryset.filter(status='error').count(),
        'pending_accounts': queryset.filter(status='pending').count(),
        'smtp_accounts': queryset.filter(connection_type='imap/smtp').count(),
        'gmail_accounts': queryset.filter(connection_type='gmail').count(),
        'outlook_accounts': queryset.filter(connection_type='outlook').count(),
        'yahoo_accounts': queryset.filter(connection_type='yahoo').count(),
        'total_daily_limit': sum(account.daily_limit for account in queryset),
        'total_emails_sent_today': sum(account.emails_sent for account in queryset),
    }
    
    # Calculate remaining capacity
    stats['remaining_capacity'] = stats['total_daily_limit'] - stats['total_emails_sent_today']
    
    # Calculate utilization percentage
    if stats['total_daily_limit'] > 0:
        stats['utilization_percentage'] = (stats['total_emails_sent_today'] / stats['total_daily_limit']) * 100
    else:
        stats['utilization_percentage'] = 0
    
    return stats


def get_available_accounts_for_campaign(campaign):
    """
    Get available email accounts for a specific campaign
    
    Args:
        campaign: Campaign object
        
    Returns:
        QuerySet: Available EmailAccount objects
    """
    try:
        campaign_options = campaign.campaign_options.first()
        if not campaign_options:
            return EmailAccount.objects.none()
            
        return campaign_options.email_accounts.filter(
            status='active'
        ).filter(
            Q(emails_sent__lt=F('daily_limit'))
        )
        
    except Exception as e:
        logger.error(f"Error getting available accounts for campaign {campaign.id}: {str(e)}")
        return EmailAccount.objects.none()


def bulk_update_email_account_status(account_ids, new_status):
    """
    Bulk update email account status
    
    Args:
        account_ids: List of EmailAccount IDs
        new_status: New status ('active', 'inactive', 'error', 'pending')
        
    Returns:
        int: Number of accounts updated
    """
    try:
        updated_count = EmailAccount.objects.filter(
            id__in=account_ids
        ).update(status=new_status)
        
        logger.info(f"Updated {updated_count} email accounts to status: {new_status}")
        return updated_count
        
    except Exception as e:
        logger.error(f"Error bulk updating email account status: {str(e)}")
        return 0


def create_smtp_account(company, email, smtp_config, sender_config=None):
    """
    Create a new SMTP email account
    
    Args:
        company: SubscribedCompany object
        email: Email address
        smtp_config: Dict with SMTP settings (host, port, username, password, use_tls, use_ssl)
        sender_config: Dict with sender settings (name, signature, daily_limit)
        
    Returns:
        EmailAccount object or None if creation failed
    """
    try:
        sender_config = sender_config or {}
        
        account = EmailAccount.objects.create(
            subscribed_company=company,
            email=email,
            connection_type='imap/smtp',
            status='pending',  # Start as pending until tested
            smtp_host=smtp_config.get('host'),
            smtp_port=smtp_config.get('port', 587),
            smtp_username=smtp_config.get('username', email),
            smtp_password=smtp_config.get('password'),
            smtp_use_tls=smtp_config.get('use_tls', True),
            smtp_use_ssl=smtp_config.get('use_ssl', False),
            sender_name=sender_config.get('name', ''),
            sender_signature=sender_config.get('signature', ''),
            daily_limit=sender_config.get('daily_limit', 30),
            min_wait_time=sender_config.get('min_wait_time', 1)
        )
        
        logger.info(f"Created SMTP email account: {email}")
        return account
        
    except Exception as e:
        logger.error(f"Error creating SMTP email account {email}: {str(e)}")
        return None


def validate_smtp_config(smtp_config):
    """
    Validate SMTP configuration
    
    Args:
        smtp_config: Dict with SMTP settings
        
    Returns:
        dict: {'valid': bool, 'errors': list}
    """
    errors = []
    
    required_fields = ['host', 'username', 'password']
    for field in required_fields:
        if not smtp_config.get(field):
            errors.append(f"Missing required field: {field}")
    
    port = smtp_config.get('port', 587)
    if not isinstance(port, int) or port < 1 or port > 65535:
        errors.append("Port must be a valid integer between 1 and 65535")
    
    use_tls = smtp_config.get('use_tls', True)
    use_ssl = smtp_config.get('use_ssl', False)
    
    if use_tls and use_ssl:
        errors.append("Cannot use both TLS and SSL simultaneously")
    
    return {
        'valid': len(errors) == 0,
        'errors': errors
    }


# Common SMTP configurations
SMTP_PROVIDERS = {
    'gmail': {
        'host': 'smtp.gmail.com',
        'port': 587,
        'use_tls': True,
        'use_ssl': False,
    },
    'outlook': {
        'host': 'smtp-mail.outlook.com',
        'port': 587,
        'use_tls': True,
        'use_ssl': False,
    },
    'yahoo': {
        'host': 'smtp.mail.yahoo.com',
        'port': 587,
        'use_tls': True,
        'use_ssl': False,
    },
    'zoho': {
        'host': 'smtp.zoho.com',
        'port': 587,
        'use_tls': True,
        'use_ssl': False,
    }
}


def get_smtp_config_for_provider(provider):
    """
    Get SMTP configuration for a known provider
    
    Args:
        provider: Provider name ('gmail', 'outlook', 'yahoo', 'zoho')
        
    Returns:
        dict: SMTP configuration or None if provider not found
    """
    return SMTP_PROVIDERS.get(provider.lower())
