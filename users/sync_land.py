import requests
import time
from django.conf import settings
from core.models import Opportunity

# --------------------------
#   CONFIG
# --------------------------

TOKEN = "pit-95530279-fb75-4aee-a1d0-be4d24fedd26"
LOCATION_ID = "69jbeIj2NHqOyRqcklPo"
PIPELINE_ID = "XfoSVfzmsfTSoBHP0jp7"
LIMIT = 100

GEOCODIO_API_KEY = "97c2d79c7d9d627464772763227994b2c792b4b"


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
        filtered = [o for o in batch if o.get("pipelineId") == PIPELINE_ID]
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



def sync_opportunities_land():
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

        obj, created = Opportunity.objects.get_or_create(
            contact_id=contact_id,
            defaults={
                "contact_name": contact_name,
                "pipeline_id": pipeline_id,
                "pipeline_type": "land",
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
