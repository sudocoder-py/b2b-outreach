from django.urls import path
from . import views



urlpatterns = [
    path('', views.feedback_view, name='feedback'),
    path('analytics/', views.feedback_analytics_view, name='feedback_analytics'),
    path('feature-request/analytics/', views.feature_request_analytics_view, name='feature_request_analytics'),

    # API endpoints
    path('api/analytics/', views.FeedbackAnalyticsAPIView.as_view(), name='feedback_analytics_api'),
    path('api/feature-request/analytics/', views.FeatureRequestAnalyticsAPIView.as_view(), name='feature_request_analytics_api'),
]