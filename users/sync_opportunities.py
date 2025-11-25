import requests
import time
from django.conf import settings
from core.models import Opportunity,ServerSetting

# --------------------------
#   CONFIG
# --------------------------

pipelines = {'wholesaling':'Wf9mQtXgnetMG8PrMvBZ',
             'land':'XfoSVfzmsfTSoBHP0jp7',
             'longterm':'fxII6ro6lplz3xD0vjS7',
             'new_leads':'V2qQLuub1HLlr1ZeSWeJ',
             }

stages = {
    # wholesaling (whos)
    'whos-cool': '9b1b711a-d1f4-4762-8870-072c4f41b5cd',
    'whos-warm': '50c23a7b-388f-4aa6-a736-e78159675426',
    'whos-hot': '88c41523-df95-41a4-bc29-b4062093dab7',
    'whos-appointment_set': '448fd172-54cc-469f-9063-2d4b8b735f2f',
    'whos-post_appt_confirm_dd': 'bf8859e8-e655-4079-9889-8d8868c5e786',
    'whos-offer_sent': '0f70df6f-bc4a-44d8-b21e-5e3fdba0ef6e',
    'whos-under_contract_with_seller': '1a21200c-75a3-43b3-b5e3-4480632f3644',
    'whos-buyer_signed': '87d7d2f9-5540-4d05-84c8-5ef22bead393',
    'whos-closed': '8c1f2ea2-847f-425d-b1e4-1961c9f92db7',

    # longterm
    'longterm-may_sell_12mo': '43a741b4-9851-42e2-b23a-a493d2fb4b74',
    'longterm-dead_lead': 'df930803-943a-4e90-b0f2-f4550f7299f3',

}


TOKEN = "pit-95530279-fb75-4aee-a1d0-be4d24fedd26"
LOCATION_ID = "69jbeIj2NHqOyRqcklPo"
#PIPELINE_ID = "Wf9mQtXgnetMG8PrMvBZ"
LIMIT = 100

GEOCODIO_API_KEY = ServerSetting.objects.first().geo_api_key if ServerSetting.objects.exists() else ""


def fetch_all_opportunities():
    """Fetch ALL opportunities from GHL with pagination."""
    all_opps = []
    start_after = []

    while True:
        url = "https://services.leadconnectorhq.com/opportunities/search"

        payload = {
            "locationId": LOCATION_ID,
            "query": "",
            "limit": LIMIT,
            "page": 0,
            "searchAfter": start_after,
            "additionalDetails": {
                "notes": False,
                "tasks": False,
                "calendarEvents": False,
                "unReadConversations": True
            }
        }

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {TOKEN}",
            "Version": "2021-07-28"
        }

        r = requests.post(url, json=payload, headers=headers)
        if r.status_code not in [200, 201]:
            break

        data = r.json()
        batch = data.get("opportunities", [])

        if not batch:
            break

        # filter pipeline
        filtered = [o for o in batch] #if o.get("pipelineId") == PIPELINE_ID]
        all_opps.extend(filtered)

        # pagination cursor
        start_after = batch[-1].get("sort", [])
        if not start_after:
            break

    return all_opps



def extract_address(custom_fields):
    """Extract the address field from customFields list."""
    for field in custom_fields:
        val = field.get("fieldValueString", "").strip()
        if val and "month" not in val.lower():
            return val
    return ""



def geocode(address):
    """Geocode using Geocod.io."""
    url = f"https://api.geocod.io/v1.7/geocode?q={address}&api_key={GEOCODIO_API_KEY}"

    try:
        res = requests.get(url)
        if res.status_code != 200:
            return None, None

        data = res.json()
        if not data.get("results"):
            return None, None

        loc = data["results"][0]["location"]
        return loc["lat"], loc["lng"]

    except:
        return None, None



def sync_opportunities():
    """Main sync workflow."""

    fetched = fetch_all_opportunities()

    created_count = 0
    updated_geocoded = 0
    skipped_existing = 0
    failed_geocode = 0

    for opp in fetched:
        contact_id = opp.get("contact", {}).get("id")
        contact_name = opp.get("contact", {}).get("name")
        pipeline_id = opp.get("pipelineId")

        address = extract_address(opp.get("customFields", []))

        pipeline_id = opp.get("pipelineId")

        # Detect pipeline type from GHL pipelineId
        pipeline_type = None
        for p_type, p_id in pipelines.items():
            if p_id.strip() == pipeline_id.strip():
                pipeline_type = p_type
                break

        stage_id = opp.get("pipelineStageId")
        stage_name = None
        for name, s_id in stages.items():
            if s_id.strip() == (stage_id or "").strip():
                stage_name = name
                break

        # Only overwrite stage if it’s valid
        defaults = {
            "contact_name": contact_name,
            "pipeline_id": pipeline_id,
            "pipeline_type": pipeline_type,
            "address": address,
        }
        if stage_name:
            defaults["stage"] = stage_name

        obj, created = Opportunity.objects.update_or_create(
            contact_id=contact_id,
            defaults=defaults
        )
        
        if created:
            created_count += 1
        else:
            skipped_existing += 1

        # If no address → skip
        if not address:
            continue

        # If already geocoded → skip
        if obj.lat and obj.lng:
            continue

        # Geocode only if needed
        lat, lng = geocode(address)

        if lat and lng:
            obj.lat = lat
            obj.lng = lng
            obj.save()
            updated_geocoded += 1
        else:
            failed_geocode += 1

        time.sleep(0.35)  # rate limit protection

    # Final report
    return {
        "total_fetched": len(fetched),
        "created_new": created_count,
        "already_existing": skipped_existing,
        "geocoded_new": updated_geocoded,
        "geocode_failed": failed_geocode,
    }








def update_opportunities():
    """Main sync workflow."""

    fetched = fetch_all_opportunities()
    Opportunity.objects.all().delete()

    created_count = 0
    updated_geocoded = 0
    skipped_existing = 0
    failed_geocode = 0

    for opp in fetched:
        contact_id = opp.get("contact", {}).get("id")
        contact_name = opp.get("contact", {}).get("name")
        pipeline_id = opp.get("pipelineId")

        address = extract_address(opp.get("customFields", []))

        pipeline_id = opp.get("pipelineId")

        # Detect pipeline type from GHL pipelineId
        pipeline_type = None
        for p_type, p_id in pipelines.items():
            if p_id.strip() == pipeline_id.strip():
                pipeline_type = p_type
                break

        if not pipeline_type:
            print(f"⚠️ Unknown pipelineId: {pipeline_id} for contact {contact_id} ({contact_name})")
            # Optionally skip this record
            continue
        stage_id = opp.get("pipelineStageId")  # stage ID from GHL
        stage_name = None

        for name, s_id in stages.items():
            if s_id.strip() == (stage_id or "").strip():
                stage_name = name
                break

        # If stage not found → set as blank
        if not stage_name:
            stage_name = ""

        obj, created = Opportunity.objects.get_or_create(
            contact_id=contact_id,
            defaults={
                "contact_name": contact_name,
                "pipeline_id": pipeline_id,
                "pipeline_type": pipeline_type,
                'stage': stage_name,
                "address": address,
            }
        )

        if created:
            created_count += 1
        else:
            skipped_existing += 1

        # If no address → skip
        if not address:
            continue

        # If already geocoded → skip
        if obj.lat and obj.lng:
            continue

        # Geocode only if needed
        lat, lng = geocode(address)

        if lat and lng:
            obj.lat = lat
            obj.lng = lng
            obj.save()
            updated_geocoded += 1
        else:
            failed_geocode += 1

        time.sleep(0.35)  # rate limit protection

    # Final report
    return {
        "total_fetched": len(fetched),
        "created_new": created_count,
        "already_existing": skipped_existing,
        "geocoded_new": updated_geocoded,
        "geocode_failed": failed_geocode,
    }
