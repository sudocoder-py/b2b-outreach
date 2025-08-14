from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Plan, Subscription, BillingHistory, CustomUser, SubscribedCompany, Product, EmailAccount
from django.utils.html import format_html


class CustomUserCreationForm(UserCreationForm):
    """Custom form for creating users with additional fields"""
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name', 'subscribed_company')


class CustomUserChangeForm(UserChangeForm):
    """Custom form for changing users with additional fields"""
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = UserChangeForm.Meta.fields


@admin.register(SubscribedCompany)
class SubscribedCompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'website', 'employee_count', 'location')
    search_fields = ('name', 'website')
    list_filter = ('employee_count', 'location',)



@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'billing_cycle')



@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Use custom forms
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    # Display fields in the list view
    list_display = ('username', 'email', 'first_name', 'last_name', 'subscribed_company', 'is_staff', 'is_active')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    list_filter = ('subscribed_company', 'is_staff', 'is_active', 'is_superuser')

    # Fields to display when editing an existing user
    fieldsets = UserAdmin.fieldsets + (
        ('Company Information', {'fields': ('subscribed_company',)}),
    )

    # Fields to display when adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
        ('Personal Information', {
            'fields': ('email', 'first_name', 'last_name'),
        }),
        ('Company Information', {
            'fields': ('subscribed_company',),
        }),
    )
    


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
    
    
