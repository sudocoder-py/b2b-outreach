from rest_framework import serializers
from clients.models import Product, EmailAccount
from campaign.models import Campaign, Message, MessageAssignment, LeadList, Lead, Schedule, CampaignOptions


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class EmailAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailAccount
        fields = '__all__'

class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class MessageAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageAssignment
        fields = '__all__'


class LeadListSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadList
        fields = '__all__'


class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = '__all__'   


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__' 


class CampaignOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignOptions
        fields = '__all__'