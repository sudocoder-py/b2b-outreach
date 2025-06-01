from django import forms
from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count, Sum
from django.contrib.admin import SimpleListFilter
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.urls import path
from urllib.parse import unquote

from campaign.email_sender import send_campaign_email
from .models import (
    Product, Campaign, Lead, NewsletterSubscriber,
    CampaignLead, Message, Link, MessageAssignment, CampaignStats, 
    SubscribedCompany, Plan, Subscription, BillingHistory, CustomUser
)
import logging
from django.conf import settings
from import_export.admin import ImportExportModelAdmin
from .resources import LeadResource

# Configure logger
logger = logging.getLogger(__name__)






@admin.register(SubscribedCompany)
class SubscribedCompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'website', 'employee_count', 'location')
    search_fields = ('name', 'website')
    list_filter = ('employee_count', 'location',)



@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'billing_cycle')



@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'subscribed_company')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    list_filter = ('subscribed_company',)
    


admin.site.register(Subscription)
admin.site.register(BillingHistory)













# Inline models for related objects
class CampaignLeadInline(admin.TabularInline):
    model = CampaignLead
    extra = 0
    fields = ('lead', 'is_converted', 'converted_at')

class MessageAssignmentInline(admin.TabularInline):
    model = MessageAssignment
    extra = 0
    fields = ('message', 'scheduled_at', 'responded')

# Custom filter for Campaign selection
class CampaignFilter(SimpleListFilter):
    title = 'campaign'
    parameter_name = 'campaign'

    def lookups(self, request, model_admin):
        campaigns = Campaign.objects.all()
        return [(c.id, c.name) for c in campaigns]

    def queryset(self, request, queryset):
        if self.value():
            return queryset
        return queryset

# Custom admin classes
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'campaign_count', 'landing_page_link')
    search_fields = ('name', 'description')
    
    def campaign_count(self, obj):
        return obj.campaign_set.count()
    campaign_count.short_description = 'Campaigns'
    
    def landing_page_link(self, obj):
        if obj.landing_page_url:
            return format_html('<a href="{}" target="_blank">View Landing Page</a>', obj.landing_page_url)
        return "-"
    landing_page_link.short_description = 'Landing Page'






@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('name', 'product', 'start_date', 'end_date', 'is_active', 'lead_count', 'conversion_rate')
    list_filter = ('is_active', 'product', 'start_date')
    search_fields = ('name', 'short_name', 'product__name')
    inlines = [CampaignLeadInline]
    
    def lead_count(self, obj):
        return obj.campaignlead_set.count()
    lead_count.short_description = 'Leads'
    
    def conversion_rate(self, obj):
        try:
            stats = obj.campaignstats
            return f"{stats.conversion_rate}%"
        except CampaignStats.DoesNotExist:
            return "0%"
    conversion_rate.short_description = 'Conversion'










@admin.register(Lead)
class LeadAdmin(ImportExportModelAdmin):
    resource_class = LeadResource
    list_display = ('full_name', 'email', 'company_name', 'lead_type', 'source', 'campaign_count')
    list_filter = ('lead_type', 'source', 'created_at')
    search_fields = ('full_name', 'email', 'company_name')
    fieldsets = (
        ('Owned By', {
            'fields': ('subscribed_company',)
        }),
        ('Personal Information', {
            'fields': ('full_name', 'first_name', 'last_name', 'position', 'email', 'phone_number', 'linkedin_profile')
        }),
        ('Company Information', {
            'fields': ('company_name', 'company_website', 'industry', 'employee_count')
        }),
        ('Lead Details', {
            'fields': ('source', 'lead_type')
        }),
    )
    
    def campaign_count(self, obj):
        return obj.campaignlead_set.count()
    campaign_count.short_description = 'Campaigns'
    
    def add_to_campaign(self, request, queryset):
        # Get the campaign ID from the request
        campaign_id = request.POST.get('campaign')
        
        if not campaign_id:
            self.message_user(request, "No campaign selected", level=messages.ERROR)
            return
            
        try:
            campaign = Campaign.objects.get(id=campaign_id)
            
            # Count how many leads were added
            added_count = 0
            already_exists_count = 0
            
            for lead in queryset:
                # Try to create the campaign lead, handle duplicates
                try:
                    CampaignLead.objects.create(campaign=campaign, lead=lead)
                    added_count += 1
                except Exception:  # Handle unique constraint violation
                    already_exists_count += 1
            
            # Show success message
            if added_count > 0:
                self.message_user(
                    request, 
                    f"Successfully added {added_count} leads to campaign '{campaign.name}'",
                    level=messages.SUCCESS
                )
            
            if already_exists_count > 0:
                self.message_user(
                    request,
                    f"{already_exists_count} leads were already in the campaign",
                    level=messages.WARNING
                )
                
        except Campaign.DoesNotExist:
            self.message_user(request, "Selected campaign does not exist", level=messages.ERROR)
        
    add_to_campaign.short_description = "Add selected leads to campaign"
    
    def changelist_view(self, request, extra_context=None):
        # Add campaigns to the context for the dropdown
        extra_context = extra_context or {}
        extra_context['campaigns'] = Campaign.objects.all()
        return super().changelist_view(request, extra_context=extra_context)

@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('lead_name', 'lead_email', 'joined_at', 'unsubscribed')
    list_filter = ('unsubscribed', 'joined_at')
    search_fields = ('lead__full_name', 'lead__email')
    
    def lead_name(self, obj):
        return obj.lead.full_name if obj.lead else "-"
    lead_name.short_description = 'Name'
    
    def lead_email(self, obj):
        return obj.lead.email if obj.lead else "-"
    lead_email.short_description = 'Email'






# Custom form for CampaignLead
class CampaignLeadForm(forms.ModelForm):
    class Meta:
        model = CampaignLead
        fields = '__all__'
    
    def clean(self):
        cleaned_data = super().clean()
        lead = cleaned_data.get('lead')
        campaign = cleaned_data.get('campaign')
        
        # Get filter values from POST data
        lead_type = self.data.get('lead_type')
        lead_source = self.data.get('lead_source')
        
        logger.warning(f"FORM VALIDATION: lead={lead}, lead_type={lead_type}, lead_source={lead_source}")
        
        # If filters are used, lead field is not required
        if lead_type or lead_source:
            self.fields['lead'].required = False
            if 'lead' in self._errors:
                del self._errors['lead']
            logger.warning("Using filters, lead field not required")
        elif not lead:
            # If no filters and no lead, raise validation error
            logger.warning("No filters and no lead, raising validation error")
            raise ValidationError({'lead': 'This field is required when not using filters.'})
        
        # Always require a campaign
        if not campaign:
            raise ValidationError({'campaign': 'This field is required.'})
        
        return cleaned_data

@admin.register(CampaignLead)
class CampaignLeadAdmin(admin.ModelAdmin):
    form = CampaignLeadForm
    list_display = ('lead', 'campaign', 'is_converted', 'link_count', 'converted_at', 'created_at')
    list_filter = ('is_converted', 'campaign', 'created_at')
    search_fields = ('lead__full_name', 'lead__email', 'campaign__name')
    inlines = [MessageAssignmentInline]
    
    def link_count(self, obj):
        """Count how many links this campaign lead has"""
        count = Link.objects.filter(campaign_lead=obj).count()
        if count > 0:
            return format_html('<a href="/admin/campaign/link/?campaign_lead__id__exact={}">{} links</a>', obj.id, count)
        return "0"
    link_count.short_description = 'Links'
    
    def add_view(self, request, form_url='', extra_context=None):
        # Add lead types and sources to the context
        extra_context = extra_context or {}
        extra_context['lead_types'] = dict(Lead.TYPE_CHOICES)
        extra_context['lead_sources'] = dict(Lead.SOURCE_CHOICES)
        
        # Use custom template
        self.change_form_template = 'admin/campaign/campaignlead/add_form.html'
        
        logger.warning("Rendering add_view with custom template")
        
        # Handle POST request
        if request.method == 'POST':
            lead_type = request.POST.get('lead_type')
            lead_source = request.POST.get('lead_source')
            campaign_id = request.POST.get('campaign')
            lead_id = request.POST.get('lead')
            is_converted = request.POST.get('is_converted') == 'on'
            converted_at = request.POST.get('converted_at')
            
            logger.warning(f"POST data: campaign={campaign_id}, lead_id={lead_id}, lead_type={lead_type}, lead_source={lead_source}")
            
            # Case 1: Using filters to add multiple leads
            if (lead_type or lead_source) and campaign_id:
                # Build query based on filters
                query = {}
                if lead_type:
                    query['lead_type'] = lead_type
                if lead_source:
                    query['source'] = lead_source
                
                logger.warning(f"Query filters: {query}")
                
                # Get all leads matching the filters
                leads = Lead.objects.filter(**query)
                logger.warning(f"Found {leads.count()} leads matching filters")
                
                if not leads.exists():
                    logger.warning("No leads match the selected filters")
                    messages.warning(request, "No leads match the selected filters.")
                else:
                    # Create campaign leads for each matching lead
                    campaign = Campaign.objects.get(id=campaign_id)
                    added_count = 0
                    already_exists_count = 0
                    
                    for lead in leads:
                        logger.warning(f"Processing lead: {lead.full_name} (ID: {lead.id})")
                        # Check if this lead is already in the campaign
                        if CampaignLead.objects.filter(campaign=campaign, lead=lead).exists():
                            already_exists_count += 1
                            logger.warning(f"Lead {lead.full_name} already exists in campaign")
                            continue
                        
                        try:
                            CampaignLead.objects.create(
                                campaign=campaign,
                                lead=lead,
                                is_converted=is_converted,
                                converted_at=converted_at if converted_at else None
                            )
                            added_count += 1
                            logger.warning(f"Successfully added lead {lead.full_name} to campaign")
                        except Exception as e:
                            logger.error(f"Error adding lead {lead.full_name}: {str(e)}")
                    
                    # Show messages
                    if added_count > 0:
                        success_msg = f"Successfully added {added_count} leads to campaign '{campaign.name}'"
                        messages.success(request, success_msg)
                        logger.warning(success_msg)
                    
                    if already_exists_count > 0:
                        warning_msg = f"{already_exists_count} leads were already in the campaign"
                        messages.warning(request, warning_msg)
                        logger.warning(warning_msg)
                    
                    # Redirect to the campaign lead list
                    return HttpResponseRedirect("../")
            
            # Case 2: Adding a single lead
            elif campaign_id and lead_id:
                logger.warning(f"Adding single lead: lead_id={lead_id}, campaign_id={campaign_id}")
                try:
                    campaign = Campaign.objects.get(id=campaign_id)
                    lead = Lead.objects.get(id=lead_id)
                    
                    # Check if this lead is already in the campaign
                    if CampaignLead.objects.filter(campaign=campaign, lead=lead).exists():
                        messages.warning(request, f"Lead '{lead.full_name}' is already in campaign '{campaign.name}'")
                        logger.warning(f"Lead {lead.full_name} already exists in campaign")
                    else:
                        # Create the campaign lead
                        CampaignLead.objects.create(
                            campaign=campaign,
                            lead=lead,
                            is_converted=is_converted,
                            converted_at=converted_at if converted_at else None
                        )
                        messages.success(request, f"Successfully added lead '{lead.full_name}' to campaign '{campaign.name}'")
                        logger.warning(f"Successfully added lead {lead.full_name} to campaign")
                    
                    # Redirect to the campaign lead list or to add another
                    if '_addanother' in request.POST:
                        return HttpResponseRedirect(".")
                    else:
                        return HttpResponseRedirect("../")
                except Campaign.DoesNotExist:
                    messages.error(request, "Selected campaign does not exist")
                    logger.error(f"Campaign with ID {campaign_id} does not exist")
                except Lead.DoesNotExist:
                    messages.error(request, "Selected lead does not exist")
                    logger.error(f"Lead with ID {lead_id} does not exist")
                except Exception as e:
                    messages.error(request, f"Error adding lead to campaign: {str(e)}")
                    logger.error(f"Error adding lead to campaign: {str(e)}")
        
        return super().add_view(request, form_url, extra_context)
    
    def save_model(self, request, obj, form, change):
        logger.warning(f"SAVE_MODEL called: change={change}")
        
        # For normal saves (not using filters), save normally
        super().save_model(request, obj, form, change)






@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'product', 'cta', 'message_preview')
    search_fields = ('subject', 'content', 'cta')
    
    def message_preview(self, obj):
        if len(obj.content) > 50:
            return obj.content[:50] + "..."
        return obj.content
    message_preview.short_description = 'Content Preview'








class LinkAdminForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make URL and utm_campaign not required in the form
        self.fields['url'].required = False
        self.fields['utm_campaign'].required = False
        
        # Update help text to be more clear
        self.fields['url'].help_text = "Will be auto-populated from campaign's product landing page if left empty"
        self.fields['utm_campaign'].help_text = "Will be auto-populated from campaign's short_name if left empty"
    
    def clean(self):
        cleaned_data = super().clean()
        campaign = cleaned_data.get('campaign')
        
        # Validate that campaign is selected if URL or utm_campaign is empty
        if not cleaned_data.get('url') and not campaign:
            self.add_error('campaign', 'Campaign is required when URL is not provided')
        
        if not cleaned_data.get('utm_campaign') and not campaign:
            self.add_error('campaign', 'Campaign is required when UTM Campaign is not provided')
        
        return cleaned_data

@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    form = LinkAdminForm
    list_display = ('url', 'campaign', 'campaign_lead', 'purpose', 'tracking_url', 'message_assignments_count', 'visit_count', 'visited_at')
    list_filter = ('campaign', 'purpose', 'visit_count')
    search_fields = ('url', 'utm_campaign', 'ref', 'description')
    
    def get_form(self, request, obj=None, **kwargs):
        """
        Override get_form to filter campaign_lead based on selected campaign
        """
        form = super().get_form(request, obj, **kwargs)
        
        # Get the campaign_id from the request or the object
        campaign_id = request.GET.get('campaign')
        
        # If we're in a POST request, get the campaign from the POST data
        if request.method == 'POST':
            campaign_id = request.POST.get('campaign')
        
        # If still no campaign_id but we have an object, use its campaign
        if not campaign_id and obj and obj.campaign:
            campaign_id = obj.campaign.id
            
        # Filter campaign_lead based on the campaign
        if campaign_id:
            form.base_fields['campaign_lead'].queryset = CampaignLead.objects.filter(campaign_id=campaign_id)
        else:
            form.base_fields['campaign_lead'].queryset = CampaignLead.objects.none()
            
        return form
    
    def tracking_url(self, obj):
        """Display the tracking URL with a copy button"""
        if obj.ref:
            # Use the existing get_redirect_url method
            redirect_url = obj.get_redirect_url()
            full_url = f"{settings.SITE_URL}{redirect_url}" if hasattr(settings, 'SITE_URL') else redirect_url
            return format_html('<a href="{0}" target="_blank">{0}</a>', full_url)
        return "-"
    tracking_url.short_description = 'Tracking URL'
    
    def message_assignments_count(self, obj):
        """Count how many message assignments use this link"""
        count = obj.message_assignments.count()
        if count > 0:
            return format_html('<a href="/admin/campaign/messageassignment/?url__id__exact={}">{} assignments</a>', obj.id, count)
        return "0"
    message_assignments_count.short_description = 'Used in Messages'
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('get-campaign-leads/', self.admin_site.admin_view(self.get_campaign_leads), name='get_campaign_leads'),
        ]
        return custom_urls + urls
    
    def get_campaign_leads(self, request):
        """AJAX view to get campaign leads for a campaign"""
        campaign_id = request.GET.get('campaign_id')
        if not campaign_id:
            return JsonResponse({'error': 'No campaign ID provided'}, status=400)
        
        # Get campaign leads
        campaign_leads = CampaignLead.objects.filter(campaign_id=campaign_id)
        leads_data = [{'id': cl.id, 'text': str(cl)} for cl in campaign_leads]
        
        return JsonResponse({'campaign_leads': leads_data})    
    
        
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['campaign_lead_filter_js'] = """
        <script type="text/javascript">
            (function($) {
                $(document).ready(function() {
                    // When campaign select changes, reload the page with the campaign parameter
                    $('#id_campaign').on('change', function() {
                        var campaignId = $(this).val();
                        var currentUrl = window.location.href;
                        
                        // Remove existing campaign parameter if any
                        currentUrl = currentUrl.replace(/[?&]campaign=\\d+/, '');
                        
                        // Add the new campaign parameter
                        if (campaignId) {
                            if (currentUrl.indexOf('?') > -1) {
                                currentUrl += '&campaign=' + campaignId;
                            } else {
                                currentUrl += '?campaign=' + campaignId;
                            }
                        }
                        
                        // Reload the page
                        window.location.href = currentUrl;
                    });
                });
            })(django.jQuery);
        </script>
        """
        return super().changelist_view(request, extra_context)
        
    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['campaign_lead_filter_js'] = """
        <script type="text/javascript">
            (function($) {
                $(document).ready(function() {
                    // Function to update campaign leads dropdown
                    function updateCampaignLeads(campaignId) {
                        if (!campaignId) {
                            // Clear the dropdown if no campaign is selected
                            var $campaignLeadSelect = $('#id_campaign_lead');
                            $campaignLeadSelect.empty();
                            $campaignLeadSelect.append('<option value="">---------</option>');
                            return;
                        }
                        
                        // Show loading indicator
                        $('#id_campaign_lead').prop('disabled', true);
                        
                        // Make AJAX request to get campaign leads
                        $.ajax({
                            url: '/admin/campaign/link/get-campaign-leads/',
                            data: {
                                'campaign_id': campaignId
                            },
                            dataType: 'json',
                            success: function(data) {
                                var $campaignLeadSelect = $('#id_campaign_lead');
                                $campaignLeadSelect.empty();
                                $campaignLeadSelect.append('<option value="">---------</option>');
                                
                                // Add options for each campaign lead
                                $.each(data.campaign_leads, function(i, item) {
                                    $campaignLeadSelect.append(
                                        $('<option></option>').val(item.id).text(item.text)
                                    );
                                });
                                
                                // Enable the dropdown
                                $campaignLeadSelect.prop('disabled', false);
                            },
                            error: function(xhr, status, error) {
                                console.error("Error loading campaign leads:", error);
                                // Enable the dropdown even on error
                                $('#id_campaign_lead').prop('disabled', false);
                            }
                        });
                    }
                    
                    // When campaign select changes, update campaign leads
                    $('#id_campaign').on('change', function() {
                        var campaignId = $(this).val();
                        updateCampaignLeads(campaignId);
                    });
                    
                    // Initial load if campaign is already selected
                    var initialCampaignId = $('#id_campaign').val();
                    if (initialCampaignId) {
                        updateCampaignLeads(initialCampaignId);
                    }
                });
            })(django.jQuery);
        </script>
        """
        return super().add_view(request, form_url, extra_context)
        
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['campaign_lead_filter_js'] = """
        <script type="text/javascript">
            (function($) {
                $(document).ready(function() {
                    // When campaign select changes, reload the page with the campaign parameter
                    $('#id_campaign').on('change', function() {
                        var campaignId = $(this).val();
                        var currentUrl = window.location.href;
                        
                        // Remove existing campaign parameter if any
                        currentUrl = currentUrl.replace(/[?&]campaign=\\d+/, '');
                        
                        // Add the new campaign parameter
                        if (campaignId) {
                            if (currentUrl.indexOf('?') > -1) {
                                currentUrl += '&campaign=' + campaignId;
                            } else {
                                currentUrl += '?campaign=' + campaignId;
                            }
                        }
                        
                        // Reload the page
                        window.location.href = currentUrl;
                    });
                });
            })(django.jQuery);
        </script>
        """
        return super().change_view(request, object_id, form_url, extra_context)

class MessageAssignmentAdminForm(forms.ModelForm):
    create_for_all_leads = forms.BooleanField(
        required=False,
        label="Create for all campaign leads",
        help_text="If checked, this message will be assigned to all leads in the selected campaign"
    )
    
    utm_source = forms.CharField(max_length=100, required=False, 
                                help_text="Source of the traffic (default: campaign)")
    utm_medium = forms.CharField(max_length=100, required=False, 
                               help_text="Marketing medium (default: email)")
    utm_term = forms.CharField(max_length=100, required=False, 
                             help_text="Keywords for paid search")
    utm_content = forms.CharField(max_length=100, required=False, 
                                help_text="Content identifier (default: email_[message_id])")
    
    description = forms.CharField(max_length=100, required=False, 
                                help_text="Optional description of this link's purpose")
    
    class Meta:
        model = MessageAssignment
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make campaign_lead not required in the form (we'll validate in clean)
        self.fields['campaign_lead'].required = False
        
        # If this is an existing object with a URL, populate UTM fields
        if self.instance and self.instance.pk and self.instance.url:
            self.fields['utm_source'].initial = self.instance.url.utm_source
            self.fields['utm_medium'].initial = self.instance.url.utm_medium
            self.fields['utm_term'].initial = self.instance.url.utm_term
            self.fields['utm_content'].initial = self.instance.url.utm_content
            self.fields['description'].initial = self.instance.url.description
            
        # If this is an existing message assignment, hide the create_for_all_leads field
        if self.instance and self.instance.pk:
            self.fields['create_for_all_leads'].widget = forms.HiddenInput()
            
    def clean(self):
        cleaned_data = super().clean()
        campaign_lead = cleaned_data.get('campaign_lead')
        create_for_all_leads = cleaned_data.get('create_for_all_leads')
        campaign = cleaned_data.get('campaign')
        
        # If creating for all leads, campaign is required
        if create_for_all_leads and not campaign:
            self.add_error('campaign', 'Please select a campaign when creating assignments for all leads')
            
        # If not creating for all leads, either campaign_lead or campaign is required
        if not create_for_all_leads and not campaign_lead and not campaign:
            self.add_error('campaign_lead', 'Either Campaign Lead or Campaign must be selected')
            
        return cleaned_data

@admin.register(MessageAssignment)
class MessageAssignmentAdmin(admin.ModelAdmin):
    form = MessageAssignmentAdminForm
    list_display = ('id', 'campaign_lead', 'message', 'link_info', 'scheduled_at', 'sent_at', 'responded', 'sent')
    list_filter = ('campaign', 'responded', 'scheduled_at', 'sent_at', 'sent')
    search_fields = ('campaign_lead__lead__full_name', 'message__subject')
    
    # Add a template for the add form
    add_form_template = 'admin/campaign/messageassignment/add_form.html'
    change_form_template = 'admin/campaign/messageassignment/change_form.html'
    
    fieldsets = (
        ('Message Assignment', {
            'fields': ('campaign', 'campaign_lead', 'message', 'create_for_all_leads', 'personlized_msg_tmp', 'personlized_msg_to_send', 'scheduled_at', 'sent', 'sent_at', 'responded', 'responded_content')
        }),
        ('Tracking Link Parameters', {
            'classes': ('collapse',),
            'description': 'Customize the tracking link for this message',
            'fields': ('utm_source', 'utm_medium', 'utm_term', 'utm_content', 'description')
        }),
    )
    
    actions = ['personalize_selected_messages', 'send_selected_messages']
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('get-campaign-leads/', self.admin_site.admin_view(self.get_campaign_leads), name='get_campaign_leads'),
            path('get-campaign-messages/', self.admin_site.admin_view(self.get_campaign_messages), name='get_campaign_messages'),
            path('<int:message_id>/personalize/', self.admin_site.admin_view(self.personalize_message), name='personalize_message'),
            path('<int:message_id>/send/', self.admin_site.admin_view(self.send_message), name='send_message'),
        ]
        return custom_urls + urls
    
    def get_campaign_leads(self, request):
        """AJAX view to get campaign leads for a campaign"""
        campaign_id = request.GET.get('campaign_id')
        if not campaign_id:
            return JsonResponse({'error': 'No campaign ID provided'}, status=400)
        
        # Get campaign leads
        campaign_leads = CampaignLead.objects.filter(campaign_id=campaign_id)
        leads_data = [{'id': cl.id, 'text': str(cl)} for cl in campaign_leads]
        
        return JsonResponse({'campaign_leads': leads_data})
    
    def get_campaign_messages(self, request):
        """AJAX view to get messages for a campaign's product"""
        campaign_id = request.GET.get('campaign_id')
        if not campaign_id:
            return JsonResponse({'error': 'No campaign ID provided'}, status=400)
        
        try:
            campaign = Campaign.objects.get(id=campaign_id)
            product = campaign.product
            messages = Message.objects.filter(product=product)
            messages_data = [{'id': m.id, 'text': str(m)} for m in messages]
            
            return JsonResponse({'messages': messages_data})
        except Campaign.DoesNotExist:
            return JsonResponse({'error': 'Campaign not found'}, status=404)
    
    def get_form(self, request, obj=None, **kwargs):
        """
        Override get_form to filter campaign_lead and message based on selected campaign
        """
        form = super().get_form(request, obj, **kwargs)
        
        # Get the campaign_id from the request or the object
        campaign_id = request.GET.get('campaign')
        
        # If we're in a POST request, get the campaign from the POST data
        if request.method == 'POST':
            campaign_id = request.POST.get('campaign')
        
        # If still no campaign_id but we have an object, use its campaign
        if not campaign_id and obj and obj.campaign:
            campaign_id = obj.campaign.id
            
        # Filter campaign_lead based on the campaign
        if campaign_id:
            form.base_fields['campaign_lead'].queryset = CampaignLead.objects.filter(campaign_id=campaign_id)
            
            # Filter messages based on the campaign's product
            try:
                campaign = Campaign.objects.get(id=campaign_id)
                form.base_fields['message'].queryset = Message.objects.filter(product=campaign.product)
            except Campaign.DoesNotExist:
                form.base_fields['message'].queryset = Message.objects.none()
        else:
            form.base_fields['campaign_lead'].queryset = CampaignLead.objects.none()
            form.base_fields['message'].queryset = Message.objects.all()
            
        return form
    
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['campaign_lead_filter_js'] = """
        <script type="text/javascript">
            (function($) {
                $(document).ready(function() {
                    // When campaign select changes, reload the page with the campaign parameter
                    $('#id_campaign').on('change', function() {
                        var campaignId = $(this).val();
                        var currentUrl = window.location.href;
                        
                        // Remove existing campaign parameter if any
                        currentUrl = currentUrl.replace(/[?&]campaign=\\d+/, '');
                        
                        // Add the new campaign parameter
                        if (campaignId) {
                            if (currentUrl.indexOf('?') > -1) {
                                currentUrl += '&campaign=' + campaignId;
                            } else {
                                currentUrl += '?campaign=' + campaignId;
                            }
                        }
                        
                        // Reload the page
                        window.location.href = currentUrl;
                    });
                });
            })(django.jQuery);
        </script>
        """
        return super().changelist_view(request, extra_context)
        
    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['campaign_lead_filter_js'] = """
        <script type="text/javascript">
            (function($) {
                $(document).ready(function() {
                    // Function to update campaign leads dropdown
                    function updateCampaignLeads(campaignId) {
                        if (!campaignId) {
                            // Clear the dropdown if no campaign is selected
                            var $campaignLeadSelect = $('#id_campaign_lead');
                            $campaignLeadSelect.empty();
                            $campaignLeadSelect.append('<option value="">---------</option>');
                            return;
                        }
                        
                        // Show loading indicator
                        $('#id_campaign_lead').prop('disabled', true);
                        
                        // Make AJAX request to get campaign leads
                        $.ajax({
                            url: '/admin/campaign/messageassignment/get-campaign-leads/',
                            data: {
                                'campaign_id': campaignId
                            },
                            dataType: 'json',
                            success: function(data) {
                                var $campaignLeadSelect = $('#id_campaign_lead');
                                $campaignLeadSelect.empty();
                                $campaignLeadSelect.append('<option value="">---------</option>');
                                
                                // Add options for each campaign lead
                                $.each(data.campaign_leads, function(i, item) {
                                    $campaignLeadSelect.append(
                                        $('<option></option>').val(item.id).text(item.text)
                                    );
                                });
                                
                                // Enable the dropdown
                                $campaignLeadSelect.prop('disabled', false);
                            },
                            error: function(xhr, status, error) {
                                console.error("Error loading campaign leads:", error);
                                console.error("Response:", xhr.responseText);
                                // Enable the dropdown even on error
                                $('#id_campaign_lead').prop('disabled', false);
                            }
                        });
                    }
                    
                    // Function to update messages dropdown
                    function updateMessages(campaignId) {
                        if (!campaignId) {
                            // Clear the dropdown if no campaign is selected
                            var $messageSelect = $('#id_message');
                            $messageSelect.empty();
                            $messageSelect.append('<option value="">---------</option>');
                            return;
                        }
                        
                        // Show loading indicator
                        $('#id_message').prop('disabled', true);
                        
                        // Make AJAX request to get messages for this campaign's product
                        $.ajax({
                            url: '/admin/campaign/messageassignment/get-campaign-messages/',
                            data: {
                                'campaign_id': campaignId
                            },
                            dataType: 'json',
                            success: function(data) {
                                var $messageSelect = $('#id_message');
                                $messageSelect.empty();
                                $messageSelect.append('<option value="">---------</option>');
                                
                                // Add options for each message
                                $.each(data.messages, function(i, item) {
                                    $messageSelect.append(
                                        $('<option></option>').val(item.id).text(item.text)
                                    );
                                });
                                
                                // Enable the dropdown
                                $messageSelect.prop('disabled', false);
                            },
                            error: function(xhr, status, error) {
                                console.error("Error loading messages:", error);
                                console.error("Response:", xhr.responseText);
                                // Enable the dropdown even on error
                                $('#id_message').prop('disabled', false);
                            }
                        });
                    }
                    
                    // When campaign select changes, update both dropdowns
                    $('#id_campaign').on('change', function() {
                        var campaignId = $(this).val();
                        updateCampaignLeads(campaignId);
                        updateMessages(campaignId);
                    });
                    
                    // Initial load if campaign is already selected
                    var initialCampaignId = $('#id_campaign').val();
                    if (initialCampaignId) {
                        updateCampaignLeads(initialCampaignId);
                        updateMessages(initialCampaignId);
                    }
                });
            })(django.jQuery);
        </script>
        """
        return super().add_view(request, form_url, extra_context)
        
    def change_view(self, request, object_id, form_url='', extra_context=None):
        obj = self.get_object(request, object_id)
        extra_context = extra_context or {}
        
        # Add JavaScript for dynamic dropdowns
        extra_context['campaign_lead_filter_js'] = """
        <script type="text/javascript">
            (function($) {
                $(document).ready(function() {
                    // Store initial values
                    var initialCampaignId = %s;
                    var initialCampaignLeadId = %s;
                    var initialMessageId = %s;
                    
                    // Function to update campaign leads dropdown
                    function updateCampaignLeads(campaignId, selectCampaignLeadId) {
                        if (!campaignId) {
                            // Clear the dropdown if no campaign is selected
                            var $campaignLeadSelect = $('#id_campaign_lead');
                            $campaignLeadSelect.empty();
                            $campaignLeadSelect.append('<option value="">---------</option>');
                            return;
                        }
                        
                        // Show loading indicator
                        $('#id_campaign_lead').prop('disabled', true);
                        
                        // Make AJAX request to get campaign leads
                        $.ajax({
                            url: '/admin/campaign/messageassignment/get-campaign-leads/',
                            data: {
                                'campaign_id': campaignId
                            },
                            dataType: 'json',
                            success: function(data) {
                                var $campaignLeadSelect = $('#id_campaign_lead');
                                $campaignLeadSelect.empty();
                                $campaignLeadSelect.append('<option value="">---------</option>');
                                
                                // Add options for each campaign lead
                                $.each(data.campaign_leads, function(i, item) {
                                    var option = $('<option></option>').val(item.id).text(item.text);
                                    
                                    // Select the option if it matches the initial value
                                    if (selectCampaignLeadId && item.id == selectCampaignLeadId) {
                                        option.attr('selected', 'selected');
                                    }
                                    
                                    $campaignLeadSelect.append(option);
                                });
                                
                                // Enable the dropdown
                                $campaignLeadSelect.prop('disabled', false);
                            },
                            error: function(xhr, status, error) {
                                console.error("Error loading campaign leads:", error);
                                console.error("Response:", xhr.responseText);
                                // Enable the dropdown even on error
                                $('#id_campaign_lead').prop('disabled', false);
                            }
                        });
                    }
                    
                    // Function to update messages dropdown
                    function updateMessages(campaignId, selectMessageId) {
                        if (!campaignId) {
                            // Clear the dropdown if no campaign is selected
                            var $messageSelect = $('#id_message');
                            $messageSelect.empty();
                            $messageSelect.append('<option value="">---------</option>');
                            return;
                        }
                        
                        // Show loading indicator
                        $('#id_message').prop('disabled', true);
                        
                        // Make AJAX request to get messages for this campaign's product
                        $.ajax({
                            url: '/admin/campaign/messageassignment/get-campaign-messages/',
                            data: {
                                'campaign_id': campaignId
                            },
                            dataType: 'json',
                            success: function(data) {
                                var $messageSelect = $('#id_message');
                                $messageSelect.empty();
                                $messageSelect.append('<option value="">---------</option>');
                                
                                // Add options for each message
                                $.each(data.messages, function(i, item) {
                                    var option = $('<option></option>').val(item.id).text(item.text);
                                    
                                    // Select the option if it matches the initial value
                                    if (selectMessageId && item.id == selectMessageId) {
                                        option.attr('selected', 'selected');
                                    }
                                    
                                    $messageSelect.append(option);
                                });
                                
                                // Enable the dropdown
                                $messageSelect.prop('disabled', false);
                            },
                            error: function(xhr, status, error) {
                                console.error("Error loading messages:", error);
                                console.error("Response:", xhr.responseText);
                                // Enable the dropdown even on error
                                $('#id_message').prop('disabled', false);
                            }
                        });
                    }
                    
                    // When campaign select changes, update both dropdowns
                    $('#id_campaign').on('change', function() {
                        var campaignId = $(this).val();
                        updateCampaignLeads(campaignId, null);
                        updateMessages(campaignId, null);
                    });
                    
                    // Set the initial campaign value
                    if (initialCampaignId) {
                        // Find the campaign option and select it
                        $('#id_campaign option[value="' + initialCampaignId + '"]').prop('selected', true);
                        
                        // Update the dependent dropdowns with initial values
                        updateCampaignLeads(initialCampaignId, initialCampaignLeadId);
                        updateMessages(initialCampaignId, initialMessageId);
                    }
                });
            })(django.jQuery);
        </script>
        """ % (
            obj.campaign_id or 'null',
            obj.campaign_lead_id or 'null',
            obj.message_id or 'null'
        )
        
        return super().change_view(request, object_id, form_url, extra_context)
    
    def link_info(self, obj):
        """Display link information if available"""
        if obj.url:
            visit_count = obj.url.visit_count
            visit_text = f"{visit_count} visit{'s' if visit_count != 1 else ''}"
            return format_html(
                '<a href="/admin/campaign/link/{}/change/">{}</a> ({}) - <a href="{}" target="_blank">View</a>',
                obj.url.id,
                obj.url.ref,
                visit_text,
                obj.url.get_redirect_url()
            )
        return "No link"
    link_info.short_description = 'Tracking Link'
    
    def save_model(self, request, obj, form, change):
        create_for_all_leads = form.cleaned_data.get('create_for_all_leads')
        campaign = form.cleaned_data.get('campaign')
        
        if create_for_all_leads and not change:
            # Get the message and campaign
            message = obj.message
            
            if not campaign:
                self.message_user(
                    request,
                    "Please select a campaign when creating assignments for all leads",
                    level=messages.ERROR
                )
                # Set flag to prevent default success message
                request._message_assignment_duplicate = True
                return
                
            # Get all campaign leads for this campaign that don't already have this message assigned
            campaign_leads = CampaignLead.objects.filter(campaign=campaign).exclude(
                id__in=MessageAssignment.objects.filter(campaign=campaign, message=message).values('campaign_lead_id')
            )
            
            if campaign_leads.exists():
                # Get UTM parameters from form
                utm_source = form.cleaned_data.get('utm_source')
                utm_medium = form.cleaned_data.get('utm_medium')
                utm_term = form.cleaned_data.get('utm_term')
                utm_content = form.cleaned_data.get('utm_content')
                description = form.cleaned_data.get('description')
                
                # Create a message assignment for each campaign lead
                created_count = 0
                for campaign_lead in campaign_leads:
                    # First create the link
                    link = Link(
                        campaign=campaign,
                        campaign_lead=campaign_lead,
                        url=campaign.product.landing_page_url,
                        utm_source=utm_source or "campaign",
                        utm_medium=utm_medium or "email",
                        utm_term=utm_term,
                        utm_content=utm_content,
                        description=description
                    )
                    link.save()
                    
                    # Then create the message assignment with the link already set
                    # This prevents the MessageAssignment.save() method from creating another link
                    message_assignment = MessageAssignment(
                        campaign=campaign,
                        campaign_lead=campaign_lead,
                        message=message,
                        personlized_msg_tmp=obj.personlized_msg_tmp,
                        scheduled_at=obj.scheduled_at,
                        url=link  # Set the link here to prevent auto-creation
                    )
                    
                    # Use the model's save method directly to bypass any custom save logic
                    # that might create additional links
                    self.model.save(message_assignment)

                    if not message_assignment.personlized_msg_tmp:
                        message_assignment.personlized_msg_tmp = message_assignment.get_personalized_content_tmp()
                        message_assignment.save(update_fields=['personlized_msg_tmp'])
                    
                    created_count += 1
                
                # Show a success message
                self.message_user(
                    request, 
                    f"Created {created_count} message assignments for campaign leads in '{campaign.name}'",
                    level=messages.SUCCESS
                )
                
                # Set flag to prevent default success message
                request._message_assignment_duplicate = True
                
                # Redirect to the message assignment list
                from django.http import HttpResponseRedirect
                return HttpResponseRedirect("../")
            else:
                # No campaign leads found
                self.message_user(
                    request,
                    f"No campaign leads found for campaign '{campaign.name}'",
                    level=messages.WARNING
                )
                # Set flag to prevent default success message
                request._message_assignment_duplicate = True
                return
        
        # Normal save for a single message assignment
        if not change:


            # Check if this campaign lead already has this message assigned
            if obj.campaign_lead and obj.message and MessageAssignment.objects.filter(
                campaign_lead=obj.campaign_lead, 
                message=obj.message
            ).exists():
                self.message_user(
                    request,
                    f"Lead '{obj.campaign_lead.lead}' already has message '{obj.message.subject}' assigned",
                    level=messages.WARNING
                )
                # Set an attribute on the request to indicate we've handled this
                request._message_assignment_duplicate = True
                return
            
            # Get UTM parameters from form
            utm_source = form.cleaned_data.get('utm_source')
            utm_medium = form.cleaned_data.get('utm_medium')
            utm_term = form.cleaned_data.get('utm_term')
            utm_content = form.cleaned_data.get('utm_content')
            description = form.cleaned_data.get('description')
            
            # Create link first if we have a campaign lead
            if obj.campaign_lead:
                # Create new link
                link = Link(
                    campaign=obj.campaign_lead.campaign,
                    campaign_lead=obj.campaign_lead,
                    url=obj.campaign_lead.campaign.product.landing_page_url,
                    utm_source=utm_source or "campaign",
                    utm_medium=utm_medium or "email",
                    utm_term=utm_term,
                    utm_content=utm_content or f"email_new",  # Will be updated after save
                    description=description
                )
                link.save()
                
                # Attach link to message assignment
                obj.url = link
            
            # Now save the object to get an ID
            super().save_model(request, obj, form, change)
            
            # Update the link's utm_content with the message assignment ID if needed
            if obj.url and not utm_content:
                obj.url.utm_content = f"email_{obj.id}"
                obj.url.save()
            
            # Generate personalized content with the link
            if not obj.personlized_msg_tmp:
                obj.personlized_msg_tmp = obj.get_personalized_content_tmp()
                obj.save(update_fields=['personlized_msg_tmp'])
        else:
            # For existing assignments, just update
            super().save_model(request, obj, form, change)
            
            # Update the link if it exists
            if obj.url:
                link = obj.url
                utm_source = form.cleaned_data.get('utm_source')
                utm_medium = form.cleaned_data.get('utm_medium')
                utm_term = form.cleaned_data.get('utm_term')
                utm_content = form.cleaned_data.get('utm_content')
                description = form.cleaned_data.get('description')
                
                if utm_source:
                    link.utm_source = utm_source
                if utm_medium:
                    link.utm_medium = utm_medium
                if utm_term:
                    link.utm_term = utm_term
                if utm_content:
                    link.utm_content = utm_content
                if description:
                    link.description = description
                
                link.save()

    def response_add(self, request, obj, post_url_continue=None):
        # If we've marked this as a duplicate, redirect without the success message
        if hasattr(request, '_message_assignment_duplicate') and request._message_assignment_duplicate:
            from django.http import HttpResponseRedirect
            return HttpResponseRedirect("../")
        
        # Otherwise, proceed with the default behavior
        return super().response_add(request, obj, post_url_continue)
    
    def personalize_message(self, request, message_id):
        """View to personalize a single message using Celery"""
        try:
            # Check if the message assignment exists
            message_assignment = self.model.objects.get(id=message_id)
            
            # Schedule the Celery task
            from campaign.tasks import personalize_message_task
            task = personalize_message_task.delay(message_id)
            
            self.message_user(
                request, 
                f"Scheduled personalization task (ID: {task.id}) for {message_assignment.campaign_lead}",
                level=messages.SUCCESS
            )
                    
        except self.model.DoesNotExist:
            self.message_user(request, f"Message assignment with ID {message_id} does not exist", level=messages.ERROR)
        except Exception as e:
            self.message_user(request, f"Error scheduling personalization task: {str(e)}", level=messages.ERROR)
            
        # Redirect back to the change page
        return HttpResponseRedirect(f"../../../campaign/messageassignment/{message_id}/change/")

    def personalize_selected_messages(self, request, queryset):
        """Action to personalize multiple messages using Celery"""
        try:
            # Schedule a task for each message assignment
            from campaign.tasks import personalize_message_task
            count = 0
            for message_assignment in queryset:
                personalize_message_task.delay(message_assignment.id)
                count += 1
            
            self.message_user(
                request, 
                f"Scheduled personalization tasks for {count} messages",
                level=messages.SUCCESS
            )
        except Exception as e:
            self.message_user(request, f"Error scheduling personalization tasks: {str(e)}", level=messages.ERROR)
    
    personalize_selected_messages.short_description = "Personalize selected messages with AI"
    
    def send_message(self, request, message_id):
        """View to send an email for a single message using Celery"""
        try:
            # Check if the message assignment exists
            message_assignment = self.model.objects.get(id=message_id)
            
            # Check if it has personalized content and hasn't been sent
            if not message_assignment.personlized_msg_to_send:
                self.message_user(request, f"Message assignment ID {message_id} has no personalized content", level=messages.ERROR)
                return HttpResponseRedirect(f"../../../campaign/messageassignment/{message_id}/change/")
                
            if message_assignment.sent:
                self.message_user(request, f"Message assignment ID {message_id} has already been sent", level=messages.WARNING)
                return HttpResponseRedirect(f"../../../campaign/messageassignment/{message_id}/change/")
            
            # Schedule the Celery task
            from campaign.tasks import send_email_task
            task = send_email_task.delay(message_id)
            
            self.message_user(
                request, 
                f"Scheduled email sending task (ID: {task.id}) for {message_assignment.campaign_lead.lead.email}",
                level=messages.SUCCESS
            )
                
        except self.model.DoesNotExist:
            self.message_user(request, f"Message assignment with ID {message_id} does not exist", level=messages.ERROR)
        except Exception as e:
            self.message_user(request, f"Error scheduling email sending task: {str(e)}", level=messages.ERROR)
        
        # Redirect back to the change page
        return HttpResponseRedirect(f"../../../campaign/messageassignment/{message_id}/change/")

    def send_selected_messages(self, request, queryset):
        """Action to send emails for multiple messages using Celery"""
        try:
            # Filter to only include personalized messages that haven't been sent
            queryset = queryset.filter(
                personlized_msg_to_send__isnull=False,
                personlized_msg_to_send__gt='',
                sent=False
            )
            
            if not queryset.exists():
                self.message_user(
                    request, 
                    "No messages selected that are personalized and not yet sent",
                    level=messages.WARNING
                )
                return
                
            # Schedule a task for each message assignment
            from campaign.tasks import send_email_task
            count = 0
            for message_assignment in queryset:
                send_email_task.delay(message_assignment.id)
                count += 1
            
            self.message_user(
                request, 
                f"Scheduled email sending tasks for {count} messages",
                level=messages.SUCCESS
            )
        except Exception as e:
            self.message_user(request, f"Error scheduling email sending tasks: {str(e)}", level=messages.ERROR)
    
    send_selected_messages.short_description = "Send emails for selected messages"
    
    # Add a button to the change form
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_personalize_button'] = True
        return super().change_view(request, object_id, form_url, extra_context)
