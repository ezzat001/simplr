from django.shortcuts import render

# Create your views here.

def home_page(request):
    return render(request, 'index.html')  # or 'users/home.html' if you want it namespaced
