import logging
import inngest
from environ import Env

env = Env()

inngest_client = inngest.Inngest(
    app_id="social_share",
    logger=logging.getLogger("gunicorn"),
)
