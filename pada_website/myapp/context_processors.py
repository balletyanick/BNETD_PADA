from myapp.models import publicites  

def publicite_context(request):
    pub = publicites.objects.first()
    return {
        'publicite_globale': pub
    }
