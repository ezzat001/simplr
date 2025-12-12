from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

# Create your views here.

from django.views.decorators.http import require_POST
from django.http import JsonResponse
import json

from django.http import JsonResponse
from .sync_opportunities import sync_opportunities, update_opportunities

from core.models import Opportunity

def sync_opportunities_view(request):
    report = sync_opportunities()
    return JsonResponse(report, safe=False)


def update_opportunities_view(request):
    report = update_opportunities()
    return JsonResponse(report, safe=False)


# Map raw stage keys to friendly display names for all pipelines
STAGE_DISPLAY = {
    # Wholesaling
    'active_new_leads':"New Leads",
    "active_no_contact":"No Contact Made",
    'active_cool':"Cool",
    'active_warm':"Warm",
    "active_hot":"Hot",
    "active_appointment_set":"Appointment Set",
    "active_fell_off_contract":"Fell Off Contract/Purgatory",
    "active_offer_sent":"Offer Sent",
    "active_under_contract_with_seller":"Under Contract with Seller",
    "active_buyer_signed":"Buyer Signed",
    "active_closed":"Closed",
    

    
}

@login_required(login_url='login')
def home_page(request):
    # One DB hit
    all_leads = list(Opportunity.objects.all())

    PIPELINES = {
        'active_leads': 'Wf9mQtXgnetMG8PrMvBZ',
        'warm_leads': 'fxII6ro6lplz3xD0vjS7',
    }

    # Stages for the checkbox filter card
    stages = {key: key for key in STAGE_DISPLAY.keys()}

    # Combined locations dict
    locations = {}
    total_locations = 0

    # Lead type counts
    wholesaling_leads = []
    longterm_leads = []

    wholesaling_locations = 0
    closed_deals = 0
    longterm_locations = 0

    def make_marker(lead):
        return {
            'latitude': lead.lat,
            'longitude': lead.lng,
            'name': lead.contact_name or "No Name",
            'address': lead.address or "No Address",
            'stage': STAGE_DISPLAY.get(lead.stage, ""),
            'stage_key': lead.stage,
            'pipeline': lead.pipeline_type or "",
            'contact_url': f"https://ninja.xleads.com/v2/location/69jbeIj2NHqOyRqcklPo/conversations/conversations/{lead.contact_id}",
        }

    for lead in all_leads:
        # Categorize lead by pipeline type
        if lead.pipeline_id == PIPELINES['active_leads']:
            wholesaling_leads.append(lead)
            if lead.lat and lead.lng:
                wholesaling_locations += 1

        

        elif lead.pipeline_id == PIPELINES['warm_leads']:
            longterm_leads.append(lead)
            if lead.lat and lead.lng:
                longterm_locations += 1
        

        # Add marker to locations dict
        if lead.lat and lead.lng:
            locations[str(lead.id)] = make_marker(lead)
            total_locations += 1
        if lead.stage == 'active_closed':
            closed_deals += 1 
           

    context = {
        'locations': json.dumps(locations),

        # Total markers on map
        'total_locations': total_locations,

        # Total leads (regardless of map)
        'total_leads': len(all_leads),

        # Counts of leads
        'active_leads_count': len(wholesaling_leads),
        'warm_leads_count': len(longterm_leads),

        # Counts of markers with coordinates
        'active_locations_count': wholesaling_locations,
        'warm_locations_count': longterm_locations,
        
        "closed_deals_count": closed_deals,

        'stages': STAGE_DISPLAY,
    }

    return render(request, 'index.html', context)


def login_view(request):
    context = {}

    if request.user.is_authenticated:
       
        return redirect('/')
    else:
        if request.method == "POST":
            data = request.POST
            username=data.get('username')
            password = data.get('password')
            
            
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.first_name}!")
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password.")
                return redirect('login')   

   
            
                
    
    return render(request,'login.html',context)

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    
    return redirect('login')  # change this to your login URL name or path



"""@require_POST
def update_theme(request):
    if request.user.is_authenticated:
        theme = request.POST.get('theme')
        if theme in ['light', 'dark']:
            profile = request.user.profile
            profile.settings_theme = theme
            profile.save()
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)"""



@require_POST
def update_theme(request):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'unauthenticated'}, status=403)
    
    theme = request.POST.get('theme')
    if theme in ['light', 'dark']:
        try:
            profile = request.user.profile
            if profile.settings_theme != theme:
                profile.settings_theme = theme
                profile.save()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'invalid_theme'}, status=400)