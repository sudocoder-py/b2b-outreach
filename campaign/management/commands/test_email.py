from django.core.management.base import BaseCommand
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from campaign.models import MessageAssignment
from campaign.email_sender import send_campaign_email, CustomEmailBackend
from clients.models import EmailAccount
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Test email sending with Zoho Mail'

    def add_arguments(self, parser):
        parser.add_argument('--id', type=int, help='ID of a specific message assignment to send')
        parser.add_argument('--test', action='store_true', help='Send a simple test email')
        parser.add_argument('--recipient', type=str, help='Email address to send test email to')
        parser.add_argument('--account-id', type=int, help='ID of email account to use for test')

    def handle(self, *args, **options):
        message_id = options.get('id')
        test = options.get('test')
        recipient = options.get('recipient')
        account_id = options.get('account_id')

        if test:
            if not recipient:
                self.stdout.write(self.style.ERROR("Please provide a recipient email with --recipient"))
                return

            self.stdout.write(f"Sending test email to {recipient}...")

            try:
                # Get email account to use
                email_account = None
                if account_id:
                    try:
                        email_account = EmailAccount.objects.get(id=account_id)
                        self.stdout.write(f"Using email account: {email_account.email}")
                    except EmailAccount.DoesNotExist:
                        self.stdout.write(self.style.ERROR(f"Email account with ID {account_id} not found"))
                        return
                else:
                    # Use first active email account
                    email_account = EmailAccount.objects.filter(status='active').first()
                    if not email_account:
                        self.stdout.write(self.style.ERROR("No active email accounts found. Please create one first."))
                        return
                    self.stdout.write(f"Using first active email account: {email_account.email}")

                # Simple test email
                subject = "Test Email from Django Campaign System"
                message = f"This is a test email sent from Django using {email_account.email}."
                html_message = f"<h1>Test Email</h1><p>This is a <strong>test email</strong> sent from Django using <code>{email_account.email}</code>.</p>"

                # Determine sender information
                sender_name = email_account.sender_name or email_account.email.split('@')[0]
                from_email = f"{sender_name} <{email_account.email}>"

                if email_account.is_smtp():
                    # Use custom backend for SMTP accounts
                    backend = CustomEmailBackend(email_account)

                    # Create email message with both HTML and plain text versions
                    email = EmailMultiAlternatives(
                        subject=subject,
                        body=message,  # Plain text version
                        from_email=from_email,
                        to=[recipient],
                        connection=backend
                    )

                    # Add HTML version
                    email.attach_alternative(html_message, "text/html")

                    # Send the email
                    sent = email.send(fail_silently=False)

                else:
                    self.stdout.write(self.style.ERROR(f"OAuth2 accounts not yet supported for testing"))
                    return

                if sent:
                    self.stdout.write(self.style.SUCCESS(f"Successfully sent test email to {recipient} from {email_account.email}"))
                else:
                    self.stdout.write(self.style.ERROR(f"Failed to send test email to {recipient}"))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error sending test email: {str(e)}"))
                
        elif message_id:
            # Send a specific message
            self.stdout.write(f"Sending email for message assignment ID {message_id}...")
            
            try:
                message_assignment = MessageAssignment.objects.get(id=message_id)
                success = send_campaign_email(message_assignment)
                
                if success:
                    self.stdout.write(self.style.SUCCESS(f"Successfully sent email for message assignment ID {message_id}"))
                else:
                    self.stdout.write(self.style.ERROR(f"Failed to send email for message assignment ID {message_id}"))
                    
            except MessageAssignment.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"Message assignment with ID {message_id} does not exist"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error sending email: {str(e)}"))
                
        else:
            self.stdout.write(self.style.ERROR("Please specify --id or --test"))