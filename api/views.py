from rest_framework import generics
from clients.models import Product, EmailAccount
from campaign.models import Campaign, Lead, LeadList, Message
from .serializers import LeadSerializer, ProductSerializer, EmailAccountSerializer, CampaignSerializer, MessageSerializer, LeadListSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


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



class BulkLeadCreateView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data

        if not isinstance(data, list):
            return Response({'error': 'Expected a list of leads'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate all objects
        serializer = LeadSerializer(data=data, many=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Build Lead instances manually
        validated_data = serializer.validated_data
        leads = [Lead(**item) for item in validated_data]

        # Bulk create leads
        Lead.objects.bulk_create(leads)

        return Response({'message': f'{len(leads)} leads created successfully'}, status=status.HTTP_201_CREATED)


class BulkLeadDeleteView(APIView):
    def delete(self, request, *args, **kwargs):
        ids = request.data.get('ids', None)

        if not ids or not isinstance(ids, list):
            return Response({'error': 'Expected a list of lead IDs under "ids".'}, status=status.HTTP_400_BAD_REQUEST)

        # Filter leads by IDs and delete
        leads_to_delete = Lead.objects.filter(id__in=ids)
        count = leads_to_delete.count()
        leads_to_delete.delete()

        return Response({'message': f'{count} leads deleted successfully.'}, status=status.HTTP_200_OK)