import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics
from api.utils import auto_unassign_if_list_empty
from clients.models import Product, EmailAccount
from campaign.models import Campaign, CampaignLead, Lead, LeadList, Link, Message, MessageAssignment, Schedule
from .serializers import LeadSerializer, MessageAssignmentSerializer, ProductSerializer, EmailAccountSerializer, CampaignSerializer, MessageSerializer, LeadListSerializer, ScheduleSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.decorators import api_view
from django.db import transaction
import uuid


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


class MessageAssignmentListCreateView(generics.ListCreateAPIView):
    queryset = MessageAssignment.objects.all()
    serializer_class = MessageAssignmentSerializer

class MessageAssignmentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MessageAssignment.objects.all()
    serializer_class = MessageAssignmentSerializer


class MessageAssignmentBulkCreateView(APIView):
    def post(self, request):
        campaign_id = request.data.get("campaign_id")
        message_id = request.data.get("message_id")

        if not campaign_id or not message_id:
            return Response(
                {"error": "campaign_id and message_id are required."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            campaign = Campaign.objects.get(id=campaign_id)
            message = Message.objects.get(id=message_id)
        except Campaign.DoesNotExist:
            return Response({"error": "Campaign not found."}, status=status.HTTP_404_NOT_FOUND)
        except Message.DoesNotExist:
            return Response({"error": "Message not found."}, status=status.HTTP_404_NOT_FOUND)

        # Get leads without this message assignment
        existing_assignments = MessageAssignment.objects.filter(
            campaign=campaign, 
            message=message
        ).values_list("campaign_lead_id", flat=True)

        campaign_leads = CampaignLead.objects.filter(campaign=campaign).exclude(
            id__in=existing_assignments
        ).select_related('lead')

        if not campaign_leads.exists():
            return Response(
                {"message": "All leads already have this message assigned."},
                status=status.HTTP_200_OK
            )

        utm_params = {
            "utm_source": request.data.get("utm_source", "email_outreach"),
            "utm_medium": request.data.get("utm_medium", "email"),
            "utm_campaign": request.data.get("utm_campaign", campaign.short_name),
            "utm_term": request.data.get("utm_term", ""),
            "utm_content": request.data.get("utm_content", ""),
            "description": request.data.get("description", ""),
            "purpose": "message",
        }

        with transaction.atomic():
            # PREPARE ALL LINKS FIRST WITH UNIQUE REFS
            links = []
            link_refs = set()  # Track refs to ensure uniqueness
            
            for lead in campaign_leads:
                while True:
                    # Generate the same ref format as in Link.save()
                    base_ref = f"L{lead.lead.id}-CL{lead.id}-C{campaign.id}"
                    unique_suffix = uuid.uuid4().hex[:6]
                    ref = f"{base_ref}-{unique_suffix}"
                    
                    # Ensure ref is truly unique in this batch
                    if ref not in link_refs:
                        link_refs.add(ref)
                        break
                
                links.append(Link(
                    campaign=campaign,
                    campaign_lead=lead,
                    url=campaign.product.landing_page_url,
                    ref=ref,
                    **utm_params
                ))
            
            # Bulk create links (this will still trigger save() methods)
            created_links = Link.objects.bulk_create(links)
            
            # PREPARE MESSAGE ASSIGNMENTS
            assignments = []
            for link, lead in zip(created_links, campaign_leads):
                assignments.append(MessageAssignment(
                    campaign=campaign,
                    campaign_lead=lead,
                    message=message,
                    url=link,
                    delayed_by_days=request.data.get("delayed_by_days", 0),
                    personlized_msg_tmp=message.full_content or ""
                ))
            
            # Bulk create assignments
            created_assignments = MessageAssignment.objects.bulk_create(assignments)
            
            # UPDATE PERSONALIZED CONTENT IN BATCHES
            batch_size = 500
            for i in range(0, len(created_assignments), batch_size):
                batch = created_assignments[i:i + batch_size]
                for assignment in batch:
                    if not assignment.personlized_msg_tmp:
                        assignment.personlized_msg_tmp = assignment.get_personalized_content_tmp()
                
                MessageAssignment.objects.bulk_update(
                    batch, 
                    ['personlized_msg_tmp'],
                    batch_size=batch_size
                )

        return Response(
            {
                "created": len(created_assignments),
                "campaign": campaign.name,
                "message": message.subject,
            },
            status=status.HTTP_201_CREATED,
        )


def campaign_sequence_message_assignments(request, message_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    
    try:
        data = json.loads(request.body)
        campaign_id = data.get('campaign_id')
        
        if not campaign_id:
            return JsonResponse({'error': 'campaign_id is required'}, status=400)
            
        assignments = MessageAssignment.objects.filter(
            message_id=message_id,
            campaign_id=campaign_id
        ).values(
            'id',
            'sent',
            'sent_at',
            'responded',
            'campaign_lead__lead__first_name',
            'campaign_lead__lead__last_name',
            'campaign_lead__lead__email'
        )
        return JsonResponse(list(assignments), safe=False)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    

@api_view(['POST'])
def delete_assignments_by_message(request):
    message_id = request.data.get('message_id')
    campaign_id = request.data.get('campaign_id')

    if not message_id or not campaign_id:
        return Response({'error': 'message_id and campaign_id required'}, status=400)

    count, _ = MessageAssignment.objects.filter(
        message_id=message_id,
        campaign_id=campaign_id
    ).delete()

    return Response({'deleted': count}, status=200)   


class LeadListCreateView(generics.ListCreateAPIView):
    queryset = LeadList.objects.all()
    serializer_class = LeadListSerializer

class LeadListRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LeadList.objects.all()
    serializer_class = LeadListSerializer



class LeadListViewSet(viewsets.ModelViewSet):
    queryset = LeadList.objects.all()
    serializer_class = LeadListSerializer

    @action(detail=True, methods=["PATCH"])
    def assign_campaign(self, request, pk=None):
        lead_list = get_object_or_404(self.queryset, pk=pk)

        if not lead_list.lead_lists.all():
            return Response({'error': 'Cannot assign list to campaign if the list doesnot have any leads'}, status=status.HTTP_400_BAD_REQUEST)

        campaign_id = request.data.get("campaign_id")

        try:
            campaign = Campaign.objects.get(id=campaign_id)
            lead_list.campaigns.add(campaign)  # Add to ManyToMany

            leads = lead_list.lead_lists.all()  # Get all leads in the list
            campaign_leads = [
                CampaignLead(campaign=campaign, lead=lead)
                for lead in leads
            ]

            CampaignLead.objects.bulk_create(campaign_leads, ignore_conflicts=True)  # avoid duplicate


            return Response({"status": "success"})
        except Campaign.DoesNotExist:
            return Response({"error": "Campaign not found"}, status=400)

    @action(detail=True, methods=["PATCH"])
    def unassign_campaign(self, request, pk=None):
        lead_list = get_object_or_404(self.queryset, pk=pk)
        campaign_id = request.data.get("campaign_id")

        try:
            campaign = Campaign.objects.get(id=campaign_id)
            lead_list.campaigns.remove(campaign)  # Remove from ManyToMany

            leads = lead_list.lead_lists.all()

            CampaignLead.objects.filter(campaign=campaign, lead__in=leads).delete()

            return Response({"status": "success"})
        except Campaign.DoesNotExist:
            return Response({"error": "Campaign not found"}, status=400)


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
    


class MoveLeadsToListView(APIView):
    def post(self, request):
        lead_ids = request.data.get('lead_ids')
        target_list_id = request.data.get('target_list_id')

        if not lead_ids or not target_list_id:
            return Response({'error': 'lead_ids and target_list_id are required'}, status=status.HTTP_400_BAD_REQUEST)

        target_list = get_object_or_404(LeadList, id=target_list_id)

        leads_to_move = Lead.objects.filter(id__in=lead_ids).exclude(lead_list=target_list)
        source_list_ids = leads_to_move.values_list("lead_list", flat=True).distinct()

        if not leads_to_move.exists():
            return Response({'status': 'no leads to move'}, status=status.HTTP_200_OK)

        # Handle campaign lead updates
        target_campaigns = set(target_list.campaigns.all())

        for source_list_id in source_list_ids:
            if not source_list_id:
                continue  # skip leads not in a list

            source_list = LeadList.objects.get(id=source_list_id)
            source_campaigns = set(source_list.campaigns.all())

            leads_from_this_source = leads_to_move.filter(lead_list=source_list)

            campaigns_to_add = target_campaigns - source_campaigns
            campaigns_to_remove = source_campaigns - target_campaigns

            # Delete old CampaignLeads (campaigns no longer assigned)
            if campaigns_to_remove:
                CampaignLead.objects.filter(
                    campaign__in=campaigns_to_remove,
                    lead__in=leads_from_this_source
                ).delete()

            # Create new CampaignLeads (campaigns newly assigned)
            campaign_leads_to_create = [
                CampaignLead(campaign=campaign, lead=lead)
                for campaign in campaigns_to_add
                for lead in leads_from_this_source
            ]
            if campaign_leads_to_create:
                CampaignLead.objects.bulk_create(campaign_leads_to_create, ignore_conflicts=True)

        # Update lead_list on the leads
        updated_count = leads_to_move.update(lead_list=target_list)
        
        # Unassign the original list if it's empty
        original_list = LeadList.objects.get(id=source_list_id)
        if original_list.campaigns:
            auto_unassign_if_list_empty(original_list)

        skipped_count = len(lead_ids) - updated_count

        return Response({
            'status': 'success',
            'moved_count': updated_count,
            'skipped_count': skipped_count
        }, status=status.HTTP_200_OK)




class ScheduleListCreateView(generics.ListCreateAPIView):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer

class ScheduleRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer