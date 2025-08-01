from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

# Create your views here.

from django.views.decorators.http import require_POST
from django.http import JsonResponse



@login_required(login_url='login')  # Redirect to 'login' if not authenticated
def home_page(request):
    return render(request, 'index.html')

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