import inngest
import inngest.django

from .client import inngest_client
from .functions import (
    campaign_scheduler
)

# Import campaign processing functions
from campaign.tasks_inngest import (
    personalize_message_task,
    personalize_campaign_messages_task,
    send_email_task,
    send_campaign_emails_task,
    personalize_and_send_all_emails_at_once
)


active_inngest_functions = [
    campaign_scheduler,
    personalize_message_task,
    personalize_campaign_messages_task,
    send_email_task,
    send_campaign_emails_task,
    personalize_and_send_all_emails_at_once
]


scheduler_inngest_view_path = inngest.django.serve(inngest_client, active_inngest_functions)