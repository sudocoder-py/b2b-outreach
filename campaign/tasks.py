from celery import shared_task  # Removed chain import since we're making tasks independent
from django.utils import timezone
from django.conf import settings
import logging
from datetime import timedelta
from .models import MessageAssignment
from .services import AnalyticsService

logger = logging.getLogger(__name__)


@shared_task(name="personalize_message_task")
def personalize_message_task(message_assignment_id, skip=True):
    """
    Celery task to personalize a message using AI and save it to the database.
    Rate limited to respect AI API limits.

    Args:
        message_assignment_id: ID of the MessageAssignment to personalize
        skip: If True, skip AI and use simple replacement

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        logger.info(f"📝 Personalizing message for assignment ID: {message_assignment_id}")

        # Get the message assignment
        message_assignment = MessageAssignment.objects.get(id=message_assignment_id)
        logger.info(f"✅ Message assignment found for lead: {message_assignment.campaign_lead.lead.email}")

        # Use the model's method to personalize
        logger.info(f"🔄 Starting personalization (skip AI: {skip})")
        success = message_assignment.personalize_with_ai(skip=skip)

        if success:
            logger.info(f"✅ Successfully personalized message for assignment ID {message_assignment_id}")
        else:
            logger.error(f"❌ Failed to personalize message for assignment ID {message_assignment_id}")

        return success

    except MessageAssignment.DoesNotExist:
        logger.error(f"❌ MessageAssignment with ID {message_assignment_id} does not exist")
        return False
    except Exception as e:
        logger.error(f"💥 Error personalizing message {message_assignment_id}: {str(e)}")
        import traceback
        logger.error(f"💥 Full traceback:\n{traceback.format_exc()}")
        return False

@shared_task(name="personalize_campaign_messages_task")
def personalize_campaign_messages_task(campaign_id, force=False):
    """
    Celery task to personalize all messages for a campaign.

    Args:
        campaign_id: ID of the Campaign
        force: Whether to force personalization even if already personalized

    Returns:
        dict: Results of the operation
    """
    try:
        logger.info(f"📝 Starting personalization for campaign ID: {campaign_id}")

        # Get the campaign object
        from .models import Campaign
        try:
            campaign = Campaign.objects.get(id=campaign_id)
            logger.info(f"✅ Campaign found: {campaign.name}")
        except Campaign.DoesNotExist:
            error_msg = f"Campaign with ID {campaign_id} not found"
            logger.error(f"❌ {error_msg}")
            return {
                'status': 'error',
                'message': error_msg,
                'campaign_id': campaign_id
            }

        # Get all message assignments for this campaign
        query = MessageAssignment.objects.filter(campaign_id=campaign_id)
        if not force:
            query = query.filter(personlized_msg_to_send='')

        count = query.count()
        logger.info(f"📝 Found {count} message assignments to personalize for campaign ID {campaign_id}")

        if count == 0:
            logger.info(f"ℹ️ No messages to personalize for campaign {campaign_id}")
            return {
                'status': 'success',
                'message': 'No messages to personalize',
                'campaign_id': campaign_id
            }

        # Create a task for each message assignment
        for message_assignment in query:
            personalize_message_task.delay(message_assignment.id)

        logger.info(f"✅ Scheduled personalization for {count} messages in campaign {campaign_id}")

        return {
            'status': 'success',
            'message': f'Scheduled personalization for {count} messages',
            'campaign_id': campaign_id
        }

    except Exception as e:
        logger.error(f"💥 Error scheduling personalization tasks for campaign {campaign_id}: {str(e)}")
        import traceback
        logger.error(f"💥 Full traceback:\n{traceback.format_exc()}")
        return {
            'status': 'error',
            'message': str(e),
            'campaign_id': campaign_id
        }

# @shared_task
# def personalize_all_messages_task(force=False):
#     """
#     Celery task to personalize all messages in the system.
    
#     Args:
#         force: Whether to force personalization even if already personalized
        
#     Returns:
#         dict: Results of the operation
#     """
#     try:
#         # Get all message assignments
#         query = MessageAssignment.objects.all()
#         if not force:
#             query = query.filter(personlized_msg_to_send='')
            
#         count = query.count()
#         logger.info(f"Personalizing {count} message assignments")
        
#         # Create a task for each message assignment
#         for message_assignment in query:
#             personalize_message_task.delay(message_assignment.id)
            
#         return {
#             'status': 'success',
#             'message': f'Scheduled personalization for {count} messages'
#         }
        
#     except Exception as e:
#         logger.error(f"Error scheduling personalization tasks: {str(e)}")
#         return {
#             'status': 'error',
#             'message': str(e)
#         }

@shared_task(name="send_email_task")
def send_email_task(message_assignment_id, campaign_id):
    """
    Celery task to send an email for a message assignment.
    Respects daily email sending limits.

    Args:
        message_assignment_id: ID of the MessageAssignment to send
        campaign_id: ID of the Campaign

    Returns:
        str/bool: "rate_limit_exceeded" if rate limit exceeded, True if successful, False otherwise
    """
    try:
        logger.info(f"📧 Processing email task for message assignment ID: {message_assignment_id}")

        # Get the campaign object
        from .models import Campaign
        try:
            campaign = Campaign.objects.get(id=campaign_id)
            logger.info(f"✅ Campaign found: {campaign.name}")
        except Campaign.DoesNotExist:
            logger.error(f"❌ Campaign with ID {campaign_id} not found")
            return False

        # Get the message assignment
        message_assignment = MessageAssignment.objects.get(id=message_assignment_id)
        logger.info(f"✅ Message assignment found for lead: {message_assignment.campaign_lead.lead.email}")

        # Check if it has personalized content and hasn't been sent
        if not message_assignment.personlized_msg_to_send:
            logger.error(f"❌ Message assignment ID {message_assignment_id} has no personalized content")
            return False

        if message_assignment.sent:
            logger.warning(f"⚠️ Message assignment ID {message_assignment_id} has already been sent")
            return "already sent"

        # Send the email using the existing function
        logger.info(f"🔄 Sending email to {message_assignment.campaign_lead.lead.email}")
        from campaign.email_sender import send_campaign_email
        success = send_campaign_email(message_assignment, campaign)

        if success:
            logger.info(f"✅ Email sent successfully to {message_assignment.campaign_lead.lead.email}")
        else:
            logger.error(f"❌ Failed to send email to {message_assignment.campaign_lead.lead.email}")

        return success

    except MessageAssignment.DoesNotExist:
        logger.error(f"❌ MessageAssignment with ID {message_assignment_id} does not exist")
        return False
    except Exception as e:
        logger.error(f"💥 Error sending email for assignment {message_assignment_id}: {str(e)}")
        import traceback
        logger.error(f"💥 Full traceback:\n{traceback.format_exc()}")
        return False

@shared_task(name="send_campaign_emails_task")
def send_campaign_emails_task(campaign_id, only_personalized=True):
    """
    Celery task to send emails for all message assignments in a campaign.

    Args:
        campaign_id: ID of the Campaign
        only_personalized: Only send emails that have personalized content

    Returns:
        dict: Results of the operation
    """
    try:
        logger.info(f"📧 Starting email sending for campaign ID: {campaign_id}")

        # Get the campaign object
        from .models import Campaign
        try:
            campaign = Campaign.objects.get(id=campaign_id)
            logger.info(f"✅ Campaign found: {campaign.name}")
        except Campaign.DoesNotExist:
            error_msg = f"Campaign with ID {campaign_id} not found"
            logger.error(f"❌ {error_msg}")
            return {
                'status': 'error',
                'message': error_msg,
                'campaign_id': campaign_id
            }

        # Get all message assignments for this campaign that haven't been sent
        query = MessageAssignment.objects.filter(
            campaign_id=campaign_id,
            sent=False
        )

        if only_personalized:
            query = query.filter(personlized_msg_to_send__gt='')

        count = query.count()
        logger.info(f"📧 Found {count} emails to send for campaign ID {campaign_id}")

        if count == 0:
            logger.info(f"ℹ️ No emails to send for campaign {campaign_id}")
            return {
                'status': 'success',
                'message': 'No emails to send',
                'campaign_id': campaign_id
            }

        # Create a task for each message assignment
        for message_assignment in query:
            send_email_task.delay(message_assignment.id, campaign_id)

        logger.info(f"✅ Scheduled sending for {count} emails in campaign {campaign_id}")

        return {
            'status': 'success',
            'message': f'Scheduled sending for {count} emails',
            'campaign_id': campaign_id
        }

    except Exception as e:
        logger.error(f"💥 Error scheduling email sending tasks for campaign {campaign_id}: {str(e)}")
        import traceback
        logger.error(f"💥 Full traceback:\n{traceback.format_exc()}")
        return {
            'status': 'error',
            'message': str(e),
            'campaign_id': campaign_id
        }

# @shared_task
# def send_all_emails_task(only_personalized=True):
#     """
#     Celery task to send all pending emails in the system.
    
#     Args:
#         only_personalized: Only send emails that have personalized content
        
#     Returns:
#         dict: Results of the operation
#     """
#     try:
#         # Get all message assignments that haven't been sent
#         query = MessageAssignment.objects.filter(sent=False)
        
#         if only_personalized:
#             query = query.filter(personlized_msg_to_send__gt='')
            
#         count = query.count()
#         logger.info(f"Sending {count} emails")
        
#         # Create a task for each message assignment
#         for message_assignment in query:
#             send_email_task.delay(message_assignment.id)
            
#         return {
#             'status': 'success',
#             'message': f'Scheduled sending for {count} emails'
#         }
        
#     except Exception as e:
#         logger.error(f"Error scheduling email sending tasks: {str(e)}")
#         return {
#             'status': 'error',
#             'message': str(e)
#         }

# @shared_task
# def personalize_and_send_message_task(message_assignment_id, skip=True):
#     """
#     Celery task to personalize a message and then send it immediately if rate limits allow.
    
#     Args:
#         message_assignment_id: ID of the MessageAssignment to personalize and send
#         skip: If True, skip AI and use simple replacement
        
#     Returns:
#         dict: Results of the operation
#     """
#     try:
#         # Get the message assignment
#         message_assignment = MessageAssignment.objects.get(id=message_assignment_id)
        
#         # Use the model's method to personalize
#         success = message_assignment.personalize_with_ai(skip=skip)
        
#         if success:
#             logger.info(f"Successfully personalized message for assignment ID {message_assignment_id}")
            

#             # Immediately send the email
#             from campaign.email_sender import send_campaign_email
#             send_result = send_campaign_email(message_assignment)
            
#             if send_result is True:
#                 logger.info(f"Successfully sent email for assignment ID {message_assignment_id}")
#                 return {
#                     'status': 'success',
#                     'message': 'Successfully personalized and sent email',
#                     'assignment_id': message_assignment_id
#                 }
#             else:
#                 logger.error(f"Failed to send email for assignment ID {message_assignment_id}")
#                 return {
#                     'status': 'partial_success',
#                     'message': 'Personalized but failed to send email',
#                     'assignment_id': message_assignment_id
#                 }
            
#         else:
#             logger.error(f"Failed to personalize message for assignment ID {message_assignment_id}")
#             return {
#                 'status': 'error',
#                 'message': 'Failed to personalize message',
#                 'assignment_id': message_assignment_id
#             }
            
#     except MessageAssignment.DoesNotExist:
#         logger.error(f"MessageAssignment with ID {message_assignment_id} does not exist")
#         return {
#             'status': 'error',
#             'message': f"MessageAssignment with ID {message_assignment_id} does not exist",
#             'assignment_id': message_assignment_id
#         }
#     except Exception as e:
#         logger.error(f"Error personalizing and sending message: {str(e)}")
#         return {
#             'status': 'error',
#             'message': str(e),
#             'assignment_id': message_assignment_id
#         }

# @shared_task
# def personalize_campaign_messages_and_send_task(campaign_id, force=False):
    """
    Celery task to personalize all messages for a campaign and send them immediately if rate limits allow.
    
    Args:
        campaign_id: ID of the Campaign
        force: Whether to force personalization even if already personalized
        
    Returns:
        dict: Results of the operation
    """
    try:
        # Get all message assignments for this campaign
        query = MessageAssignment.objects.filter(campaign_id=campaign_id, sent=False)
        if not force:
            query = query.filter(personlized_msg_to_send='')
            
        count = query.count()
        logger.info(f"Personalizing and sending {count} message assignments for campaign ID {campaign_id}")
        
        # Create a task for each message assignment
        for message_assignment in query:
            personalize_and_send_message_task.delay(message_assignment.id)
            
        return {
            'status': 'success',
            'message': f'Scheduled personalization and sending for {count} messages',
            'campaign_id': campaign_id,
        }
        
    except Exception as e:
        logger.error(f"Error scheduling personalization and sending tasks: {str(e)}")
        return {
            'status': 'error',
            'message': str(e),
            'campaign_id': campaign_id
        }

@shared_task(name="personalize_and_send_all_emails_at_once")
def personalize_and_send_all_emails_at_once(campaign_id):
    """
    Celery task to personalize and send all emails at once for a specific campaign.

    Args:
        campaign_id: ID of the Campaign

    Returns:
        dict: Results of the operation
    """
    try:
        logger.info(f"🚀 Starting personalize and send process for campaign ID: {campaign_id}")

        # Get the campaign object
        from .models import Campaign
        try:
            campaign = Campaign.objects.get(id=campaign_id)
            logger.info(f"✅ Campaign found: {campaign.name}")
        except Campaign.DoesNotExist:
            error_msg = f"Campaign with ID {campaign_id} not found"
            logger.error(f"❌ {error_msg}")
            return {
                'status': 'error',
                'message': error_msg,
                'campaign_id': campaign_id
            }

        # First personalize all messages
        logger.info(f"🔄 Starting personalization for campaign {campaign_id}")
        personalize_result = personalize_campaign_messages_task.delay(campaign_id=campaign_id, force=False)
        logger.info(f"✅ Personalization task started: {getattr(personalize_result, 'id', 'Unknown')}")

        # Then send all personalized emails
        logger.info(f"🔄 Starting email sending for campaign {campaign_id}")
        send_result = send_campaign_emails_task.delay(campaign_id=campaign_id, only_personalized=True)
        logger.info(f"✅ Email sending task started: {getattr(send_result, 'id', 'Unknown')}")

        logger.info(f"🎉 Campaign {campaign_id} launch initiated successfully")

        return {
            'status': 'success',
            'message': f'Campaign {campaign_id} launch initiated successfully',
            'campaign_id': campaign_id,
            'campaign_name': campaign.name,
            'personalize_task_id': personalize_result.id if hasattr(personalize_result, 'id') else None,
            'send_task_id': send_result.id if hasattr(send_result, 'id') else None
        }

    except Exception as e:
        logger.error(f"💥 Error launching campaign {campaign_id}: {str(e)}")
        import traceback
        logger.error(f"💥 Full traceback:\n{traceback.format_exc()}")
        return {
            'status': 'error',
            'message': str(e),
            'campaign_id': campaign_id
        }

# ============================================================================
# ANALYTICS TASKS
# ============================================================================

@shared_task
def calculate_daily_stats_task(campaign_id, target_date=None):
    """
    Celery task to calculate daily stats for a specific campaign.

    Args:
        campaign_id: ID of the Campaign
        target_date: Date string in YYYY-MM-DD format, defaults to today

    Returns:
        dict: Results of the operation
    """
    try:
        from .models import Campaign, CampaignDailyStats
        from datetime import datetime

        # Get the campaign
        campaign = Campaign.objects.get(id=campaign_id)

        # Parse target date if provided
        if target_date:
            target_date = datetime.strptime(target_date, '%Y-%m-%d').date()

        # Calculate daily stats
        daily_stats = CampaignDailyStats.calculate_daily_stats(campaign, target_date)

        logger.info(f"Calculated daily stats for campaign {campaign.name} on {daily_stats.date}")

        return {
            'status': 'success',
            'message': f'Daily stats calculated for {campaign.name}',
            'campaign_id': campaign_id,
            'date': str(daily_stats.date),
            'emails_sent': daily_stats.emails_sent_today,
            'opens': daily_stats.opens_today,
            'clicks': daily_stats.clicks_today
        }

    except Campaign.DoesNotExist:
        error_msg = f"Campaign with ID {campaign_id} not found"
        logger.error(error_msg)
        return {
            'status': 'error',
            'message': error_msg,
            'campaign_id': campaign_id
        }
    except Exception as e:
        logger.error(f"Error calculating daily stats for campaign {campaign_id}: {str(e)}")
        return {
            'status': 'error',
            'message': str(e),
            'campaign_id': campaign_id
        }


@shared_task
def calculate_all_campaigns_daily_stats_task(target_date=None):
    """
    Celery task to calculate daily stats for all active campaigns.

    Args:
        target_date: Date string in YYYY-MM-DD format, defaults to today

    Returns:
        dict: Results of the operation
    """
    try:
        from .models import Campaign

        # Get all active campaigns
        campaigns = Campaign.objects.filter(status='active')
        count = campaigns.count()

        logger.info(f"Calculating daily stats for {count} active campaigns")

        # Schedule a task for each campaign
        for campaign in campaigns:
            calculate_daily_stats_task.delay(campaign.id, target_date)

        return {
            'status': 'success',
            'message': f'Scheduled daily stats calculation for {count} campaigns',
            'campaigns_count': count
        }

    except Exception as e:
        logger.error(f"Error scheduling daily stats calculation: {str(e)}")
        return {
            'status': 'error',
            'message': str(e)
        }


@shared_task
def backfill_daily_stats_task(campaign_id, start_date, end_date):
    """
    Celery task to backfill daily stats for a campaign over a date range.
    Useful for populating historical data.

    Args:
        campaign_id: ID of the Campaign
        start_date: Start date string in YYYY-MM-DD format
        end_date: End date string in YYYY-MM-DD format

    Returns:
        dict: Results of the operation
    """
    try:
        from .models import Campaign
        from datetime import datetime, timedelta

        # Get the campaign
        campaign = Campaign.objects.get(id=campaign_id)

        # Parse dates
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        # Calculate stats for each day in the range
        current_date = start_date
        days_processed = 0

        while current_date <= end_date:
            calculate_daily_stats_task.delay(campaign_id, current_date.strftime('%Y-%m-%d'))
            current_date += timedelta(days=1)
            days_processed += 1

        logger.info(f"Scheduled backfill for {days_processed} days for campaign {campaign.name}")

        return {
            'status': 'success',
            'message': f'Scheduled backfill for {days_processed} days',
            'campaign_id': campaign_id,
            'days_processed': days_processed
        }

    except Campaign.DoesNotExist:
        error_msg = f"Campaign with ID {campaign_id} not found"
        logger.error(error_msg)
        return {
            'status': 'error',
            'message': error_msg,
            'campaign_id': campaign_id
        }
    except Exception as e:
        logger.error(f"Error scheduling backfill for campaign {campaign_id}: {str(e)}")
        return {
            'status': 'error',
            'message': str(e),
            'campaign_id': campaign_id
        }
