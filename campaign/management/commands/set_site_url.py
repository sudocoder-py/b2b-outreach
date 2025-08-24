from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site

class Command(BaseCommand):
    help = "Set the SITE_URL for the current site"

    def add_arguments(self, parser):
        parser.add_argument("domain", type=str, help="The new site domain (e.g. vibereach.gatara.org)")

    def handle(self, *args, **options):
        domain = options["domain"]
        site = Site.objects.get_current()
        site.domain = domain
        site.name = domain
        site.save()

        self.stdout.write(self.style.SUCCESS(f"Site URL updated to {domain}"))
