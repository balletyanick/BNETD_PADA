from django.shortcuts import render

def home(request):
    return render(request, 'street_views/home.html')
