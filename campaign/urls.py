from django.urls import path
from . import views

urlpatterns = [
    path('redirect/<str:ref_code>/', views.redirect_and_track, name='redirect_and_track_emails'),
    path('leads/<int:pk>/', views.leads_view, name='leads_view'),
    path('leads/lists/', views.leads_lists, name='leads_lists'),
    path('leads/all/', views.show_all_leads_view, name='show_all_leads'),
    path('view-list/', views.campaign_view_list, name='campaign_view_list'),
    path('leads/add/<int:pk>/', views.add_leads, name='add_leads'),
    path('campaigns/new/', views.create_campaign_view, name='create_campaign'),
    path('dashboard/<int:pk>/', views.campaign_dashboard, name='campaign_dashboard'),
    path('campaign-leads/<int:pk>/', views.campaign_leads, name='campaign_leads'),
    path('campaign-leads/<int:pk>/filter', views.campaign_leads_filter, name='campaign_leads_filter'),
    path('campaign-sequence/<int:pk>/', views.campaign_sequence, name='campaign_sequence'),
    path('message/assignments/<int:message_id>/', views.campaign_sequence_message_assignments, name='campaign_sequence_message'),
    path('campaign-scheduele/<int:pk>/', views.campaign_scheduele, name='campaign_scheduele'),
    path('campaign-options/<int:pk>/', views.campaign_options, name='campaign_options'),

    # New navigation pages
    path('products/', views.products_view, name='products'),
    #path('email-accounts/', views.email_accounts_view, name='email_accounts'),
    path('messages/', views.messages_view, name='messages'),
    path('messages/edit/<int:pk>/', views.messages_edit_view, name='messages_edit'),
    path('messages/add/', views.messages_add_view, name='messages_add'),
    path('links/', views.links_view, name='links'),
    path('overall-dashboard/', views.overall_dashboard_view, name='overall_dashboard'),
    path('feedback/', views.feedback_view, name='feedback'),
    path('account-settings/', views.account_settings_view, name='account_settings'),
]

