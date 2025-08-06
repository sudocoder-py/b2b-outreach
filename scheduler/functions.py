from datetime import timedelta, datetime
from django.utils import timezone

import inngest

from .client import inngest_client


# Create an Inngest function
@inngest_client.create_function(
    fn_id="campaign_scheduler",
    # Event that triggers this function
    trigger=inngest.TriggerEvent(event="posts/campaign.scheduled"),
)
def campaign_scheduler(ctx: inngest.Context) -> str:
    """
    Schedules a campaign for a future date.
    """
    pass
    