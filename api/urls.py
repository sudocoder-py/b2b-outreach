from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', views.ProductRetrieveUpdateDestroyView.as_view(), name='product-detail'),
    
    path('email-accounts/', views.EmailAccountListCreateView.as_view(), name='email-account-list-create'),
    path('email-accounts/<int:pk>/', views.EmailAccountRetrieveUpdateDestroyView.as_view(), name='email-account-detail'),
    path('email-accounts/<int:pk>/test-connection/', views.test_email_account_connection, name='email-account-test-connection'),

    path('campaigns/', views.CampaignListCreateView.as_view(), name='campaign-list-create'),
    path('campaigns/<int:pk>/', views.CampaignRetrieveUpdateDestroyView.as_view(), name='campaign-detail'),
    
    path('campaigns/<int:pk>/launch/', views.launch_campaign, name='campaign-launch'),
    path('campaigns/<int:pk>/status/', views.campaign_launch_status, name='campaign-launch-status'),

    path('messages/', views.MessageListCreateView.as_view(), name='message-list-create'),
    path('messages/<int:pk>/', views.MessageRetrieveUpdateDestroyView.as_view(), name='message-detail'),    

    path('message-assignments/', views.MessageAssignmentListCreateView.as_view(), name='message-assignment-list-create'),
    path('message-assignments/<int:pk>/', views.MessageAssignmentRetrieveUpdateDestroyView.as_view(), name='message-assignment-detail'),
    path('message-assignments/bulk-create/', views.MessageAssignmentBulkCreateView.as_view(), name='message-assignment-bulk-create'),
    path('message/assignments/details/<int:message_id>/', views.campaign_sequence_message_assignments, name='campaign_sequence_message'),
    path("message-assignments/bulk-delete-by-message/", views.delete_assignments_by_message, name="delete_assignments_by_message"),
    path('message-assignments/<int:assignment_id>/mark-replied/', views.mark_assignment_as_replied, name='mark-assignment-replied'),

    
    path('leads/lists/', views.LeadListCreateView.as_view(), name='lead-list-list-create'),
    path('leads/lists/<int:pk>/', views.LeadListRetrieveUpdateDestroyView.as_view(), name='lead-list-detail'),
    path('leads/lists/<int:pk>/assign/', views.LeadListViewSet.as_view({'patch': 'assign_campaign'}), name='lead-list-assign-campaign'),
    path('leads/lists/<int:pk>/unassign/', views.LeadListViewSet.as_view({'patch': 'unassign_campaign'}), name='lead-list-unassign-campaign'),

    path("lead/fields/", views.LeadFieldsView.as_view(), name='lead-fields'),
    path('leads/', views.LeadCreateView.as_view(), name='lead-create'),
    path('leads/<int:pk>/', views.LeadRetrieveUpdateDestroyView.as_view(), name='lead-detail'),
    path('leads/bulk-create/', views.BulkLeadCreateView.as_view(), name='bulk-lead-create'),
    path('leads/bulk-delete/', views.BulkLeadDeleteView.as_view(), name='bulk-lead-delete'),
    path('leads/move-to-list/', views.MoveLeadsToListView.as_view(), name='move-leads-to-list'),

    path('schedule/', views.ScheduleListCreateView.as_view(), name='schedule-list-create'),
    path('schedule/<int:pk>/', views.ScheduleRetrieveUpdateDestroyView.as_view(), name='schedule-detail'),

    path('campaign-options/', views.CampaignOptionsListCreateView.as_view(), name='campaign-options-list-create'),
    path('campaign-options/<int:pk>/', views.CampaignOptionsRetrieveUpdateDestroyView.as_view(), name='campaign-options-detail'),

    path('campaign-stats/', views.CampaignStatsListCreateView.as_view(), name='campaign-options-list-create'),
    path('campaign-stats/<int:pk>/', views.CampaignStatsRetrieveUpdateDestroyView.as_view(), name='campaign-options-detail'),
    path('campaigns/<int:campaign_id>/update-opportunity-value/', views.update_opportunity_value, name='update-opportunity-value'),
    path('refresh-daily-stats/', views.refresh_campaign_daily_stats, name='refresh-daily-stats'),



    path('inngest/launch/test/', views.launch_inggest_test, name='launch_inggest_test'),
]
