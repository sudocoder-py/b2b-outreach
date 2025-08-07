import inngest
import inngest.django

from .client import inngest_client
from .functions import (
    campaign_scheduler
)

# Import campaign processing functions
from campaign.tasks_inngest import (
    personalize_and_send_all_emails_at_once,
    process_scheduled_emails,
    send_single_email,
    send_rate_limited_batch
)


active_inngest_functions = [
    campaign_scheduler,
    personalize_and_send_all_emails_at_once,
    process_scheduled_emails,
    send_single_email,
    send_rate_limited_batch
]


scheduler_inngest_view_path = inngest.django.serve(inngest_client, active_inngest_functions)