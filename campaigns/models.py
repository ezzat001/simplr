from django.db import models
from users.models import Profile
from django.utils import timezone
from django.contrib.auth.models import User
from core.models import TimestampMixin




ACTIVITY = (
    ('active', 'Active'),
    ('hold', 'Hold'),
    ('pending','Pending'),
    ('inactive', 'Inactive'),
)

class Platform(TimestampMixin): 
    PLATFORM_TYPES = (
    ('voip_dialer', 'VoIP Dialer'),            # e.g., ReadyMode, CallTools
    ('sms_platform', 'Text Messaging'),        # e.g., SmarterContact
    ('crm', 'CRM'),                            # e.g., GoHighLevel, Pipedrive
    ('data_provider', 'Data Source'),          # e.g., Propstream, BatchLeads
    ('email_marketing', 'Email Marketing'),    # e.g., Mailchimp, Constant Contact
    ('automation_tool', 'Automation Tool'),    # e.g., Zapier, Make (Integromat)
    ('admin_platform', 'Admin Platform'),      # e.g., Odoo, internal tools
    )
   
    name = models.CharField(max_length=50, null=True, blank=True)
    source_type = models.CharField(max_length=50, choices=PLATFORM_TYPES, null=True, blank=True)
    

    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name


class Campaign(TimestampMixin): # Client Campaigns
    SERVICE_TYPES = (
        ('calling','Calling Service'),
        ('texting', 'Texting Service'),
        ('email', 'Email Service'),
        ('admin', 'Admin Service'),
        ('marketing', 'Marketing Service'),
        ('sales', 'Sales Service'),
    )

    name = models.CharField(max_length=50, null=True, blank=True)
    client = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    agents_count = models.PositiveIntegerField(default=0)
    #agents_rate = models.PositiveIntegerField(default=0)
    daily_leads = models.PositiveIntegerField(default=0)
    platforms = models.ManyToManyField(Platform, related_name='platform_campaign', blank=True)

    campaign_type = models.CharField(max_length=50, choices=SERVICE_TYPES, null=True, blank=True)

    lead_points = models.PositiveIntegerField(default=0)

    #lookerstudio = models.TextField(null=True , blank=True)
    
    #dialer_api_key = models.TextField(null=True, blank=True)

    documentation = models.TextField(null=True, blank=True)
    qa_sop = models.TextField(null=True, blank=True)

    status = models.CharField(max_length=50,default="active", choices=ACTIVITY, null=True, blank=True)

    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Lead(TimestampMixin):
    PROPERTY_CHOICES = (
        ('house','House'),
        ('vacant_land','Vacant Land'),
        ('business', 'Business'),
        ('apartment', 'Apartment'),
        ('condo', 'Condo'),
        ('mobile_home','Mobile Home'),
    )

    TIMELINE_CHOICES = (
        ('two_weeks', "2 Weeks"),
        ('one_month', "1 Month"),
        ('two_months', "2 Months"),
        ('three_months', "3 Months"),
        ('four_months', "4 Months"),
        ('five_months', "5 Months"),
        ('six_months', "6 Months"),
        ('six_plus_months', "6+ Months"),
    )
    
    LEAD_CHOICES = (
        ('pending','Pending'),
        ('qualified', 'Qualified'),
        ('disqualified','Disqualified'),
        ('callback', 'Callback'),
        ('duplicated', 'Duplicated'),
    )
    handled = models.DateTimeField(null=True, blank=True)

    
    agent_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    agent_profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name="lead_profile")
    
    #lead_type = models.CharField(max_length=50, choices=LEAD_TYPE_CHOICES, null=True, blank=True)
    campaign = models.ForeignKey(Campaign, on_delete=models.SET_NULL, related_name="lead_campaign", null=True, blank=True)
    #contact_list = models.ForeignKey(ContactList, on_delete=models.SET_NULL, related_name="lead_list", null=True, blank=True)
    property_type = models.CharField(max_length=50, choices=PROPERTY_CHOICES, default="house",null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    timeline = models.CharField(max_length=50, choices=TIMELINE_CHOICES, default="two_weeks" ,null=True, blank=True)
    reason = models.TextField(null=True, blank=True)
    property_address = models.TextField( null=True, blank=True)
    asking_price = models.CharField(max_length=50, null=True, blank=True)
    market_value = models.CharField(max_length=50, null=True, blank=True)
    general_info = models.TextField( null=True, blank=True)
    property_url = models.TextField(null=True,blank=True)
    callback = models.CharField(max_length=50, null=True, blank=True)
    extra_notes = models.TextField( null=True, blank=True)



    roof_age = models.CharField(max_length=50, null=True, blank=True)
    appointment_time = models.CharField(max_length=50, null=True, blank=True)
    known_issues = models.TextField(null=True, blank=True)



    state = models.CharField(max_length=50, default=0, null=True, blank=True)
    county = models.CharField(max_length=50, default=0, null=True, blank=True)
    latitude = models.FloatField(default=0, null=True, blank=True)
    longitude = models.FloatField(default=0, null=True , blank=True)
    status = models.CharField(max_length=50, choices=LEAD_CHOICES, default='pending', null=True, blank=True)
    quality_notes = models.TextField( null=True, blank=True)
    quality_to_agent_notes = models.TextField(  null=True, blank=True)
    assigned = models.ForeignKey(Profile,on_delete=models.SET_NULL, related_name="assigned_profile", null=True, blank=True)
    assigned_time = models.DateTimeField(null=True, blank=True)
    fireback = models.BooleanField(default=False)
    handling_time = models.DurationField(null=True, blank=True)
    handled_by = models.ForeignKey(User,on_delete=models.SET_NULL, related_name="handled_by_lead_post",null=True,blank=True)
    lead_flow = models.FloatField(default=0,null=True, blank=True)
    lead_flow_json = models.JSONField(default=dict, null=True, blank=True)

    
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name or 'Unnamed Lead'} #{self.id or 'unsaved'}"
