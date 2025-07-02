from rest_framework import serializers
from clients.models import Product
from campaign.models import Campaign


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
