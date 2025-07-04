from django.urls import path
from .views import CampaignListCreateView, CampaignRetrieveUpdateDestroyView, MessageListCreateView, MessageRetrieveUpdateDestroyView, ProductListCreateView, ProductRetrieveUpdateDestroyView, EmailAccountListCreateView, EmailAccountRetrieveUpdateDestroyView

urlpatterns = [
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductRetrieveUpdateDestroyView.as_view(), name='product-detail'),
    
    path('email-accounts/', EmailAccountListCreateView.as_view(), name='email-account-list-create'),
    path('email-accounts/<int:pk>/', EmailAccountRetrieveUpdateDestroyView.as_view(), name='email-account-detail'),

    path('campaigns/', CampaignListCreateView.as_view(), name='campaign-list-create'),
    path('campaigns/<int:pk>/', CampaignRetrieveUpdateDestroyView.as_view(), name='campaign-detail'),

    path('messages/', MessageListCreateView.as_view(), name='message-list-create'),
    path('messages/<int:pk>/', MessageRetrieveUpdateDestroyView.as_view(), name='message-detail'),      
]
