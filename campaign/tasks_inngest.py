# Inngest functions for campaign processing
import inngest
from scheduler.client import inngest_client

from django.utils import timezone
from django.conf import settings
import logging
from datetime import timedelta
from .models import MessageAssignment
from .services import AnalyticsService

logger = logging.getLogger(__name__)


# COMMENTED OUT - Using batch processing instead of individual message processing
# @inngest_client.create_function(
#     fn_id="personalize_message",
#     trigger=inngest.TriggerEvent(event="campaigns/personalize.message"),
# )
# def personalize_message_task(ctx: inngest.Context):
#     """
#     Inngest function to personalize a message using AI and save it to the database.
#     Rate limited to respect AI API limits.
#
#     DEPRECATED: Now using batch processing in personalize_and_send_all_emails_at_once
#     """
#     pass






# COMMENTED OUT - Using batch processing instead of individual campaign message processing
# @inngest_client.create_function(
#     fn_id="personalize_campaign_messages",
#     trigger=inngest.TriggerEvent(event="campaigns/personalize.campaign_messages"),
# )
# def personalize_campaign_messages_task(ctx: inngest.Context):
#     """
#     Inngest function to personalize all messages for a campaign.
#
#     DEPRECATED: Now using batch processing in personalize_and_send_all_emails_at_once
#     """
#     pass















# COMMENTED OUT - Using batch processing instead of individual email sending
# @inngest_client.create_function(
#     fn_id="send_email",
#     trigger=inngest.TriggerEvent(event="campaigns/send.email"),
# )
# def send_email_task(ctx: inngest.Context):
#     """
#     Inngest function to send an email for a message assignment.
#
#     DEPRECATED: Now using batch processing in personalize_and_send_all_emails_at_once
#     """
#     pass



















# COMMENTED OUT - Using batch processing instead of individual campaign email sending
# @inngest_client.create_function(
#     fn_id="send_campaign_emails",
#     trigger=inngest.TriggerEvent(event="campaigns/send.campaign_emails"),
# )
# def send_campaign_emails_task(ctx: inngest.Context):
#     """
#     Inngest function to send emails for all message assignments in a campaign.
#
#     DEPRECATED: Now using batch processing in personalize_and_send_all_emails_at_once
#     """
#     pass











@inngest_client.create_function(
    fn_id="personalize_and_send_all_emails",
    trigger=inngest.TriggerEvent(event="campaigns/personalize_and_send.all_emails"),
)
def personalize_and_send_all_emails_at_once(ctx: inngest.Context):
    """
    Inngest function to personalize and send all emails at once for a specific campaign.
    This function processes everything in batches to avoid creating too many individual events.

    Args:
        ctx.event.data.campaign_id: ID of the Campaign

    Returns:
        dict: Results of the operation
    """
    try:
        campaign_id = ctx.event.data.get("campaign_id")

        if not campaign_id:
            return {"status": "error", "message": "campaign_id is required"}

        # Get the campaign object
        from .models import Campaign
        try:
            campaign = Campaign.objects.get(id=campaign_id)
        except Campaign.DoesNotExist:
            error_msg = f"Campaign with ID {campaign_id} not found"
            return {
                'status': 'error',
                'message': error_msg,
                'campaign_id': campaign_id
            }

        logger.info(f"🚀 Starting campaign launch for {campaign.name} (ID: {campaign_id})")

        # Step 1: Personalize all messages that need personalization
        query = MessageAssignment.objects.filter(
            campaign_id=campaign_id,
            personlized_msg_to_send=''
        )

        personalize_count = query.count()
        logger.info(f"📝 Personalizing {personalize_count} messages")

        for message_assignment in query:
            success = message_assignment.personalize_with_ai(skip=True)
            if success:
                logger.info(f"✅ Personalized message for assignment ID {message_assignment.id}")
            else:
                logger.error(f"❌ Failed to personalize message for assignment ID {message_assignment.id}")

        # Step 2: Send all personalized emails
        send_query = MessageAssignment.objects.filter(
            campaign_id=campaign_id,
            sent=False,
            personlized_msg_to_send__gt=''
        )

        send_count = send_query.count()
        logger.info(f"📧 Sending {send_count} emails")

        from campaign.email_sender import send_campaign_email
        sent_successfully = 0

        for message_assignment in send_query:
            try:
                success = send_campaign_email(message_assignment, campaign)
                if success:
                    sent_successfully += 1
                    logger.info(f"✅ Email sent successfully to {message_assignment.campaign_lead.lead.email}")
                else:
                    logger.error(f"❌ Failed to send email to {message_assignment.campaign_lead.lead.email}")
            except Exception as e:
                logger.error(f"💥 Error sending email to {message_assignment.campaign_lead.lead.email}: {str(e)}")

        return {
            'status': 'success',
            'message': f'Campaign {campaign_id} launch completed successfully',
            'campaign_id': campaign_id,
            'campaign_name': campaign.name,
            'personalized_count': personalize_count,
            'sent_count': sent_successfully,
            'total_processed': send_count
        }

    except Exception as e:
        logger.error(f"Error launching campaign {campaign_id}: {str(e)}")
        return {
            'status': 'error',
            'message': str(e),
            'campaign_id': campaign_id
        }












@inngest_client.create_function(
    fn_id="process_scheduled_emails",
    trigger=inngest.TriggerEvent(event="campaigns/process_scheduled_emails"),
)
def process_scheduled_emails(ctx: inngest.Context):
    """
    Process scheduled emails with intelligent batch sending and rate limiting.
    This function handles timezone-aware email delivery in optimized batches.
    """
    try:
        campaign_id = ctx.event.data.get("campaign_id")
        scheduled_time = ctx.event.data.get("scheduled_time")

        if not campaign_id:
            return {"status": "error", "message": "campaign_id is required"}

        logger.info(f"📧 Processing scheduled emails for campaign {campaign_id} at {scheduled_time}")

        # Get the campaign, schedule, and rate limiter
        from .models import Campaign
        from .scheduling_utils import create_scheduler_from_campaign, create_rate_limiter_from_campaign

        campaign = Campaign.objects.get(id=campaign_id)
        scheduler = create_scheduler_from_campaign(campaign)
        rate_limiter = create_rate_limiter_from_campaign(campaign)

        # Check if we have email accounts configured
        if not rate_limiter:
            return {
                'status': 'error',
                'message': 'No active email accounts found for campaign',
                'campaign_id': campaign_id
            }

        # Get all message assignments that need processing
        query = MessageAssignment.objects.filter(
            campaign_id=campaign_id,
            sent=False
        )

        total_emails = query.count()
        logger.info(f"📊 Found {total_emails} emails to process for campaign {campaign_id}")

        if total_emails == 0:
            return {
                'status': 'success',
                'message': 'No emails to process',
                'campaign_id': campaign_id
            }

        # Check if we can send all emails with current daily limits
        if not rate_limiter.can_send_emails(total_emails):
            capacity_summary = rate_limiter.get_capacity_summary()
            logger.warning(f"⚠️ Campaign {campaign_id}: Cannot send {total_emails} emails. Daily capacity: {capacity_summary['total_daily_capacity']}")
            return {
                'status': 'error',
                'message': f'Daily capacity exceeded. Can send {capacity_summary["total_daily_capacity"]} emails, requested {total_emails}',
                'campaign_id': campaign_id,
                'capacity_summary': capacity_summary
            }

        # Log capacity summary
        capacity_summary = rate_limiter.get_capacity_summary()
        logger.info(f"📧 Email capacity: {capacity_summary}")

        # Determine processing strategy
        if scheduler and total_emails > 10:  # Lower threshold for batching
            # Use intelligent batch scheduling with rate limiting
            return _process_emails_with_smart_scheduling(campaign, scheduler, rate_limiter, query, total_emails)
        else:
            # Process emails immediately with rate limiting
            return _process_emails_with_rate_limiting(campaign, rate_limiter, query, total_emails)

    except Campaign.DoesNotExist:
        error_msg = f"Campaign {campaign_id} not found"
        logger.error(error_msg)
        return {"status": "error", "message": error_msg}

    except Exception as e:
        error_msg = f"Error processing scheduled emails for campaign {campaign_id}: {str(e)}"
        logger.error(error_msg)
        return {"status": "error", "message": error_msg}


def _process_emails_with_rate_limiting(campaign, rate_limiter, query, total_emails):
    """Process emails immediately with proper rate limiting across multiple accounts."""
    logger.info(f"🚀 Processing {total_emails} emails immediately with rate limiting for campaign {campaign.id}")

    # Personalize all messages first
    personalize_count = 0
    for message_assignment in query.filter(personlized_msg_to_send=''):
        success = message_assignment.personalize_with_ai(skip=True)
        if success:
            personalize_count += 1

    logger.info(f"📝 Personalized {personalize_count} messages")

    # Get personalized message assignments
    message_assignments = list(query.filter(personlized_msg_to_send__gt=''))

    if not message_assignments:
        return {
            'status': 'success',
            'message': 'No personalized messages to send',
            'campaign_id': campaign.id,
            'personalized_count': personalize_count,
            'sent_count': 0,
            'processing_type': 'immediate_rate_limited'
        }

    # Calculate send schedule with rate limiting
    from django.utils import timezone
    start_time = timezone.now() + timedelta(seconds=5)  # Small delay
    send_schedule = rate_limiter.calculate_send_schedule(len(message_assignments), start_time)

    logger.info(f"📅 Created send schedule for {len(send_schedule)} emails across {len(rate_limiter.email_accounts)} accounts")

    # Schedule individual emails
    scheduled_count = 0
    for i, (message_assignment, schedule_item) in enumerate(zip(message_assignments, send_schedule)):
        try:
            inngest_client.send_sync(
                inngest.Event(
                    name="campaigns/send_single_email",
                    data={
                        "campaign_id": campaign.id,
                        "message_assignment_id": message_assignment.id,
                        "email_account_id": schedule_item['account'].id,
                        "sequence_number": i + 1,
                        "total_emails": len(message_assignments)
                    },
                    ts=int(schedule_item['send_time'].timestamp())
                )
            )
            scheduled_count += 1
        except Exception as e:
            logger.error(f"💥 Error scheduling email {message_assignment.id}: {str(e)}")

    return {
        'status': 'success',
        'message': f'Scheduled {scheduled_count} emails with rate limiting',
        'campaign_id': campaign.id,
        'personalized_count': personalize_count,
        'scheduled_count': scheduled_count,
        'processing_type': 'immediate_rate_limited',
        'capacity_summary': rate_limiter.get_capacity_summary()
    }


def _process_emails_with_smart_scheduling(campaign, scheduler, rate_limiter, query, total_emails):
    """Process emails with intelligent scheduling that respects both time windows and rate limits."""
    logger.info(f"📦 Processing {total_emails} emails with smart scheduling for campaign {campaign.id}")

    # Personalize all messages first
    personalize_count = 0
    for message_assignment in query.filter(personlized_msg_to_send=''):
        success = message_assignment.personalize_with_ai(skip=True)
        if success:
            personalize_count += 1

    logger.info(f"📝 Personalized {personalize_count} messages")

    # Get personalized message assignments
    message_assignments = list(query.filter(personlized_msg_to_send__gt=''))

    if not message_assignments:
        return {
            'status': 'success',
            'message': 'No personalized messages to send',
            'campaign_id': campaign.id,
            'personalized_count': personalize_count,
            'sent_count': 0,
            'processing_type': 'smart_scheduled'
        }

    # Calculate optimal batch times based on schedule
    batch_size = min(50, rate_limiter.total_daily_capacity // 4)  # Conservative batching
    batch_send_times = scheduler.calculate_batch_send_times(len(message_assignments), batch_size)

    logger.info(f"📅 Calculated {len(batch_send_times)} batches for delivery")

    # Schedule batches with rate limiting
    scheduled_batches = 0

    for i, send_time in enumerate(batch_send_times):
        start_idx = i * batch_size
        end_idx = min(start_idx + batch_size, len(message_assignments))
        batch_assignments = message_assignments[start_idx:end_idx]

        if batch_assignments:
            # Schedule this batch with rate limiting
            batch_ids = [ma.id for ma in batch_assignments]

            inngest_client.send_sync(
                inngest.Event(
                    name="campaigns/send_rate_limited_batch",
                    data={
                        "campaign_id": campaign.id,
                        "message_assignment_ids": batch_ids,
                        "batch_number": i + 1,
                        "total_batches": len(batch_send_times),
                        "batch_send_time": send_time.isoformat()
                    },
                    ts=int(send_time.timestamp())
                )
            )

            scheduled_batches += 1
            logger.info(f"⏰ Scheduled rate-limited batch {i + 1}/{len(batch_send_times)} for {send_time} ({len(batch_assignments)} emails)")

    return {
        'status': 'success',
        'message': f'Scheduled {scheduled_batches} rate-limited batches for campaign {campaign.id}',
        'campaign_id': campaign.id,
        'personalized_count': personalize_count,
        'total_emails': len(message_assignments),
        'scheduled_batches': scheduled_batches,
        'processing_type': 'smart_scheduled',
        'capacity_summary': rate_limiter.get_capacity_summary()
    }


@inngest_client.create_function(
    fn_id="send_single_email",
    trigger=inngest.TriggerEvent(event="campaigns/send_single_email"),
)
def send_single_email(ctx: inngest.Context):
    """
    Send a single email using a specific email account.
    This function handles individual email sending with proper account tracking.
    """
    try:
        campaign_id = ctx.event.data.get("campaign_id")
        message_assignment_id = ctx.event.data.get("message_assignment_id")
        email_account_id = ctx.event.data.get("email_account_id")
        sequence_number = ctx.event.data.get("sequence_number", 1)
        total_emails = ctx.event.data.get("total_emails", 1)

        if not all([campaign_id, message_assignment_id, email_account_id]):
            return {"status": "error", "message": "campaign_id, message_assignment_id, and email_account_id are required"}

        logger.info(f"📧 Sending email {sequence_number}/{total_emails} for campaign {campaign_id}")

        # Get models
        from .models import Campaign
        from clients.models import EmailAccount

        campaign = Campaign.objects.get(id=campaign_id)
        message_assignment = MessageAssignment.objects.get(id=message_assignment_id)
        email_account = EmailAccount.objects.get(id=email_account_id)

        # Check if already sent
        if message_assignment.sent:
            return {
                'status': 'success',
                'message': 'Email already sent',
                'campaign_id': campaign_id,
                'message_assignment_id': message_assignment_id
            }

        # Send email using specific account
        from campaign.email_sender import send_campaign_email_with_account
        success = send_campaign_email_with_account(message_assignment, campaign, email_account)

        if success:
            logger.info(f"✅ Email {sequence_number}/{total_emails} sent to {message_assignment.campaign_lead.lead.email} via {email_account.email}")
            return {
                'status': 'success',
                'message': 'Email sent successfully',
                'campaign_id': campaign_id,
                'message_assignment_id': message_assignment_id,
                'email_account': email_account.email,
                'sequence_number': sequence_number,
                'total_emails': total_emails
            }
        else:
            logger.error(f"❌ Failed to send email {sequence_number}/{total_emails} to {message_assignment.campaign_lead.lead.email}")
            return {
                'status': 'error',
                'message': 'Failed to send email',
                'campaign_id': campaign_id,
                'message_assignment_id': message_assignment_id,
                'email_account': email_account.email
            }

    except (Campaign.DoesNotExist, MessageAssignment.DoesNotExist, EmailAccount.DoesNotExist) as e:
        error_msg = f"Model not found: {str(e)}"
        logger.error(error_msg)
        return {"status": "error", "message": error_msg}

    except Exception as e:
        error_msg = f"Error sending single email: {str(e)}"
        logger.error(error_msg)
        return {"status": "error", "message": error_msg}


@inngest_client.create_function(
    fn_id="send_rate_limited_batch",
    trigger=inngest.TriggerEvent(event="campaigns/send_rate_limited_batch"),
)
def send_rate_limited_batch(ctx: inngest.Context):
    """
    Send a batch of emails with intelligent rate limiting across multiple accounts.
    This function distributes emails across available accounts respecting their limits.
    """
    try:
        campaign_id = ctx.event.data.get("campaign_id")
        message_assignment_ids = ctx.event.data.get("message_assignment_ids", [])
        batch_number = ctx.event.data.get("batch_number", 1)
        total_batches = ctx.event.data.get("total_batches", 1)
        batch_send_time = ctx.event.data.get("batch_send_time")

        if not campaign_id or not message_assignment_ids:
            return {"status": "error", "message": "campaign_id and message_assignment_ids are required"}

        logger.info(f"📧 Sending rate-limited batch {batch_number}/{total_batches} for campaign {campaign_id} ({len(message_assignment_ids)} emails)")

        # Get campaign and rate limiter
        from .models import Campaign
        from .scheduling_utils import create_rate_limiter_from_campaign

        campaign = Campaign.objects.get(id=campaign_id)
        rate_limiter = create_rate_limiter_from_campaign(campaign)

        if not rate_limiter:
            return {"status": "error", "message": "No active email accounts found"}

        # Get message assignments
        message_assignments = list(MessageAssignment.objects.filter(
            id__in=message_assignment_ids,
            sent=False
        ))

        if not message_assignments:
            return {
                'status': 'success',
                'message': 'No emails to send (already sent or not found)',
                'batch_number': batch_number
            }

        # Calculate send schedule for this batch
        from django.utils import timezone
        from datetime import datetime

        if batch_send_time:
            start_time = datetime.fromisoformat(batch_send_time.replace('Z', '+00:00'))
        else:
            start_time = timezone.now()

        send_schedule = rate_limiter.calculate_send_schedule(len(message_assignments), start_time)

        # Schedule individual emails
        scheduled_count = 0
        for message_assignment, schedule_item in zip(message_assignments, send_schedule):
            try:
                inngest_client.send_sync(
                    inngest.Event(
                        name="campaigns/send_single_email",
                        data={
                            "campaign_id": campaign_id,
                            "message_assignment_id": message_assignment.id,
                            "email_account_id": schedule_item['account'].id,
                            "sequence_number": scheduled_count + 1,
                            "total_emails": len(message_assignments)
                        },
                        ts=int(schedule_item['send_time'].timestamp())
                    )
                )
                scheduled_count += 1
            except Exception as e:
                logger.error(f"💥 Error scheduling email {message_assignment.id}: {str(e)}")

        logger.info(f"📊 Rate-limited batch {batch_number}/{total_batches} scheduled: {scheduled_count} emails")

        return {
            'status': 'success',
            'message': f'Rate-limited batch {batch_number}/{total_batches} scheduled',
            'campaign_id': campaign_id,
            'batch_number': batch_number,
            'total_batches': total_batches,
            'scheduled_count': scheduled_count,
            'total_in_batch': len(message_assignment_ids)
        }

    except Campaign.DoesNotExist:
        error_msg = f"Campaign {campaign_id} not found"
        logger.error(error_msg)
        return {"status": "error", "message": error_msg}

    except Exception as e:
        error_msg = f"Error processing rate-limited batch for campaign {campaign_id}: {str(e)}"
        logger.error(error_msg)
        return {"status": "error", "message": error_msg}


# Helper function for backward compatibility
def personalize_and_send_all_emails_at_once_sync(campaign_id):
    """
    Synchronous helper function to trigger the Inngest function.
    Used for backward compatibility with existing code.
    """
    try:
        inngest_client.send_sync(
            inngest.Event(
                name="campaigns/campaign.scheduled",
                data={"object_id": campaign_id}
            )
        )
        return {
            'status': 'success',
            'message': f'Campaign {campaign_id} launch initiated successfully',
            'campaign_id': campaign_id
        }
    except Exception as e:
        logger.error(f"Error triggering campaign launch {campaign_id}: {str(e)}")
        return {
            'status': 'error',
            'message': str(e),
            'campaign_id': campaign_id
        }
