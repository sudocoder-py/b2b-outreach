from django.db import models
from django.conf import settings



class Feedback(models.Model):
    SATISFACTION_SCALE = [(i, str(i)) for i in range(1, 11)]
    EASE_SCALE = [(i, str(i)) for i in range(1, 11)]
    USEFULNESS_SCALE = [(i, str(i)) for i in range(1, 11)]
    RECOMMENDATION_SCALE = [(i, str(i)) for i in range(0, 11)]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="feedbacks")

    # Overall
    satisfaction = models.IntegerField(choices=SATISFACTION_SCALE)
    satisfaction_comment = models.TextField(blank=True, null=True)

    # Onboarding
    ease_of_onboarding = models.IntegerField(choices=EASE_SCALE)
    onboarding_comment = models.TextField(blank=True, null=True)

    # Clarity
    setup_confusion = models.TextField(blank=True, null=True)

    # Value
    met_expectations = models.BooleanField()  # Yes/No
    expectations_comment = models.TextField(blank=True, null=True)
    usefulness = models.IntegerField(choices=USEFULNESS_SCALE)

    # Improvement
    change_one_thing = models.TextField(blank=True, null=True)

    # Future fit
    no_brainer_feature = models.TextField(blank=True, null=True)

    # NPS
    recommendation = models.IntegerField(choices=RECOMMENDATION_SCALE)
    
    is_approved_to_share = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback #{self.id} (Satisfaction {self.satisfaction})"


class QuickFeedback(models.Model):
    EXPERIENCE_CHOICES = [
        ('positive', '👍 Positive'),
        ('negative', '👎 Negative'),
    ]
    RECOMMENDATION_SCALE = [(i, str(i)) for i in range(0, 11)]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="quick_feedbacks")

    experience = models.CharField(max_length=10, choices=EXPERIENCE_CHOICES)
    comment = models.TextField(blank=True, null=True)
    recommendation = models.IntegerField(choices=RECOMMENDATION_SCALE, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"QuickFeedback #{self.id} ({self.experience})"


class FeatureRequest(models.Model):
    PRIORITY_CHOICES = [
        ('nice', 'Nice to have'),
        ('important', 'Important'),
        ('critical', 'Critical'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="feature_requests")

    title = models.CharField(max_length=255)  # Short idea
    description = models.TextField()          # What it should do
    reason = models.TextField(blank=True, null=True)  # Why is it important
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, blank=True, null=True)
    workaround = models.TextField(blank=True, null=True)

    is_approved_to_share = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"FeatureRequest #{self.id}: {self.title}"




class FeedbackUpvote(models.Model):
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE, related_name="upvotes")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('feedback', 'user')  # one vote per user

    def __str__(self):
        return f"Upvote by {self.user} on Feedback #{self.feedback.id}"



class FeatureRequestUpvote(models.Model):
    feature_request = models.ForeignKey(FeatureRequest, on_delete=models.CASCADE, related_name="upvotes")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('feature_request', 'user')

    def __str__(self):
        return f"Upvote by {self.user} on FeatureRequest #{self.feature_request.id}"