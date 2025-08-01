from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Campaign
# Create your views here.

from django.http import JsonResponse
# Create your views here.
@login_required(login_url='login')  # Redirect to 'login' if not authenticated
def lead_form(request):
    context = {}
    campaigns = Campaign.objects.filter(active=True, status='active')
    context['campaigns'] = campaigns

    if request.method == 'POST':
        campaign_id = request.POST.get('campaign')
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        market_value = request.POST.get('market_value')
        timeline = request.POST.get('timeline')
        callback = request.POST.get('callback')
        notes = request.POST.get('notes')
        property_url = request.POST.get('property_url')
        property_type = request.POST.get('property_type')
        callback_time = request.POST.get('callback_time')
        reason = request.POST.get('reason')
        print(request.POST)
        
        messages.success(request, "Lead submitted successfully!")
        return redirect('/')
    return render(request, 'campaigns/leads/lead_form.html', context)