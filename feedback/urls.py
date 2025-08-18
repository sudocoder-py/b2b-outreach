from django.urls import path
from . import views



urlpatterns = [
    path('', views.feedback_view, name='feedback'),
    path('analytics/', views.feedback_analytics_view, name='feedback_analytics'),
    path('feature-request/analytics/', views.feature_request_analytics_view, name='feature_request_analytics'),

    # API endpoints
    path('api/analytics/', views.FeedbackAnalyticsAPIView.as_view(), name='feedback_analytics_api'),
    path('api/feature-request/analytics/', views.FeatureRequestAnalyticsAPIView.as_view(), name='feature_request_analytics_api'),

    path('api/quick-feedback/', views.QuickFeedbackAPIView.as_view(), name='quick_feedback_api'),
    path('api/feature-request/', views.FeatureRequestAPIView.as_view(), name='feature_request_api'),
    path('api/main-feedback/', views.FeedbackAPIView.as_view(), name='main_feedback_api'),
]