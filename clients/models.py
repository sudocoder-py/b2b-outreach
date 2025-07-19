from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from urllib.parse import urlparse, urlunparse



class SubscribedCompany(models.Model):
    name = models.CharField(max_length=255)
    website = models.URLField(unique=True)
    email= models.EmailField(unique=True)
    industry = models.CharField(max_length=100)
    employee_count = models.CharField(max_length=50)
    linkedin_page= models.URLField(blank=True)
    location= models.CharField(max_length=255)

    manager_full_name = models.CharField(max_length=255, blank=True)
    manager_position = models.CharField(max_length=100, blank=True, help_text="ex: founder, cofounder...")
    manager_email = models.EmailField(unique=True, blank=True, null=True)
    manager_phone_number = models.CharField(max_length=20, blank=True)
    manager_linkedin_profile = models.URLField(unique=True, blank=True, null=True)
    
    newsletter_link = models.URLField(
        blank=True,
        help_text="newsletter link"
    )


    def __str__(self):
        return f"{self.name}"



class Plan(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    billing_cycle = models.CharField(max_length=20, choices=[
        ('monthly', 'Monthly'),
        ('annual', 'Annual')
    ])
    
    def __str__(self):
        return f"{self.name} (${self.price}/{self.billing_cycle})"




class Subscription(models.Model): 
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('trial', 'Trial'),
        ('past_due', 'Past Due'),
        ('canceled', 'Canceled'),
        ('expired', 'Expired'),
    ]
    
    subscribed_company = models.ForeignKey(SubscribedCompany, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT, related_name='subscriptions')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='trial')
    start_date = models.DateTimeField(auto_now_add=True)
    trial_end_date = models.DateTimeField(null=True, blank=True)
    current_period_end = models.DateTimeField(null=True, blank=True)
    canceled_at = models.DateTimeField(null=True, blank=True)
    
    
    # Billing information
    billing_email = models.EmailField()
    payment_method_id = models.CharField(max_length=255, blank=True)
    
    
    def __str__(self):
        return f"{self.subscribed_company.name}-{self.plan.name}-{self.id}"








class BillingHistory(models.Model):
    subscribed_company = models.ForeignKey(SubscribedCompany, on_delete=models.CASCADE, related_name='billing_history')
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    invoice_id = models.CharField(max_length=255, blank=True)
    payment_method = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded')
    ])
    
    class Meta:
        verbose_name_plural = "Billing Histories"
    
    def __str__(self):
        return f"{self.amount}-{self.status}-{self.subscribed_company}"



class CustomUser(AbstractUser):
    subscribed_company = models.ForeignKey(SubscribedCompany, on_delete=models.CASCADE, related_name='users')
    
    # Fix group conflicts
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )





class Product(models.Model):
    subscribed_company = models.ForeignKey(SubscribedCompany, on_delete=models.CASCADE)

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    landing_page_url = models.URLField(blank=True)

    def clean(self):
        """Clean the model fields before validation"""
        super().clean()
        
        # Clean the landing page URL
        if self.landing_page_url:
            self.landing_page_url = self._normalize_url(self.landing_page_url)
    
    def _normalize_url(self, url):
        """Normalize URL to ensure consistent format"""
        if not url:
            return ""
            
        # Parse the URL into components
        parsed = urlparse(url)
        
        # Normalize path (ensure consistent trailing slash handling)
        path = parsed.path
        if not path:
            path = "/"
        elif path != "/" and not path.endswith("/"):
            # Add trailing slash for consistency
            path = path + "/"
            
        # Rebuild the URL with normalized path
        normalized = urlunparse((
            parsed.scheme,
            parsed.netloc,
            path,
            parsed.params,
            parsed.query,
            parsed.fragment  # Preserve fragment (#) if present
        ))
        
        return normalized
    
    def save(self, *args, **kwargs):
        # Clean the URL before saving
        if self.landing_page_url:
            self.landing_page_url = self._normalize_url(self.landing_page_url)
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name



class EmailAccount(models.Model):
    CONNECTION_TYPE_CHOICES = [
        ('gmail', 'Gmail (OAuth2)'),
        ('outlook', 'Outlook/Microsoft 365 (OAuth2)'),
        ('yahoo', 'Yahoo (OAuth2)'),
        ('imap/smtp', 'IMAP/SMTP'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('error', 'Error'),
        ('pending', 'Pending'),
    ]

    subscribed_company = models.ForeignKey(
        SubscribedCompany,
        on_delete=models.CASCADE,
        related_name='email_accounts'
    )

    email = models.EmailField(unique=True)
    connection_type = models.CharField(max_length=20, choices=CONNECTION_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    # For SMTP accounts only
    smtp_host = models.CharField(max_length=255, blank=True)
    smtp_port = models.IntegerField(default=587)
    smtp_use_tls = models.BooleanField(default=True)
    smtp_use_ssl = models.BooleanField(default=False) 

    smtp_username = models.CharField(max_length=255, blank=True)
    smtp_password = models.CharField(max_length=255, blank=True)

    # Optional sender profile settings
    sender_name = models.CharField(max_length=255, blank=True)
    sender_signature = models.TextField(blank=True)
    default_from_email = models.EmailField(blank=True)

    # For Gmail/Outlook/Yahoo OAuth2
    access_token = models.TextField(blank=True)
    refresh_token = models.TextField(blank=True)
    token_expiry = models.DateTimeField(null=True, blank=True)
    last_auth_url = models.URLField(blank=True, null=True)

    # Rate control
    min_wait_time = models.IntegerField(default=1)
    emails_sent = models.IntegerField(default=0)
    daily_limit = models.IntegerField(default=30)

    def __str__(self):
        return f"{self.email} - {self.get_connection_type_display()}"

    def requires_oauth(self):
        return self.connection_type in ['gmail', 'outlook', 'yahoo']

    def is_smtp(self):
        return self.connection_type == 'imap/smtp'
    
    def test_connection(self):
        pass 

