from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', views.ProductRetrieveUpdateDestroyView.as_view(), name='product-detail'),
    
    path('email-accounts/', views.EmailAccountListCreateView.as_view(), name='email-account-list-create'),
    path('email-accounts/<int:pk>/', views.EmailAccountRetrieveUpdateDestroyView.as_view(), name='email-account-detail'),

    path('campaigns/', views.CampaignListCreateView.as_view(), name='campaign-list-create'),
    path('campaigns/<int:pk>/', views.CampaignRetrieveUpdateDestroyView.as_view(), name='campaign-detail'),

    path('messages/', views.MessageListCreateView.as_view(), name='message-list-create'),
    path('messages/<int:pk>/', views.MessageRetrieveUpdateDestroyView.as_view(), name='message-detail'),    
    
    path('leads/lists/', views.LeadListListCreateView.as_view(), name='lead-list-list-create'),
    path('leads/lists/<int:pk>/', views.LeadListRetrieveUpdateDestroyView.as_view(), name='lead-list-detail'),
]
