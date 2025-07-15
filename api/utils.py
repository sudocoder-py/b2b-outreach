



def auto_unassign_if_list_empty(lead_list):
    if lead_list and not lead_list.lead_lists.exists():
        campaigns = lead_list.campaigns.all()
        if campaigns.exists():
            lead_list.campaigns.clear()