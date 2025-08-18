from django.shortcuts import redirect, get_object_or_404, render

from rest_framework import generics
from .models import Feedback, QuickFeedback, FeatureRequest
from .serializers import FeedbackAnalyticsSerializer, FeatureRequestAnalyticsSerializer, QuickFeedbackSerializer,  FeatureRequestSerializer, FeedbackSerializer







def feedback_view(request):
    """Feedback and feature requests page"""
    return render(request, "app/feedback/feedback.html")





def feedback_analytics_view(request):
    """Public feedback analytics page"""
    # Only approved feedback
    feedbacks = Feedback.objects.filter(is_approved_to_share=True).order_by('-id')  # newest first
    # Annotate upvote counts
    feedbacks_with_upvotes = [
        {
            "feedback": f,
            "upvotes": f.upvotes.count()
        } for f in feedbacks
    ]

    context = {
        "feedbacks_with_upvotes": feedbacks_with_upvotes,
    }
    return render(request, "app/feedback/feedback-analytics.html", context)


def feature_request_analytics_view(request):
    """Public feature request analytics page"""
    # Only approved feature requests
    requests = FeatureRequest.objects.filter(is_approved_to_share=True).order_by('-id')
    requests_with_upvotes = [
        {
            "request": r,
            "upvotes": r.upvotes.count()
        } for r in requests
    ]

    context = {
        "requests_with_upvotes": requests_with_upvotes,
    }
    return render(request, "app/feedback/feature-request-analytics.html", context)








# drf API views
class FeedbackAnalyticsAPIView(generics.ListAPIView):
    """
    Public API for approved feedback with upvotes
    """
    queryset = Feedback.objects.filter(is_approved_to_share=True)
    serializer_class = FeedbackAnalyticsSerializer


class FeatureRequestAnalyticsAPIView(generics.ListAPIView):
    """
    Public API for approved feature requests with upvotes
    """
    queryset = FeatureRequest.objects.filter(is_approved_to_share=True)
    serializer_class = FeatureRequestAnalyticsSerializer




class QuickFeedbackAPIView(generics.CreateAPIView):
    """
    API for quick feedback
    """
    queryset = QuickFeedback.objects.all()
    serializer_class = QuickFeedbackSerializer


class FeatureRequestAPIView(generics.CreateAPIView):
    """
    API for feature requests
    """
    queryset = FeatureRequest.objects.all()
    serializer_class = FeatureRequestSerializer


class FeedbackAPIView(generics.CreateAPIView):
    """
    API for feedback
    """
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer



