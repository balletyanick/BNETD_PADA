from django.shortcuts import render
from .models import Voirie_Pada_V15


def index(request):
    articles = Voirie_Pada_V15.objects.all()
    terme_recherche = request.GET.get('terme_recherche')
    if terme_recherche:
           articles = Voirie_Pada_V15.objects.filter(new_name__icontains=terme_recherche)
    else:
         articles = Voirie_Pada_V15.objects.all()
    return render(request, 'index.html', {'articles': articles})
    
def __str__(self):
        return self.title

