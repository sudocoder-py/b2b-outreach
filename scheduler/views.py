import inngest
import inngest.django 

from .client import inngest_client
from .functions import (
    campaign_scheduler
)


active_inngest_functions = [
    campaign_scheduler
]


scheduler_inngest_view_path = inngest.django.serve(inngest_client, active_inngest_functions)