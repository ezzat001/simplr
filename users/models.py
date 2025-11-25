from django.db import models
from django.contrib.auth.models import User
from simplr.constants import US_STATES_CHOICES,COUNTRIES_CHOICES
from core.models import TimestampMixin



class Role(TimestampMixin):
    role_name = models.CharField(max_length=50, null=True, blank=True)





    work_status = models.BooleanField(default=False)

    client_dashboard = models.BooleanField(default=False)
    client_lookerstudio = models.BooleanField(default=False)
    client_campaign_performance = models.BooleanField(default=False)

    affiliate_dashboard = models.BooleanField(default=False)

    caller_dashboard = models.BooleanField(default=False)

    lead_submission = models.BooleanField(default=False)
    my_leads = models.BooleanField(default=False)
    lead_scoring = models.BooleanField(default=False)
    leaderboard = models.BooleanField(default=False)

    campaign_documentation = models.BooleanField(default=False)
    campaign_sop = models.BooleanField(default=False)


    leave_request = models.BooleanField(default=False)
    prepayment_request = models.BooleanField(default=False)
    action_request = models.BooleanField(default=False)

    leave_handling = models.BooleanField(default=False)
    prepayment_handling = models.BooleanField(default=False)
    action_handling = models.BooleanField(default=False)
    delete_handling_request = models.BooleanField(default=False)

    qa_pending = models.BooleanField(default=False)
    qa_lead_handling = models.BooleanField(default=False)
    qa_unassign_lead = models.BooleanField(default=False)
    qa_lead_reports = models.BooleanField(default=False)
    qa_auditing = models.BooleanField(default=False)
    qa_auditing_handling = models.BooleanField(default=False)
    qa_agents_table = models.BooleanField(default=False)


    seats = models.BooleanField(default=False)
    camp_hours = models.BooleanField(default=False)
    camp_leads = models.BooleanField(default=False)

    dialer_reports = models.BooleanField(default=False)

    sales_dashboard = models.BooleanField(default=False)
    sales_lookerstudio = models.BooleanField(default=False)
    sales_performance = models.BooleanField(default=False)


    agents_table = models.BooleanField(default=False)
    working_hours = models.BooleanField(default=False)
    attendance_monitor = models.BooleanField(default=False)
    lateness_monitor = models.BooleanField(default=False)

    salaries_table = models.BooleanField(default=False)
    adjusting_hours = models.BooleanField(default=False)

    company_tasks = models.BooleanField(default=False)

    operations = models.BooleanField(default=False)


    admin_home = models.BooleanField(default=False)

    admin_applications = models.BooleanField(default=False)

    admin_accounts = models.BooleanField(default=False)
    admin_clients = models.BooleanField(default=False)
    admin_affiliates = models.BooleanField(default=False)

    admin_campaigns = models.BooleanField(default=False)
    admin_contactlists = models.BooleanField(default=False)

    admin_roles = models.BooleanField(default=False)
    admin_provided_services = models.BooleanField(default=False)
    admin_dialers = models.BooleanField(default=False)
    admin_sources = models.BooleanField(default=False)
    admin_packages = models.BooleanField(default=False)
    admin_contracts = models.BooleanField(default=False)

    admin_server_settings = models.BooleanField(default=False)

    super_admin = models.BooleanField(default=False)


    active=models.BooleanField(default=True)



    ROLE_FIELD_NAMES = {
        "work_status": "Work Status",
        "client_dashboard": "Client Dashboard (Client Role Only)",
        "client_lookerstudio": "Client Looker Studio (Client Role Only)",
        "client_campaign_performance": "Client Campaign Performance (Client Role Only)",
        "affiliate_dashboard": "Affiliate Dashboard (Affiliate Role Only)",
        "caller_dashboard": "Caller Dashboard",
        "lead_submission": "Lead Submission",
        "my_leads": "My Leads",
        "lead_scoring": "Lead Scoring",
        "leaderboard": "Leaderboard",
        "campaign_documentation": "Campaigns Documentation",
        'campaign_sop':"QA Pushing SOP",
        "leave_request": "Leave Request",
        "prepayment_request": "Prepayment Request",
        "action_request": "Action Request",
        "leave_handling": "Leave Handling",
        "prepayment_handling": "Prepayment Handling",
        "action_handling": "Action Handling",
        "delete_handling_request": "Delete Handling Request",
        "qa_pending": "QA Pending",
        "qa_lead_handling": "QA Lead Handling",
        "qa_unassign_lead": "QA Lead Unassignment",
        "qa_lead_reports": "QA Lead Reports",
        "qa_auditing": "QA Auditing",
        "qa_auditing_handling": "QA Auditing Handling",
        "qa_agents_table": "QA Agents Table",
        "seats": "Seats",
        "camp_hours": "Campaign Hours",
        "camp_leads": "Campaign Leads",
        "dialer_reports": "Dialer Reports",
        "sales_dashboard": "Sales Dashboard",
        "sales_lookerstudio": "Sales Looker Studio",
        "sales_performance": "Sales Performance",
        "agents_table": "Agents Table",
        "working_hours": "Working Hours",
        "attendance_monitor": "Attendance Monitor",
        "lateness_monitor": "Lateness Monitor",
        "salaries_table": "Salaries Table",
        "adjusting_hours": "Adjusting Hours",
        "company_tasks": "Company Tasks",
        "operations": "Operations",
        "admin_home": "Admin Home",
        "admin_applications": "Admin Applications",
        "admin_accounts": "Admin Accounts",
        "admin_clients": "Admin Clients",
        "admin_affiliates": "Admin Affiliates",
        "admin_campaigns": "Admin Campaigns",
        "admin_contactlists": "Admin Contact Lists",
        "admin_roles": "Admin Roles",
        "admin_provided_services": "Admin Provided Services",
        "admin_dialers": "Admin Dialers",
        "admin_sources": "Admin Third-Parties",
        "admin_packages": "Admin Packages",
        "admin_contracts": "Admin Contracts",
        "admin_server_settings": "Admin Server Settings",
        }


    def __str__(self):
        return str(self.role_name)
    
    def get_field_labels(self):
        # Use self.__class__.ROLE_FIELD_NAMES to reference class-level attribute
        return {
            field.name: self.__class__.ROLE_FIELD_NAMES.get(field.name, field.name)
            for field in self._meta.fields
        }
    



class Profile(TimestampMixin): #Profile Standard Information
    STATUS_CHOICES = (
    ('active','Active'),
    ('upl', 'UPL'),
    ('annual','Annual'),
    ('casual','Casual'),
    ('sick','Sick'),
    ('hold','Hold'),
    ('dropped','Dropped'),
    ('blacklisted','Blacklisted'),
    )

    SALARY_TYPE = (
    ('monthly','Monthly'),
    ('hourly', 'Hourly'),
    )

    PAYMENT_CHOICES = (
        ("payoneer","Payoneer"),
        ("instapay","InstaPay"),
        ('mobilewallet','Mobile Wallet')
    )

    THEME_CHOICES = (
    ("light","Light"),
    ("dark","Dark"),
)

    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True)
    #picture = models.ImageField(upload_to=random_name_profile_pic, blank=True, null=True)
    

    password = models.CharField(max_length=50,blank=True,null=True)
    phone_name = models.CharField(max_length=50, null=True, blank=True)
    #team = models.ForeignKey(Team, on_delete=models.SET_NULL,blank=True,null=True)
    hiring_date = models.DateField(blank=True, null=True)
    birth_date = models.DateField(blank=True,null=True)
    role = models.ForeignKey(Role, blank=True, null=True, related_name="profile_role", on_delete=models.SET_NULL)

    login_time = models.TimeField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', blank=True, null=True)
    hourly_rate = models.FloatField(default=0,null=True, blank=True)
    monthly_salary = models.FloatField(default=0,null=True, blank=True)
    salary_type = models.CharField(max_length=20 , choices=SALARY_TYPE, blank=True, null=True)
    phone_number = models.CharField(max_length=50,null=True,blank=True)
    residence = models.CharField(max_length=50, choices=COUNTRIES_CHOICES, null=True, blank=True)
    discord = models.CharField(max_length=100, null=True, blank=True)
    payoneer = models.CharField(max_length=100, null=True, blank=True)
    instapay = models.CharField(max_length=100, null=True, blank=True)
    payment_method = models.CharField(max_length=50,default="payoneer", choices=PAYMENT_CHOICES)

    #national_id = models.ImageField(upload_to=random_name_national_id, blank=True, null=True)


    settings_theme = models.CharField(max_length=50,default="dark", choices=THEME_CHOICES)
    #maps_theme = models.CharField(max_length=50,default="dark", choices=THEME_CHOICES)


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    active = models.BooleanField(default=True)

    @property
    def email(self):
        return self.user.email if self.user else None

    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}".strip() if self.user else None



    def __str__(self):
        return (self.full_name or self.user.username) if self.full_name else "Unnamed Profile"






