from django.db import models
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode
import uuid
from django.utils import timezone
from django.conf import settings
import re
from clients.models import SubscribedCompany, Product




class PostsCampaign(models.Model):
    subscribed_company = models.ForeignKey(SubscribedCompany, on_delete=models.CASCADE)

    name = models.CharField(max_length=255)
    short_name = models.SlugField(unique=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

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







class Link(models.Model):
    PURPOSE_CHOICES = [
        ('message', 'DM'),
        ('social', 'Social Media'),
        ('manual', 'Manual Sharing'),
        ('other', 'Other')
    ]
    
    campaign = models.ForeignKey(PostsCampaign, on_delete=models.CASCADE)
    
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
            self.ref = f"R-{uuid.uuid4().hex[:10]}"
            
        # Auto-populate URL from product if not set
        if not self.url and self.campaign:
            self.url = self.campaign.product.landing_page_url
            
        super().save(*args, **kwargs)
    
    def get_redirect_url(self):
        """Get the Django redirect URL for tracking"""
        from django.urls import reverse
        return reverse('redirect_and_track_post', kwargs={'ref_code': self.ref})

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





class Post(models.Model):
    campaign = models.ForeignKey(PostsCampaign, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    url = models.ForeignKey(Link, null=True, blank=True, on_delete=models.SET_NULL, related_name='message_assignments')
    newsletter_link = models.ForeignKey(Link, null=True, blank=True, on_delete=models.SET_NULL, help_text="Link for newsletter signup")

    headline = models.CharField(max_length=255)
    intro = models.TextField(blank=True)
    content = models.TextField()
    cta = models.CharField(max_length=255, blank=True)
    ps = models.TextField(blank=True)
    pps = models.TextField(blank=True)

    full_content = models.TextField(blank=True)


    scheduled_at = models.DateTimeField(null=True, blank=True)

    posted = models.BooleanField(default=False)
    posted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.headline}"


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
    

    def save(self, *args, **kwargs):
        # Combine all message components into full_content
        parts = []
        if self.headline:
            parts.append(self.headline)
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

        if not self.url:
            # Create a new Link object with proper utm_content using the now-available ID
            link = Link(
                campaign=self.campaign,
                url=self.product.landing_page_url,
                utm_content=f"post_{self.id}"
            )
            # Save it to generate unique ref and apply other logic
            link.save()
            self.url = link
            # Save again with the link
            kwargs['force_insert'] = False



        if not self.newsletter_link:
            if self.campaign.subscribed_company.newsletter_link:
                # Create a new Link object with proper utm_content using the now-available ID
                link = Link(
                    campaign=self.campaign,
                    url=self.campaign.subscribed_company.newsletter_link,
                    utm_content=f"post_{self.id}"
                )
                # Save it to generate unique ref and apply other logic
                link.save()
                self.newsletter_link = link
                # Save again with the link
                kwargs['force_insert'] = False

        
        content=  "\n\n".join(parts)  
        content = self.get_post_urls(content=content)
        self.full_content = content

        super().save(*args, **kwargs)


    def get_post_urls(self, content):
        """Get the personalized message content with tracking URLs"""
        content = content

        def _replace(tag, url):
            pattern = rf'{{{tag}(?:\|([^}}]+))?}}'  
            def repl(m):
                text = m.group(1) or "here"
                return f'<a href="{url}">{text}</a>'
            return re.sub(pattern, repl, content)
        
        if self.url:
            product_tracking_url = self.get_tracking_url(url_type="product_url")
            content = _replace("ps_url", product_tracking_url)

        if self.newsletter_link and self.pps:
                newsletter_tracking_url = self.get_tracking_url(url_type="newsletter")
                content = _replace("pps_url", newsletter_tracking_url)    

        return content
