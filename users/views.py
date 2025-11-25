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
    'whos-cool': 'Wholesaling - Cool',
    'whos-warm': 'Wholesaling - Warm',
    'whos-hot': 'Wholesaling - Hot',
    'whos-appointment_set': 'Wholesaling - App. Set',
    'whos-post_appt_confirm_dd': 'Wholesaling - Post App. Confirm',
    'whos-offer_sent': 'Wholesaling - Offer Sent',
    'whos-under_contract_with_seller': 'Wholesaling - Under Contract',
    'whos-buyer_signed': 'Wholesaling - Buyer Signed',
    'whos-closed': 'Wholesaling - Closed',

    # Land
    'land-new_lead': 'Land - New Lead',
    'land-offer_sent': 'Land - Offer Sent',
    'land-under_contract': 'Land - Under Contract',
    'land-closed': 'Land - Closed',
    'land-dead_lead': 'Land - Dead Lead',

    # Long Term
    'longterm-may_sell_12mo': 'Long Term - May Sell 12 Mo',
    'longterm-dead_lead': 'Long Term - Dead Lead',
}

@login_required(login_url='login')
def home_page(request):
    # One DB hit
    all_leads = list(Opportunity.objects.all())

    PIPELINES = {
        'wholesaling': 'Wf9mQtXgnetMG8PrMvBZ',
        'land': 'XfoSVfzmsfTSoBHP0jp7',
        'longterm': 'fxII6ro6lplz3xD0vjS7',
    }

    # Stages for the checkbox filter card
    stages = {key: key for key in STAGE_DISPLAY.keys()}

    # Combined locations dict
    locations = {}
    total_locations = 0

    # Lead type counts
    wholesaling_leads = []
    land_leads = []
    longterm_leads = []

    for lead in all_leads:
        display_stage = STAGE_DISPLAY.get(lead.stage, "")

        def make_marker(lead):
            return {
                'latitude': lead.lat,
                'longitude': lead.lng,
                'name': lead.contact_name or "No Name",
                'address': lead.address or "No Address",
                'stage': STAGE_DISPLAY.get(lead.stage, ""),  # friendly name
                'stage_key': lead.stage,                      # raw key for JS filtering
                'pipeline': lead.pipeline_type or "",
                'contact_url': f"https://ninja.xleads.com/v2/location/69jbeIj2NHqOyRqcklPo/conversations/conversations/{lead.contact_id}",
            }

        # Append to lead-type lists for counts
        if lead.pipeline_id == PIPELINES['wholesaling']:
            wholesaling_leads.append(lead)
        elif lead.pipeline_id == PIPELINES['land']:
            land_leads.append(lead)
        elif lead.pipeline_id == PIPELINES['longterm']:
            longterm_leads.append(lead)

        # Add to combined locations
        if lead.lat and lead.lng:
            locations[str(lead.id)] = make_marker(lead)
            total_locations += 1

    context = {
        'locations': json.dumps(locations),
        'total_locations': total_locations,
        'wholesaling_leads_count': len(wholesaling_leads),
        'land_leads_count': len(land_leads),
        'longterm_leads_count': len(longterm_leads),
        'total_leads': len(all_leads),
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