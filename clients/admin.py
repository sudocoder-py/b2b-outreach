from django.contrib import admin
from .models import Plan, Subscription, BillingHistory, CustomUser, SubscribedCompany, Product, EmailAccount
from django.utils.html import format_html



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



@admin.register(EmailAccount)
class EmailAccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'connection_type', 'status', 'emails_sent', 'daily_limit')
    search_fields = ('email',)
    list_filter = ('connection_type', 'status',)
    
    
