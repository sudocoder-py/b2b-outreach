from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from clients.models import Product, EmailAccount, CustomUser, SubscribedCompany, Plan, Subscription, BillingHistory
from campaign.models import Campaign, CampaignStats, Message, MessageAssignment, LeadList, Lead, Schedule, CampaignOptions


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
        validators = []


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__' 


class CampaignOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignOptions
        fields = '__all__'


class CampaignStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignStats
        fields = '__all__'


# Authentication Serializers
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            # Try to find user by email
            try:
                user = CustomUser.objects.get(email=email)
                username = user.username
            except CustomUser.DoesNotExist:
                raise serializers.ValidationError("Invalid email or password.")

            # Authenticate with username
            user = authenticate(username=username, password=password)

            if not user:
                raise serializers.ValidationError("Invalid email or password.")

            if not user.is_active:
                raise serializers.ValidationError("User account is disabled.")

            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError("Must include email and password.")


class CompanyRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscribedCompany
        fields = ['name', 'website', 'email', 'industry', 'location', 'employee_count', 'linkedin_page']


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    terms_accepted = serializers.BooleanField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'password_confirm', 'terms_accepted']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match.")

        if not attrs.get('terms_accepted'):
            raise serializers.ValidationError("You must accept the terms and conditions.")

        return attrs

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        validated_data.pop('terms_accepted')
        password = validated_data.pop('password')

        user = CustomUser.objects.create_user(
            password=password,
            **validated_data
        )
        return user


# Account Settings Serializers
class SubscribedCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscribedCompany
        fields = '__all__'


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    plan = PlanSerializer(read_only=True)

    class Meta:
        model = Subscription
        fields = '__all__'


class BillingHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingHistory
        fields = '__all__'


from django.contrib.auth import get_user_model
User = get_user_model()

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "position", "phone_number", "linkedin_profile", "onboarding_completed"]
