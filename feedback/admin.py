from django.contrib import admin
from .models import Feedback, QuickFeedback, FeatureRequest




@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'satisfaction', 'ease_of_onboarding', 'setup_confusion', 'met_expectations', 'usefulness', 'is_approved_to_share', 'upvote_count', 'created_at')
    search_fields = ('user__username', 'user__email')
    list_filter = ('satisfaction', 'ease_of_onboarding', 'setup_confusion', 'usefulness', 'recommendation', 'is_approved_to_share', 'created_at')
    actions = ['approve_selected', 'disapprove_selected']

    def upvote_count(self, obj):
        return obj.upvotes.count()
    upvote_count.short_description = "Upvotes"

    def approve_selected(self, request, queryset):
        queryset.update(is_approved_to_share=True)
    approve_selected.short_description = "Approve selected requests"

    def disapprove_selected(self, request, queryset):
        queryset.update(is_approved_to_share=False)
    disapprove_selected.short_description = "Disapprove selected requests"






@admin.register(QuickFeedback)
class QuickFeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'experience', 'comment', 'recommendation', 'created_at')
    search_fields = ('user__username', 'user__email')
    list_filter = ('experience', 'recommendation', 'created_at')
    



@admin.register(FeatureRequest)
class FeatureRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'reason', 'priority', 'is_approved_to_share', 'upvote_count', 'created_at')
    search_fields = ('user__username', 'user__email', 'title')
    list_filter = ('priority', 'is_approved_to_share', 'created_at')
    actions = ['approve_selected', 'disapprove_selected']

    def upvote_count(self, obj):
        return obj.upvotes.count()
    upvote_count.short_description = "Upvotes"

    def approve_selected(self, request, queryset):
        queryset.update(is_approved_to_share=True)
    approve_selected.short_description = "Approve selected feedback"

    def disapprove_selected(self, request, queryset):
        queryset.update(is_approved_to_share=False)
    disapprove_selected.short_description = "Disapprove selected feedback"

