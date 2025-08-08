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
        logger.info("🔍 DEBUG: process_scheduled_emails function started")
        logger.info(f"🔍 DEBUG: ctx = {ctx}")
        logger.info(f"🔍 DEBUG: ctx.event = {ctx.event}")
        logger.info(f"🔍 DEBUG: ctx.event.data = {ctx.event.data}")

        # Check if ctx.event.data exists
        if not hasattr(ctx.event, 'data') or ctx.event.data is None:
            logger.error("❌ ERROR: ctx.event.data is None or missing")
            return {"status": "error", "message": "event data is missing"}

        campaign_id = ctx.event.data.get("campaign_id")
        scheduled_time = ctx.event.data.get("scheduled_time")

        logger.info(f"🔍 DEBUG: campaign_id = {campaign_id}")
        logger.info(f"🔍 DEBUG: scheduled_time = {scheduled_time}")

        if not campaign_id:
            logger.error("❌ ERROR: campaign_id is required but not provided")
            return {"status": "error", "message": "campaign_id is required"}

        logger.info(f"📧 Processing scheduled emails for campaign {campaign_id} at {scheduled_time}")

        # Get the campaign, schedule, and rate limiter
        logger.info(f"🔍 DEBUG: Importing models and utilities")
        from .models import Campaign
        from .scheduling_utils import create_scheduler_from_campaign, create_rate_limiter_from_campaign

        logger.info(f"🔍 DEBUG: Getting campaign with ID: {campaign_id}")
        campaign = Campaign.objects.get(id=campaign_id)
        logger.info(f"🔍 DEBUG: Found campaign: {campaign.name}")

        logger.info(f"🔍 DEBUG: Creating scheduler from campaign")
        scheduler = create_scheduler_from_campaign(campaign)
        logger.info(f"🔍 DEBUG: Scheduler created: {scheduler}")

        logger.info(f"🔍 DEBUG: Creating rate limiter from campaign")
        rate_limiter = create_rate_limiter_from_campaign(campaign)
        logger.info(f"🔍 DEBUG: Rate limiter created: {rate_limiter}")

        # Check if we have email accounts configured
        if not rate_limiter:
            return {
                'status': 'error',
                'message': 'No active email accounts found for campaign',
                'campaign_id': campaign_id
            }

        # Get all message assignments that need processing
        logger.info(f"🔍 DEBUG: Querying message assignments for campaign {campaign_id}")

        # Get campaign options to check stop_on_reply setting
        campaign_options = campaign.campaign_options.first()

        # Base query for unsent messages
        query = MessageAssignment.objects.filter(
            campaign_id=campaign_id,
            sent=False
        )

        # Handle stop_on_reply: exclude messages for leads that have already replied
        if campaign_options and campaign_options.stop_on_reply:
            # Get leads that have replied to any message in this campaign
            replied_lead_ids = MessageAssignment.objects.filter(
                campaign_id=campaign_id,
                responded=True
            ).values_list('campaign_lead_id', flat=True).distinct()

            # Exclude message assignments for leads that have replied
            query = query.exclude(campaign_lead_id__in=replied_lead_ids)
            logger.info(f"🛑 Stop on reply enabled: excluded {len(replied_lead_ids)} leads who have replied")

        # Handle delayed_by_days: only include messages that are ready to send

        ready_to_send_ids = []
        for assignment in query:
            if assignment.delayed_by_days and assignment.delayed_by_days > 0:
                # Find the most recent sent message for this lead in this campaign
                last_sent = MessageAssignment.objects.filter(
                    campaign_id=campaign_id,
                    campaign_lead=assignment.campaign_lead,
                    sent=True,
                    sent_at__isnull=False
                ).order_by('-sent_at').first()

                if last_sent:
                    # Check if enough days have passed since the last sent message
                    days_since_last = (timezone.now() - last_sent.sent_at).days
                    if days_since_last >= assignment.delayed_by_days:
                        ready_to_send_ids.append(assignment.id)
                    else:
                        logger.info(f"⏰ Message {assignment.id} delayed: {days_since_last}/{assignment.delayed_by_days} days passed")
                else:
                    # No previous message sent, this can be sent immediately
                    ready_to_send_ids.append(assignment.id)
            else:
                # No delay specified, ready to send
                ready_to_send_ids.append(assignment.id)

        # Filter query to only include ready-to-send messages
        query = query.filter(id__in=ready_to_send_ids)

        total_emails = query.count()
        logger.info(f"📊 Found {total_emails} emails to process for campaign {campaign_id}")
        logger.info(f"🔍 DEBUG: Message assignments query: {query}")

        # Log some sample message assignments
        sample_assignments = list(query[:3])  # Get first 3 for debugging
        for i, assignment in enumerate(sample_assignments):
            logger.info(f"🔍 DEBUG: Sample assignment {i+1}: ID={assignment.id}, sent={assignment.sent}, lead={assignment.campaign_lead.lead.email}")

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
                    ts=int(schedule_item['send_time'].timestamp()) * 1000
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
                    ts=int(send_time.timestamp()) * 1000
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

        # Check stop_on_reply: don't send if lead has already replied
        campaign_options = campaign.campaign_options.first()
        if campaign_options and campaign_options.stop_on_reply:
            # Check if this lead has replied to any message in this campaign
            has_replied = MessageAssignment.objects.filter(
                campaign_id=campaign_id,
                campaign_lead=message_assignment.campaign_lead,
                responded=True
            ).exists()

            if has_replied:
                logger.info(f"🛑 Skipping email to {message_assignment.campaign_lead.lead.email} - lead has already replied")
                return {
                    'status': 'skipped',
                    'message': 'Email skipped - lead has replied (stop_on_reply enabled)',
                    'campaign_id': campaign_id,
                    'message_assignment_id': message_assignment_id
                }

        # Send email using specific account
        from campaign.email_sender import send_campaign_email_with_account
        success = send_campaign_email_with_account(message_assignment, campaign, email_account)

        if success:
            logger.info(f"✅ Email {sequence_number}/{total_emails} sent to {message_assignment.campaign_lead.lead.email} via {email_account.email}")

            # Check if this was the last email in the campaign
            if sequence_number == total_emails:
                # Check if all emails in campaign are now sent
                remaining_emails = MessageAssignment.objects.filter(
                    campaign=campaign,
                    sent=False
                ).count()

                if remaining_emails == 0:
                    logger.info(f"🏁 All emails sent for campaign {campaign.name}, triggering completion")
                    # Trigger campaign completion
                    inngest_client.send_sync(
                        inngest.Event(
                            name="campaigns/complete",
                            data={"campaign_id": campaign_id}
                        )
                    )

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
                        ts=int(schedule_item['send_time'].timestamp()) * 1000
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


# ============================================================================
# ANALYTICS AND MAINTENANCE TASKS
# ============================================================================

@inngest_client.create_function(
    fn_id="reset_daily_email_limits",
    trigger=inngest.TriggerCron(cron="0 0 * * *"),  # Daily at midnight UTC
)
def reset_daily_email_limits(ctx: inngest.Context):
    """
    Reset daily email counts for all email accounts.
    Runs daily at midnight UTC to reset the emails_sent counter.
    """
    try:
        logger.info("🔄 Starting daily email limit reset")

        from clients.models import EmailAccount

        # Reset all email accounts that have sent emails
        updated_count = EmailAccount.objects.filter(emails_sent__gt=0).update(emails_sent=0)

        logger.info(f"✅ Reset daily email counts for {updated_count} email accounts")

        return {
            "status": "success",
            "message": f"Reset daily email counts for {updated_count} email accounts",
            "updated_count": updated_count
        }

    except Exception as e:
        logger.error(f"💥 Error resetting daily email limits: {str(e)}")
        import traceback
        logger.error(f"💥 Full traceback:\n{traceback.format_exc()}")
        return {
            "status": "error",
            "message": str(e)
        }


@inngest_client.create_function(
    fn_id="calculate_daily_stats",
    trigger=inngest.TriggerEvent(event="analytics/calculate_daily_stats"),
)
def calculate_daily_stats(ctx: inngest.Context):
    """
    Calculate daily stats for a specific campaign.
    Triggered by event with campaign_id and optional target_date.
    """
    try:
        campaign_id = ctx.event.data.get("campaign_id")
        target_date_str = ctx.event.data.get("target_date")  # YYYY-MM-DD format

        if not campaign_id:
            return {"status": "error", "message": "campaign_id is required"}

        logger.info(f"📊 Calculating daily stats for campaign {campaign_id}")

        from .models import Campaign, CampaignDailyStats
        from datetime import datetime

        # Get the campaign
        campaign = Campaign.objects.get(id=campaign_id)

        # Parse target date if provided
        target_date = None
        if target_date_str:
            target_date = datetime.strptime(target_date_str, '%Y-%m-%d').date()

        # Calculate daily stats
        daily_stats = CampaignDailyStats.calculate_daily_stats(campaign, target_date)

        logger.info(f"✅ Calculated daily stats for campaign {campaign.name} on {daily_stats.date}")

        return {
            "status": "success",
            "message": f"Daily stats calculated for {campaign.name}",
            "campaign_id": campaign_id,
            "date": daily_stats.date.isoformat(),
            "stats": {
                "emails_sent": daily_stats.emails_sent,
                "emails_opened": daily_stats.emails_opened,
                "links_clicked": daily_stats.links_clicked,
                "replies_received": daily_stats.replies_received
            }
        }

    except Exception as e:
        logger.error(f"💥 Error calculating daily stats: {str(e)}")
        import traceback
        logger.error(f"💥 Full traceback:\n{traceback.format_exc()}")
        return {
            "status": "error",
            "message": str(e),
            "campaign_id": campaign_id if 'campaign_id' in locals() else None
        }


@inngest_client.create_function(
    fn_id="calculate_all_campaigns_daily_stats",
    trigger=inngest.TriggerCron(cron="0 1 * * *"),  # Daily at 1 AM UTC
)
def calculate_all_campaigns_daily_stats(ctx: inngest.Context):
    """
    Calculate daily stats for all active campaigns.
    Runs daily at 1 AM UTC (after email limit reset).
    """
    try:
        logger.info("📊 Starting daily stats calculation for all active campaigns")

        from .models import Campaign

        # Get all active campaigns
        campaigns = Campaign.objects.filter(status='active')
        count = campaigns.count()

        logger.info(f"📊 Found {count} active campaigns for daily stats calculation")

        # Trigger individual calculation for each campaign
        for campaign in campaigns:
            inngest_client.send_sync(
                inngest.Event(
                    name="analytics/calculate_daily_stats",
                    data={
                        "campaign_id": campaign.id,
                        "target_date": None  # Use today's date
                    }
                )
            )

        logger.info(f"✅ Scheduled daily stats calculation for {count} campaigns")

        return {
            "status": "success",
            "message": f"Scheduled daily stats calculation for {count} campaigns",
            "campaigns_count": count
        }

    except Exception as e:
        logger.error(f"💥 Error scheduling daily stats calculation: {str(e)}")
        import traceback
        logger.error(f"💥 Full traceback:\n{traceback.format_exc()}")
        return {
            "status": "error",
            "message": str(e)
        }


@inngest_client.create_function(
    fn_id="create_campaign_stats",
    trigger=inngest.TriggerEvent(event="campaigns/create_stats"),
)
def create_campaign_stats(ctx: inngest.Context):
    """
    Create and initialize campaign stats when a campaign is launched.
    This replaces the stats creation during campaign creation.
    """
    try:
        campaign_id = ctx.event.data.get("campaign_id")

        if not campaign_id:
            return {"status": "error", "message": "campaign_id is required"}

        logger.info(f"📊 Creating campaign stats for campaign {campaign_id}")

        from .models import Campaign, CampaignStats
        from .services import AnalyticsService

        # Get the campaign
        campaign = Campaign.objects.get(id=campaign_id)

        # Create or get campaign stats
        stats, created = CampaignStats.objects.get_or_create(campaign=campaign)

        if created:
            logger.info(f"✅ Created new campaign stats for {campaign.name}")
        else:
            logger.info(f"📊 Campaign stats already exist for {campaign.name}, updating...")

        # Perform full recalculation to ensure accuracy
        AnalyticsService.recalculate_campaign_stats(campaign)

        # Refresh stats from database
        stats.refresh_from_db()

        logger.info(f"✅ Campaign stats initialized for {campaign.name}")

        return {
            "status": "success",
            "message": f"Campaign stats created/updated for {campaign.name}",
            "campaign_id": campaign_id,
            "stats": {
                "sequence_started_count": stats.sequence_started_count,
                "opened_count": stats.opened_count,
                "clicked_count": stats.clicked_count,
                "replied_count": stats.replied_count,
                "opportunities_count": stats.opportunities_count,
                "conversions_count": stats.conversions_count
            }
        }

    except Exception as e:
        logger.error(f"💥 Error creating campaign stats: {str(e)}")
        import traceback
        logger.error(f"💥 Full traceback:\n{traceback.format_exc()}")
        return {
            "status": "error",
            "message": str(e),
            "campaign_id": campaign_id if 'campaign_id' in locals() else None
        }


@inngest_client.create_function(
    fn_id="complete_campaign",
    trigger=inngest.TriggerEvent(event="campaigns/complete"),
)
def complete_campaign(ctx: inngest.Context):
    """
    Complete a campaign when all message assignments are sent.
    Updates campaign status and releases email accounts.
    """
    try:
        campaign_id = ctx.event.data.get("campaign_id")

        if not campaign_id:
            return {"status": "error", "message": "campaign_id is required"}

        logger.info(f"🏁 Completing campaign {campaign_id}")

        from .models import Campaign, MessageAssignment

        # Get the campaign
        campaign = Campaign.objects.get(id=campaign_id)

        # Check if all message assignments are sent
        pending_assignments = MessageAssignment.objects.filter(
            campaign=campaign,
            sent=False
        ).count()

        if pending_assignments > 0:
            logger.warning(f"⚠️ Campaign {campaign_id} still has {pending_assignments} pending assignments")
            return {
                "status": "warning",
                "message": f"Campaign still has {pending_assignments} pending assignments",
                "campaign_id": campaign_id,
                "pending_assignments": pending_assignments
            }

        # Update campaign status
        campaign.status = 'completed'
        campaign.is_active = False
        campaign.save(update_fields=['status', 'is_active'])

        # Release email accounts from campaign options
        campaign_options = campaign.campaign_options.first()
        if campaign_options:
            email_accounts = list(campaign_options.email_accounts.all())
            campaign_options.email_accounts.clear()

            logger.info(f"🔓 Released {len(email_accounts)} email accounts from campaign {campaign.name}")
            for account in email_accounts:
                logger.info(f"  - Released: {account.email}")

        logger.info(f"✅ Campaign {campaign.name} completed successfully")

        return {
            "status": "success",
            "message": f"Campaign {campaign.name} completed successfully",
            "campaign_id": campaign_id,
            "campaign_name": campaign.name,
            "released_accounts": len(email_accounts) if 'email_accounts' in locals() else 0
        }

    except Exception as e:
        logger.error(f"💥 Error completing campaign: {str(e)}")
        import traceback
        logger.error(f"💥 Full traceback:\n{traceback.format_exc()}")
        return {
            "status": "error",
            "message": str(e),
            "campaign_id": campaign_id if 'campaign_id' in locals() else None
        }
