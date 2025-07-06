from rest_framework import generics
from clients.models import Product, EmailAccount
from campaign.models import Campaign, Lead, LeadList, Message
from .serializers import LeadSerializer, ProductSerializer, EmailAccountSerializer, CampaignSerializer, MessageSerializer, LeadListSerializer


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class EmailAccountListCreateView(generics.ListCreateAPIView):
    queryset = EmailAccount.objects.all()
    serializer_class = EmailAccountSerializer

class EmailAccountRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EmailAccount.objects.all()
    serializer_class = EmailAccountSerializer


class CampaignListCreateView(generics.ListCreateAPIView):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer

class CampaignRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer    


class MessageListCreateView(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class MessageRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer    


class LeadListCreateView(generics.ListCreateAPIView):
    queryset = LeadList.objects.all()
    serializer_class = LeadListSerializer

class LeadListRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LeadList.objects.all()
    serializer_class = LeadListSerializer



class LeadCreateView(generics.ListCreateAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer

class LeadRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer