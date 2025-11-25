from django.urls import path
from .views import *

urlpatterns = [
    path('lead-form/', lead_form, name='lead_form'),
    path('qa-pending-leads/', qa_pending_leads, name='qa_pending_leads'),
    
]
