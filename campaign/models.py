from django.db import models
from django.utils import timezone
import uuid
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
import re
from clients.models import EmailAccount, SubscribedCompany, Product
import markdown
from .dicts import timezone_options, days_options, time_options, get_default_days
from django.contrib.postgres.fields import ArrayField
from django.core import validators


class Campaign(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('draft', 'Draft'),
        ('ended', 'Ended')
    ]
    subscribed_company = models.ForeignKey(SubscribedCompany, on_delete=models.CASCADE)

    name = models.CharField(max_length=255)
    short_name = models.SlugField(unique=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    status= models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')

    def save(self, *args, **kwargs):
        # Generate short_name if not provided
        if not self.short_name:
            # First save to get an ID if this is a new campaign
            if not self.id:
                super().save(*args, **kwargs)
                
            # Get first letter of each word in campaign name
            name_initials = ''.join([word[0].lower() for word in self.name.split() if word])
            
            # Create short_name with campaign ID and initials
            self.short_name = f"c{self.id}-{name_initials}"
            
            # Save again with the generated short_name
            kwargs['force_insert'] = False
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.product.name}"

    def to_dict_for_ai(self):
        """Return a dictionary with campaign data formatted for AI personalization"""
        return {
            'name': self.name,
            'short_name': self.short_name,
            'product_name': self.product.name,
            'product_description': self.product.description,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat() if self.end_date else None
        }


class Schedule(models.Model):
    subscribed_company = models.ForeignKey(SubscribedCompany, on_delete=models.CASCADE, null=True, blank=True)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, null=True, blank=True)

    TIME_ZONES = timezone_options
    DAYES_CHOICES = days_options
    TIME_CHOICES= time_options

    name = models.CharField(max_length=255, default="Default Schedule")
    start_date = models.DateTimeField(default=timezone.now)
    timing_from = models.CharField(max_length=255, choices=TIME_CHOICES, default="00:00", blank=True)
    timing_to = models.CharField(max_length=255, choices=TIME_CHOICES, default="23:00", blank=True)
    time_zone = models.CharField(max_length=255, choices=TIME_ZONES, default="Europe/London", blank=True)
    days = ArrayField(
        models.CharField(max_length=3, choices=days_options),
        blank=True,
        default=get_default_days,
    )

    def __str__(self):
        return self.name





class CampaignOptions(models.Model):
    """
    Model to store various options and settings for a marketing campaign,
    as derived from the VibeReach UI screenshot.
    """

    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='campaign_options')
    
    # Accounts to use
    email_accounts = models.ManyToManyField(EmailAccount, related_name='email_accounts_campaign_options')
    
    # Stop sending emails on reply
    stop_on_reply = models.BooleanField(default=True)
    
    # Open Tracking
    open_tracking_enabled = models.BooleanField(default=True)
    link_tracking_enabled = models.BooleanField(default=True)
    
    # Delivery Optimization
    send_as_text_only = models.BooleanField(default=False)
    send_first_email_as_text_only = models.BooleanField(default=True)
    
    # Daily Limit
    daily_limit = models.IntegerField(
        validators=[
            validators.MinValueValidator(1, "Daily limit must be at least 1."),
            validators.MaxValueValidator(1000, "Daily limit cannot exceed 1000.")
        ],
        default=30
    )
    
    def __str__(self):
        return f"Options for Campaign: {self.campaign.name}"
     
    class Meta:
        verbose_name = "Campaign Option"
        verbose_name_plural = "Campaign Options" 
   




class LeadList(models.Model):
    subscribed_company = models.ForeignKey(SubscribedCompany, on_delete=models.CASCADE, null=True, blank=True)
    title= models.CharField(max_length=255)
    tags= models.CharField(max_length=255, default='new list', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    campaigns= models.ManyToManyField(Campaign, null=True, blank=True)

    def __str__(self):
        return f"{self.title}"



class Lead(models.Model):
    lead_list = models.ForeignKey(LeadList, on_delete=models.CASCADE, null=True, blank=True, related_name="lead_lists")
    subscribed_company = models.ForeignKey(SubscribedCompany, on_delete=models.CASCADE, null=True, blank=True)

    full_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    position = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True)
    linkedin_profile = models.URLField(blank=True)
    
    company_name = models.CharField(max_length=255)
    company_website = models.URLField(blank=True)
    industry = models.CharField(max_length=100, blank=True)
    employee_count = models.CharField(max_length=50, blank=True)
    campany_linkedin_page= models.URLField(blank=True)

    location= models.CharField(max_length=255, blank=True)

    SOURCE_CHOICES = [
        ("linkedin_scrape", "LinkedIn Scrape"),
        ("social", "Social Media"),
        ("newsletter", "Newsletter Opt-in"),
        ("form", "Form"),
        ("other", "Other"),
    ]
    TYPE_CHOICES = [
        ("cold", "Cold"),
        ("warm", "Warm"),
        ("hot", "Hot"),
        ("customer", "Customer"),
        ("other", "Other"),
    ]
    source = models.CharField(max_length=50, choices=SOURCE_CHOICES)
    lead_type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Auto-populate first_name and last_name from full_name if not set
        if self.full_name and (not self.first_name or not self.last_name):
            name_parts = self.full_name.strip().split()
            
            if len(name_parts) > 0:
                # First name is the first part
                self.first_name = name_parts[0]
                
                # Last name is everything else (including middle names)
                if len(name_parts) > 1:
                    self.last_name = ' '.join(name_parts[1:])
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name}"

    def to_dict_for_ai(self):
        """Return a dictionary with lead data formatted for AI personalization"""
        return {
            'full_name': self.full_name,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'position': self.position,
            'company_name': self.company_name,
            'industry': self.industry,
            'source': self.get_source_display(),
            'lead_type': self.get_lead_type_display(),
            'created_at': self.created_at.isoformat()
        }





class CampaignLead(models.Model):
    OPPORTUNITY_STATUS_CHOICES = [
        ('none', 'No Opportunity'),
        ('positive', 'Positive'),
        ('won', 'Won'),
        ('lost', 'Lost'),
    ]

    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE)

    # Legacy conversion field (keep for backward compatibility)
    is_converted = models.BooleanField(default=False)
    converted_at = models.DateTimeField(null=True, blank=True)

    # Enhanced opportunity tracking
    opportunity_status = models.CharField(
        max_length=20,
        choices=OPPORTUNITY_STATUS_CHOICES,
        default='none',
        help_text="Current opportunity status for this lead"
    )
    opportunity_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Expected value of this opportunity"
    )
    opportunity_marked_at = models.DateTimeField(null=True, blank=True)

    # Conversion tracking (when opportunity becomes won)
    conversion_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Actual conversion value (can be different from opportunity_value)"
    )
    conversion_notes = models.TextField(blank=True, help_text="Notes about the conversion")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('campaign', 'lead')

    def __str__(self):
        return f"{self.lead} - {self.campaign.name}"

    def convert(self):
        """Mark this lead as converted (legacy method)"""
        if not self.is_converted:
            self.is_converted = True
            self.converted_at = timezone.now()
            self.save()

            # Update campaign stats
            stats, _ = CampaignStats.objects.get_or_create(campaign=self.campaign)
            stats.update_from_campaign()

            return True
        return False

    def mark_as_opportunity(self, value=None):
        """Mark this lead as a positive opportunity"""
        self.opportunity_status = 'positive'
        self.opportunity_value = value
        self.opportunity_marked_at = timezone.now()
        self.save()

        # Update campaign stats
        stats, _ = CampaignStats.objects.get_or_create(campaign=self.campaign)
        stats.update_from_campaign()

    def mark_as_won(self, conversion_value=None, notes=""):
        """Mark this opportunity as won (converted)"""
        self.opportunity_status = 'won'
        self.conversion_value = conversion_value or self.opportunity_value
        self.conversion_notes = notes

        # Also update legacy fields for backward compatibility
        self.is_converted = True
        self.converted_at = timezone.now()

        self.save()

        # Update campaign stats
        stats, _ = CampaignStats.objects.get_or_create(campaign=self.campaign)
        stats.update_from_campaign()

    def mark_as_lost(self, notes=""):
        """Mark this opportunity as lost"""
        self.opportunity_status = 'lost'
        self.conversion_notes = notes
        self.save()

        # Update campaign stats
        stats, _ = CampaignStats.objects.get_or_create(campaign=self.campaign)
        stats.update_from_campaign()

    @property
    def is_opportunity(self):
        """Check if this lead is marked as a positive opportunity"""
        return self.opportunity_status == 'positive'

    @property
    def is_won(self):
        """Check if this lead has been converted (won)"""
        return self.opportunity_status == 'won'






class NewsletterSubscriber(models.Model):
    lead = models.ForeignKey(Lead, null=True, blank=True, on_delete=models.SET_NULL)
    joined_at = models.DateTimeField(auto_now_add=True)
    unsubscribed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.lead.full_name} - {self.lead.email} - {self.joined_at}"











class Message(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    intro = models.TextField(blank=True)
    content = models.TextField()
    cta = models.CharField(max_length=255, blank=True)
    ps = models.TextField(blank=True)
    pps = models.TextField(blank=True)
    end = models.TextField(blank=True)

    full_content = models.TextField(blank=True)

    def __str__(self):
        return f"{self.subject}"
    

    def _convert_markdown_to_html(self, text):
        """
        Converts markdown links [text](url) to <a href="url">text</a>.
        """
        result = markdown.markdown(text)
        return result


    def save(self, *args, **kwargs):
        # Combine all message components into full_content
        parts = []
        if self.intro:
            parts.append(self.intro)
        if self.content:
            parts.append(self.content)
        if self.cta:
            parts.append(f"{self.cta}")  
        if self.ps:
            parts.append(f"{self.ps}")
        if self.pps:
            parts.append(f"{self.pps}")
        if self.end:
            parts.append(f"{self.end}")      
            
        combined_content = "\n\n".join(parts)

        # Apply markdown link replacements
        combined_content = self._convert_markdown_to_html(combined_content)

        self.full_content = combined_content
        
        super().save(*args, **kwargs)        





class Link(models.Model):
    PURPOSE_CHOICES = [
        ('message', 'Email Message'),
        ('social', 'Social Media'),
        ('manual', 'Manual Sharing'),
        ('other', 'Other')
    ]
    
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    campaign_lead = models.ForeignKey(CampaignLead, on_delete=models.CASCADE, null=True, blank=True)
    
    # Purpose of this link
    purpose = models.CharField(
        max_length=20, 
        choices=PURPOSE_CHOICES,
        default='message',
        help_text="What this link will be used for"
    )
    
    # Optional description
    description = models.CharField(max_length=255, blank=True, help_text="Optional description of this link's purpose")
    
    # Base URL from product's landing page
    url = models.URLField(
        blank=True,
        help_text="Will be auto-populated from campaign's product landing page if left empty"
    )
    
    # UTM parameters with defaults
    utm_source = models.CharField(max_length=100, default="email_outreach")
    utm_medium = models.CharField(max_length=100, default="email")
    utm_campaign = models.CharField(
        max_length=100,
        blank=True,
        help_text="Will be auto-populated from campaign's short_name if left empty"
    )
    utm_term = models.CharField(max_length=100, blank=True)
    utm_content = models.CharField(max_length=100, blank=True)
    
    # Reference code for tracking
    ref = models.CharField(
        max_length=50, 
        unique=True, 
        blank=True, 
        help_text="Unique reference code for tracking (auto-generated if left empty)"
    )
    
    # Tracking
    visited_at = models.DateTimeField(null=True, blank=True)
    visit_count = models.IntegerField(default=0)
    
    # Add created_at field
    created_at = models.DateTimeField(auto_now_add=True)

    def clean_url(self):
        """Normalize the URL to prevent issues with trailing slashes and fragments"""
        if not self.url:
            return ""
            
        # Parse the URL into components
        parsed = urlparse(self.url)
        
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
        # Normalize the URL before saving
        if self.url:
            self.url = self.clean_url()
            
        # Auto-populate utm_campaign from campaign short_name if not set
        if not self.utm_campaign and self.campaign:
            self.utm_campaign = self.campaign.short_name
            
        # Generate unique ref if not set
        if not self.ref:
            if self.campaign_lead:
                # Base on campaign lead ID with unique suffix
                base_ref = f"L{self.campaign_lead.lead.id}-CL{self.campaign_lead.id}-C{self.campaign.id}"
                # Add unique suffix to prevent duplicates
                unique_suffix = uuid.uuid4().hex[:6]
                self.ref = f"{base_ref}-{unique_suffix}"
            else:
                # If no campaign lead, generate completely random ref
                self.ref = f"R-{uuid.uuid4().hex[:10]}"
            
        # Auto-populate URL from product if not set
        if not self.url and self.campaign:
            self.url = self.campaign.product.landing_page_url
            
        super().save(*args, **kwargs)
    
    def get_redirect_url(self):
        """Get the Django redirect URL for tracking"""
        from django.urls import reverse
        return reverse('redirect_and_track_emails', kwargs={'ref_code': self.ref})
    
    def get_full_redirect_url(self):
        redirect_url = self.get_redirect_url()
        full_url = f"{settings.SITE_URL}{redirect_url}" if hasattr(settings, 'SITE_URL') else redirect_url
        return full_url

    def full_url(self):
        """Get the full URL with all UTM parameters while preserving fragments"""
        if not self.url:
            return ""
            
        # Parse the base URL
        parsed = urlparse(self.url)
        
        # Get existing query parameters
        query_params = parse_qs(parsed.query)
        
        # Add UTM parameters
        utm_params = {
            'utm_source': self.utm_source,
            'utm_medium': self.utm_medium,
            'utm_campaign': self.utm_campaign
        }
        
        # Only add non-empty parameters
        if self.utm_term:
            utm_params['utm_term'] = self.utm_term
        if self.utm_content:
            utm_params['utm_content'] = self.utm_content
        if self.ref:
            utm_params['ref'] = self.ref
            
        # Update query parameters with UTM parameters
        query_params.update(utm_params)
        
        # Convert query parameters to string
        query_string = urlencode(query_params, doseq=True)
        
        # Rebuild the URL with the new query string, preserving the fragment
        result = urlunparse((
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            query_string,
            parsed.fragment  # Preserve fragment (#) if present
        ))
        
        return result

    def track_visit(self):
        """Record a visit to this link"""
        self.visit_count += 1
        self.visited_at = timezone.now()
        self.save()

    def __str__(self):
        return f"{self.ref}"



class MessageAssignment(models.Model):
    # Add campaign field for direct access
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, null=True, blank=True)
    
    campaign_lead = models.ForeignKey(CampaignLead, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    url = models.ForeignKey(Link, null=True, blank=True, on_delete=models.SET_NULL, related_name='message_assignments')
    
    newsletter_link = models.ForeignKey(Link, null=True, blank=True, on_delete=models.SET_NULL, related_name='newsletter_message_assignments', help_text="Link for newsletter signup")

    personlized_msg_tmp = models.TextField(blank=True)
    personlized_msg_to_send = models.TextField(blank=True)
    
    delayed_by_days = models.IntegerField(null=True, blank=True)

    sent = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, blank=True)

    opened = models.BooleanField(default=False)
    opened_at = models.DateTimeField(null=True, blank=True)
    
    responded = models.BooleanField(default=False)
    responded_content = models.TextField(blank=True)

    def get_tracking_url(self, url_type="product_url"):
        if url_type == "product_url" and self.url:
            redirect_url = self.url.get_redirect_url()
            full_url = f"{settings.SITE_URL}{redirect_url}" if hasattr(settings, 'SITE_URL') else redirect_url
            return full_url

        if url_type == "newsletter" and self.newsletter_link:
            redirect_url = self.newsletter_link.get_redirect_url()
            full_url = f"{settings.SITE_URL}{redirect_url}" if hasattr(settings, 'SITE_URL') else redirect_url
            return full_url

        return ""
    
    

    def get_personalized_content_tmp(self):
        """Get the personalized message content with tracking URLs"""
        content = self.personlized_msg_tmp or self.message.full_content

        def _replace(tag, url):
            pattern = rf'{{{tag}(?:\|([^}}]+))?}}'   # captures optional anchor text
            def repl(m):
                text = m.group(1) or "here"
                return f'<a href="{url}">{text}</a>'
            return re.sub(pattern, repl, content)
        
        if self.url:
            product_tracking_url = self.get_tracking_url(url_type="product_url")
            content = _replace("ps_url", product_tracking_url)

        if self.newsletter_link and self.message.pps:
                newsletter_tracking_url = self.get_tracking_url(url_type="newsletter")
                content = _replace("pps_url", newsletter_tracking_url)

        return content


    # def get_personalized_content_tmp(self):
    #     """Get the personalized message content with tracking URL"""
    #     content = self.personlized_msg_tmp or self.message.full_content

    #     # Replace CTA placeholder with tracking URL if available
    #     if self.url:
    #         product_tracking_url = self.get_tracking_url(url_type="product_url")
    #         # Allow the user to define the anchor text, e.g., {ps_url|Click Here}
    #         if '{ps_url' in content:
    #             parts = content.split('{ps_url', 1)
    #             before = parts[0]
    #             after = parts[1]
                
    #             # Check if anchor text is provided
    #             if '|' in after:
    #                 anchor_text = after.split('}', 1)[0].split('|')[1]
    #                 content = before + f'<a href="{product_tracking_url}">{anchor_text}</a>' + after.split('}', 1)[1]
    #             else:
    #                 content = before + f'<a href="{product_tracking_url}">here</a>' + after.split('}', 1)[1]

    #     if self.newsletter_link:
    #         newsletter_tracking_url = self.get_tracking_url(url_type="newsletter")
    #         if self.message.pps:
    #             if '{pps_url' in content:
    #                 parts = content.split('{pps_url', 1)
    #                 before = parts[0]
    #                 after = parts[1]
    #                 # Check if anchor text is provided
    #                 if '|' in after:
    #                     anchor_text = after.split('}', 1)[0].split('|')[1]
    #                     content = before + f'<a href="{newsletter_tracking_url}">{anchor_text}</a>' + after.split('}', 1)[1]
    #                 else:
    #                     content = before + f'<a href="{newsletter_tracking_url}">here</a>' + after.split('}', 1)[1]            

            

    #     return content

    def __str__(self):
        if not hasattr(self, 'campaign_lead') or self.campaign_lead is None:
            return f"New message assignment - {self.message.subject if hasattr(self, 'message') else 'No message'}"
        return f"{self.campaign_lead} - {self.message.subject}"
    
    def save(self, *args, **kwargs):
        # Set campaign from campaign_lead if not explicitly set
        if self.campaign_lead and not self.campaign:
            self.campaign = self.campaign_lead.campaign
          
        # First save to get an ID if this is a new assignment
        if not self.id:
            super().save(*args, **kwargs)
            
        # Auto-create a link if one doesn't exist
        if not self.url and self.campaign_lead:
            # Create a new Link object with proper utm_content using the now-available ID
            link = Link(
                campaign=self.campaign_lead.campaign,
                campaign_lead=self.campaign_lead,
                url=self.campaign_lead.campaign.product.landing_page_url,
                utm_content=f"email_{self.id}"
            )
            # Save it to generate unique ref and apply other logic
            link.save()
            self.url = link
            # Save again with the link
            kwargs['force_insert'] = False
            super().save(*args, **kwargs)
            
        
        # Auto-create a link if one doesn't exist
        if not self.newsletter_link and self.campaign_lead:
            if self.campaign.subscribed_company.newsletter_link: 
                # Create a new Link object with proper utm_content using the now-available ID
                link = Link(
                    campaign=self.campaign_lead.campaign,
                    campaign_lead=self.campaign_lead,
                    url=self.campaign.subscribed_company.newsletter_link,
                    utm_content=f"email_{self.id}"
                )
                # Save it to generate unique ref and apply other logic
                link.save()
                self.newsletter_link = link
                # Save again with the link
                kwargs['force_insert'] = False
                super().save(*args, **kwargs)
            
        
        if not self.personlized_msg_tmp:
            self.personlized_msg_tmp = self.get_personalized_content_tmp() 
        
        super().save(*args, **kwargs)

    def get_ai_personalization_data(self):
        """
        Gather all relevant data needed for AI personalization.
        Returns a dictionary with lead, campaign, and message data.
        """
        data = {
            'lead': {},
            'campaign': {},
            'message': {
                'template': self.personlized_msg_tmp
            }
        }
        
        # Get lead data
        if self.campaign_lead and self.campaign_lead.lead:
            data['lead'] = self.campaign_lead.lead.to_dict_for_ai()
        
        # Get campaign data
        if self.campaign:
            data['campaign'] = self.campaign.to_dict_for_ai()
        
        return data

    def personalize_with_ai(self, skip=True):
        """
        Use AI to personalize this message and save the result.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            from campaign.ai_service import personalize_message
            
            # Get personalized text
            personalized_text = personalize_message(self, skip=skip)
            
            # Save it to the database
            self.personlized_msg_to_send = personalized_text
            self.save(update_fields=['personlized_msg_to_send'])
            
            return True
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error personalizing message: {str(e)}")
            return False



class CampaignStats(models.Model):
    campaign = models.OneToOneField(Campaign, on_delete=models.CASCADE)

    # Basic counts
    total_leads = models.IntegerField(default=0)

    # 1. Sequence Started: leads that received at least one email
    sequence_started_count = models.IntegerField(default=0)

    # 2. Open Rate: leads that opened at least one email
    opened_count = models.IntegerField(default=0)

    # 3. Click Rate: leads that clicked at least one link
    clicked_count = models.IntegerField(default=0)

    # 4. Reply Rate: leads that replied to at least one message
    replied_count = models.IntegerField(default=0)

    # 5. Opportunities: leads marked as positive opportunities
    opportunities_count = models.IntegerField(default=0)
    opportunities_total_value = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # 6. Conversions: leads that won (converted)
    conversions_count = models.IntegerField(default=0)
    conversions_total_value = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # Legacy fields (keep for backward compatibility)
    total_messages_sent = models.IntegerField(default=0)
    total_opens = models.IntegerField(default=0)
    total_clicks = models.IntegerField(default=0)
    total_conversions = models.IntegerField(default=0)

    best_cta = models.ForeignKey(Link, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    best_message = models.ForeignKey(Message, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')

    updated_at = models.DateTimeField(auto_now=True)

    @property
    def open_rate(self):
        return round(self.total_opens / self.total_messages_sent * 100, 2) if self.total_messages_sent else 0

    @property
    def click_rate(self):
        return round(self.total_clicks / self.total_opens * 100, 2) if self.total_opens else 0

    @property
    def conversion_rate(self):
        return round(self.total_conversions / self.total_leads * 100, 2) if self.total_leads else 0
        
    @property
    def click_to_conversion_rate(self):
        return round(self.total_conversions / self.total_clicks * 100, 2) if self.total_clicks else 0

    # New percentage calculations for the 6 key metrics
    @property
    def sequence_started_rate(self):
        """Percentage of leads that started the sequence (received at least one email)"""
        return round(self.sequence_started_count / self.total_leads * 100, 2) if self.total_leads else 0

    @property
    def open_rate_percentage(self):
        """Percentage of leads that opened at least one email"""
        return round(self.opened_count / self.total_leads * 100, 2) if self.total_leads else 0

    @property
    def click_rate_percentage(self):
        """Percentage of leads that clicked at least one link"""
        return round(self.clicked_count / self.total_leads * 100, 2) if self.total_leads else 0

    @property
    def reply_rate_percentage(self):
        """Percentage of leads that replied to at least one message"""
        return round(self.replied_count / self.total_leads * 100, 2) if self.total_leads else 0

    @property
    def opportunities_rate(self):
        """Percentage of leads marked as opportunities"""
        return round(self.opportunities_count / self.total_leads * 100, 2) if self.total_leads else 0

    @property
    def conversion_rate_percentage(self):
        """Percentage of leads that converted (won)"""
        return round(self.conversions_count / self.total_leads * 100, 2) if self.total_leads else 0

    def update_from_campaign(self):
        """Update stats based on campaign data"""
        from django.db.models import Q

        # Count total leads
        campaign_leads = self.campaign.campaignlead_set.all()
        self.total_leads = campaign_leads.count()

        # 1. Sequence Started: leads that have been sent at least one email
        leads_with_sent_messages = campaign_leads.filter(
            messageassignment__sent_at__isnull=False
        ).distinct()
        self.sequence_started_count = leads_with_sent_messages.count()

        # 2. Open Rate: leads that opened at least one email
        leads_with_opens = campaign_leads.filter(
            messageassignment__opened=True
        ).distinct()
        self.opened_count = leads_with_opens.count()

        # 3. Click Rate: leads that clicked at least one link
        leads_with_clicks = campaign_leads.filter(
            Q(messageassignment__url__visit_count__gt=0) |
            Q(messageassignment__newsletter_link__visit_count__gt=0)
        ).distinct()
        self.clicked_count = leads_with_clicks.count()

        # 4. Reply Rate: leads that replied to at least one message
        leads_with_replies = campaign_leads.filter(
            messageassignment__responded=True
        ).distinct()
        self.replied_count = leads_with_replies.count()

        # 5. Opportunities: leads marked as positive opportunities
        opportunities = campaign_leads.filter(opportunity_status='positive')
        self.opportunities_count = opportunities.count()
        self.opportunities_total_value = sum(
            lead.opportunity_value or 0 for lead in opportunities
        )

        # 6. Conversions: leads that won (converted)
        conversions = campaign_leads.filter(opportunity_status='won')
        self.conversions_count = conversions.count()
        self.conversions_total_value = sum(
            lead.conversion_value or 0 for lead in conversions
        )

        # Legacy calculations (keep for backward compatibility)
        message_assignments = MessageAssignment.objects.filter(
            campaign_lead__campaign=self.campaign,
            sent_at__isnull=False
        )
        self.total_messages_sent = message_assignments.count()
        self.total_opens = message_assignments.filter(opened=True).count()

        # Count clicks (from link visits)
        links = Link.objects.filter(campaign=self.campaign)
        self.total_clicks = sum(link.visit_count for link in links)

        # Count conversions (legacy)
        self.total_conversions = campaign_leads.filter(is_converted=True).count()

        # Find best performing CTA (link with most visits)
        if links.exists():
            self.best_cta = links.order_by('-visit_count').first()

        # Find best performing message (most clicks)
        if message_assignments.exists():
            # Group by message and count clicks
            message_clicks = {}
            for ma in message_assignments:
                if ma.url and ma.url.visit_count > 0:
                    message_id = ma.message_id
                    if message_id in message_clicks:
                        message_clicks[message_id] += ma.url.visit_count
                    else:
                        message_clicks[message_id] = ma.url.visit_count

            # Find message with most clicks
            if message_clicks:
                best_message_id = max(message_clicks, key=message_clicks.get)
                self.best_message_id = best_message_id

        self.save()

    def __str__(self):
        return f"Stats for {self.campaign.name}"

@receiver(post_save, sender=Link)
def update_campaign_stats_on_link_visit(sender, instance, **kwargs):
    """Update campaign stats when a link is visited"""
    if instance.visit_count > 0 and instance.campaign:
        # Get or create campaign stats
        stats, _ = CampaignStats.objects.get_or_create(campaign=instance.campaign)

        # Update stats
        stats.update_from_campaign()

        # If this link is associated with a campaign lead, check for conversion
        if instance.campaign_lead and instance.campaign_lead.is_converted:
            # This could be a good place to trigger conversion tracking
            pass
