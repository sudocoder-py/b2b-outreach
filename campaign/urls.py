from django.urls import path
from . import views

urlpatterns = [
    path('redirect/<str:ref_code>/', views.redirect_and_track, name='redirect_and_track_emails'),
    path('dashboard-test-not-functional/', views.dashboard_non_functional, name='dashboard_non_functional'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('leads/', views.leads_view, name='leads_view'),
    path('view-list/', views.campaign_view_list, name='campaign_view_list'),
    path('dashboard/<int:pk>', views.campaign_dashboard, name='campaign_dashboard'),
    path('campaign-leads/<int:pk>', views.campaign_leads, name='campaign_leads'),
    path('campaign-leads/<int:pk>/filter', views.campaign_leads_filter, name='campaign_leads_filter'),
    path('campaign-sequence/<int:pk>', views.campaign_sequence, name='campaign_sequence'),
    path('campaign-scheduele/<int:pk>', views.campaign_scheduele, name='campaign_scheduele'),
    path('campaign-options/<int:pk>', views.campaign_options, name='campaign_options'),

    # New navigation pages
    path('products/', views.products_view, name='products'),
    path('email-accounts/', views.email_accounts_view, name='email_accounts'),
    path('messages/', views.messages_view, name='messages'),
    path('links/', views.links_view, name='links'),
    path('overall-dashboard/', views.overall_dashboard_view, name='overall_dashboard'),
    path('feedback/', views.feedback_view, name='feedback'),
    path('account-settings/', views.account_settings_view, name='account_settings'),
]

