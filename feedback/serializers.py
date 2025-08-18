from rest_framework import serializers
from .models import Feedback, FeatureRequest


class FeedbackAnalyticsSerializer(serializers.ModelSerializer):
    upvotes = serializers.SerializerMethodField()

    class Meta:
        model = Feedback
        fields = ['id', 'satisfaction', 'satisfaction_comment', 'ease_of_onboarding',
                  'onboarding_comment', 'setup_confusion', 'met_expectations',
                  'expectations_comment', 'usefulness', 'change_one_thing',
                  'no_brainer_feature', 'recommendation', 'upvotes']

    def get_upvotes(self, obj):
        return obj.upvotes.count()



class FeatureRequestAnalyticsSerializer(serializers.ModelSerializer):
    upvotes = serializers.SerializerMethodField()

    class Meta:
        model = FeatureRequest
        fields = ['id', 'title', 'description', 'reason', 'priority', 'workaround', 'upvotes']

    def get_upvotes(self, obj):
        return obj.upvotes.count()
