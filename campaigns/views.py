from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Campaign, CustomForm, CustomFormField, Lead, RealEstateLead, RoofingLead, CustomLead
from django.db.models import Prefetch
from django.utils.text import slugify

from django.http import JsonResponse

@login_required(login_url='login')  # Redirect to 'login' if not authenticated
def lead_form(request):
    context = {}
    campaigns = Campaign.objects.filter(active=True, status='active')
    context['campaigns'] = campaigns
    form = CustomForm.objects.get(name="Solar")  # or by ID
    fields = form.fields.filter(active=True).order_by('order')  # Get only active fields
    #context['fields'] = fields
    context['custom_form'] = form
    custom_forms =  CustomForm.objects.prefetch_related(
    Prefetch('fields', queryset=CustomFormField.objects.filter(active=True).order_by('order'))
).filter(active=True)
    context['custom_forms'] = custom_forms


    if request.method == 'POST':
        form_id = request.POST.get("form_id")
        if form_id == "re_form":
            print("Real Estate Form Submitted")
            campaign_id = request.POST.get('campaign')
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            address = request.POST.get('address')
            asking_price = request.POST.get('asking_price')
            market_value = request.POST.get('market_value')
            timeline = request.POST.get('timeline')
            callback = request.POST.get('callback')
            notes = request.POST.get('notes')
            property_url = request.POST.get('property_url')
            property_type = request.POST.get('property_type')
            callback_time = request.POST.get('callback_time')
            reason = request.POST.get('reason')
            # Handle the RealEstateLead creation logic here
            lead = Lead.objects.create(
                campaign_id=campaign_id,
                agent=request.user.profile,
                name=name,
                email=email,
                phone=phone,
                lead_type='real_estate',
            )
            RealEstateLead.objects.create(lead=lead, 
                property_type=property_type,
                timeline=timeline,
                reason=reason,
                property_address=address,
                asking_price=asking_price,
                market_value=market_value,
                callback=callback,
                property_url=property_url,
                general_notes=notes,

            )
            messages.success(request, "Lead submitted successfully!")
            return redirect('/')


        elif form_id == "roofing_form":
            print("Roofing Form Submitted")
            campaign_id = request.POST.get('campaign')
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            address = request.POST.get('address')
            property_type = request.POST.get('property_type')
            notes = request.POST.get('notes')
            roof_age = request.POST.get('roof_age')
            appointment_time = request.POST.get('appointment_time')
            lead = Lead.objects.create(
                campaign_id=campaign_id,
                agent=request.user.profile,
                name=name,
                email=email,
                phone=phone,
                lead_type='roofing',
            )

            RoofingLead.objects.create(lead=lead, 
                roof_age=roof_age,
                property_type=property_type,
                property_address=address,
                appointment_time=appointment_time,
                general_notes=notes,

            )
            messages.success(request, "Lead submitted successfully!")
            return redirect('/')
        else:
            print("Custom Form Submitted, ID:", form_id)
            form_id = request.POST.get("form_id")
            campaign_id = request.POST.get('campaign')
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            
            form = CustomForm.objects.get(id=form_id)
            fields = form.fields.all()

            response_data = {}
            for field in fields:
                key = f"field_{field.id}"
                value = request.POST.get(key)

                response_data[field.label] = {
                    "value": value,
                    "type": field.field_type
                }

            print("Response Data:", response_data)

            lead = Lead.objects.create(
                campaign_id=campaign_id,
                agent=request.user.profile,
                name=name,
                email=email,
                phone=phone,
                lead_type='custom',
            )
            CustomLead.objects.create(lead=lead, form=form, data=response_data)
            messages.success(request, "Lead submitted successfully!")
            return redirect('/')
        
        
    return render(request, 'campaigns/leads/lead_form.html', context)





def qa_pending_leads(request):
    context = {}
    leads = Lead.objects.filter(status='pending', active=True)
    context['leads'] = leads
    return render(request, 'campaigns/quality/pending_leads.html', context)